---
status: APPROVED
documentType: SPEC
phase: delivery
version: 2.1
createdAt: "2026-05-02"
updatedAt: "2026-06-10"
author: Oleg Shulyakov
owner: Oleg Shulyakov
reviewers: Skill authors and maintainers
targetDate: Milestone-gated; no fixed calendar date
tracker: TASKS.md
tags:
  - skills
  - agents
  - team-roles
related:
  - PRD.md
  - TASKS.md
---

# SPEC: Software Team Roles as Skills

## 1. Overview

### 1.1 Purpose

This specification defines the local skill library for software delivery roles: its catalog, naming rules, filesystem structure, routing behavior, validation gates, and release readiness requirements.

The goal is to make role-specific agent behavior reusable and testable. A user should be able to ask for a PRD, API contract, test suite, runbook, security audit, or similar artifact without restating the role, structure, quality bar, or verification expectations each time.

### 1.2 Background

CLI agents can produce many software delivery artifacts, but output quality drifts when role instructions live only in prompts. Teams repeatedly explain what a good PRD, technical spec, database migration, E2E test suite, release checklist, or postmortem should contain. This creates duplicated prompting effort and weak transfer between sessions.

Software Team Roles as Skills turns those repeated instructions into a versioned local library. Each skill owns one role capability or artifact family, declares when it should trigger, and carries its own workflow, output format, references, evals, and packaging expectations.

The first catalog release is milestone-gated. It is ready when all 56 cataloged skills are implemented, validated, evaluated, documented, and packageable from local artifacts.

### 1.3 Roles & Responsibilities

|Role / Team|Responsibility|Decision Area|
|---|---|---|
|Product owner|Approves product scope, target personas, goals, and non-goals.|Catalog scope and success criteria|
|Skill maintainer|Creates, tests, packages, and updates skills.|Skill structure, references, evals, and readiness|
|Skill author|Writes role instructions and artifact formats.|Trigger behavior and output quality|
|CLI agent user|Invokes skills through direct names or natural task intent.|Feedback on usability and output fit|
|Reviewer|Reviews skill behavior, eval coverage, and drift against docs.|Release readiness|

### 1.4 Customer & Business Context

The primary users are product, engineering, quality, security, operations, data, ML, and leadership practitioners who need predictable AI assistance for common software delivery artifacts. The business value is less prompt drift, fewer one-off instructions, and a reusable quality bar for team workflows.

The library must remain local-first. It is not a plugin marketplace, a project management system, or a live integration layer.

### 1.5 Goals

|Goal|Success Metric|Target|
|---|---|---|
|Complete catalog coverage|Cataloged software delivery role skills exist in `src/skills/`.|56 skills|
|Keep discovery predictable|Skill names follow verb-first convention.|100% compliance|
|Reduce repeated prompting|Completed skills encode trigger, output, and quality expectations.|Every completed skill has specific frontmatter and instructions|
|Keep complex domains usable|Router skills select variants from context.|Ask at most one clarifying question when materially ambiguous|
|Maintain quality|Skills pass validation and eval thresholds.|`validate.py` pass plus required eval coverage|
|Support local distribution|Release-ready skills package as `.skill` files.|Successful local package build|

### 1.6 Non-Goals

Runtime plugin hosting, remote skill fetching, marketplace behavior, live Jira/GitHub/CI/observability/cloud integrations, long-lived workflow automation, task-state management, real-time dashboards, and organization-specific convention packs are out of scope for this release.

## 2. Functional Requirements

### 2.1 Actors

|Actor|Description|
|---|---|
|User|Requests an artifact or names a skill directly.|
|Agent|Selects, loads, and applies the relevant local skill.|
|Skill maintainer|Builds, validates, evaluates, packages, and updates skills.|
|Reviewer|Confirms behavior, catalog fit, and readiness gates.|

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
3. Maintainer validates the skill with `validate.py`.
4. Maintainer runs or reviews eval coverage where available.
5. Maintainer updates PRD, SPEC, TASKS, and memory notes when catalog behavior changes.
6. Maintainer packages the skill once release-ready.

### 2.3 Requirements

#### FR-001: Catalog Definition

**Priority:** Must-have
**Actor:** Skill maintainer
**Requirement:** The library shall define exactly 56 catalog skills for the first full release.

**Acceptance criteria:**

- The catalog lists each skill name, primary roles, and output artifact.
- Each catalog skill maps to one approved verb.
- PRD, SPEC, and TASKS agree on catalog names.
- Drift between docs and `src/skills/` is treated as a release blocker.

