---
type: concept
title: Skill catalog
description: The 56-skill software team roles library — catalog, distribution model, and implementation status.
tags: [skills, catalog, distribution, release]
created: "2026-06-25T00:00:00Z"
updated: "2026-07-07T00:00:00Z"
---

# Skill catalog

The Prompt Pasture skill library targets 56 software-team skills covering the full delivery cycle. Stable skills live under `src/skills/<catalog>/<skill>/`; unfinished skills live under `src/skills/in-progress/`.

## Verb groups

`audit` · `check` · `build` · `design` · `diagram` · `model` · `document` · `plan` · `report` · `review` · `configure` · `create` · `track` · `write` · `code`

## Catalog areas

|Catalog|Examples|
|---|---|
|Product / analysis|`to-prd`, `to-ticket`, `write-spec`|
|Engineering|`code-backend`, `code-frontend`, `code-database`, `code-tests`|
|Quality / security|`review-code`, `audit-security`|
|Productivity|`brainstorm`, `plan`, `wiki`, `markitdown`|
|Legal|`lawyer`|
|Landscape|`landscape-design`|

## Distribution model (decided 2026-06-13)

Each tagged GitHub Release produces:

- **One ZIP per stable skill** — `prompt-pasture-agent-<skill-name>-<tag>.zip` — unpacks as `<skill-name>/` with `SKILL.md` and bundled resources.
- **One complete archive** — `prompt-pasture-agent-<tag>.zip` — contains all stable catalogs as `skills/<catalog>/<skill>/...` plus `skills/README.md`.

`src/skills/in-progress/` is **excluded** from all plugins and release archives.

Plugin manifests (Codex and Claude) explicitly list every stable skill path. No content is duplicated. GitHub Actions owns release assembly — no npm package or standalone generator script.

## Implementation status tracking

- Source: `wiki/sources/2026-06-11-skill-catalog/BRAINSTORM.md`, `wiki/sources/2026-05-02-team-roles-as-skills/TASKS.md`
- 10 of 56 skills existed as of 2026-05-23 (18% catalog completion at that point)
- Progress is milestone-gated, not calendar-dated

## Release readiness criteria

1. `validate.py` passes
2. 8–10 eval prompts present in source (router skills: per routed reference)
3. ≥ 85% aggregate eval pass rate, zero failed critical expectations
4. Packages successfully as a `.skill` file
5. No security or packaging blockers

See [Skill system](/docs/skills/skill-system.md) for naming and structure rules.
