---
type: concept
title: Software engineering skills
description: Code generation and code review skills for backend, frontend, database, and tests.
tags: [skills, software-engineering, code, review]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Software engineering skills

All code-generation skills follow the same four-phase pattern: **Discover → Plan → Build → Validate**. Each phase gates the next and is skippable when the user provides the relevant context upfront.

## Shared phase pattern

|Phase|Output|
|---|---|
|Discover|Stack/engine detection summary; suggest defaults when project is empty|
|Plan|Confirmed interface/API/schema/test contract before writing any code|
|Build|Written files with explicit decomposition rationale|
|Validate|P0–P3 checklist — must pass before declaring output complete|

## P0–P3 checklist tiers

|Priority|Meaning|
|---|---|
|P0 — Blocking|Security, critical safety (destructive ops, SQL injection, XSS, CSRF)|
|P1 — Required|TypeScript strictness, error handling, correctness|
|P2 — Expected|Performance, observability, data fetching patterns|
|P3 — Polish|Bundle hints, animation, image sizing|

## Skills

### `code-backend`

Generates production-ready backend code. Auto-detects stack (Go, Node.js, Python, Java, Kotlin, Rust, and more). Confirms API contract and DB schema before writing. Graduated from in-progress: 2026-06-21.

### `code-frontend`

Generates production-ready frontend components for real project codebases. Auto-detects framework from `package.json`, `tsconfig.json`, and framework config files (Next.js, Vite+React, SvelteKit, Nuxt, Astro, Remix). Plan phase produces a full interface contract (name, file path, props, events, slots, deps). Build phase applies decomposition heuristics (extract >5–7 props, split >~150 JSX lines, colocate styles/tests, feature folders over type folders). Companion skill: `frontend-design` for visual direction.

Extensibility: `SKILL.md` is the stable core; `references/` adds new frameworks or concerns without touching the core.

### `code-database`

Generates production-ready SQL, migrations, and ORM code. Auto-detects database engine. Confirms schema and query contracts before writing. P0 checklist covers SQL injection, destructive change safety, migration correctness.

### `code-tests`

Generates production-ready automated tests. One test type per invocation: E2E, API, integration, or load/performance. Confirms test plan before writing. P0 checklist covers determinism, assertions, CI readiness.

### `review-code`

Reviews code changes, diffs, pull requests, branches, or patches. Surfaces findings grouped by severity.

## Source documents

- `wiki/sources/2026-06-12-code-frontend-skill/BRAINSTORM.md`
- `wiki/sources/2026-06-21-code-backend-skill/BRAINSTORM.md`
- `wiki/sources/2026-06-21-code-database-skill/BRAINSTORM.md`
- `wiki/sources/2026-06-21-code-tests-skill/BRAINSTORM.md`
