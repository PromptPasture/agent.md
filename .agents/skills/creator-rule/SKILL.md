---
name: creator-rule
description: >
  Use when writing or improving CLI-agent rules, custom instruction files,
  AGENTS.md, CLAUDE.md, Cursor rules, Copilot instructions, or modular
  `.agents/rules/*.md` files.
author: Oleg Shulyakov
license: MIT
version: 1.2.0
---

# creator-rule

Write agent rules like executable project configuration: concise, scoped, and specific enough for another agent to follow without guessing.

## Output Locations

**Choose the narrowest shared location that matches the target runtime.**

| Runtime | Location |
| --- | --- |
| Agent Playbook *(default)* | `.agents/rules/<name>.md` |
| Codex / multi-agent | `AGENTS.md` for shared global rules; `.agents/rules/*.md` for scoped concerns |
| Claude Code | `CLAUDE.md` or `.claude/rules/*.md` |
| GitHub Copilot / VS Code | `.github/copilot-instructions.md` (repo-wide); `.github/instructions/*.instructions.md` (scoped) |

Default to Agent Playbook format when runtime is unspecified.

## Workflow

**Inspect first, then write only durable operating rules.**

1. Identify the target runtime, intended audience, output path, and whether the rule is global or path-scoped.
2. Inspect existing instruction entry points before writing: `AGENTS.md`, `CLAUDE.md`, `.agents/rules/`, `.claude/rules/`, `.github/copilot-instructions.md`, `.github/instructions/`, `.cursorrules`, and `.cursor/rules/` when present.
3. Extract durable behavior only: build and test commands, repo layout, coding standards, generated-file workflows, review expectations, security constraints, deployment boundaries, and domain conventions.
4. Exclude temporary task notes, personal environment details, vague preferences, stale context, secrets, and commands that require credentials the agent cannot verify.
5. Scope narrowly. Use a project-wide file for global behavior; use a path-scoped rule for language, framework, package, generated-code, infrastructure, migration, or review guidance.
6. Write direct imperatives with concrete commands, paths, globs, or examples. Add a short reason only when it helps an agent make an edge-case decision.
7. Avoid duplication. Reference authoritative docs as the source of truth and summarize only the behavior an agent must follow during work.
8. Check for conflicts. If a new rule contradicts existing instructions, call out the conflict and either update the older rule deliberately or ask one concise question before proceeding.
9. Add safety boundaries when relevant for shell commands, secrets, destructive actions, generated files, migrations, deployment, production data, and external services.
10. Keep one concern per file. Split mixed drafts into multiple rules and update the runtime index when the project expects one.
11. Report changed files, assumptions, and verification performed after writing.

## Rule Template

**Use front matter when the runtime supports filtering, scoping, or priority.**

```markdown
---
name: [Human-Readable Rule Name]
description: [One sentence describing the behavior this rule governs]
applies_to: ["glob/or/path/**"]
priority: low | medium | high | critical
---

# [Human-Readable Rule Name] Rules

- [Direct, testable instruction]
- [Instruction with `command` or `path` where useful]
- [Instruction referencing authoritative source instead of duplicating it]
```

Use `applies_to: ["**/*"]` or omit for global scope. Reserve `critical` for security, data-loss, compliance, or production-safety rules.

For runtimes with their own front matter, adapt the fields instead of forcing this exact schema. For plain `AGENTS.md`, write a short section with imperative bullets and concrete paths or commands.

## Good vs. Bad

**Prefer instructions that can be verified from the repository.**

**Write this:**

- `pnpm test -- --runInBand` for integration tests (shared DB fixture).
- Never edit `src/generated/**`; update the schema and run `pnpm generate`.
- When changing `db/migrations/**`, include a rollback note in the response.
- Keep personal URLs and machine-specific paths in local, uncommitted instructions.

**Not this:**

- "Write clean code" or "be careful."
- Long README sections or style guides copied verbatim.
- Tone/personality mixed with build, test, or security rules (unless writing a top-level instruction file).
- Rules requiring unlisted tools, hidden knowledge, or credentials.
- Temporary issue notes or one-off instructions disguised as durable policy.

## Quality Checklist

**Finish only after the rule is scoped, concrete, and non-conflicting.**

Before finishing, verify the rule:

- One concern; descriptive `lowercase-hyphenated` filename
- Front matter present when runtime supports filtering or priority
- Concrete commands, paths, globs, or examples where they reduce ambiguity
- Non-obvious rationale explained briefly
- No secrets, personal preferences, stale context, or unrelated docs
- No conflict with existing instructions
- Runtime-specific format matches the requested tool
- Indexed from `AGENTS.md`, `CLAUDE.md`, Copilot instructions, or the runtime entry point when the project expects an index
- Final response names changed files and any verification skipped or completed
