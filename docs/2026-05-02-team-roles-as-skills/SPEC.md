# SPEC: Software Team Roles as Skills

## Document Info

**Status:** APPROVED  
**Version:** 2.0  
**Date:** 2026-05-23  
**Owner:** Oleg Shulyakov
**Reviewers:** Skill authors and maintainers
**Target release:** Milestone-gated; no fixed calendar date  
**Source PRD:** [PRD.md](PRD.md)  
**Tracker:** [TASKS.md](TASKS.md)

## 1. Overview

### 1.1 Purpose

This specification defines the local skill library for software delivery roles: its catalog, naming rules, filesystem structure, routing behavior, validation gates, and release readiness requirements.

The goal is to make role-specific agent behavior reusable and testable. A user should be able to ask for a PRD, API contract, test suite, runbook, security audit, or similar artifact without restating the role, structure, quality bar, or verification expectations each time.

### 1.2 Background

CLI agents can produce many software delivery artifacts, but output quality drifts when role instructions live only in prompts. Teams repeatedly explain what a good PRD, technical spec, database migration, E2E test suite, release checklist, or postmortem should contain. This creates duplicated prompting effort and weak transfer between sessions.

Software Team Roles as Skills turns those repeated instructions into a versioned local library. Each skill owns one role capability or artifact family, declares when it should trigger, and carries its own workflow, output format, references, evals, and packaging expectations.

The first catalog release is milestone-gated. It is ready when all 55 cataloged skills are implemented, validated, evaluated, documented, and packageable from local artifacts.

### 1.3 Roles & Responsibilities

| Role / Team | Responsibility | Decision Area |
| --- | --- | --- |
| Product owner | Approves product scope, target personas, goals, and non-goals. | Catalog scope and success criteria |
| Skill maintainer | Creates, tests, packages, and updates skills. | Skill structure, references, evals, and readiness |
| Skill author | Writes role instructions and artifact formats. | Trigger behavior and output quality |
| CLI agent user | Invokes skills through direct names or natural task intent. | Feedback on usability and output fit |
| Reviewer | Reviews skill behavior, eval coverage, and drift against docs. | Release readiness |

### 1.4 Customer & Business Context

The primary users are product, engineering, quality, security, operations, data, ML, and leadership practitioners who need predictable AI assistance for common software delivery artifacts. The business value is less prompt drift, fewer one-off instructions, and a reusable quality bar for team workflows.

The library must remain local-first. It is not a plugin marketplace, a project management system, or a live integration layer.

### 1.5 Goals

| Goal | Success Metric | Target |
| --- | --- | --- |
| Complete catalog coverage | Cataloged software delivery role skills exist in `.agents/skills/`. | 55 skills |
| Keep discovery predictable | Skill names follow prefix-first convention. | 100% compliance |
| Reduce repeated prompting | Completed skills encode trigger, output, and quality expectations. | Every completed skill has specific frontmatter and instructions |
| Keep complex domains usable | Router skills select variants from context. | Ask at most one clarifying question when materially ambiguous |
| Maintain quality | Skills pass validation and eval thresholds. | `quick_validate.py` pass plus required eval coverage |
| Support local distribution | Release-ready skills package as `.skill` files. | Successful local package build |

### 1.6 Non-Goals

Runtime plugin hosting, remote skill fetching, marketplace behavior, live Jira/GitHub/CI/observability/cloud integrations, long-lived workflow automation, task-state management, real-time dashboards, and organization-specific convention packs are out of scope for this release.

## 2. Functional Requirements

### 2.1 Actors

| Actor | Description |
| --- | --- |
| User | Requests an artifact or names a skill directly. |
| Agent | Selects, loads, and applies the relevant local skill. |
| Skill maintainer | Builds, validates, evaluates, packages, and updates skills. |
| Reviewer | Confirms behavior, catalog fit, and readiness gates. |

### 2.2 Key Flows