#### FR-002: Verb-First Naming

**Priority:** Must-have
**Actor:** Skill maintainer
**Requirement:** Every catalog skill shall use `<verb>-<subject>[-<variant>]`.

**Acceptance criteria:**

- Valid verbs are `audit`, `check`, `build`, `design`, `diagram`, `model`, `document`, `plan`, `report`, `review`, `configure`, `create`, `track`, and `write`.
- Skill folders sort predictably by action in the filesystem.
- Renames update PRD, SPEC, TASKS, references, and evals in the same change.

#### FR-003: Standard Skill Structure

**Priority:** Must-have
**Actor:** Skill author
**Requirement:** Each completed skill shall have a standard local folder layout.

**Acceptance criteria:**

- `SKILL.md` exists and contains valid YAML frontmatter with `name` and `description`.
- `description` states when to trigger the skill and what artifact it produces.
- `evals/evals.yaml` exists for release-ready skills.
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

- `python3 src/skills/create-skill/scripts/validate.py src/skills/<skill-name>` passes.
- Focused skills have 8-10 realistic eval prompts.
- Router skills have 8-10 eval prompts per routed reference before release readiness.
- Eval assertions reach at least 85% aggregate pass rate with no failed critical expectations.
- Safety-sensitive or boundary-heavy skills include evals for error handling and misuse resistance.

#### FR-007: Packaging

**Priority:** Should-have
**Actor:** Skill maintainer
**Requirement:** Release-ready skills shall package into local `.skill` artifacts.

**Acceptance criteria:**

- Packaging runs from `src/skills/create-skill`.
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
- `code-tests` owns executable tests, AI evals, tool-use evals, performance tests, fixtures, framework setup, and CI test setup.
- Boundary prompts route consistently between the two.

## 3. Non-Functional Requirements

|Category|Requirement|Target|Priority|
|---|---|---|---|
|Maintainability|Skill instructions remain concise and modular.|`SKILL.md` under 500 lines; detailed variants in `references/`|High|
|Testability|Behavior can be evaluated with representative prompts.|8-10 evals per focused skill or per router reference|High|
|Discoverability|Users can invoke by skill name, artifact, or task intent.|Frontmatter descriptions include triggers and output artifacts|High|
|Consistency|Terms, names, priorities, and status stay aligned.|PRD, SPEC, TASKS, and skill folders match|High|
|Local-first operation|Skills work without live network integrations.|Instructions, references, scripts, assets, and evals are local|High|
|Token efficiency|Skills load only needed guidance.|Router references are loaded on demand|Medium|
|Extensibility|Complex domains can grow without skill-count explosion.|Router pattern handles variants sharing one role context|Medium|

## 4. Skill Architecture

### 4.1 Naming Convention

All skills use verb-first naming:

```text
<verb>-<subject>[-<variant>]
```

The verb identifies the artifact or action family. The subject identifies the domain. The optional variant is allowed only when a separate folder is clearer than a router reference.

### 4.2 Filesystem Layout

