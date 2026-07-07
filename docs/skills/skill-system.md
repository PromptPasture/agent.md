---
type: concept
title: Skill system
description: How Agent Skills are structured, named, discovered, and loaded in this repository.
tags: [skills, agents, naming, conventions]
created: "2026-06-25T00:00:00Z"
updated: "2026-07-06T00:00:00Z"
---

# Skill system

Skills are reusable, independently installable task procedures. Each skill lives in `.agents/skills/<name>/SKILL.md` (project-local) or `~/.agents/skills/<name>/SKILL.md` (global).

## Naming convention

All skills use **verb-first naming**: `<verb>-<subject>[-<variant>]` or a bare verb.

Examples: `code-tests`, `to-prd`, `review-code`, `brainstorm`, `adapt`.

Approved verb groups: `audit`, `check`, `build`, `design`, `diagram`, `model`, `document`, `plan`, `report`, `review`, `configure`, `create`, `track`, `write`, `code`, `to`.

## SKILL.md structure

```yaml
---
name: <skill-name>           # REQUIRED — matches parent directory
description: <1–1024 chars>  # REQUIRED — what it does and when to trigger it
license: Apache-2.0          # optional
compatibility: ...           # optional
metadata:
  author: ...
  version: "1.0.0"           # semantic version; bump on every material update
  source: github.com/olegshulyakov/agent.md
  catalog: <catalog-name>
  category: <category>
  tags: [...]
---
```

Body: Markdown workflow instructions the agent follows when the skill is active.

## Progressive disclosure

Runtimes scan metadata first (startup cost), then load the full `SKILL.md` body when the request matches the description. `references/` and `scripts/` are loaded only when the workflow explicitly needs them.

## Multi-variant router skills

For domains where one trigger should select among related artifact variants (backend, frontend, database, tests, security…), a **router skill** detects the variant from prompt and repo context, then loads only the matching reference doc. It asks at most one clarifying question when context is ambiguous.

## Quality bar

|Criterion|Target|
|---|---|
|Line limit|≤ 500 lines; overflow → `references/`|
|Eval prompts|8–10 per skill; 8–10 per routed reference for routers|
|Eval pass rate|≥ 85% aggregate; zero failed critical expectations|
|Validation|Passes `validate.py`|

## Skill catalog

See [Skill catalog](/docs/skills/skill-catalog.md) for the full list of 56 cataloged skills and their implementation status.
