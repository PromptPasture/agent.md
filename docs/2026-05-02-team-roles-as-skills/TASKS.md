---
status: IN-PROGRESS
documentType: TASKS
phase: delivery
version: 2.0
createdAt: "2026-05-02"
updatedAt: "2026-05-23"
author: Oleg Shulyakov
tags:
  - skills
  - agents
  - team-roles
related:
  - PRD.md
  - SPEC.md
---

# Tasks

A collection of skills for AI coding agents, modeled after real software team roles.
Each skill is a `SKILL.md` that teaches the agent how to produce a specific artifact — document, code, diagram, report, or plan.

---

## Naming Convention

```text
<verb>-<subject>[-<variant>]
```

The **verb prefix** comes first so skills sort naturally on the filesystem and visually cluster by what they _do_, not what they’re about.

Use `[-<variant>]` only when the variant needs its own trigger, eval set, and lifecycle. Otherwise, keep variants as router references under one skill.

| Verb | Produces |
| ------------ | ------------------------------------------------ |
| `audit-` | Review report or model with findings, risks, and recommendations |
| `check-` | Step-by-step verification list |
| `build-` | Source code, scripts, or executable configuration files |
| `design-` | Design document or spec (contract-first) |
| `diagram-` | Visual diagram (C4, DFD, flow, etc.) |
| `model-` | Structured model definition |
| `document-` | Pattern catalogue with examples |
| `plan-` | Planning document with estimates |
| `report-` | Status or analysis report |
| `review-` | Review findings against a concrete code or artifact change |
| `configure-` | Configuration files and scaffolding |
| `plan-` | Decision framework and approach |
| `create-` | Reusable blank template |
| `track-` | Metrics or progress tracking document |
| `write-` | Authored prose artifact (spec, doc, story, etc.) |

---

## Priority Guide

| Priority | Meaning |
| -------- | ------------------------------------------------ |
| 🔴 P1 | Build first — highest daily leverage, cross-role |
| 🟠 P2 | High value — foundational for a whole domain |
| 🟡 P3 | Important — core to a specific role |
| ⚪ P4 | Specialized — niche or lower frequency |

---

## Skills

Ordered alphabetically by name (matches filesystem order).

### `audit-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------------ | -------- | ------------ | ----------------- | ----------------------------------------------------------------------- |
| - [ ] | `audit-a11y` | 🟠 P2 | UI/UX | Frontend / UX | Accessibility checklist with annotated findings and fix recommendations |
| - [ ] | `audit-gap` | 🟡 P3 | Requirements | System Analyst | Gap analysis report between current and target state |
| - [ ] | `audit-security` | 🟠 P2 | Security | Security Engineer | Security router for OWASP review, secrets exposure, and threat modeling |
| - [x] | `audit-skill-security` | 🟠 P2 | Security | Security Engineer | Pre-install skill security audit with findings, risks, and install recommendation |
| - [ ] | `audit-test-flaky` | 🟡 P3 | Testing | AQA | Root cause report for flaky tests with fix recommendations |

### `check-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ----------------------- | -------- | ---------- | --------------- | ------------------------------------------------- |
| - [ ] | `check-release` | 🟡 P3 | Release | Release Manager | Go/no-go release checklist with sign-off sections |

### `build-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------------ | -------- | ------- | ------------- | ------------------------------------------------------------------------------------------- |
| - [x] | `code-backend` | 🔴 P1 | Code | Backend Dev | Production-ready backend code across TIOBE-informed backend routes |
| - [x] | `code-database` | 🔴 P1 | Database | DBA / Backend | Database code router for OLTP SQL, analytics SQL, schema design, and migrations |
| - [x] | `code-frontend` | 🔴 P1 | Code | Frontend Dev | Production-ready frontend code + design system tokens + component style guide |
| - [ ] | `build-mobile` | 🟠 P2 | Code | Mobile Dev | Production-ready mobile code (Swift/iOS, Kotlin/Android, React Native, Flutter) |
| - [x] | `code-tests` | 🔴 P1 | Testing | AQA / Backend / ML | Test suite and test framework generation (e2e, api, perf, AI evals, CI config) |