#### Flow: Invoke a focused skill

1. User names a completed skill or asks for the artifact it owns.
2. Agent loads the skill's `SKILL.md`.
3. Agent follows the skill workflow and produces or edits the requested artifact.
4. Agent verifies the result using the checks appropriate to the task.

#### Flow: Invoke a router skill

1. User asks for a broad domain artifact, such as tests, backend code, frontend code, technical docs, specs, infrastructure setup, or security audit.
2. Agent detects the variant from explicit text, repository files, imports, package metadata, or existing context.
3. Agent loads only the required reference files.
4. If routing remains materially ambiguous, agent asks one concise clarifying question.
5. Agent produces the requested artifact and reports assumptions or verification gaps.

#### Flow: Add or update a skill

1. Maintainer confirms trigger scope, output artifact, routing needs, and eval expectations.
2. Maintainer creates or updates `SKILL.md`, references, and evals.
3. Maintainer validates the skill with `quick_validate.py`.
4. Maintainer runs or reviews eval coverage where available.
5. Maintainer updates PRD, SPEC, TASKS, and memory notes when catalog behavior changes.
6. Maintainer packages the skill once release-ready.

### 2.3 Requirements

#### FR-001: Catalog Definition

**Priority:** Must-have  
**Actor:** Skill maintainer  
**Requirement:** The library shall define exactly 55 catalog skills for the first full release.

**Acceptance criteria:**

- The catalog lists each skill name, primary roles, and output artifact.
- Each catalog skill maps to one approved prefix type.
- PRD, SPEC, and TASKS agree on catalog names.
- Drift between docs and `.agents/skills/` is treated as a release blocker.

#### FR-002: Prefix-First Naming

**Priority:** Must-have  
**Actor:** Skill maintainer  
**Requirement:** Every catalog skill shall use `<type>-<subject>[-<variant>]`.

**Acceptance criteria:**

- Valid types are `audit`, `checklist`, `codegen`, `design`, `diagram`, `model`, `patterns`, `planner`, `report`, `review`, `setup`, `strategy`, `template`, `tracker`, and `writer`.
- Skill folders sort predictably by artifact type in the filesystem.
- Renames update PRD, SPEC, TASKS, references, and evals in the same change.

#### FR-003: Standard Skill Structure

**Priority:** Must-have  
**Actor:** Skill author  
**Requirement:** Each completed skill shall have a standard local folder layout.

**Acceptance criteria:**

- `SKILL.md` exists and contains valid YAML frontmatter with `name` and `description`.
- `description` states when to trigger the skill and what artifact it produces.
- `evals/evals.json` exists for release-ready skills.
- `references/` is used only for substantial reusable guidance loaded on demand.
- `SKILL.md` stays under 500 lines.

#### FR-004: Router Skill Behavior

**Priority:** Should-have  
**Actor:** Agent  
**Requirement:** Multi-variant skills shall route to the correct reference from context before asking the user.

**Acceptance criteria:**

- Router skills detect variants from explicit user wording, file extensions, imports, package names, and repository structure where applicable.
- Router skills load only relevant references unless the skill explicitly permits bounded secondary references.
- Router skills ask at most one clarifying question when the variant is materially ambiguous.
- Router evals include a `reference` field for each routed case.

#### FR-005: Trigger Collision Prevention

**Priority:** Must-have  
**Actor:** Skill author  
**Requirement:** Skills with overlapping domains shall define explicit trigger boundaries.

**Acceptance criteria:**

- High-risk pairs have documented disambiguation rules.
- Evals include boundary prompts for likely collisions.
- Skill descriptions favor correct over-triggering but avoid stealing work from more specific skills.

#### FR-006: Validation and Eval Coverage

**Priority:** Must-have  
**Actor:** Skill maintainer  
**Requirement:** Release-ready skills shall pass structural validation and required eval coverage.

**Acceptance criteria:**

