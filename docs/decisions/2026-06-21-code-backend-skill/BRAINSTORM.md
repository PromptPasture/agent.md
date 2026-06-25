---
topic: code-backend skill
method: comparative analysis
date: "2026-06-21"
related:
  - wiki/sources/2026-06-12-code-frontend-skill/BRAINSTORM.md
  - src/skills/in-progress/code-frontend/SKILL.md
---

# Brainstorm - code-backend Skill

## Goal

Design a skill that guides an agent to generate production-ready backend code
for real project codebases. The skill must detect the project stack automatically
(polyglot), enforce quality across security, API contracts, observability, and
performance, and gate output behind an explicit validation checklist.

## Context

- Output target: files written to disk inside an existing (or new) project
- Framework stance: polyglot — detect from lockfiles and framework config files;
  suggest a stack when the project is empty
- Companion to `code-frontend`; the two skills compose naturally on full-stack tasks
- Scope: API routes, services, middleware, workers/queues, persistence (ORM/migrations),
  observability, and configuration — full backend stack
- Skill location: `src/skills/code-backend/SKILL.md`

## Agenda

1. Define the four phases and their gates
2. Define what "production-ready" means for backend
3. Define stack detection heuristics (polyglot)
4. Define the validate checklist axes and priority tiers
5. Define the reference doc coverage map

## Ideas Considered

### Approach A: Same 4-phase structure as frontend

- **Description:** Mirror the frontend skill exactly — Discover → Plan → Build → Validate.
- **Benefits:** Familiar pattern across both skills, easier to reason about.
- **Trade-offs:** "Plan" in frontend means component interface contract; for backend
  it needs to cover API contracts, DB schema, and service interfaces — the word
  "Plan" undersells that.

### Approach B: Same structure, renamed phases ✅ Selected

- **Description:** Discover → Design → Build → Validate. Same gating logic as
  frontend, but "Design" explicitly signals that the phase produces API contracts,
  DB schema changes, and service interface contracts — not just a component plan.
- **Benefits:** Mirrors frontend rhythm, but the phase name communicates the
  richer backend artifact. User knows what to expect and confirm.
- **Trade-offs:** Slight asymmetry with frontend. Acceptable — backend concerns
  are genuinely different.

### Approach C: Checklist-first / triage-led

- **Description:** Lead with a triage step that decides ceremony level before
  jumping into phases. Small incremental tasks (add one endpoint) skip most gates.
- **Benefits:** Less friction for routine tasks.
- **Trade-offs:** Inconsistent experience; phases can be marked skippable instead,
  which achieves the same effect without abandoning structure.

## Outcomes

### Summary

`code-backend` is a four-phase, phase-gated skill for writing production-ready
backend code into real codebases. It auto-detects the project stack from lockfiles
and framework config files across any backend language (Go, Node.js, Python, Java,
Kotlin, Rust, and others). The Design phase produces confirmed API contracts,
DB schema changes, and service interface contracts before any code is written.
The Validate phase enforces a P0–P3 quality checklist covering security, API
correctness, observability, and performance.

### Decisions

- **Structure:** Approach B — Discover → Design → Build → Validate, phase-gated
  with skippable phases
- **Stack detection:** Polyglot from day one. Detect from:
  - `go.mod` → Go; inspect for Gin, Echo, Fiber, Chi, standard `net/http`
  - `package.json` → Node.js; inspect for Express, Fastify, NestJS, Hono, Nitro
  - `requirements.txt` / `pyproject.toml` / `Pipfile` → Python; inspect for FastAPI, Django, Flask
  - `pom.xml` / `build.gradle` → Java/Kotlin; inspect for Spring Boot, Quarkus, Micronaut, Ktor
  - `Cargo.toml` → Rust; inspect for Axum, Actix-web, Warp
  - Also detect: ORM/query layer, DB type, auth library, queue/worker library,
    observability stack (logging, tracing, metrics)
- **No config file:** Detection purely from existing project files
- **Design phase output:** API contract (method, path, request schema, response
  schema, status codes, error shape) + DB schema changes + service interface
  signatures; user confirms before Build
