---
status: APPROVED
documentType: PRD
phase: delivery
version: 2.1
createdAt: "2026-05-02"
updatedAt: "2026-06-10"
author: Oleg Shulyakov
owner: Oleg Shulyakov
stakeholders: CLI agent users, software delivery teams, skill maintainers
targetDate: Milestone-gated; no fixed calendar date
tracker: TASKS.md
tags:
  - skills
  - agents
  - team-roles
related:
  - SPEC.md
  - TASKS.md
---

# PRD: Software Team Roles as Skills

## 🎯 Objective

CLI agents are broadly capable, but software teams still have to repeat role-specific instructions every time they need a PRD, schema, API contract, E2E test suite, runbook, threat model, or release checklist. The result is uneven output quality, duplicated prompting effort, and no versioned source of truth for "how this team produces this artifact."

Software Team Roles as Skills creates a reusable local skill library for software delivery work. Each skill captures a specific role capability, expected artifact format, quality bar, routing behavior, and verification guidance so users can invoke a focused capability instead of rebuilding the prompt from scratch.

The initiative targets teams and individual practitioners who want role-aware AI assistance without turning the agent into a project management system or runtime plugin marketplace. The cost of inaction is continued prompt drift, inconsistent artifacts, and fragile knowledge transfer across sessions and contributors.

---

## 📊 Goals

|Goal ID|Target Outcome|Success Metric|
|---|---|---|
|G-1|Cover the core artifact-producing responsibilities of a software delivery team.|56 cataloged skills exist across the approved verb groups.|
|G-1a|Track current implementation progress against the catalog.|10 of 56 catalog skills existed in `src/skills/` as of 2026-05-23; catalog completion was 18%.|
|G-2|Make skill discovery predictable from the filesystem.|100% of catalog skills follow the `<verb>-<subject>[-<variant>]` naming convention.|
|G-3|Reduce repeated role-specific prompting.|Users can invoke each completed skill by artifact or task intent without restating its output structure or role conventions.|
|G-4|Produce concrete, reusable artifacts instead of generic advice.|Every completed skill description names the artifact it produces and when it should trigger.|
|G-5|Keep complex domains usable without exploding the skill count.|Multi-variant router skills select the correct reference from context or ask only when materially ambiguous.|
|G-6|Maintain quality through repeatable evaluation.|Each release-ready skill passes `validate.py`, has required eval coverage, and clears an 85% aggregate expectation pass rate with no failed critical expectations.|
|G-7|Make completed skills distributable from local artifacts.|Each release-ready skill packages successfully as a `.skill` file with bundled instructions, references, scripts, and assets as applicable.|

---

## 👥 Target Audience Focus

- **Persona ID: P-1 Product and analysis practitioners**: PMs, POs, and system analysts who need consistent PRDs, specs, use cases, epics, stories, gap analyses, and integration maps without rewriting structure and acceptance criteria each time.
- **Persona ID: P-2 Engineers and technical leads**: Backend, frontend, mobile, database, platform, and team lead users who need production-ready code, patterns, reviews, architecture artifacts, and implementation guidance aligned to known conventions.
- **Persona ID: P-3 Quality, security, and operations specialists**: AQA, SRE, DevOps, security, data, and ML users who need test suites, eval harnesses, audits, runbooks, alert rules, compliance docs, infrastructure setup, and operational reports.
- **Persona ID: P-4 Skill maintainers**: Contributors who create, test, package, and evolve skills while keeping naming, structure, references, and evals consistent.

---

## 📐 Scope

### ✅ In Scope

- A local library of 56 software-team skills defined in [SPEC.md](SPEC.md).
- Verb-first naming across `audit`, `check`, `build`, `design`, `diagram`, `model`, `document`, `plan`, `report`, `review`, `configure`, `create`, `track`, and `write`.
- Skill folders containing `SKILL.md`, eval coverage, and optional `references/` for detailed variant guidance.
- Multi-variant router skills for domains where one trigger should select among related artifact variants, including backend, frontend, database, testing, architecture, security, infrastructure, and templates.
- Packaging each completed skill as a distributable `.skill` artifact [assumed].
- Documentation that links product intent, technical design, and build tracking through this PRD, [SPEC.md](SPEC.md), and [TASKS.md](TASKS.md).

### 🚫 Out of Scope