- `python3 .agents/skills/creator-skill/scripts/quick_validate.py .agents/skills/<skill-name>` passes.
- Focused skills have 8-10 realistic eval prompts.
- Router skills have 8-10 eval prompts per routed reference before release readiness.
- Eval assertions reach at least 85% aggregate pass rate with no failed critical expectations.
- Safety-sensitive or boundary-heavy skills include evals for error handling and misuse resistance.

#### FR-007: Packaging

**Priority:** Should-have  
**Actor:** Skill maintainer  
**Requirement:** Release-ready skills shall package into local `.skill` artifacts.

**Acceptance criteria:**

- Packaging runs from `.agents/skills/creator-skill`.
- Package command succeeds: `python3 -m scripts.package_skill ../<skill-name> /tmp/skills-dist`.
- Package includes required instructions, references, scripts, and assets.
- Root-level `evals/` are intentionally excluded from packaged artifacts by `package_skill.py`.
- Package output is verified by listing the archive and confirming it contains `<skill-name>/SKILL.md`.

#### FR-008: Security and Testing Separation

**Priority:** Must-have  
**Actor:** Skill author  
**Requirement:** Security audit behavior and test-generation behavior shall stay separated.

**Acceptance criteria:**

- `audit-security` owns prompt injection, jailbreak, exfiltration, secrets, OWASP review, and threat modeling.
- `codegen-test` owns executable tests, AI evals, tool-use evals, performance tests, fixtures, framework setup, and CI test setup.
- Boundary prompts route consistently between the two.

## 3. Non-Functional Requirements

| Category | Requirement | Target | Priority |
| --- | --- | --- | --- |
| Maintainability | Skill instructions remain concise and modular. | `SKILL.md` under 500 lines; detailed variants in `references/` | High |
| Testability | Behavior can be evaluated with representative prompts. | 8-10 evals per focused skill or per router reference | High |
| Discoverability | Users can invoke by skill name, artifact, or task intent. | Frontmatter descriptions include triggers and output artifacts | High |
| Consistency | Terms, names, priorities, and status stay aligned. | PRD, SPEC, TASKS, and skill folders match | High |
| Local-first operation | Skills work without live network integrations. | Instructions, references, scripts, assets, and evals are local | High |
| Token efficiency | Skills load only needed guidance. | Router references are loaded on demand | Medium |
| Extensibility | Complex domains can grow without skill-count explosion. | Router pattern handles variants sharing one role context | Medium |

## 4. Skill Architecture

### 4.1 Naming Convention

All skills use prefix-first naming:

```text
<type>-<subject>[-<variant>]
```

The type identifies the artifact or action family. The subject identifies the domain. The optional variant is allowed only when a separate folder is clearer than a router reference.

### 4.2 Filesystem Layout

```text
.agents/skills/
├── <skill-name>/
│   ├── SKILL.md
│   ├── evals/
│   │   └── evals.json
│   ├── references/
│   │   └── <variant>.md
│   ├── scripts/
│   │   └── <helper>.py
│   └── assets/
│       └── <asset>
```

Only `SKILL.md` is required while drafting. Release-ready skills require eval coverage. `references/`, `scripts/`, and `assets/` are optional and should exist only when they are used.

### 4.3 Frontmatter Metadata

```yaml
---
name: <skill-name>
description: Use when <trigger conditions>. Produces <specific output artifact>.
license: Apache-2.0
version: 1.2.0
tags:
  - docs
  - planning
author: Oleg Shulyakov
metadata:
  catalog: software-team-roles
---
```

Descriptions are routing metadata. They must name likely user wording, related contexts, and the artifact produced.

Allowed frontmatter fields are:

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | A unique identifier for the skill. |
| `description` | Yes | A concise explanation of the skill's purpose and when to use it. |
| `license` | No | The name of the license, such as `MIT` or `Apache-2.0`. |
| `version` | No | Semantic versioning string, such as `1.2.0`. |
| `tags` | No | A list of categories for easier discovery and filtering. |
| `author` | No | The creator's name or GitHub profile URL. |
| `metadata` | No | A nested mapping for arbitrary key-value pairs. |