```text
src/skills/
├── <skill-name>/
│   ├── SKILL.md
│   ├── evals/
│   │   └── evals.yaml
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

|Field|Required|Description|
|---|---|---|
|`name`|Yes|A unique identifier for the skill.|
|`description`|Yes|A concise explanation of the skill's purpose and when to use it.|
|`license`|No|The name of the license, such as `MIT` or `Apache-2.0`.|
|`version`|No|Semantic versioning string, such as `1.2.0`.|
|`tags`|No|A list of categories for easier discovery and filtering.|
|`author`|No|The creator's name or GitHub profile URL.|
|`metadata`|No|A nested mapping for arbitrary key-value pairs.|

### 4.4 Router Pattern

Router skills use one `SKILL.md` plus variant references when related artifacts share a role context. The router must:

1. Detect the target variant from explicit request text.
2. Inspect repository context when useful and available.
3. Load the smallest useful reference set.
4. Ask one concise question only when the route changes the output materially.
5. Mark inferred details with `[assumed]` when producing a spec or planning artifact.

Router skills for this release are `audit-security`, `code-frontend`, `code-backend`, `code-database`, `build-mobile`, `code-tests`, `design-arch`, `write-spec`, `configure-infra`, `create-template`, `review-code`, and `plan-capacity`.

## 5. Catalog

### 5.1 Full Skill Catalog

|Skill|Primary Roles|Output Artifact|
|---|---|---|
|`audit-a11y`|Frontend Dev, UX|Accessibility audit with WCAG violations, severity, and fixes|
|`audit-gap`|System Analyst|Gap analysis report: current state, target state, remediation|
|`audit-security`|Security Eng|Security router: OWASP review, secrets audit, threat model|
|`audit-test-flaky`|AQA|Flaky test report with root cause and fix recommendations|
|`check-release`|Release Manager|Release checklist with rollback criteria|
|`code-backend`|Backend Dev|Backend code: routes, services, middleware, tests|
|`code-database`|DBA, Backend, Data Eng|Database code: schemas, SQL, migrations, analytics queries|
|`code-frontend`|Frontend Dev|Frontend code: components, pages, state, styling|
|`build-mobile`|Mobile Dev|Mobile code: screens, navigation, platform patterns|
|`code-tests`|AQA|Test suites, eval harnesses, fixtures, configs, CI setup|
|`design-api`|Backend Dev|API contract: OpenAPI, AsyncAPI, GraphQL, endpoints, schemas|
|`design-arch`|Architect|Architecture router: system design, ADR, C4 diagram|
|`diagram-dfd`|System Analyst|Data flow diagram in Mermaid or structured text|
|`diagram-integration`|System Analyst|Integration map: systems, APIs, data flows, ownership|
|`diagram-ux-flow`|UX Designer|User flow or journey map|
|`model-dbt`|Data Eng|dbt model with SQL, schema, tests, and docs|
|`document-auth-patterns`|Backend Dev|Auth implementation patterns for JWT, OAuth2, sessions, RBAC|
|`document-graphql-patterns`|Backend Dev|GraphQL schema, resolver, pagination, and N+1 patterns|
|`document-realtime-patterns`|Backend Dev|WebSocket, SSE, and polling strategy patterns|
|`plan-capacity`|DevOps, SRE|Capacity plan for traffic, storage, compute, and scaling|
|`plan-sprint`|Scrum Master|Sprint plan with goal, capacity, stories, impediments|
|`report-cve`|Security Eng|CVE triage report with affected versions and remediation|
|`report-db-health`|DBA|Database health report|
|`report-team-health`|Team Lead|Team health report with delivery and risk signals|
|`review-code`|Team Lead|Code review findings prioritized by risk|
|`configure-developer-portal`|Platform Eng|Developer portal setup and onboarding structure|
|`configure-eval-harness`|ML Eng|Eval harness with dataset, rubric, metrics, benchmark runner|
|`configure-infra`|DevOps, Data Eng|Infrastructure setup router: IaC, CI/CD, ETL, observability|
|`configure-monorepo`|Platform Eng|Monorepo setup and tooling configuration|
|`configure-rag`|AI Eng|RAG pipeline setup|
|`plan-api-versioning`|Backend Dev, Architect|API versioning and deprecation strategy|
|`plan-backup`|DBA|Backup strategy with retention and restore SLAs|
|`plan-dependency-upgrade`|Release Manager, DevOps|Dependency upgrade strategy|
|`plan-feature-flag`|Team Lead, Backend|Feature flag rollout, lifecycle, and kill-switch strategy|
|`create-template`|Team Lead, Scrum Master, PM, PO|Reusable templates for team workflows|
|`track-velocity`|Scrum Master|Sprint metrics and velocity report|
|`write-alert-rules`|SRE|Alert rules with severity, routing, and runbook links|
|`write-api-docs`|Tech Writer, Backend|Reference documentation for implemented APIs|
|`write-backlog`|PO|Groomed backlog with priority, sizing, and dependencies|
|`write-changelog`|Tech Writer, Release Mgr|Developer-facing changelog entries and release history|
|`write-compliance`|Security, Legal|Compliance documentation and evidence checklist|
|`write-epic`|PO|Epic with goal, value, child stories, definition of done|
|`write-lineage`|Data Eng|Data lineage document|
|`write-mentorship`|Team Lead|Mentorship guide|
|`write-ml-experiment`|ML Eng|ML experiment report and model-card section|
|`write-postmortem`|Team Lead, SRE|Postmortem with timeline, root cause, action items|
|`write-prd`|PM, PO|Product Requirements Document|
|`write-prompt`|ML, AI Eng|Prompt specification with examples and eval criteria|
|`write-readme`|Tech Writer, Developers|Project README with installation, usage, and contribution guidance|
|`write-release-notes`|Tech Writer, Release Mgr|User-facing release communication and upgrade guidance|
|`write-runbook`|Tech Writer, SRE|Routine and on-call operational procedures|
|`write-slo`|SRE|SLO definition with SLI, target, error budget, alerts|
|`write-spec`|SA, Architect, UX|Functional, technical, NFR, design, or data-contract spec|
|`write-stakeholder`|PM, PO|Stakeholder update|
|`write-team-agreement`|Scrum Master|Team working agreement|
|`write-tech-radar`|Architect|Tech radar|
|`write-test-strategy`|AQA, QA|Test strategy|
|`write-ticket`|PO, Team Lead, Developers|Jira or GitHub bug, feature, task, or spike ticket|
|`write-use-case`|System Analyst|Use case document|
|`write-user-story`|PO, Team Lead|User story with acceptance criteria|

## 6. Variant References

### 6.1 Required Router Reference Sets

|Skill|Required references|
|---|---|
|`write-spec`|`functional.md`, `technical.md`, `non-functional.md`, `design-ui.md`, `data-contract.md`|
|`design-arch`|`system-design.md`, `adr.md`, `c4.md`|
|`code-database`|`schema-design.md`, `migration.md`, `common.md`, plus supported dialect references|
|`code-frontend`|Language, framework, styling, accessibility, forms, state, performance, PWA, i18n, visualization references|
|`code-backend`|Language-level references plus supported framework references|
|`build-mobile`|`swift.md`, `kotlin-android.md`, `react-native.md`, `flutter.md`|
|`code-tests`|`e2e.md`, `api.md`, `perf.md`, `framework-setup.md`, `ai-output.md`, `ai-tool-use.md`, `ai-perf.md`|
|`configure-infra`|`iac.md`, `cicd.md`, `etl.md`, `observability.md`|
|`plan-capacity`|`db.md`, `infra.md`|
|`audit-security`|`owasp.md`, `secrets.md`, `threat-model.md`|
|`review-code`|`checklist.md`, `regressions.md`, `security.md`, `performance.md`, `test-gaps.md`|
|`create-template`|`pr.md`, `retro.md`, `issue.md`, `meeting.md`, `decision.md`, `incident.md`, `release.md`|

### 6.2 Collision Rules

|Pair|Routing rule|
|---|---|
|`write-prd` vs `write-spec`|PRD owns product goals, personas, scope, and success metrics; spec owns behavior, technical detail, system handoff, and requirements.|
|`design-api` vs `write-api-docs`|`design-api` is contract-first before implementation; `write-api-docs` documents an existing API.|
|`design-arch` variants|System design is broad architecture; ADR is one decision; C4 is diagram-focused.|
|`write-ticket` vs `write-user-story`|Ticket owns tracker work items using type-specific writing; user story owns persona, user value, and story acceptance criteria.|
|`write-user-story` vs `write-epic`|User story is one user-value increment with acceptance criteria; epic groups related stories.|
|`code-tests` vs `write-test-strategy`|`code-tests` writes executable tests/config/evals; `write-test-strategy` writes planning guidance.|
|`review-code` vs `audit-security`|`review-code` reviews a code change; `audit-security` performs standalone security analysis.|
|`create-template` vs `write-*`|`create-template` creates reusable blank templates; `write-*` creates filled artifacts.|
|`audit-security` vs `code-tests` AI evals|`audit-security` owns abuse, exfiltration, secrets, and threat modeling; `code-tests` owns quality, tool-use, latency, cost, and regression evals.|

## 7. Validation

### 7.1 Structural Validation

Each release-ready skill must pass:

```bash
python3 src/skills/create-skill/scripts/validate.py src/skills/<skill-name>
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

