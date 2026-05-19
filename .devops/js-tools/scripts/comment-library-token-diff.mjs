#!/usr/bin/env node

import { execFile } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { normalizeTokenUsage } from "tokentally";

const execFileAsync = promisify(execFile);
const scriptDir = dirname(fileURLToPath(import.meta.url));
const toolRoot = join(scriptDir, "..");
const repoRoot = join(toolRoot, "..", "..");

const baseRef = requiredValueAfter("--base");
const headRef = valueAfter("--head") ?? "HEAD";
const outputPath = resolvePath(valueAfter("--output") ?? "dist/LIBRARY_TOKEN_DIFF.md");

function valueAfter(flag) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? null : process.argv[index + 1];
}

function requiredValueAfter(flag) {
  const value = valueAfter(flag);
  if (!value) {
    throw new Error(`Missing required ${flag} argument`);
  }
  return value;
}

function resolvePath(value) {
  return isAbsolute(value) ? value : join(repoRoot, value);
}

async function main() {
  const rows = await changedLibraryFiles();
  const body = renderComment(rows);
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, body);
  console.log(`Wrote ${relative(repoRoot, outputPath)}`);
}

async function changedLibraryFiles() {
  const { stdout } = await git([
    "diff",
    "--name-status",
    "--find-renames",
    `${baseRef}...${headRef}`,
    "--",
    ".agents/",
  ]);

  const rows = [];
  for (const line of stdout.trim().split("\n").filter(Boolean)) {
    const fields = line.split("\t");
    const status = fields[0];
    const basePath = status.startsWith("R") ? fields[1] : fields[1] ?? fields[0];
    const headPath = status.startsWith("R") ? fields[2] : fields[1] ?? fields[0];
    const baseInLibrary = basePath?.startsWith(".agents/");
    const headInLibrary = headPath?.startsWith(".agents/");
    const displayPath = headInLibrary ? headPath : basePath;

    if (!baseInLibrary && !headInLibrary) continue;
    if (isEvalPath(basePath) || isEvalPath(headPath)) continue;

    const beforeTokens = baseInLibrary && status !== "A" ? await tokensAtRef(baseRef, basePath) : 0;
    const afterTokens = headInLibrary && status !== "D" ? await tokensAtRef(headRef, headPath) : 0;

    rows.push({
      path: displayPath.replace(/^.agents\//, ""),
      status: statusLabel(status),
      beforeTokens,
      afterTokens,
      delta: afterTokens - beforeTokens,
    });
  }

  rows.sort((a, b) => a.path.localeCompare(b.path));
  return rows;
}

function isEvalPath(path) {
  return path?.startsWith(".agents/") && path.split("/").includes("evals");
}

function statusLabel(status) {
  if (status === "A") return "added";
  if (status === "D") return "deleted";
  if (status === "M") return "modified";
  if (status.startsWith("R")) return "renamed";
  return status.toLowerCase();
}

async function tokensAtRef(ref, path) {
  if (!path) return 0;
  const { stdout } = await git(["show", `${ref}:${path}`], {
    maxBuffer: 50 * 1024 * 1024,
  });
  const estimatedTokens = estimateMarkdownTokens(stdout);
  const usage = normalizeTokenUsage({ input_tokens: estimatedTokens });
  return usage?.totalTokens ?? estimatedTokens;
}

async function git(args, options = {}) {
  return execFileAsync("git", args, {
    cwd: repoRoot,
    encoding: "utf8",
    ...options,
  });
}

function estimateMarkdownTokens(content) {
  const normalized = content
    .replace(/```[\s\S]*?```/g, (block) => ` ${block} `)
    .replace(/`([^`]+)`/g, " $1 ");
  const pieces = normalized.match(/[A-Za-z0-9]+|[^\sA-Za-z0-9]/g) ?? [];
  return pieces.length;
}

function renderComment(rows) {
  const marker = "<!-- library-token-diff -->";
  if (rows.length === 0) {
    return `${marker}
No \`.agents/\` file token changes detected.
`;
  }

  const totalBefore = rows.reduce((sum, row) => sum + row.beforeTokens, 0);
  const totalAfter = rows.reduce((sum, row) => sum + row.afterTokens, 0);
  const totalDelta = totalAfter - totalBefore;
  const tableRows = rows
    .map(
      (row) =>
        `| \`${escapeTableCell(row.path)}\` | ${row.status} | ${row.beforeTokens} | ${row.afterTokens} | ${formatDelta(row.delta)} |`,
    )
    .join("\n");

  return `${marker}
## Library Token Diff

Estimated token changes for files under \`.agents/\`.

| File | Status | Before | After | Delta |
| --- | --- | ---: | ---: | ---: |
${tableRows}
| **Total** |  | **${totalBefore}** | **${totalAfter}** | **${formatDelta(totalDelta)}** |

Counts use the repository's local Markdown token estimator, so they are for review comparison rather than provider billing.
`;
}

function formatDelta(delta) {
  return delta > 0 ? `+${delta}` : String(delta);
}

function escapeTableCell(value) {
  return value.replaceAll("|", "\\|");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