### 4.4 Router Pattern

Router skills use one `SKILL.md` plus variant references when related artifacts share a role context. The router must:

1. Detect the target variant from explicit request text.
2. Inspect repository context when useful and available.
3. Load the smallest useful reference set.
4. Ask one concise question only when the route changes the output materially.
5. Mark inferred details with `[assumed]` when producing a spec or planning artifact.

Router skills for this release are `audit-security`, `codegen-frontend`, `codegen-backend`, `codegen-database`, `codegen-mobile`, `codegen-test`, `design-arch`, `writer-spec`, `setup-infra`, `template-creator`, `writer-tech-docs`, `review-code`, and `planner-capacity`.

## 5. Catalog

### 5.1 Full Skill Catalog

| Skill | Primary Roles | Output Artifact |
| --- | --- | --- |
| `audit-a11y` | Frontend Dev, UX | Accessibility audit with WCAG violations, severity, and fixes |
| `audit-gap` | System Analyst | Gap analysis report: current state, target state, remediation |
| `audit-security` | Security Eng | Security router: OWASP review, secrets audit, threat model |
| `audit-test-flaky` | AQA | Flaky test report with root cause and fix recommendations |
| `checklist-release` | Release Manager | Release checklist with rollback criteria |
| `codegen-backend` | Backend Dev | Backend code: routes, services, middleware, tests |
| `codegen-database` | DBA, Backend, Data Eng | Database code: schemas, SQL, migrations, analytics queries |
| `codegen-frontend` | Frontend Dev | Frontend code: components, pages, state, styling |
| `codegen-mobile` | Mobile Dev | Mobile code: screens, navigation, platform patterns |
| `codegen-test` | AQA | Test suites, eval harnesses, fixtures, configs, CI setup |
| `design-api` | Backend Dev | API contract: OpenAPI, AsyncAPI, GraphQL, endpoints, schemas |
| `design-arch` | Architect | Architecture router: system design, ADR, C4 diagram |
| `diagram-dfd` | System Analyst | Data flow diagram in Mermaid or structured text |
| `diagram-integration` | System Analyst | Integration map: systems, APIs, data flows, ownership |
| `diagram-ux-flow` | UX Designer | User flow or journey map |
| `model-dbt` | Data Eng | dbt model with SQL, schema, tests, and docs |
| `patterns-auth` | Backend Dev | Auth implementation patterns for JWT, OAuth2, sessions, RBAC |
| `patterns-graphql` | Backend Dev | GraphQL schema, resolver, pagination, and N+1 patterns |
| `patterns-realtime` | Backend Dev | WebSocket, SSE, and polling strategy patterns |
| `planner-capacity` | DevOps, SRE | Capacity plan for traffic, storage, compute, and scaling |
| `planner-sprint` | Scrum Master | Sprint plan with goal, capacity, stories, impediments |
| `report-cve` | Security Eng | CVE triage report with affected versions and remediation |
| `report-db-health` | DBA | Database health report |
| `report-team-health` | Team Lead | Team health report with delivery and risk signals |
| `review-code` | Team Lead | Code review findings prioritized by risk |
| `setup-developer-portal` | Platform Eng | Developer portal setup and onboarding structure |
| `setup-eval-harness` | ML Eng | Eval harness with dataset, rubric, metrics, benchmark runner |
| `setup-infra` | DevOps, Data Eng | Infrastructure setup router: IaC, CI/CD, ETL, observability |
| `setup-monorepo` | Platform Eng | Monorepo setup and tooling configuration |
| `setup-rag` | AI Eng | RAG pipeline setup |
| `strategy-api-versioning` | Backend Dev, Architect | API versioning and deprecation strategy |
| `strategy-backup` | DBA | Backup strategy with retention and restore SLAs |
| `strategy-dependency-upgrade` | Release Manager, DevOps | Dependency upgrade strategy |
| `strategy-feature-flag` | Team Lead, Backend | Feature flag rollout, lifecycle, and kill-switch strategy |
| `template-creator` | Team Lead, Scrum Master, PM, PO | Reusable templates for team workflows |
| `tracker-velocity` | Scrum Master | Sprint metrics and velocity report |
| `writer-alert-rules` | SRE | Alert rules with severity, routing, and runbook links |
| `writer-backlog` | PO | Groomed backlog with priority, sizing, and dependencies |
| `writer-compliance` | Security, Legal | Compliance documentation and evidence checklist |
| `writer-epic` | PO | Epic with goal, value, child stories, definition of done |
| `writer-lineage` | Data Eng | Data lineage document |
| `writer-mentorship` | Team Lead | Mentorship guide |
| `writer-ml-experiment` | ML Eng | ML experiment report and model-card section |
| `writer-postmortem` | Team Lead, SRE | Postmortem with timeline, root cause, action items |
| `writer-prd` | PM, PO | Product Requirements Document |
| `writer-prompt` | ML, AI Eng | Prompt specification with examples and eval criteria |
| `writer-slo` | SRE | SLO definition with SLI, target, error budget, alerts |
| `writer-spec` | SA, Architect, UX | Functional, technical, NFR, design, or data-contract spec |
| `writer-stakeholder` | PM, PO | Stakeholder update |
| `writer-team-agreement` | Scrum Master | Team working agreement |
| `writer-tech-docs` | Tech Writer, Backend, SRE, Release Mgr | Technical docs router: README, API docs, runbooks, changelog, release notes |
| `writer-tech-radar` | Architect | Tech radar |
| `writer-test-strategy` | AQA, QA | Test strategy |
| `writer-use-case` | System Analyst | Use case document |
| `writer-user-story` | PO, Team Lead | User story with acceptance criteria and developer tasks |

