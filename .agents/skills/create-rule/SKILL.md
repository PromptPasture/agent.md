---
name: create-rule
description: Use when writing or improving CLI-agent rules, custom instruction files, AGENTS.md, CLAUDE.md, Cursor rules, Copilot instructions, or modular `.agents/rules/*.md` files.
license: MIT
tags:
  - creator
  - rules
  - agents
metadata:
  author: Oleg Shulyakov
  version: "1.3.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
---

# create-rule

Write agent rules as durable operating instructions: concise, scoped, concrete, and easy for another agent to apply without guessing.

## Output Locations

**Choose the narrowest durable location that the target runtime actually loads.**

| Runtime | Location |
| --- | --- |
| `.agents/` *(default)* | `.agents/rules/<name>.md` |
| Codex / multi-agent | `AGENTS.md` for shared global rules; `.agents/rules/*.md` for scoped concerns |
| Claude Code | `CLAUDE.md` or `.claude/rules/*.md` |
| GitHub Copilot / VS Code | `.github/copilot-instructions.md` (repo-wide); `.github/instructions/*.instructions.md` (scoped) |

Default to `.agents/rules/<name>.md` when runtime is unspecified.

Keep personal, machine-specific, or unshared preferences out of committed project instructions. If the user asks for local-only behavior, put it in an explicitly local/uncommitted location or explain that it should not be added to shared rules.

## Workflow

**Inspect existing instructions before writing, then add only behavior that should guide future agents.**

1. **Identify target**: determine the runtime, intended audience, output path, and whether the rule is global or path-scoped.
2. **Inspect existing instructions**: read `AGENTS.md`, `CLAUDE.md`, `.agents/rules/`, `.claude/rules/`, `.github/copilot-instructions.md`, `.github/instructions/`, `.cursorrules`, and `.cursor/rules/` when present.
3. **Extract durable behavior**: keep build and test commands, repo layout, coding standards, generated-file workflows, review expectations, security constraints, deployment boundaries, and domain conventions.
4. **Exclude temporary context**: remove task notes, vague preferences, stale context, secrets, personal environment details, and commands that require credentials the agent cannot verify.
5. **Scope narrowly**: use a project-wide file for global behavior; use a path-scoped rule for language, framework, package, generated-code, infrastructure, migration, or review guidance.
6. **Check conflicts**: if the requested rule contradicts existing instructions, call out the conflict and either update the older rule deliberately or ask one concise question before proceeding.
7. **Write direct imperatives**: use concrete commands, paths, globs, or examples. Add a short rationale only when it helps an agent decide an edge case.
8. **Reference source material**: prefer authoritative docs over duplicated policy. Summarize only the behavior an agent must follow while working.
9. **Add safety boundaries**: cover shell commands, secrets, destructive actions, generated files, migrations, deployment, production data, and external services when relevant.
10. **Keep one concern per file**: split mixed drafts into separate rules and update the runtime index when the project expects one.
11. **Report completion details**: name changed files, assumptions, and verification performed after writing.

## Rule Scope

**Make each rule specific enough to act on and small enough to stay true.**

Write rules for recurring agent behavior, not one-off task execution. Good subjects include test commands, package-manager policy, generated-code workflows, migration handling, public API documentation, review format, architecture boundaries, frontend visual QA, and security constraints.

Do not turn broad human documentation into agent rules wholesale. Extract the parts that change an agent's actions during coding, review, verification, or release work. If the source material mixes unrelated concerns, split it by concern instead of preserving the original shape.

Use concrete identifiers whenever possible: `pnpm test`, `src/generated/**`, `infra/**`, `openapi.yaml`, `make fmt`, or `packages/shared`. Avoid instructions like "write clean code," "be careful," or "follow best practices" unless they are immediately followed by project-specific behavior that can be checked.

## Rule Template

**Use front matter only when the runtime supports filtering, scoping, or priority.**

```markdown
---
name: [Human-Readable Rule Name]
description: [One sentence describing the behavior this rule governs]
applies_to: ["glob/or/path/**"]
priority: low | medium | high | critical
metadata:
  author: [Name or profile URL]
  version: "[semantic version]"
  source: [Repository or canonical source reference]
---

# [Human-Readable Rule Name] Rules

- **Direct instruction**: [testable behavior]
- **Concrete reference**: [instruction with `command` or `path` where useful]
- **Source link**: [instruction referencing authoritative source instead of duplicating it]
```

Use `applies_to: ["**/*"]` or omit scope for global rules. Reserve `critical` for security, data-loss, compliance, or production-safety rules. Put optional ownership, release, and origin fields such as `author`, `version`, and compact `source` references under `metadata`, not at the top level.

For runtimes with their own front matter, adapt the fields instead of forcing this exact schema. For plain `AGENTS.md`, write a short section with imperative bullets and concrete paths or commands.

## Good vs. Bad

**Prefer instructions that name observable behavior over taste or intent.**

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

## Runtime Notes

**Adapt to the target tool without inventing a private format.**

Use `.agents/rules/*.md` for modular CLI-agent rules when the project has no stricter convention. Use `AGENTS.md` for shared Codex-style project instructions and indexes. Use `CLAUDE.md` or `.claude/rules/*.md` for Claude Code. Use `.github/copilot-instructions.md` for repository-wide Copilot behavior and `.github/instructions/*.instructions.md` for scoped Copilot instructions. Use Cursor's existing rule format if `.cursorrules` or `.cursor/rules/` is already present.

When a runtime has required front matter fields, preserve them. When the runtime is plain Markdown, do not add front matter just to look organized. It is not a stationery contest.

## Quality Checklist

**Finish only after the rule is scoped, concrete, non-conflicting, and in the right place.**

Before finishing, verify the rule:

- **Single concern**: one concern per file with a descriptive `lowercase-hyphenated` filename
- **Front matter**: present when the runtime supports filtering or priority
- **Concrete anchors**: commands, paths, globs, or examples included where they reduce ambiguity
- **Rationale**: non-obvious reasoning explained briefly
- **Clean content**: no secrets, personal preferences, stale context, or unrelated docs
- **No conflicts**: checked against existing instructions
- **Runtime format**: matches the requested tool
- **Indexing**: linked from `AGENTS.md`, `CLAUDE.md`, Copilot instructions, or the runtime entry point when the project expects an index
- **Final report**: names changed files and any verification skipped or completed
