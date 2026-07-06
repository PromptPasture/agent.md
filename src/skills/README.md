# Skill Library

This folder contains maintained agent skills, grouped by category.

A complete skill is a directory with a required `SKILL.md` file and optional bundled resources such as `references/`, `scripts/`, and `assets/`.

## Folder Layout

|Folder|Contains|
|---|---|
|[`productivity/`](productivity/)|General reasoning, communication, planning, investigation, coordination, and memory skills.|
|[`product/`](product/)|Product requirements, specifications, user stories, and delivery definition skills.|
|[`software-engineering/`](software-engineering/)|Code, test, API design, and code review skills.|
|[`utility/`](utility/)|Operational helper skills that support the skill library itself.|
|[`lifestyle/`](lifestyle/)|Domain-specific skills for everyday non-technical tasks.|
|[`in-progress/`](in-progress/)|Skills under active development, not yet ready for production use.|
|[`deprecated/`](deprecated/)|Skills replaced by newer alternatives, kept for reference.|

## Productivity Skills

|Skill|Use it for|Notable resources|
|---|---|---|
|[`adapt`](productivity/adapt/SKILL.md)|Detecting evidence-driven change needs and routing updates to the right skill, workflow, artifact, or owner.|-|
|[`brainstorm`](productivity/brainstorm/SKILL.md)|Working through ambiguous problems, assumptions, hypotheses, and problem framing before deciding or planning.|-|
|[`dry`](productivity/dry/SKILL.md)|Catching duplicated knowledge, logic, or structure that should have a single authoritative source.|-|
|[`plan`](productivity/plan/SKILL.md)|Sequencing work before execution with phases, dependencies, risks, validation, and next actions.|-|
|[`review`](productivity/review/SKILL.md)|Reviewing artifacts and returning a retrospective board covering what is working, what is not, what to improve, and what to change.|-|
|[`wiki`](productivity/wiki/SKILL.md)|Creating, updating, ingesting, querying, or linting a structured wiki knowledge base.|-|
|[`yagni`](productivity/yagni/SKILL.md)|Catching speculative additions before they are built.|-|

## Software Engineering Skills

|Skill|Use it for|Notable resources|
|---|---|---|
|[`code-backend`](software-engineering/code-backend/SKILL.md)|Production backend code: APIs, services, middleware, workers, persistence, validation, auth, and backend tests.|[`references/`](software-engineering/code-backend/references/)|
|[`code-database`](software-engineering/code-database/SKILL.md)|Database code: schemas, DDL, OLTP SQL, analytics SQL, migrations, indexes, stored procedures, and dialect-specific scripts.|[`references/`](software-engineering/code-database/references/)|
|[`code-frontend`](software-engineering/code-frontend/SKILL.md)|Production frontend code: components, routes, client state, forms, styling, accessibility, performance, PWA behavior, and visualization.|[`references/`](software-engineering/code-frontend/references/)|
|[`code-tests`](software-engineering/code-tests/SKILL.md)|Automated product and system tests, including E2E, API, integration, load, and performance suites.|[`references/`](software-engineering/code-tests/references/)|
|[`review-code`](software-engineering/review-code/SKILL.md)|Reviewing code changes, diffs, pull requests, branches, or patches for correctness, regressions, security, performance, and test gaps.|—|

## Product Skills

|Skill|Use it for|Notable resources|
|---|---|---|
|[`write-prd`](product/write-prd/SKILL.md)|Product requirements, product briefs, feature requirements, product scope, and launch requirements.|[`references/`](product/write-prd/references/)|
|[`write-spec`](product/write-spec/SKILL.md)|Technical specs, design docs, functional and non-functional requirements, data contracts, UI specs, release specs, and handoff docs.|[`references/`](product/write-spec/references/)|
|[`write-user-story`](product/write-user-story/SKILL.md)|User stories, acceptance criteria, story points, and sprint-ready user-value increments.|-|

## Utility Skills

|Skill|Use it for|Notable resources|
|---|---|---|
|[`audit-skill-security`](utility/audit-skill-security/SKILL.md)|Auditing third-party or local skills before installing, updating, or trusting them.|[`references/audit-protocol.md`](utility/audit-skill-security/references/audit-protocol.md)|
|[`avoid-ai-writing`](utility/avoid-ai-writing/SKILL.md)|Auditing and rewriting content to remove AI writing patterns ("AI-isms").|-|
|[`git-branch`](utility/git-branch/SKILL.md)|Generating, switching, and renaming Git branches using repository-aware conventions.|-|
|[`git-commit`](utility/git-commit/SKILL.md)|Generating and applying Conventional Commit messages from repository evidence.|-|
|[`to-skill`](utility/to-skill/SKILL.md)|Drafting, revising, or pruning a skill using the Trigger, Structure, Steering, and Pruning checklist.|-|

## Lifestyle Skills

|Skill|Use it for|Notable resources|
|---|---|---|
|[`landscape-design`](lifestyle/landscape-design/SKILL.md)|Landscape and garden planning: plant selection, yard design, and backyard makeovers.|-|
|[`lawyer`](lifestyle/lawyer/SKILL.md)|Legal documents, contracts, compliance review, and drafting legal text in plain language.|-|

## In-Progress Skills

Skills under active development. Not yet production-ready.

|Skill|Use it for|
|---|---|
|[`design-api`](in-progress/design-api/SKILL.md)|Contract-first API design for OpenAPI, AsyncAPI, GraphQL, endpoints, schemas, and request/response shapes.|
|[`manage`](in-progress/manage/SKILL.md)|Managing active work across people, agents, tasks, dependencies, blockers, status, and handoffs.|
|[`markitdown`](in-progress/markitdown/SKILL.md)|Reading extraction-dependent local documents or converting them to Markdown with the MarkItDown CLI.|
|[`write-api-docs`](in-progress/write-api-docs/SKILL.md)|Reference documentation for implemented API endpoints, operations, schemas, errors, authentication, and examples.|
|[`write-changelog`](in-progress/write-changelog/SKILL.md)|Developer-facing changelogs, unreleased sections, release entries, breaking changes, and security changes.|
|[`write-readme`](in-progress/write-readme/SKILL.md)|Project READMEs covering purpose, installation, quick starts, usage, configuration, and contribution.|
|[`write-release-notes`](in-progress/write-release-notes/SKILL.md)|User-facing release notes, product updates, known issues, upgrade guidance, and action-required notices.|
|[`write-runbook`](in-progress/write-runbook/SKILL.md)|Routine operational procedures and on-call response runbooks with verification, rollback, mitigation, and escalation.|
|[`write-ticket`](in-progress/write-ticket/SKILL.md)|Jira and GitHub bug, feature, task, chore, documentation, and spike tickets using type-specific writing models.|

## Resource Folders

|Folder|Meaning|
|---|---|
|`references/`|Focused docs loaded only when needed, such as language guides, dialect notes, templates, and checklists.|
|`scripts/`|Deterministic helpers, validators, converters, eval runners, or packaging tools.|
|`assets/`|Templates, images, HTML views, example files, or other reusable artifacts.|
|`agents/`|Supporting agent prompts used by skill workflows.|

## Maintenance Notes

Keep `SKILL.md` and any files it references together. If a skill says to read `references/postgres.md`, that file must remain available relative to that skill folder.

When moving a skill between categories, update this index and any relative links in that skill's `SKILL.md` or supporting resources.