- **Validate checklist tiers:**
  - P0 — Blocking: auth/authz on every protected route, input validation at all
    entry points, no injection vulnerabilities (SQL, command, path traversal),
    no secrets in code or logs, broken API contract
  - P1 — Required: error handling (no silent failures, typed error responses),
    type safety (no untyped `any`/`interface{}`/`object` at boundaries), all
    status codes correct and documented, all error shapes match the contract
  - P2 — Expected: structured logging on every request/response/error, tracing
    spans for external calls, query performance (N+1 detection, missing index
    hints), input/output validation at service boundaries
  - P3 — Polish: config hygiene (no hardcoded env values), worker/queue
    idempotency, graceful shutdown, connection pool sizing noted

### Extensibility Model

Same as `code-frontend`: `SKILL.md` is the stable core — phases and checklist
axes never change. `references/` is the extension surface — adding a new language,
framework, or concern means adding or updating one file only. No changes to `SKILL.md`.

The agent loads only the reference docs relevant to the current task.

### Frontmatter Description

Rewrite the `description` field to be precise and trigger-oriented, matching
the style of `code-frontend`:

> Use when asked to build or modify any backend code: API endpoints, service
> logic, middleware, workers, queues, persistence (ORM, migrations, queries),
> auth, config, or observability. Detects stack automatically (Go, Node.js,
> Python, Java, Kotlin, Rust, and more). Produces confirmed API contracts and
> DB schema before writing code. Enforces a P0–P3 checklist covering security,
> API correctness, observability, and performance.

### Coverage Map

|Concern|Delivery|Location|
|---|---|---|
|Language detection (all ecosystems)|Inline — Discover phase|`SKILL.md`|
|Framework detection|Inline — Discover phase|`SKILL.md`|
|API contract (Design phase)|Inline — Design phase|`SKILL.md`|
|DB schema changes (Design phase)|Inline — Design phase|`SKILL.md`|
|Service interface contracts|Inline — Design phase|`SKILL.md`|
|Decomposition heuristics|Inline — Build phase|`SKILL.md`|
|Validate checklist (P0–P3)|Inline — Validate phase|`SKILL.md`|
|Code conventions|Reference doc|`references/conventions.md`|
|Error handling|Reference doc|`references/error-handling.md`|
|Input validation|Reference doc|`references/validation.md`|
|Auth / authorization|Reference doc|`references/auth.md`|
|Persistence (ORM, queries, migrations)|Reference doc|`references/persistence.md`|
|Workers / queues|Reference doc|`references/workers.md`|
|Observability (logging, tracing, metrics)|Reference doc|`references/observability.md`|
|Configuration / secrets|Reference doc|`references/config.md`|
|Testing (unit, integration, contract)|Reference doc|`references/testing.md`|
|Performance (query, caching, concurrency)|Reference doc|`references/performance.md`|
|API design (REST conventions, versioning)|Reference doc|`references/api-design.md`|
|Security patterns|Reference doc|`references/security.md`|

New languages, frameworks, or concerns → add a file to `references/`. No other
changes required.

### Open Questions

None.

## Next Steps

1. ✅ Rewrite frontmatter `description` in `src/skills/in-progress/code-backend/SKILL.md`
2. ✅ Write full `SKILL.md` — 4 phases, Design phase contracts, decomposition heuristics, P0–P3 validate checklist
3. ✅ Write `references/conventions.md`
4. ✅ Write `references/error-handling.md`
5. ✅ Write `references/validation.md`
6. ✅ Write `references/auth.md`
7. ✅ Write `references/persistence.md`
8. ✅ Write `references/workers.md`
9. ✅ Write `references/observability.md`
10. ✅ Write `references/config.md`
11. ✅ Write `references/testing.md`
12. ✅ Write `references/performance.md`
13. ✅ Write `references/api-design.md`
14. ✅ Write `references/security.md`
15. ✅ Convert all code examples to language-agnostic pseudocode throughout `SKILL.md` and all reference docs
16. ✅ Tag fenced code blocks: `pseudocode` for logic, `text` for output/templates, `sql` for SQL, `json` for JSON
17. ⬜ Graduate from `in-progress/` to `published/`