- Runtime plugin hosting, remote skill fetching, or marketplace behavior.
- Live integrations with Jira, Confluence, GitHub, CI systems, observability platforms, or cloud APIs.
- Long-lived workflow automation, task state, or project management features.
- Team-specific convention overrides beyond install-time instructions or local customization.
- Real-time dashboards, monitoring, or data ingestion.

### ⏳ Later

- Integration-specific variants once the local skill format is stable.
- Organization-level convention packs layered on top of the base skills.
- Automated release validation for packaged `.skill` files.
- Usage analytics or quality telemetry if a future runtime supports it.

---

## 📋 Functional Requirements

|Requirement ID|Capability / Feature|Priority|Acceptance Criteria|Tracker|
|---|---|---|---|---|
|FR-1|Define and track the full team-role skill catalog.|MUST|Catalog includes 56 named skills; each skill maps to at least one primary role and one output artifact; implementation status is checked against `src/skills/`; catalog stays aligned across PRD, SPEC, and TASKS.|[TASKS.md](TASKS.md)|
|FR-2|Enforce verb-first skill naming.|MUST|Every skill name follows `<verb>-<subject>[-<variant>]`; verbs match the approved verb list in SPEC.md; renames are reflected in docs and task tracking.|[SPEC.md](SPEC.md)|
|FR-3|Provide a standard skill structure.|MUST|Each skill has a `SKILL.md` with valid frontmatter; each skill has eval coverage; large reusable guidance lives in `references/` instead of bloating `SKILL.md`.|[SPEC.md](SPEC.md)|
|FR-4|Support multi-variant routing where domains share one role context.|SHOULD|Router skills detect variants from prompt and repo context; router skills ask at most one clarifying question when context is materially ambiguous; variant references are loaded on demand.|[SPEC.md](SPEC.md)|
|FR-5|Prioritize build order by daily leverage and role coverage.|MUST|P1 foundation skills are built first; P2/P3/P4 priorities are visible in TASKS.md; completed skills are marked in the tracker.|[TASKS.md](TASKS.md)|
|FR-6|Package completed skills for distribution.|SHOULD|Completed skills can be exported as `.skill` files; package contents include instructions, references, scripts, and assets needed for reuse; root-level evals are retained in the source folder and excluded from packaged artifacts by the current packager.|[SPEC.md](SPEC.md), [src/skills/README.md](../../src/skills/README.md)|
|FR-7|Keep security and test responsibilities separated.|MUST|`audit-security` owns prompt-injection, jailbreak, exfiltration, secrets, and threat-modeling guidance; `code-tests` owns functional tests, AI evals, tool-use evals, performance tests, and CI test setup.|[SPEC.md](SPEC.md)|

---

## ⚡ Non-Functional Requirements

|NFR ID|Category|Target Specification|
|---|---|---|
|NFR-1|Maintainability|Each `SKILL.md` stays under 500 lines; overflow content moves to `references/`.|
|NFR-2|Testability|Focused skills have 8-10 eval prompts; router skills have 8-10 eval prompts per routed reference before being considered complete.|
|NFR-3|Discoverability|Skill descriptions clearly state trigger conditions and output artifacts.|
|NFR-4|Consistency|Shared terminology for roles, prefixes, priorities, and artifacts is consistent across PRD, SPEC, and TASKS.|
|NFR-5|Local-first operation|Skills work from local instructions and repository context without requiring live network integrations.|

---

## 🌟 Milestones

|Milestone|Target Date|Exit Criteria|Owner|
|---|---|---|---|
|M-1 Foundation skills|Milestone-gated|P1 skills in TASKS.md are implemented, evaluated, and documented. Current status: complete for the P1 catalog skills listed in TASKS.md.|Oleg Shulyakov [assumed]|
|M-2 Delivery skills|Milestone-gated|P2/P3 delivery and operational skills are implemented with eval coverage.|Skill maintainers [assumed]|
|M-3 Specialist skills|Milestone-gated|Remaining specialist skills are implemented or deliberately deferred with rationale.|Skill maintainers [assumed]|
|M-4 Distribution readiness|Milestone-gated|Completed skills can be packaged and installed from local artifacts.|Skill maintainers [assumed]|

---

## 👤 User Interaction

Users invoke skills by naming the skill directly, asking for the artifact the skill owns, or describing a role-specific task. The agent should select the matching skill from its description, load only the needed references, and produce or edit the requested artifact in the repository.