## 6. Variant References

### 6.1 Required Router Reference Sets

| Skill | Required references |
| --- | --- |
| `writer-spec` | `functional.md`, `technical.md`, `non-functional.md`, `design-ui.md`, `data-contract.md` |
| `design-arch` | `system-design.md`, `adr.md`, `c4.md` |
| `codegen-database` | `schema-design.md`, `migration.md`, `common.md`, plus supported dialect references |
| `codegen-frontend` | Language, framework, styling, accessibility, forms, state, performance, PWA, i18n, visualization references |
| `codegen-backend` | Language-level references plus supported framework references |
| `codegen-mobile` | `swift.md`, `kotlin-android.md`, `react-native.md`, `flutter.md` |
| `codegen-test` | `e2e.md`, `api.md`, `perf.md`, `framework-setup.md`, `ai-output.md`, `ai-tool-use.md`, `ai-perf.md` |
| `setup-infra` | `iac.md`, `cicd.md`, `etl.md`, `observability.md` |
| `planner-capacity` | `db.md`, `infra.md` |
| `audit-security` | `owasp.md`, `secrets.md`, `threat-model.md` |
| `writer-tech-docs` | `readme.md`, `api-docs.md`, `runbook-routine.md`, `runbook-oncall.md`, `changelog.md`, `release-notes.md` |
| `review-code` | `checklist.md`, `regressions.md`, `security.md`, `performance.md`, `test-gaps.md` |
| `template-creator` | `pr.md`, `retro.md`, `issue.md`, `meeting.md`, `decision.md`, `incident.md`, `release.md` |

### 6.2 Collision Rules