|Error Path|Expected Behavior|
|---|---|
|Missing skill folder|Report that the skill is not implemented and continue with the closest available skill only if safe.|
|Missing `SKILL.md`|Treat the skill as not release-ready. Do not package it.|
|Invalid frontmatter|Fix before validation or release.|
|Missing evals|Mark as draft or incomplete; do not call it release-ready.|
|Ambiguous router request|Ask one concise clarifying question when context cannot decide the variant.|
|Missing router reference|State the missing reference and either use a narrower available reference or stop if behavior would be invented.|
|Catalog/doc drift|Update PRD, SPEC, TASKS, and relevant memory notes together.|
|Packaging failure|Fix validation, missing assets, or packaging metadata before distribution.|

## 9. Build Process

Each skill should be built with `create-skill` using this sequence:

1. Clarify trigger scope, expected output, routing needs, and eval expectations.
2. Draft `SKILL.md` with frontmatter, concise workflow instructions, clear section headings, and scan anchors.
3. Move reusable detail into `references/` only when needed.
4. Add `evals/evals.yaml` with required focused or routed coverage.
5. Run `validate.py`.
6. Run or review eval iterations when behavior needs evidence.
7. Review outputs qualitatively and assertions quantitatively where objective checks apply.
8. Iterate until feedback is resolved, improvements flatten, or the user accepts behavior.
9. Tune the description for triggering accuracy after behavior is stable.
10. Package release-ready skills from `src/skills/create-skill`:

```bash
python3 -m scripts.package_skill ../<skill-name> /tmp/skills-dist
```

## 10. Release Readiness

### 10.1 Milestones

|Milestone|Exit Criteria|Owner|
|---|---|---|
|M-1 Foundation skills|P1 skills in TASKS are implemented, evaluated, and documented.|Oleg Shulyakov|
|M-2 Delivery skills|P2/P3 delivery and operational skills are implemented with eval coverage.|Skill maintainers|
|M-3 Specialist skills|Remaining specialist skills are implemented or deliberately deferred with rationale.|Skill maintainers|
|M-4 Distribution readiness|Completed skills package and install from local artifacts.|Skill maintainers|

### 10.2 Launch Checklist

|Activity|Owner|Required Before Launch|
|---|---|---|
|Catalog reconciliation|Skill maintainer|Yes|
|Structural validation|Skill maintainer|Yes|
|Eval coverage review|Reviewer|Yes|
|Router collision review|Reviewer|Yes|
|Packaging smoke test|Skill maintainer|Yes|
|Documentation update|Skill maintainer|Yes|
|Support/training note|Skill maintainer|Before broader team rollout|
|Feedback collection path|Product owner|Before broader team rollout|

## 11. Risks and Mitigations

|Risk|Impact|Mitigation|Status|
|---|---|---|---|
|Similar skills route ambiguously.|High|Keep descriptions trigger-specific and add boundary evals.|Open|
|Router skills become too broad.|Medium|Use references for related variants only when they share role context.|Open|
|Eval requirements slow creation.|Medium|Treat evals as definition of done, not cleanup.|Open|
|Team conventions do not fit base skills.|Medium|Keep base skills generic; defer convention packs.|Open|
|Docs drift from folders.|High|Update PRD, SPEC, TASKS, and memory together.|Open|
|Older skills fail current validation.|High|Run validation per skill and fix blockers before release readiness.|Open|
|Implementation count is inconsistent.|Medium|Reconcile PRD status, TASKS, and actual `src/skills/` folders.|Open|

## 12. Decisions

|Decision|Rationale|Owner|Date|
|---|---|---|---|
|Use milestone gates instead of a fixed date.|Release depends on complete implementation, evals, docs, and packaging.|Oleg Shulyakov|2026-05-23|
|Use router skills for complex shared domains.|Prevents skill-count explosion while keeping role context coherent.|Skill maintainers|2026-05-23|
|Use `create-skill` validation and eval expectations.|Keeps skill authoring aligned with the maintained local workflow.|Skill maintainers|2026-05-23|
|Defer organization convention packs.|Base local skill library should stabilize before layering org-specific behavior.|Oleg Shulyakov|2026-05-23|

## 13. Resolved Questions

|#|Question|Answer|Owner|Status|
|---|---|---|---|---|
|1|What assertion pass threshold is required for eval release readiness?|Release-ready skills must reach at least 85% aggregate expectation pass rate, with no failed critical expectations, after `validate.py` passes and required eval coverage exists. Human review may require fixes above that threshold when failures affect the skill's core artifact.|Skill maintainers [assumed]|Closed|
|2|What local install command or workflow confirms packaged `.skill` artifacts are installable?|No separate local install command exists in the repo today. Current release verification is package-and-inspect: run `python3 -m scripts.package_skill ../<skill-name> /tmp/skills-dist`, confirm exit code 0, then list the `.skill` archive and verify `<skill-name>/SKILL.md` plus required references, scripts, and assets are present.|Oleg Shulyakov [assumed]|Closed|

## 14. Appendix

### 14.1 Reference Links

- Product requirements: [PRD.md](PRD.md)
- Build tracker: [TASKS.md](TASKS.md)
- Prior memory note: [src/memory/2026-05-18.md](../../src/memory/2026-05-18.md)
- Skill authoring support: [create-skill](../../src/skills/create-skill/SKILL.md)

### 14.2 Totals

|Item|Count|
|---|---:|
|Catalog skills|56|
|Approved verbs|15|
|Required router skills|13|