### `design-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ----------------- | -------- | ------------ | ------------------ | ------------------------------------------------------------- |
| - [x] | `design-api` | 🔴 P1 | Code | Backend Dev | Contract-first API spec (OpenAPI / AsyncAPI) |
| - [ ] | `design-arch` | 🟠 P2 | Architecture | Solution Architect | Architecture router for system design docs, ADRs, and C4 diagrams |

### `diagram-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | --------------------- | -------- | ------------ | ------------------ | ----------------------------------------------------------- |
| - [ ] | `diagram-dfd` | 🟡 P3 | Requirements | System Analyst | Data flow diagram (L0 context through L2 process detail) |
| - [ ] | `diagram-integration` | 🟡 P3 | Requirements | System Analyst | Integration map showing system boundaries and data exchange |
| - [ ] | `diagram-ux-flow` | 🟡 P3 | UI/UX | UX Designer | User flows and journey maps |

### `model-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | -------------- | -------- | -------- | ----------------- | -------------------------------------------------- |
| - [ ] | `model-dbt` | 🟡 P3 | Data | Data Engineer | dbt model definitions with tests and documentation |

### `document-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------------- | -------- | ------ | ------------ | ------------------------------------------------------------------------------------- |
| - [ ] | `document-auth-patterns` | 🟠 P2 | Code | Backend Dev | Auth pattern catalogue (JWT, OAuth2, sessions, API keys) with implementation examples |
| - [ ] | `document-graphql-patterns` | 🟡 P3 | Code | Backend Dev | GraphQL schema, resolver, and N+1 pattern guide |
| - [ ] | `document-realtime-patterns` | 🟡 P3 | Code | Backend Dev | WebSocket / SSE / polling pattern guide with tradeoffs |

### `plan-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------------ | -------- | ------ | ------------ | ---------------------------------------------------------- |
| - [ ] | `plan-capacity` | ⚪ P4 | Ops | DBA / DevOps | Capacity plan with growth projections and scaling triggers |
| - [ ] | `plan-sprint` | 🟡 P3 | Agile | Scrum Master | Sprint plan with goals, capacity, impediment log |

### `report-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | -------------------- | -------- | ---------- | ----------------- | -------------------------------------------------------- |
| - [ ] | `report-cve` | 🟡 P3 | Security | Security Engineer | CVE triage report with severity, impact, and remediation |
| - [ ] | `report-db-health` | 🟡 P3 | Database | DBA | Database health report (indexes, bloat, slow queries) |
| - [ ] | `report-team-health` | ⚪ P4 | Leadership | Team Lead | Team health report (velocity, satisfaction, blockers) |

### `review-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------- | -------- | ---------- | ------------ | --------------------------------------------------------------------- |
| - [x] | `review-code` | 🟠 P2 | Leadership | Team Lead | Structured code review findings plus a reusable review checklist reference |

### `configure-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------------------ | -------- | ------------ | ----------------- | ------------------------------------------------------------ |
| - [ ] | `configure-developer-portal` | ⚪ P4 | Platform | Platform Engineer | Internal developer portal structure with service catalog |
| - [ ] | `configure-eval-harness` | 🟡 P3 | ML / AI | ML Engineer | Model evaluation harness with metrics and baselines |
| - [ ] | `configure-infra` | 🟠 P2 | DevOps | DevOps | Ops setup router for IaC, observability, CI/CD, and ETL pipeline config |
| - [ ] | `configure-monorepo` | 🟡 P3 | Platform | Platform Engineer | Monorepo configuration (Nx, Turborepo, Bazel) |
| - [ ] | `configure-rag` | 🟡 P3 | ML / AI | AI Engineer | RAG pipeline setup (chunking, embedding, retrieval) |

