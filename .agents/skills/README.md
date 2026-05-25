# Skill Library

This folder contains maintained agent skills.

A complete skill is a directory with a required `SKILL.md` file and optional bundled resources such as `references/`, `scripts/`, `assets/`, and `evals/`.

## Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`adapt`](adapt/SKILL.md) | Detecting evidence-driven change needs and routing updates to the right skill, workflow, artifact, or owner. | [`evals/`](adapt/evals/) |
| [`ask`](ask/SKILL.md) | Generating high-leverage questions, clarifying missing context, and surfacing assumptions. | [`evals/`](ask/evals/) |
| [`audit-skill-security`](audit-skill-security/SKILL.md) | Auditing third-party or local skills before installing, updating, or trusting them. | [`references/audit-protocol.md`](audit-skill-security/references/audit-protocol.md) |
| [`brainstorm`](brainstorm/SKILL.md) | Working through ambiguous problems, assumptions, hypotheses, and problem framing before deciding or planning. | [`evals/`](brainstorm/evals/) |
| [`choose`](choose/SKILL.md) | Comparing options, weighing tradeoffs, and recommending a direction using explicit criteria. | [`evals/`](choose/evals/) |
| [`classify`](classify/SKILL.md) | Organizing material into meaningful groups by criteria, similarity, priority, dependency, or abstraction level. | [`evals/`](classify/evals/) |
| [`code-backend`](code-backend/SKILL.md) | Production backend code: APIs, services, middleware, workers, persistence, validation, auth, and backend tests. | [`references/`](code-backend/references/), [`evals/`](code-backend/evals/) |
| [`code-database`](code-database/SKILL.md) | Database code: schemas, DDL, OLTP SQL, analytics SQL, migrations, indexes, stored procedures, and dialect-specific scripts. | [`references/`](code-database/references/), [`evals/`](code-database/evals/) |
| [`code-frontend`](code-frontend/SKILL.md) | Production frontend code: components, routes, client state, forms, styling, accessibility, performance, PWA behavior, and visualization. | [`references/`](code-frontend/references/), [`evals/`](code-frontend/evals/) |
| [`code-tests`](code-tests/SKILL.md) | Automated tests and evals, including E2E, API, integration, performance, AI output, tool-use, RAG, and prompt regression suites. | [`references/`](code-tests/references/), [`scripts/`](code-tests/scripts/), [`evals/`](code-tests/evals/) |
| [`create-rule`](create-rule/SKILL.md) | Writing or improving agent rules, instruction files, `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions, and `.agents/rules/*.md`. | [`scripts/`](create-rule/scripts/), [`evals/`](create-rule/evals/) |
| [`create-skill`](create-skill/SKILL.md) | Creating, editing, reviewing, evaluating, packaging, optimizing, or improving skills. Start here for skill authoring. | [`references/`](create-skill/references/), [`scripts/`](create-skill/scripts/), [`eval-viewer/`](create-skill/eval-viewer/), [`agents/`](create-skill/agents/), [`assets/`](create-skill/assets/), [`evals/`](create-skill/evals/) |
| [`design-api`](design-api/SKILL.md) | Contract-first API design for OpenAPI, AsyncAPI, GraphQL, endpoints, schemas, and request/response shapes. | [`references/`](design-api/references/), [`evals/`](design-api/evals/) |
| [`explain`](explain/SKILL.md) | Explaining general knowledge, concepts, code, behavior, design, architecture, APIs, data flow, and tradeoffs in simple terms. | [`evals/`](explain/evals/) |
| [`explore`](explore/SKILL.md) | Investigating local repository, project document, and attached-artifact context with evidence. | [`evals/`](explore/evals/) |
| [`manage`](manage/SKILL.md) | Managing active work across people, agents, tasks, dependencies, blockers, status, and handoffs. | [`evals/`](manage/evals/) |
| [`manage-git`](manage-git/SKILL.md) | Git branch naming, branch actions, commit-message drafting, and committing staged changes. | [`references/`](manage-git/references/), [`evals/`](manage-git/evals/) |
| [`plan`](plan/SKILL.md) | Sequencing work before execution with phases, dependencies, risks, validation, and next actions. | [`evals/`](plan/evals/) |
| [`remember`](remember/SKILL.md) | Preserving durable project facts, decisions, conventions, and useful observations in `.agents/memory/`. | [`evals/`](remember/evals/) |
| [`review-code`](review-code/SKILL.md) | Reviewing code changes, diffs, pull requests, branches, or patches for correctness, regressions, security, performance, and test gaps. | [`references/`](review-code/references/), [`evals/`](review-code/evals/) |
| [`write-prd`](write-prd/SKILL.md) | Product requirements, product briefs, feature requirements, product scope, and launch requirements. | [`references/`](write-prd/references/), [`evals/`](write-prd/evals/) |
| [`write-spec`](write-spec/SKILL.md) | Technical specs, design docs, functional and non-functional requirements, data contracts, UI specs, release specs, and handoff docs. | [`references/`](write-spec/references/), [`evals/`](write-spec/evals/) |
| [`write-tech-docs`](write-tech-docs/SKILL.md) | READMEs, API docs, endpoint references, routine and on-call runbooks, changelogs, and release notes. | [`references/`](write-tech-docs/references/), [`evals/`](write-tech-docs/evals/) |
| [`write-user-story`](write-user-story/SKILL.md) | User stories, acceptance criteria, developer tasks, tickets, story points, and sprint planning breakdowns. | [`references/`](write-user-story/references/), [`evals/`](write-user-story/evals/) |

## Resource Folders

| Folder | Meaning |
| --- | --- |
| `references/` | Focused docs loaded only when needed, such as language guides, dialect notes, templates, and checklists. |
| `scripts/` | Deterministic helpers, validators, converters, eval runners, or packaging tools. |
| `assets/` | Templates, images, HTML views, example files, or other reusable artifacts. |
| `agents/` | Supporting agent prompts used by skill workflows. |
| `evals/` | Development-time eval prompts and fixtures. These are not runtime instructions. |

## Common Entry Points

Use [`create-skill`](create-skill/SKILL.md) to create, revise, package, or evaluate skills. Its schema notes live in [`create-skill/references/schemas.md`](create-skill/references/schemas.md), and its package command is:

```bash
cd .agents/skills/create-skill
python3 -m scripts.package_skill ../code-database /tmp/skills-dist
```

Use this validation command when changing an existing skill:

```bash
python3 .agents/skills/create-skill/scripts/quick_validate.py .agents/skills/code-database
```

The key rule is simple: keep `SKILL.md` and any files it references together. If a skill says to read `references/postgres.md`, that file must remain available relative to the skill folder. Tiny rule, large consequences. Filesystems enjoy pettiness.
