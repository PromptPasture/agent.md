---
type: concept
title: Conventions
description: Key naming, memory, documentation, and skill-authoring conventions for this repository.
tags: [conventions, naming, memory, docs, skills]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Conventions

## Skill naming

All skills use verb-first naming: `<verb>-<subject>[-<variant>]` or a bare concise verb.

Examples: `code-tests`, `write-prd`, `review-code`, `brainstorm`, `adapt`.

Whenever a skill is materially updated its `metadata.version` must be incremented using semantic versioning.

## Skill metadata (compact format)

```yaml
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: <catalog>
  category: <category>
  tags: [...]
```

Fields: `author`, `version`, `source`, `category`. No verbose inline lists.

## Document metadata (YAML frontmatter)

PRDs, specs, stories, runbooks, and similar generated Markdown artifacts put document-level metadata in YAML frontmatter. No body metadata tables or `Document Info` blocks. Quote date-like values. Use no-space status tokens: `IN_REVIEW`, `IN_PROGRESS`, `READY_FOR_DEV`.

Decided: 2026-05-24.

## Docs folder structure

```
docs/
└── YYYY-MM-DD-task-name/
    ├── BRAINSTORM.md   # discovery and explored ideas
    ├── PRD.md
    ├── SPEC.md
    ├── ARCHITECTURE.md
    ├── DESIGN.md
    └── TASKS.md
```

- Task folder names: UTC date prefix + lowercase hyphenated name.
- Create a task folder only when the work needs durable product, technical, architecture, or design documentation.
- Do not create a task folder only to store a checklist or completed-task summary — use `.agents/memory/` instead.

## Memory conventions

- Daily notes: `.agents/memory/YYYY-MM-DD.md` (UTC dating).
- Write small completed-task observations, decisions, and conventions. Avoid raw git-log summaries and transient task noise.
- `MEMORY.md` in the memory folder is the index; each dated file holds the actual notes.
- Library content (skills, rules, commands) lives under `.agents/`.

## Skill audit grouping

When auditing skill format or authoring compliance, write remediation checklists as one top-level task per skill folder. Put style, structure, reference, and validation fixes as subitems under that skill — not grouped by issue type across all skills.

Decided: 2026-05-25.

## Root `AGENTS.md`

The root `AGENTS.md` is the primary entry point for all agent guidance. Updated on 2026-05-12 to be the concrete entry point. Skills, rules, and commands are loaded from `.agents/` as extensions.
