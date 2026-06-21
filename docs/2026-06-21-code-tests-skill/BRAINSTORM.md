---
topic: code-tests skill
method: comparative analysis
date: "2026-06-21"
related:
  - src/skills/in-progress/code-tests/SKILL.md
  - src/skills/in-progress/code-frontend/SKILL.md
  - src/skills/in-progress/code-backend/SKILL.md
---

# Brainstorm — code-tests skill

## Goal

Design and implement a `code-tests` skill that guides an AI agent through writing production-quality automated tests. Covers E2E, API, integration, and load/performance test types. One test type per invocation.

## Context

The project already has `code-frontend` and `code-backend` skills that follow a 4-phase workflow (Discover → Plan/Design → Build → Validate) with P0–P3 quality checklists and conditional reference doc loading. The `code-tests` skill should match this pattern and sit alongside them in the `software-engineering` catalog.

## Agenda

1. Test type scope and invocation model
2. Skill structure and reference doc strategy
3. Phase design per test type
4. Validate checklist structure

## Ideas Considered

### One test type per invocation vs. mixed sessions

- **Description:** Each invocation targets a single test type (E2E, API, integration, or load). The user declares intent upfront.
- **Benefits:** Focused output, relevant checklist, matches how senior AQAs organise work (separate dirs, CI stages, tooling).
- **Trade-offs:** User must invoke twice if they want API + integration coverage for the same feature.

**Decision:** One test type per invocation.

### Option A — Unified adaptive skill (no explicit type sections)

- **Description:** One SKILL.md where phases silently adapt to the detected type. No labeled sections per type.
- **Benefits:** Compact document.
- **Trade-offs:** Branching logic is implicit; hard to scan or extend.

### Option B — Unified skill with explicit type sections + reference docs

- **Description:** One SKILL.md with a 4-phase workflow. Phase 1 identifies the test type and routes to type-specific sections in Phase 2 (Plan) and Phase 3 (Build). Type-specific guidance lives in dedicated reference docs (`references/e2e.md`, `references/api.md`, `references/integration.md`, `references/load.md`). Shared concerns in additional references (`references/test-data.md`, `references/mocking.md`, `references/assertions.md`).
- **Benefits:** One consistent entry point; clean separation of test-type knowledge; easy to extend (add `references/contract.md` without touching the main skill); matches the reference-doc pattern from `code-frontend`/`code-backend`.
- **Trade-offs:** More files to maintain than a pure single-document approach.

**Decision:** Option B.

### Option C — Separate skill per test type

- **Description:** `code-tests-e2e`, `code-tests-api`, `code-tests-integration`, `code-tests-load` as four independent skills.
- **Benefits:** Maximum focus; consistent with how `code-frontend`/`code-backend` are split by concern.
- **Trade-offs:** Duplicates the 4-phase workflow across four files; no single entry point; harder to keep in sync.

## Outcomes

### Summary

A single `code-tests` skill with a 4-phase workflow (Discover → Plan → Build → Validate). Phase 1 detects the project stack and test type from user intent, then routes to type-specific sections backed by reference docs. The validate phase has a shared P0–P3 checklist core with type-specific items contributed by each reference.

### Decisions

- **One test type per invocation** — declared by the user, confirmed in Phase 1.
- **B + reference docs** — one SKILL.md, type-specific knowledge in `references/`.
- **Reference doc set:**
  - `references/e2e.md` — Playwright, Cypress; user flow design, selector strategy, fixtures
  - `references/api.md` — Supertest, httpx, REST Assured; contract assertions, auth, status codes
  - `references/integration.md` — real dependencies, DB state setup/teardown, service boundaries
  - `references/load.md` — k6, Locust, Artillery; load profiles, thresholds, ramp-up
  - `references/test-data.md` — factories, fixtures, seed strategies (shared)
  - `references/mocking.md` — mock discipline, contract fidelity, when not to mock (shared)
  - `references/assertions.md` — meaningful assertions, avoid implementation detail coupling (shared)
- **Phase structure mirrors code-backend:** Discover → Plan → Build → Validate, each phase confirmed before the next begins.
- **Validate checklist:** shared P0–P3 core (determinism, independence, meaningful assertions, no secrets) + type-specific additions loaded from the active reference doc.

### Open Questions

- Should unit tests be in scope for this skill, or handled separately? (Not included for now — user specified E2E, API, integration, load.)
- Reference docs are placeholders until authored — skill should degrade gracefully if a reference is missing.

## Next Steps

1. Write `src/skills/in-progress/code-tests/SKILL.md` — full 4-phase skill
2. Write `src/skills/in-progress/code-tests/references/e2e.md`
3. Write `src/skills/in-progress/code-tests/references/api.md`
4. Write `src/skills/in-progress/code-tests/references/integration.md`
5. Write `src/skills/in-progress/code-tests/references/load.md`
6. Write shared references: `test-data.md`, `mocking.md`, `assertions.md`
