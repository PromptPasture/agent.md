# Skill Library

This folder contains maintained agent skills, grouped by category.

A complete skill is a directory with a required `SKILL.md` file and optional bundled resources such as `references/`, `scripts/`, and `assets/`.

## Folder Layout

| Folder | Contains |
| --- | --- |
| [`productivity/`](productivity/) | General reasoning, communication, planning, investigation, coordination, and memory skills. |
| [`product/`](product/) | Product requirements, specifications, user stories, and delivery definition skills. |
| [`documentation/`](documentation/) | Technical documentation, operational guidance, and release communication skills. |
| [`software-engineering/`](software-engineering/) | Code, test, API design, and code review skills. |
| [`utility/`](utility/) | Operational helper skills that support the skill library itself. |

## Productivity Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`adapt`](productivity/adapt/SKILL.md) | Detecting evidence-driven change needs and routing updates to the right skill, workflow, artifact, or owner. | - |
| [`ask`](productivity/ask/SKILL.md) | Generating high-leverage questions, clarifying missing context, and surfacing assumptions. | - |
| [`brainstorm`](productivity/brainstorm/SKILL.md) | Working through ambiguous problems, assumptions, hypotheses, and problem framing before deciding or planning. | - |
| [`choose`](productivity/choose/SKILL.md) | Comparing options, weighing tradeoffs, and recommending a direction using explicit criteria. | - |
| [`classify`](productivity/classify/SKILL.md) | Organizing material into meaningful groups by criteria, similarity, priority, dependency, or abstraction level. | - |
| [`explain`](productivity/explain/SKILL.md) | Explaining general knowledge, concepts, code, behavior, design, architecture, APIs, data flow, and tradeoffs in simple terms. | - |
| [`investigate`](productivity/investigate/SKILL.md) | Investigating local repository, project document, and attached-artifact context with evidence. | - |
| [`manage`](productivity/manage/SKILL.md) | Managing active work across people, agents, tasks, dependencies, blockers, status, and handoffs. | - |
| [`plan`](productivity/plan/SKILL.md) | Sequencing work before execution with phases, dependencies, risks, validation, and next actions. | - |
| [`remember`](productivity/remember/SKILL.md) | Preserving durable project facts, decisions, conventions, and useful observations in memory files. | - |
| [`review`](productivity/review/SKILL.md) | Reviewing artifacts and returning a retrospective board covering what is working, what is not, what to improve, and what to change. | - |

## Software Engineering Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`code-backend`](software-engineering/code-backend/SKILL.md) | Production backend code: APIs, services, middleware, workers, persistence, validation, auth, and backend tests. | [`references/`](software-engineering/code-backend/references/) |
| [`code-database`](software-engineering/code-database/SKILL.md) | Database code: schemas, DDL, OLTP SQL, analytics SQL, migrations, indexes, stored procedures, and dialect-specific scripts. | [`references/`](software-engineering/code-database/references/) |
| [`code-frontend`](software-engineering/code-frontend/SKILL.md) | Production frontend code: components, routes, client state, forms, styling, accessibility, performance, PWA behavior, and visualization. | [`references/`](software-engineering/code-frontend/references/) |
| [`code-tests`](software-engineering/code-tests/SKILL.md) | Automated product and system tests, including E2E, API, integration, load, and performance suites. | [`references/`](software-engineering/code-tests/references/) |
| [`design-api`](software-engineering/design-api/SKILL.md) | Contract-first API design for OpenAPI, AsyncAPI, GraphQL, endpoints, schemas, and request/response shapes. | [`references/`](software-engineering/design-api/references/) |
| [`review-code`](software-engineering/review-code/SKILL.md) | Reviewing code changes, diffs, pull requests, branches, or patches for correctness, regressions, security, performance, and test gaps. | — |

## Product Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`write-prd`](product/write-prd/SKILL.md) | Product requirements, product briefs, feature requirements, product scope, and launch requirements. | [`references/`](product/write-prd/references/) |
| [`write-spec`](product/write-spec/SKILL.md) | Technical specs, design docs, functional and non-functional requirements, data contracts, UI specs, release specs, and handoff docs. | [`references/`](product/write-spec/references/) |
| [`write-user-story`](product/write-user-story/SKILL.md) | User stories, acceptance criteria, developer tasks, tickets, story points, and sprint planning breakdowns. | [`references/`](product/write-user-story/references/) |

## Documentation Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`write-tech-docs`](documentation/write-tech-docs/SKILL.md) | READMEs, API docs, endpoint references, routine and on-call runbooks, changelogs, and release notes. | [`references/`](documentation/write-tech-docs/references/) |

## Utility Skills

| Skill | Use it for | Notable resources |
| --- | --- | --- |
| [`audit-skill-security`](utility/audit-skill-security/SKILL.md) | Auditing third-party or local skills before installing, updating, or trusting them. | [`references/audit-protocol.md`](utility/audit-skill-security/references/audit-protocol.md) |
| [`git-branch`](utility/git-branch/SKILL.md) | Generating, switching, and renaming Git branches using repository-aware conventions. | - |
| [`git-commit`](utility/git-commit/SKILL.md) | Generating and applying Conventional Commit messages from repository evidence. | - |

## Resource Folders

| Folder | Meaning |
| --- | --- |
| `references/` | Focused docs loaded only when needed, such as language guides, dialect notes, templates, and checklists. |
| `scripts/` | Deterministic helpers, validators, converters, eval runners, or packaging tools. |
| `assets/` | Templates, images, HTML views, example files, or other reusable artifacts. |
| `agents/` | Supporting agent prompts used by skill workflows. |

## Maintenance Notes

Keep `SKILL.md` and any files it references together. If a skill says to read `references/postgres.md`, that file must remain available relative to that skill folder.

When moving a skill between categories, update this index and any relative links in that skill's `SKILL.md` or supporting resources.