| Pair | Routing rule |
| --- | --- |
| `writer-prd` vs `writer-spec` | PRD owns product goals, personas, scope, and success metrics; spec owns behavior, technical detail, system handoff, and requirements. |
| `design-api` vs `writer-tech-docs` API docs | `design-api` is contract-first before implementation; `writer-tech-docs` documents an existing API. |
| `design-arch` variants | System design is broad architecture; ADR is one decision; C4 is diagram-focused. |
| `writer-user-story` vs `writer-epic` | User story is one deliverable with acceptance criteria and tasks; epic groups related stories. |
| `codegen-test` vs `writer-test-strategy` | `codegen-test` writes executable tests/config/evals; `writer-test-strategy` writes planning guidance. |
| `review-code` vs `audit-security` | `review-code` reviews a code change; `audit-security` performs standalone security analysis. |
| `template-creator` vs `writer-*` | `template-creator` creates reusable blank templates; `writer-*` creates filled artifacts. |
| `audit-security` vs `codegen-test` AI evals | `audit-security` owns abuse, exfiltration, secrets, and threat modeling; `codegen-test` owns quality, tool-use, latency, cost, and regression evals. |

## 7. Validation

### 7.1 Structural Validation

Each release-ready skill must pass:

```bash
python3 .agents/skills/creator-skill/scripts/quick_validate.py .agents/skills/<skill-name>
```

Validation failures block packaging. Common blockers include invalid frontmatter, missing required sections, weak scan anchors, malformed evals, missing router `reference` fields, and unused placeholder folders.

### 7.2 Eval Requirements

Focused skills require 8-10 realistic eval prompts. Router skills require 8-10 prompts per routed reference before release readiness. Release-ready skills must reach at least 85% aggregate expectation pass rate with no failed critical expectations.

Eval prompts must cover happy paths, ambiguous requests, boundary triggers, expected error handling, and at least one realistic repository or artifact context when the skill depends on local files.

### 7.3 Manual Review

Reviewers should inspect:

- Trigger fit: the skill activates for the right requests.
- Output fit: the artifact is concrete and reusable.
- Scope control: the skill does not absorb unrelated work.
- Verification guidance: the skill tells the agent how to test or review the output.
- Token discipline: large guidance lives in references, not `SKILL.md`.

## 8. Error Handling

| Error Path | Expected Behavior |
| --- | --- |
| Missing skill folder | Report that the skill is not implemented and continue with the closest available skill only if safe. |
| Missing `SKILL.md` | Treat the skill as not release-ready. Do not package it. |
| Invalid frontmatter | Fix before validation or release. |
| Missing evals | Mark as draft or incomplete; do not call it release-ready. |
| Ambiguous router request | Ask one concise clarifying question when context cannot decide the variant. |
| Missing router reference | State the missing reference and either use a narrower available reference or stop if behavior would be invented. |
| Catalog/doc drift | Update PRD, SPEC, TASKS, and relevant memory notes together. |
| Packaging failure | Fix validation, missing assets, or packaging metadata before distribution. |

## 9. Build Process

Each skill should be built with `creator-skill` using this sequence:

1. Clarify trigger scope, expected output, routing needs, and eval expectations.
2. Draft `SKILL.md` with frontmatter, concise workflow instructions, clear section headings, and scan anchors.
3. Move reusable detail into `references/` only when needed.
4. Add `evals/evals.json` with required focused or routed coverage.
5. Run `quick_validate.py`.
6. Run or review eval iterations when behavior needs evidence.
7. Review outputs qualitatively and assertions quantitatively where objective checks apply.
8. Iterate until feedback is resolved, improvements flatten, or the user accepts behavior.
9. Tune the description for triggering accuracy after behavior is stable.
10. Package release-ready skills from `.agents/skills/creator-skill`:

```bash
python3 -m scripts.package_skill ../<skill-name> /tmp/skills-dist
```

## 10. Release Readiness

### 10.1 Milestones

