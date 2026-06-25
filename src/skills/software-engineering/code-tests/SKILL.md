---
name: code-tests
description: You use this when the user asks to write automated tests — E2E, API, integration, or load/performance. One test type per invocation. Generates production-ready test code with auto-detected stack and framework, confirmed test plan before writing, and a P0–P3 quality checklist covering determinism, coverage, assertions, and CI readiness.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "2.0.1"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: testing
  tags: [testing, e2e, api, integration, load, performance, playwright, cypress, k6, jest, vitest, pytest]
---

# Writing Automated Tests

Generates production-ready automated tests in the project's existing stack.
Four phases: **Discover → Plan → Build → Validate**. Each phase produces a confirmed output before the next begins. Phases are skippable when the user already provides the relevant context.

One test type per invocation: **E2E**, **API**, **Integration**, or **Load/Performance**.

---

## Phase 1 — Discover

**Goal:** Establish the test type, project stack, and existing test conventions before writing a single line of code.

### 1.1 Identify test type

Determine the test type from the user's request: **E2E**, **API**, **Integration**, or **Load/Performance**. If the type is ambiguous, ask one clarifying question before proceeding.

### 1.2 Read project files

Inspect the following in order. Stop reading a file once the needed signal is found.

|File|Signal to extract|
|---|---|
|`package.json`|Language, test runner (Jest, Vitest, Mocha), E2E framework (Playwright, Cypress)|
|`playwright.config.*`|Playwright presence, browsers, base URL, reporter|
|`cypress.config.*`|Cypress presence, base URL, spec pattern|
|`vitest.config.*` / `jest.config.*`|Unit/integration test runner config|
|`pyproject.toml` / `pytest.ini` / `setup.cfg`|Python; pytest, pytest-asyncio, httpx|
|`go.mod`|Go; detect `testing`, `testify`, `httptest`, `gomock`|
|`pom.xml` / `build.gradle*`|Java/Kotlin; JUnit, RestAssured, WireMock, Gatling|
|`k6/` / `load/` / `perf/` dirs|k6 scripts, Artillery configs, Locust files|
|`docker-compose.yml`|Test DB, mock services, dependency containers|
|Existing test files|Naming conventions, folder structure, helper patterns, assertion style|

### 1.3 Output a detection summary

Present a concise summary and wait for confirmation before proceeding:

```text
Test type:    E2E
Framework:    Playwright (TypeScript)
Base URL:     http://localhost:3000
Browsers:     chromium
Existing:     tests/e2e/ (3 spec files found)
Conventions:  POM pattern, data-testid selectors
```

Adapt the summary fields to the detected test type. If the user corrects any item, update and re-confirm.

### 1.4 Empty project fallback

If no test framework is found, suggest a default for the detected language and test type, then wait for explicit confirmation:

```text
No test framework detected. Suggested setup:
  Test type:  E2E
  Framework:  Playwright (TypeScript)
  Runner:     @playwright/test

Confirm, or tell me what framework to use instead.
```

Do not proceed to Plan until the stack is confirmed.

---

## Phase 2 — Plan

**Goal:** Produce a confirmed test plan — target, scenarios, and test contract — before any code is written.

### 2.1 Ask clarifying questions (if needed)

Resolve ambiguity with a single focused question at a time. Skip if the request is already specific. Common gaps:

- What is the exact target? (endpoint path, user flow, service method, page)
- What environment or base URL?
- Is there existing test data, fixtures, or seed scripts to build on?
- Any auth required to reach the target?
- For load tests: what are the acceptance thresholds (p95 latency, error rate)?

### 2.2 Draft the test plan

Produce a test plan in this format. Omit sections that are not applicable.

```text
Target:       POST /api/v1/orders
Auth:         Bearer token (role: customer)
Test data:    Seeded product catalogue, existing user fixture

Scenarios:
  Happy path
    - Create order with valid items → 201, order ID returned
    - Items reserved from inventory on success

  Edge cases
    - Empty items array → 400 VALIDATION_ERROR
    - Item quantity exceeds stock → 409 CONFLICT
    - Duplicate order idempotency key → 200, original order returned

  Failure modes
    - Missing auth token → 401 UNAUTHORIZED
    - Expired token → 401 UNAUTHORIZED
    - Payment service unavailable → 503, no partial state left
```

Adapt the format to the test type:

- **E2E:** describe user flows step by step (navigate → interact → assert)
- **API:** list endpoint + method + request shape + expected response per scenario
- **Integration:** list service boundary inputs, real dependencies used, state before/after
- **Load/Performance:** define load profile (virtual users, ramp-up, duration, thresholds for p50/p95/p99 and error rate)

For the type-specific plan format, see the reference doc loaded in Phase 2.3.

### 2.3 Identify reference docs to load

|Signal|Load|
|---|---|
|Test type is E2E|`references/e2e.md`|
|Test type is API|`references/api.md`|
|Test type is Integration|`references/integration.md`|
|Test type is Load/Performance|`references/perf.md`|
|Test data setup required|`references/test-data.md`|
|External services need to be stubbed or mocked|`references/mocking.md`|
|Assertion patterns are complex or numerous|`references/assertions.md`|

### 2.4 Wait for confirmation

Present the test plan from step 2.2 and wait for explicit confirmation before proceeding to Build. If the user corrects any item, update and re-confirm.

---

## Phase 3 — Build

**Goal:** Write production-ready test files that match the confirmed plan and detected stack.

### 3.1 Load reference docs