For multi-variant skills, the expected interaction is context-first routing. For example, a request for API tests, E2E tests, AI evals, or performance tests should route through `code-tests` and select the relevant testing reference without requiring the user to know the internal variant name.

---

## 🗺️ User Journeys / Key Flows

1. A product owner asks for a PRD. The agent loads `write-prd`, reads the required output format, extracts known context, marks inferences with `[assumed]`, and writes `PRD.md`.
2. A backend engineer asks for API code. The agent loads `code-backend`, detects language and framework from repository context, writes focused code changes, and verifies them with local tests where available.
3. A maintainer adds a new skill. The maintainer follows the skill structure in SPEC.md, adds references only when needed, writes eval cases, updates TASKS.md, and packages the skill when complete.

---

## 🤔 Risks, Assumptions, & Mitigations

|Risk ID|Assumption / Risk Description|Impact (H/M/L)|Mitigation Strategy|Status|
|---|---|---|---|---|
|R-1|Skill overlap causes ambiguous routing between similar artifacts, such as specs, stories, epics, and templates.|HIGH|Keep descriptions trigger-specific and add eval prompts for boundary cases.|OPEN|
|R-2|The 56-skill catalog becomes hard to maintain if every variant becomes a separate skill.|MEDIUM|Use router skills plus `references/` for related variants that share a role context.|OPEN|
|R-3|Eval requirements slow down early skill creation.|MEDIUM|Build P1 skills first and treat evals as part of the definition of done, not cleanup.|OPEN|
|R-4|Team-specific conventions may not fit the base library.|MEDIUM|Keep base skills generic, then support local install-time or repository-level guidance.|OPEN|
|R-5|Documentation can drift from the actual skill folders.|HIGH|Update PRD, SPEC, TASKS, and memory notes in the same change when catalog decisions change.|OPEN|
|R-6|Some implemented skills predate the current `create-skill` validation rules.|HIGH|Run `validate.py` per skill, then fix missing bold scan anchors, routed eval `reference` fields, and reference-section principles before release readiness.|OPEN|

---

## 🔗 External Dependencies

|Dependency ID|Item|Impacted Requirements|Validation Owner|
|---|---|---|---|
|D-1|Skill creation workflow and quality standards|FR-3, FR-6|Skill maintainers [assumed]|
|D-2|Local eval runner and assertion format|FR-3, G-6, NFR-2|Skill maintainers [assumed]|
|D-3|Packaging mechanism for `.skill` artifacts|FR-6, M-4|Oleg Shulyakov [assumed]|

---

## ✅ Decisions

|Decision ID|Decision|Rationale|Owner|Decision Date|
|---|---|---|---|---|
|DEC-1|Use milestone gates instead of a fixed calendar date for the first complete catalog release.|The release is ready when all 56 cataloged skills are implemented, evaluated, documented, and packageable; 10 catalog skills were implemented as of 2026-05-23.|Oleg Shulyakov [assumed]|2026-05-23|
|DEC-2|Use the `create-skill` eval bar: 8-10 realistic eval prompts for focused skills and 8-10 prompts per routed reference for router skills.|This keeps the PRD aligned with the maintained authoring workflow while allowing specialized skills to add cases for variant coverage, boundary-trigger testing, or safety-sensitive behavior.|Skill maintainers [assumed]|2026-05-23|
|DEC-3|Package release-ready skills from `src/skills/create-skill` with `python3 -m scripts.package_skill ../<skill-name> /tmp/skills-dist`.|Release readiness requires `validate.py` to pass, evals to be present in source and pass at least an 85% aggregate expectation pass rate with no failed critical expectations, router evals to include `reference` fields, references to be useful, and no security or packaging blockers to remain.|Skill maintainers [assumed]|2026-05-23|
|DEC-4|Treat organization-level convention packs as a separate follow-up.|This initiative ships the base local skill library first; organization convention packs should layer on later once the base format and release checks are stable.|Oleg Shulyakov [assumed]|2026-05-23|

---

## 📚 Reference Links

- **Ref-1**: Technical specification - [SPEC.md](SPEC.md)
- **Ref-2**: Build tracker - [TASKS.md](TASKS.md)
- **Ref-3**: Daily memory note for prior catalog updates - [src/memory/2026-05-18.md](../../src/memory/2026-05-18.md)
