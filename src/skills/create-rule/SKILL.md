---
name: create-rule
description: Use when writing or improving CLI-agent rules, custom instruction files, AGENTS.md, CLAUDE.md, Cursor rules, Copilot instructions, or modular `rules/<name>.md` files.
license: Apache-2.0
tags:
  - creator
  - rules
  - agents
metadata:
  author: Oleg Shulyakov
  version: "1.4.1"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: meta
---

# create-rule

Write agent rules as durable operating instructions: concise, scoped, concrete, and easy for another agent to apply without guessing.

---

## Workflow

1. **Identify the target.** Determine the runtime, intended audience, output path, and whether the rule is global or path-scoped.
2. **Inspect existing instructions.** Read `AGENTS.md`, `CLAUDE.md`, `.agents/rules/`, `.claude/rules/`, `.github/copilot-instructions.md`, `.github/instructions/`, `.cursorrules`, and `.cursor/rules/` when present.
3. **Extract durable behavior.** Keep build and test commands, repo layout, coding standards, generated-file workflows, review expectations, security constraints, deployment boundaries, and domain conventions.
4. **Scope narrowly.** Use a project-wide file for global behavior; use a path-scoped rule for language, framework, package, generated-code, infrastructure, migration, or review guidance.
5. **Check conflicts.** If the requested rule contradicts existing instructions, call out the conflict and either update the older rule deliberately or ask one concise question before proceeding.
6. **Write direct imperatives.** Use concrete commands, paths, globs, or examples. Add a short rationale only when it helps an agent decide an edge case.
7. **Reference source material.** Prefer authoritative docs over duplicated policy. Summarize only the behavior an agent must follow while working.
8. **Add safety boundaries.** Cover shell commands, secrets, destructive actions, generated files, migrations, deployment, production data, and external services when relevant.
9. **Keep one concern per file.** Split mixed drafts into separate rules and update the runtime index when the project expects one.
10. **Report completion details.** Name changed files, assumptions, and verification performed after writing.

---

## Output

Choose the narrowest durable location that the target runtime actually loads.

| Runtime | Location |
| --- | --- |
| `.agents/` *(default)* | `.agents/rules/<name>.md` |
| Codex / multi-agent | `AGENTS.md` for shared global rules; `.agents/rules/*.md` for scoped concerns |
| Claude Code | `CLAUDE.md` or `.claude/rules/*.md` |
| GitHub Copilot / VS Code | `.github/copilot-instructions.md` (repo-wide); `.github/instructions/*.instructions.md` (scoped) |

Default to `.agents/rules/<name>.md` when runtime is unspecified.

Write rules for recurring agent behavior, not one-off task execution. Good subjects include test commands, package-manager policy, generated-code workflows, migration handling, public API documentation, review format, architecture boundaries, frontend visual QA, and security constraints.

Use concrete identifiers whenever possible: `pnpm test`, `src/generated/**`, `infra/**`, `openapi.yaml`, `make fmt`, or `packages/shared`.

Use front matter only when the runtime supports filtering, scoping, or priority.

```markdown
---
name: [lowercase-hyphenated-rule-id]
description: [One sentence describing the behavior this rule governs]
license: [SPDX license identifier, when applicable]
applies_to: ["glob/or/path/**"]
priority: low | medium | high | critical
metadata:
  author: [Name or profile URL]
  version: "[semantic version]"
  source: [Repository or canonical source reference]
  category: [lowercase-kebab-case domain]
---

# [Human-Readable Rule Name]

- **Direct instruction**: [testable behavior]
- **Concrete reference**: [instruction with `command` or `path` where useful]
- **Source link**: [instruction referencing authoritative source instead of duplicating it]
```

Use a lowercase, hyphenated `name` as the stable rule identifier. Prefer matching the filename without `.md`, for example `.agents/rules/api-contracts.md` uses `name: api-contracts`.

Use `applies_to: ["**/*"]` or omit scope for global rules. Reserve `critical` for security, data-loss, compliance, or production-safety rules. Put `license` at the top level when the rule is imported, adapted, or has explicit licensing. Put optional ownership, release, category, and origin fields such as `author`, `version`, `category`, and compact `source` references under `metadata`.

For runtimes with their own front matter, adapt the fields instead of forcing this exact schema. For plain `AGENTS.md`, write a short section with imperative bullets and concrete paths or commands.

Write the rule body so the next agent can act without reading around it:

- **Start actionable.** Open with a `#` title, then put the workflow, rule instructions, or source-handling guidance before background or limitations.
- **Use section delimiters.** Put standalone `---` lines between long `##` sections when the target runtime treats Markdown normally. Do not add ornamental dividers to formats that reserve them for front matter or rule metadata.
- **Use scan anchors.** Add bold labels inside bullets or numbered steps when they separate distinct actions, fields, or rule types. Do not force bold labels into schemas, command examples, literal templates, or checklist items.

### Example

**Write this:**

- **Integration tests**: run `pnpm test -- --runInBand` because they share a DB fixture.
- **Generated code**: never edit `src/generated/**`; update the schema and run `pnpm generate`.
- **Migrations**: when changing `db/migrations/**`, include a rollback note in the response.
- **Local-only context**: keep personal URLs and machine-specific paths in local, uncommitted instructions.

**Not this:**

- **Vague taste**: "Write clean code" or "be careful."
- **Copied docs**: long README sections or style guides pasted verbatim.
- **Mixed concerns**: tone/personality combined with build, test, or security rules unless writing a top-level instruction file.
- **Hidden dependencies**: rules requiring unlisted tools, hidden knowledge, or credentials.
- **Temporary context**: issue notes or one-off instructions disguised as durable policy.

---

## Boundaries

Use `.agents/rules/*.md` for modular CLI-agent rules when the project has no stricter convention. Use `AGENTS.md` for shared Codex-style project instructions and indexes. Use `CLAUDE.md` or `.claude/rules/*.md` for Claude Code. Use `.github/copilot-instructions.md` for repository-wide Copilot behavior and `.github/instructions/*.instructions.md` for scoped Copilot instructions. Use Cursor's existing rule format if `.cursorrules` or `.cursor/rules/` is already present.

When a runtime has required front matter fields, preserve them. When the runtime is plain Markdown, do not add front matter just to look organized. It is not a stationery contest.

Do not turn broad human documentation into agent rules wholesale. Extract the parts that change an agent's actions during coding, review, verification, or release work. If the source material mixes unrelated concerns, split it by concern instead of preserving the original shape.

Keep personal, machine-specific, or unshared preferences out of committed project instructions. If the user asks for local-only behavior, put it in an explicitly local or uncommitted location, or explain that it should not be added to shared rules.

Exclude task notes, vague preferences, stale context, secrets, personal environment details, and commands that require credentials the agent cannot verify.

---

## Verification

- [ ] One concern per file with a descriptive `lowercase-hyphenated` filename
- [ ] Front matter is present only when the runtime supports filtering or priority
- [ ] Commands, paths, globs, or examples are included where they reduce ambiguity
- [ ] Non-obvious reasoning is explained briefly
- [ ] No secrets, personal preferences, stale context, or unrelated docs are included
- [ ] Existing instructions were checked for conflicts
- [ ] The rule format matches the requested runtime
- [ ] The final response names changed files and any verification skipped or completed