| Milestone | Exit Criteria | Owner |
| --- | --- | --- |
| M-1 Foundation skills | P1 skills in TASKS are implemented, evaluated, and documented. | Oleg Shulyakov |
| M-2 Delivery skills | P2/P3 delivery and operational skills are implemented with eval coverage. | Skill maintainers |
| M-3 Specialist skills | Remaining specialist skills are implemented or deliberately deferred with rationale. | Skill maintainers |
| M-4 Distribution readiness | Completed skills package and install from local artifacts. | Skill maintainers |

### 10.2 Launch Checklist

| Activity | Owner | Required Before Launch |
| --- | --- | --- |
| Catalog reconciliation | Skill maintainer | Yes |
| Structural validation | Skill maintainer | Yes |
| Eval coverage review | Reviewer | Yes |
| Router collision review | Reviewer | Yes |
| Packaging smoke test | Skill maintainer | Yes |
| Documentation update | Skill maintainer | Yes |
| Support/training note | Skill maintainer | Before broader team rollout |
| Feedback collection path | Product owner | Before broader team rollout |

## 11. Risks and Mitigations

| Risk | Impact | Mitigation | Status |
| --- | --- | --- | --- |
| Similar skills route ambiguously. | High | Keep descriptions trigger-specific and add boundary evals. | Open |
| Router skills become too broad. | Medium | Use references for related variants only when they share role context. | Open |
| Eval requirements slow creation. | Medium | Treat evals as definition of done, not cleanup. | Open |
| Team conventions do not fit base skills. | Medium | Keep base skills generic; defer convention packs. | Open |
| Docs drift from folders. | High | Update PRD, SPEC, TASKS, and memory together. | Open |
| Older skills fail current validation. | High | Run validation per skill and fix blockers before release readiness. | Open |
| Implementation count is inconsistent. | Medium | Reconcile PRD status, TASKS, and actual `.agents/skills/` folders. | Open |

## 12. Decisions

| Decision | Rationale | Owner | Date |
| --- | --- | --- | --- |
| Use milestone gates instead of a fixed date. | Release depends on complete implementation, evals, docs, and packaging. | Oleg Shulyakov | 2026-05-23 |
| Use router skills for complex shared domains. | Prevents skill-count explosion while keeping role context coherent. | Skill maintainers | 2026-05-23 |
| Use `creator-skill` validation and eval expectations. | Keeps skill authoring aligned with the maintained local workflow. | Skill maintainers | 2026-05-23 |
| Defer organization convention packs. | Base local skill library should stabilize before layering org-specific behavior. | Oleg Shulyakov | 2026-05-23 |

## 13. Resolved Questions

| # | Question | Answer | Owner | Status |
| --- | --- | --- | --- | --- |
| 1 | What assertion pass threshold is required for eval release readiness? | Release-ready skills must reach at least 85% aggregate expectation pass rate, with no failed critical expectations, after `quick_validate.py` passes and required eval coverage exists. Human review may require fixes above that threshold when failures affect the skill's core artifact. | Skill maintainers [assumed] | Closed |
| 2 | What local install command or workflow confirms packaged `.skill` artifacts are installable? | No separate local install command exists in the repo today. Current release verification is package-and-inspect: run `python3 -m scripts.package_skill ../<skill-name> /tmp/skills-dist`, confirm exit code 0, then list the `.skill` archive and verify `<skill-name>/SKILL.md` plus required references, scripts, and assets are present. | Oleg Shulyakov [assumed] | Closed |

## 14. Appendix

### 14.1 Reference Links

- Product requirements: [PRD.md](PRD.md)
- Build tracker: [TASKS.md](TASKS.md)
- Prior memory note: [.agents/memory/2026-05-18.md](../../.agents/memory/2026-05-18.md)
- Skill authoring support: [creator-skill](../../.agents/skills/creator-skill/SKILL.md)

### 14.2 Totals

| Item | Count |
| --- | ---: |
| Catalog skills | 55 |
| Approved prefix types | 15 |
| Required router skills | 13 |