Load every reference doc identified in Phase 2 before writing any file. Apply its guidance throughout the Build phase.

### 3.2 Apply decomposition heuristics

Before writing, state the decomposition rationale. Split into smaller files or helpers when any of the following is true:

- A spec file exceeds ~200 lines
- Setup / teardown logic is repeated across more than one file
- Test data construction logic exceeds ~20 lines per test
- A page object or helper is used across more than one spec

Do not create abstractions that serve only one test.

### 3.3 File and folder conventions

Follow the project's existing conventions if present. When no convention is established, apply these defaults:

```text
tests/
  e2e/
    specs/          # Spec files, one per user flow
    pages/          # Page Object Models
    fixtures/       # Playwright fixtures or Cypress commands
  api/
    specs/          # One spec file per endpoint or resource
    helpers/        # Auth setup, request builders
  integration/
    specs/          # One spec file per service or domain boundary
    setup/          # DB seed, container lifecycle
  load/             # or perf/ — follow the existing directory name if one is present
    scenarios/      # One script per load scenario
    thresholds.js   # Shared acceptance criteria
```

- One concern per spec file
- Helpers and fixtures co-located with the tests that use them
- No production source imports in test files beyond what is necessary for types

### 3.4 Code standards

Apply these unconditionally:

#### Structure

- Follow Arrange–Act–Assert (AAA) in every test case
- One logical assertion group per test — not multiple unrelated assertions in one `it`/`test`
- Describe blocks reflect the target; `it`/`test` blocks describe the scenario and expected outcome
- No logic in test bodies beyond setup calls and assertions — extract to helpers

#### Isolation

- Every test sets up its own state and tears it down — no dependency on test execution order
- No shared mutable state between tests
- Flaky dependencies (time, random values, external APIs) are controlled or seeded

#### Assertions

- Assert on observable behaviour and outcomes, not on implementation details
- Prefer specific assertions (`toEqual`, `toHaveStatus`) over generic truthy checks
- Every assertion has a clear failure message or description
- See `references/assertions.md` for patterns

#### Security

- No real credentials, tokens, or PII in test files or fixtures
- Test secrets loaded from environment variables or a secrets fixture
- No hardcoded base URLs — use config or environment variables

### 3.5 Write files

Write each file in full. No placeholders, no TODOs, no stub implementations. If a scenario is genuinely out of scope, omit it and state why.

After writing all files, list every file created or modified:

```text
Created:
  tests/api/specs/orders.spec.ts
  tests/api/helpers/auth.ts

Modified:
  tests/api/helpers/index.ts   (added order helpers export)
```

Present this list and wait for the user to confirm before proceeding to Validate.

---

## Phase 4 — Validate

**Goal:** Work through every checklist item before declaring the output complete. Fix any issue found — do not report and skip.

Items are ordered by severity. P0 failures block delivery. P1–P3 failures must be resolved before closing but do not require re-confirmation from the user unless the fix changes the test plan.

---

### P0 — Blocking

These issues make the tests unsafe, broken, or untrustworthy. Stop and fix before anything else.

- [ ] All tests run to completion without runtime errors
- [ ] No real credentials, tokens, or PII hardcoded in test files or fixtures
- [ ] Every test contains at least one meaningful assertion — no empty or always-passing tests
- [ ] Tests match the confirmed test plan exactly — no missing or undeclared scenarios
- [ ] No test directly modifies shared production state without cleanup

---

### P1 — Required

These issues violate production test standards. Fix before closing.

#### Coverage

- [ ] Happy path scenario covered for every target in the plan
- [ ] At least one key failure mode covered per target
- [ ] Auth-protected targets tested with both valid and invalid credentials

#### Isolation

- [ ] Tests pass when run in any order
- [ ] Tests pass when run in parallel (or documented why they cannot)
- [ ] Each test cleans up the state it creates

#### Assertions

- [ ] Assertions are on observable outcomes, not internal implementation details
- [ ] No assertion that always passes regardless of the code under test
- [ ] Failure messages identify what went wrong without reading the source

---

### P2 — Expected

These issues reduce quality below senior standards. Fix before closing.

#### Test data

- [ ] Test data is minimal — only what the scenario requires
- [ ] Fixtures and factories produce valid, realistic values
- [ ] No test depends on data left over from a previous test run

#### Mocking discipline

- [ ] Mocks reflect realistic contracts — not simplified return values that hide real failure modes
- [ ] No mock where a real dependency can be used without unacceptable cost
- [ ] See `references/mocking.md`

#### Code quality

- [ ] No spec file exceeds ~200 lines — split if so
- [ ] No setup logic duplicated across files — extract to shared helper
- [ ] Describe and test block names form a readable sentence describing the scenario

---

### P3 — Polish

Nice-to-have. Fix if the effort is small; note and defer otherwise.

- [ ] Test output is readable in CI logs — no excessive noise or truncated errors
- [ ] Load tests include a summary threshold check that fails the CI step on breach
- [ ] Flaky test risk noted with a comment where timing or network is unavoidable

---

### Completion summary

After all items are resolved, output:

```text
Validate complete.

P0  ✓ all passed
P1  ✓ all passed
P2  ✓ all passed      (or: 1 deferred — [item] — [reason])
P3  ✓ all passed      (or: 1 deferred — [item] — [reason])

Files delivered:
  tests/api/specs/orders.spec.ts
  tests/api/helpers/auth.ts
```

If any P2 or P3 item was deferred, state the reason and confirm it is acceptable before closing.
