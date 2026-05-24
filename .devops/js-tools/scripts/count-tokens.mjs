#!/usr/bin/env node

import { access, mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, isAbsolute, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { normalizeTokenUsage, tallyCosts } from "tokentally";

const scriptDir = dirname(fileURLToPath(import.meta.url));
const toolRoot = join(scriptDir, "..");
const repoRoot = join(toolRoot, "..", "..");

const outputDir = resolveOutputDir(valueAfter("--output-dir"));

function valueAfter(flag) {
  const index = process.argv.indexOf(flag);
  return index === -1 ? null : process.argv[index + 1];
}

function resolveOutputDir(value) {
  if (!value) return join(repoRoot, "dist");
  return isAbsolute(value) ? value : join(repoRoot, value);
}

async function main() {
  const report = await buildTokenReport();
  await writeReports(report);
}

async function buildTokenReport() {
  const files = await trackedFiles();
  const entries = await Promise.all(
    files.map(async (entry) => {
      const content = await readFile(join(repoRoot, entry.path), "utf8");
      const totalTokens = estimateMarkdownTokens(markdownBody(content));
      const usage = normalizeTokenUsage({ input_tokens: totalTokens });

      return {
        ...entry,
        bytes: Buffer.byteLength(content, "utf8"),
        tokens: usage?.totalTokens ?? totalTokens,
      };
    }),
  );

  entries.sort((a, b) => {
    if (a.kind !== b.kind) return a.kind.localeCompare(b.kind);
    return a.name.localeCompare(b.name);
  });

  const byKind = await tallyCosts({
    calls: entries.map((entry) => ({
      model: entry.kind,
      usage: normalizeTokenUsage({ input_tokens: entry.tokens }),
    })),
    resolvePricing: () => null,
  });

  return {
    generatedAt: new Date().toISOString(),
    estimator: "local markdown body token estimate normalized with tokentally",
    totals: {
      files: entries.length,
      tokens: entries.reduce((sum, entry) => sum + entry.tokens, 0),
      bytes: entries.reduce((sum, entry) => sum + entry.bytes, 0),
    },
    byKind: Object.fromEntries(
      Object.entries(byKind.byModel)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([kind, row]) => [
          kind,
          {
            files: row.calls,
            tokens: row.usage.totalTokens ?? 0,
          },
        ]),
    ),
    entries,
  };
}

async function trackedFiles() {
  return [
    ...(await markdownEntries("command", ".agents/commands")),
    ...(await markdownEntries("rule", ".agents/rules")),
    ...(await skillEntries()),
    ...(await agentEntries()),
  ];
}

async function markdownEntries(kind, directory) {
  const absoluteDirectory = join(repoRoot, directory);
  const files = await readdir(absoluteDirectory, { withFileTypes: true });
  return files
    .filter((file) => file.isFile() && file.name.endsWith(".md"))
    .map((file) => {
      const name = file.name.replace(/\.md$/, "");
      return {
        kind,
        name,
        path: `${directory}/${file.name}`,
      };
    });
}

async function skillEntries() {
  const skillsDirectory = join(repoRoot, ".agents/skills");
  const skills = await readdir(skillsDirectory, { withFileTypes: true });
  const entries = await Promise.all(
    skills.filter((skill) => skill.isDirectory()).map(async (skill) => ({
      kind: "skill",
      name: skill.name,
      path: `.agents/skills/${skill.name}/SKILL.md`,
      exists: await fileExists(join(skillsDirectory, skill.name, "SKILL.md")),
    })),
  );
  return entries
    .filter((entry) => entry.exists)
    .map(({ exists, ...entry }) => entry);
}

async function agentEntries() {
  const agents = [];
  const skillsDirectory = join(repoRoot, ".agents/skills");
  const skills = await readdir(skillsDirectory, { withFileTypes: true });

  for (const skill of skills.filter((entry) => entry.isDirectory())) {
    const agentsDirectory = join(skillsDirectory, skill.name, "agents");
    let files = [];
    try {
      files = await readdir(agentsDirectory, { withFileTypes: true });
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }

    for (const file of files.filter((entry) => entry.isFile() && entry.name.endsWith(".md"))) {
      const name = file.name.replace(/\.md$/, "");
      agents.push({
        kind: "agent",
        name: `${skill.name}/${name}`,
        path: `.agents/skills/${skill.name}/agents/${file.name}`,
      });
    }
  }

  return agents;
}

function estimateMarkdownTokens(content) {
  const normalized = content
    .replace(/```[\s\S]*?```/g, (block) => ` ${block} `)
    .replace(/`([^`]+)`/g, " $1 ");
  const pieces = normalized.match(/[A-Za-z0-9]+|[^\sA-Za-z0-9]/g) ?? [];
  return pieces.length;
}

function markdownBody(content) {
  return content.replace(/^---[ \t]*\r?\n[\s\S]*?\r?\n---[ \t]*(?:\r?\n|$)/, "");
}

async function fileExists(path) {
  try {
    await access(path);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

async function writeReports(report) {
  await mkdir(outputDir, { recursive: true });
  await writeFile(
    join(outputDir, "TOKEN_TALLY.json"),
    `${JSON.stringify(report, null, 2)}\n`,
  );
  await writeFile(join(outputDir, "TOKEN_TALLY.md"), renderMarkdown(report));
  console.log(`Wrote ${relative(repoRoot, join(outputDir, "TOKEN_TALLY.md"))}`);
}

function renderMarkdown(report) {
  const kindRows = Object.entries(report.byKind)
    .map(([kind, row]) => `| ${kind} | ${row.files} | ${row.tokens} |`)
    .join("\n");
  const entryRows = report.entries
    .map((entry) => `| ${entry.kind} | ${entry.name} | ${entry.tokens} | \`${entry.path}\` |`)
    .join("\n");

  return `# Token Tally

Generated at: ${report.generatedAt}

Estimator: ${report.estimator}. Counts are intended for release-to-release comparison, not provider billing.

Total tracked files: ${report.totals.files}
Total estimated tokens: ${report.totals.tokens}
Total bytes: ${report.totals.bytes}

## By Kind

| Kind | Files | Estimated tokens |
| --- | ---: | ---: |
${kindRows}

## By Entry

| Kind | Name | Estimated tokens | Path |
| --- | --- | ---: | --- |
${entryRows}
`;
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
