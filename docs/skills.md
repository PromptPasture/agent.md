---
type: concept
title: Skills
description: Complete index of all Agent Skills in this library by catalog and status.
tags: [skills, catalog, index]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Skills

All skills follow verb-first naming (`<verb>-<subject>[-<variant>]` or a bare verb) and live under `src/skills/<catalog>/<name>/SKILL.md`. See [Skill system](/docs/skills/skill-system.md) for structure and quality rules.

## Stable catalogs

|Skill|Catalog|Description|
|---|---|---|
|`adapt`|productivity|Detect mismatches in skills, rules, or workflows and route to the right skill to apply the smallest necessary change|
|`audit-skill-security`|utility|Audit any skill before installing, updating, or trusting it — checks for prompt injection, exfiltration risk, and suspicious patterns|
|`avoid-ai-writing`|utility|Audit and rewrite content to remove AI writing patterns ("AI-isms")|
|`brainstorm`|productivity|Explore user intent, requirements, and design before implementation|
|`code-backend`|software-engineering|Generate production-ready backend code with auto-detected stack and P0–P3 quality checklist|
|`code-database`|software-engineering|Generate production-ready SQL, migrations, and ORM code with confirmed schema contracts and P0–P3 checklist|
|`code-frontend`|software-engineering|Generate production-ready frontend code with auto-detected stack, interface contracts, and P0–P3 checklist|
|`code-tests`|software-engineering|Generate production-ready automated tests (E2E, API, integration, load) with confirmed test plan and P0–P3 checklist|
|`dry`|productivity|Catch duplicated knowledge, logic, or structure that should have a single authoritative source|
|`git-branch`|utility|Create, switch, or rename Git branches using repository-aware naming conventions|
|`git-commit`|utility|Generate, improve, or apply Conventional Commit messages using staged changes and history|
|`landscape-design`|lifestyle|Transform outdoor spaces into functional, beautiful landscapes with expert plant knowledge and architectural styling|
|`lawyer`|lifestyle|Plain-language legal advisor for laypeople — contract review, drafting, Q&A, compliance|
|`plan`|productivity|Sequence work into ordered phases with dependencies and success conditions|
|`review`|productivity|Surface structured findings across consistent quadrants when reviewing any artifact|
|`review-code`|software-engineering|Review code changes, diffs, pull requests, or patches|
|`wiki`|productivity|Create, update, ingest, query, or lint a structured wiki knowledge base|
|`write-prd`|product|Write or revise a PRD, product requirements, or feature scope|
|`write-spec`|product|Write or revise a technical specification|
|`write-user-story`|product|Write or revise user stories, acceptance criteria, and sprint-ready increments|
|`yagni`|productivity|Catch speculative additions before they are built|

## In progress (not published)

|Skill|Description|
|---|---|
|`design-api`|API design|
|`manage`|Coordinate active work across people, agents, tasks, dependencies, blockers, and handoffs|
|`markitdown`|Convert local documents (PDF, Word, PowerPoint, Excel, EPUB, Outlook) to Markdown|
|`write-api-docs`|Write or revise reference documentation for existing APIs|
|`write-changelog`|Write or revise developer-facing changelogs|
|`write-readme`|Write or revise project README files|
|`write-release-notes`|Write or revise user-facing release notes|
|`write-runbook`|Write or revise executable operational runbooks|
|`write-ticket`|Write or revise Jira/GitHub/Linear tickets — bug, feature, task, chore, spike|

## Deprecated

|Skill|Replaced by|
|---|---|
|`remember`|`wiki`|

## Catalog detail pages

- [Productivity](/docs/skills/productivity.md)
- [Software engineering](/docs/skills/software-engineering.md)
- [Product](/docs/skills/product.md)
- [Utility](/docs/skills/utility.md)
- [Lifestyle](/docs/skills/lifestyle.md)
- [Documentation (in-progress)](/docs/skills/documentation.md)
