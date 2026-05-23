# Skill Library

This folder contains maintained agent skills.

A complete skill is a directory with a required `SKILL.md` file and optional bundled resources such as `references/`, `scripts/`, `assets/`, and `evals/`.

## Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`audit-skill-security`](audit-skill-security/SKILL.md) | Auditing third-party or local skills before installing, updating, or trusting them. | [`references/audit-protocol.md`](audit-skill-security/references/audit-protocol.md) |
| [`codegen-backend`](codegen-backend/SKILL.md) | Production backend code: APIs, services, middleware, workers, persistence, validation, auth, and backend tests. | [`references/`](codegen-backend/references/), [`evals/`](codegen-backend/evals/) |
| [`codegen-database`](codegen-database/SKILL.md) | Database code: schemas, DDL, OLTP SQL, analytics SQL, migrations, indexes, stored procedures, and dialect-specific scripts. | [`references/`](codegen-database/references/), [`evals/`](codegen-database/evals/) |
| [`codegen-frontend`](codegen-frontend/SKILL.md) | Production frontend code: components, routes, client state, forms, styling, accessibility, performance, PWA behavior, and visualization. | [`references/`](codegen-frontend/references/), [`evals/`](codegen-frontend/evals/) |
| [`codegen-test`](codegen-test/SKILL.md) | Automated tests and evals, including E2E, API, integration, performance, AI output, tool-use, RAG, and prompt regression suites. | [`references/`](codegen-test/references/), [`scripts/`](codegen-test/scripts/), [`evals/`](codegen-test/evals/) |
| [`creator-rule`](creator-rule/SKILL.md) | Writing or improving agent rules, instruction files, `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions, and `.agents/rules/*.md`. | [`scripts/`](creator-rule/scripts/), [`evals/`](creator-rule/evals/) |
| [`creator-skill`](creator-skill/SKILL.md) | Creating, editing, reviewing, evaluating, packaging, optimizing, or improving skills. Start here for skill authoring. | [`references/`](creator-skill/references/), [`scripts/`](creator-skill/scripts/), [`eval-viewer/`](creator-skill/eval-viewer/), [`agents/`](creator-skill/agents/), [`assets/`](creator-skill/assets/), [`evals/`](creator-skill/evals/) |
| [`design-api`](design-api/SKILL.md) | Contract-first API design for OpenAPI, AsyncAPI, GraphQL, endpoints, schemas, and request/response shapes. | [`references/`](design-api/references/), [`evals/`](design-api/evals/) |
| [`explain`](explain/SKILL.md) | Explaining general knowledge, concepts, code, behavior, design, architecture, APIs, data flow, and tradeoffs in simple terms. | [`evals/`](explain/evals/) |
| [`operator-git`](operator-git/SKILL.md) | Git branch naming, branch actions, commit-message drafting, and committing staged changes. | [`references/`](operator-git/references/), [`evals/`](operator-git/evals/) |
| [`review-code`](review-code/SKILL.md) | Reviewing code changes, diffs, pull requests, branches, or patches for correctness, regressions, security, performance, and test gaps. | [`references/`](review-code/references/), [`evals/`](review-code/evals/) |
| [`writer-prd`](writer-prd/SKILL.md) | Product requirements, product briefs, feature requirements, product scope, and launch requirements. | [`references/`](writer-prd/references/), [`evals/`](writer-prd/evals/) |
| [`writer-spec`](writer-spec/SKILL.md) | Technical specs, design docs, functional and non-functional requirements, data contracts, UI specs, release specs, and handoff docs. | [`references/`](writer-spec/references/), [`evals/`](writer-spec/evals/) |
| [`writer-tech-docs`](writer-tech-docs/SKILL.md) | READMEs, API docs, endpoint references, routine and on-call runbooks, changelogs, and release notes. | [`references/`](writer-tech-docs/references/), [`evals/`](writer-tech-docs/evals/) |
| [`writer-user-story`](writer-user-story/SKILL.md) | User stories, acceptance criteria, developer tasks, tickets, story points, and sprint planning breakdowns. | [`references/`](writer-user-story/references/), [`evals/`](writer-user-story/evals/) |

## Resource Folders

| Folder | Meaning |
| --- | --- |
| `references/` | Focused docs loaded only when needed, such as language guides, dialect notes, templates, and checklists. |
| `scripts/` | Deterministic helpers, validators, converters, eval runners, or packaging tools. |
| `assets/` | Templates, images, HTML views, example files, or other reusable artifacts. |
| `agents/` | Supporting agent prompts used by skill workflows. |
| `evals/` | Development-time eval prompts and fixtures. These are not runtime instructions. |

## Common Entry Points

Use [`creator-skill`](creator-skill/SKILL.md) to create, revise, package, or evaluate skills. Its schema notes live in [`creator-skill/references/schemas.md`](creator-skill/references/schemas.md), and its package command is:

```bash
cd .agents/skills/creator-skill
python3 -m scripts.package_skill ../codegen-database /tmp/skills-dist
```

Use this validation command when changing an existing skill:

```bash
python3 .agents/skills/creator-skill/scripts/quick_validate.py .agents/skills/codegen-database
```

The key rule is simple: keep `SKILL.md` and any files it references together. If a skill says to read `references/postgres.md`, that file must remain available relative to the skill folder. Tiny rule, large consequences. Filesystems enjoy pettiness.