### `plan-` strategy

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ----------------------------- | -------- | -------- | ------------------- | --------------------------------------------------------------- |
| - [ ] | `plan-api-versioning` | 🟡 P3 | Code | Backend Dev | API versioning strategy with deprecation and migration guide |
| - [ ] | `plan-backup` | 🟡 P3 | Database | DBA | Backup and recovery strategy with RPO/RTO targets |
| - [ ] | `plan-dependency-upgrade` | 🟡 P3 | Release | DevOps / Team Lead | Dependency upgrade strategy with risk assessment |
| - [ ] | `plan-feature-flag` | 🟡 P3 | Code | Team Lead / Backend | Feature flag strategy with rollout and rollback plan |

### `create-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ---------------- | -------- | ---------- | ------------ | --------------------------------------------------------------- |
| - [ ] | `create-template` | 🟡 P3 | Leadership / Agile | Team Lead / Scrum Master | Reusable team templates for PRs, retros, issues, meetings, decisions, incidents, and releases |

### `track-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ------------------ | -------- | ------ | ------------ | ---------------------------------------------- |
| - [ ] | `track-velocity` | ⚪ P4 | Agile | Scrum Master | Sprint velocity report with trend and forecast |

### `write-`

| Done | Skill | Priority | Domain | Primary Role | Produces |
| ----- | ----------------------- | -------- | ------------ | ------------------- | --------------------------------------------------------------------- |
| - [ ] | `write-alert-rules` | 🟡 P3 | DevOps / SRE | SRE | Alert rule definitions with severity and runbook links |
| - [ ] | `write-backlog` | 🟡 P3 | Agile | Product Owner | Groomed backlog with priorities, estimates, and dependencies |
| - [ ] | `write-compliance` | ⚪ P4 | Security | Security / Legal | Compliance documentation (GDPR, SOC2, HIPAA) |
| - [ ] | `write-epic` | 🟠 P2 | Agile | Product Owner | Epic definition with goal, scope, child stories, DoD |
| - [ ] | `write-lineage` | ⚪ P4 | Data | Data Engineer | Data lineage documentation (sources, transforms, destinations) |
| - [ ] | `write-mentorship` | ⚪ P4 | Leadership | Team Lead | Mentorship guide with goals, checkpoints, and resources |
| - [ ] | `write-ml-experiment` | 🟡 P3 | ML / AI | ML Engineer | ML experiment report with setup, results, and model card |
| - [ ] | `write-postmortem` | 🟡 P3 | Leadership | Team Lead / SRE | Incident postmortem (timeline, root cause, action items) |
| - [x] | `write-prd` | 🔴 P1 | Requirements | PM / PO | Product Requirements Document (goals, personas, scope, metrics) |
| - [ ] | `write-prompt` | 🟡 P3 | ML / AI | ML / AI Engineer | Optimized prompt with system instructions, examples, and eval |
| - [x] | `write-tech-docs` | 🔴 P1 | Docs | Tech Writer | Technical docs: README, API docs, runbooks, changelog, release notes |
| - [ ] | `write-slo` | 🟡 P3 | DevOps / SRE | SRE | SLO definition with indicators, targets, and error budget |
| - [x] | `write-spec` | 🔴 P1 | Requirements | SA / Architect / UX | Specification document (functional, tech, NFR, design, data-contract) |
| - [ ] | `write-stakeholder` | 🟡 P3 | Agile | PM / PO | Stakeholder update (status, risks, decisions needed) |
| - [x] | `write-user-story` | 🔴 P1 | Agile | PO / Team Lead | User stories with acceptance criteria decomposed into dev tasks |
| - [ ] | `write-team-agreement` | ⚪ P4 | Agile | Scrum Master | Team working agreement (definition of done, norms, ceremonies) |
| - [ ] | `write-tech-radar` | ⚪ P4 | Architecture | Solution Architect | Technology radar (adopt, trial, assess, hold) |
| - [ ] | `write-test-strategy` | 🟠 P2 | Testing | AQA / QA | Test strategy document (scope, levels, tools, coverage targets) |
| - [ ] | `write-use-case` | 🟡 P3 | Requirements | System Analyst | Use case document (actors, preconditions, main/alternate flows) |
