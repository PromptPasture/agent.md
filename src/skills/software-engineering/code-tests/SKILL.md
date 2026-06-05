---
name: code-tests
description: Generate or revise automated tests. Use for E2E/browser, API/contract, integration, and load/performance test requests.
license: Apache-2.0
tags:
  - codegen
  - testing
metadata:
  author: Oleg Shulyakov
  version: "1.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: testing
---

# code-tests

Generate production-ready test code. Classify the request, read the matching reference, inspect the repository, then implement runnable tests or provide complete files when direct edits are not safe.

---

## Variant Detection

- **User phrases:** Treat "E2E", "browser", "Playwright", "Cypress", "API", "contract", "integration", "load", "performance", "k6", "Locust", "latency", and "throughput" as strong routing signals.
- **Repository signals:** Check configs, dependencies, test folders, package scripts, CI jobs, and framework imports before choosing patterns. Common signals include `playwright.config.*`, `cypress.config.*`, `supertest`, `newman`, `pytest`, `k6`, `locust`, and `jmeter`.
- **Surface signals:** Route browser user journeys to E2E, HTTP endpoints and service contracts to API, and throughput or latency scenarios to performance.
- **Security boundary:** Do not use this skill for security, abuse-resistance, jailbreak, privacy, or adversarial audit work unless the user is asking only for ordinary regression tests around already-defined behavior.
- **Ambiguity:** If two variants are plausible and the wrong one would change the files or framework, ask one short question naming the likely choices.

---

## Routing Table

| Request | Reference |
| --- | --- |
| Browser flows, smoke tests, page objects, login, checkout, onboarding, UI validation, visual user journeys | `references/e2e.md` |
| HTTP endpoints, controllers, service integration tests, OpenAPI examples, Postman/Newman collections, Supertest suites | `references/api.md` |
| Load, stress, soak, spike, capacity, p95/p99 latency, throughput, k6, Locust, JMeter | `references/perf.md` |

---

## Repository Workflow

- **Inspect first:** Identify the runner, language, fixture style, factories, auth helpers, test data setup, naming conventions, and CI commands before editing.
- **Reuse local patterns:** Prefer existing helpers, clients, fixtures, page objects, factories, config loaders, and environment handling. Add new helpers only when they remove repeated setup in the tests being added.
- **Write runnable code:** Implement tests in the repository when enough context exists. If direct edits are unsafe or the user asks for a draft, provide complete file contents with paths, assumptions, and run commands.
- **Keep scope tight:** Cover the highest-value happy path plus meaningful failure, edge, or regression cases. Avoid broad tests that only assert existence or duplicate lower-level coverage.
- **Design for determinism:** Prefer stable selectors, public API contracts, deterministic fixtures, isolated data, explicit assertions, and existing test doubles. Avoid sleeps, hidden network dependencies, shared mutable state, and order-dependent tests.
- **Protect secrets:** Keep credentials, tokens, base URLs, and environment-specific values behind existing config helpers or environment variables.

---

## Working Rules

- **Verification:** Run the narrowest relevant test command when feasible. If verification cannot run, state the blocker and provide the exact command the user should run.

---

## Output

When editing a repository, finish with changed files, the test command used, and verification status.

When only drafting code, use this structure:

```text
Assumptions:
- ...

Files:
- path/to/test-file

Run:
- command

Notes:
- ...
```

---

## Verification

- [ ] Exactly one test reference was selected unless the user explicitly requested a mixed suite
- [ ] Tests reuse existing runner, fixtures, helpers, auth setup, naming, and CI conventions
- [ ] The suite covers high-value happy path and meaningful failure, edge, regression, or performance behavior
- [ ] The narrowest relevant test command was run or the blocker and exact command were reported
