---
name: build-tests
description: >
  Generate or revise automated tests and evals. Use for E2E/browser, API/contract,
  integration, load/performance, LLM output, RAG, prompt regression, AI tool-use,
  and AI cost/latency benchmark requests.
license: MIT
tags:
  - codegen
  - testing
  - evals
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-team-roles
  category: testing
---

# build-tests

Generate production-ready test code and evaluation suites. Classify the request, read the matching reference, inspect the repository, then implement runnable tests or provide complete files when direct edits are not safe.

## Variant Detection

**Route by explicit intent first, then repo evidence, then the system surface under test.**

- **User phrases:** Treat "E2E", "browser", "Playwright", "Cypress", "API", "contract", "integration", "load", "performance", "k6", "Locust", "AI eval", "LLM eval", "RAG", "prompt regression", "tool use", "agent eval", "latency", "tokens", and "cost" as strong routing signals.
- **Repository signals:** Check configs, dependencies, test folders, package scripts, CI jobs, eval folders, and framework imports before choosing patterns. Common signals include `playwright.config.*`, `cypress.config.*`, `supertest`, `newman`, `pytest`, `k6`, `locust`, `jmeter`, `promptfoo`, `deepeval`, `ragas`, `openevals`, and model SDK usage.
- **Surface signals:** Route browser user journeys to E2E, HTTP endpoints and service contracts to API, non-AI throughput or latency scenarios to performance, AI answer quality and RAG grounding to AI output, agent tool traces to AI tool-use, and AI latency/cost/token benchmarks to AI performance.
- **Security boundary:** Do not use this skill for security, abuse-resistance, jailbreak, privacy, or adversarial audit work unless the user is asking only for ordinary regression tests around already-defined behavior.
- **Ambiguity:** If two variants are plausible and the wrong one would change the files or framework, ask one short question naming the likely choices.

## Routing Table

**Read exactly one reference unless the user explicitly asks for a mixed suite.**

| Request | Reference |
| --- | --- |
| Browser flows, smoke tests, page objects, login, checkout, onboarding, UI validation, visual user journeys | `references/e2e.md` |
| HTTP endpoints, controllers, service integration tests, OpenAPI examples, Postman/Newman collections, Supertest suites | `references/api.md` |
| Load, stress, soak, spike, capacity, p95/p99 latency, throughput, k6, Locust, JMeter | `references/perf.md` |
| LLM answer quality, prompt regression, grading rubrics, structured output checks, RAG answer grounding, citation checks | `references/ai-output.md` |
| Agent tool choice, tool arguments, mocked tool failures, recovery behavior, multi-step tool workflows | `references/ai-tool-use.md` |
| AI latency, token usage, cost per task, model-call count, retry rate, throughput, quality-per-dollar | `references/ai-perf.md` |

## Repository Workflow

**Fit the suite into the project instead of inventing a parallel test universe.**

- **Inspect first:** Identify the runner, language, fixture style, factories, auth helpers, test data setup, naming conventions, and CI commands before editing.
- **Reuse local patterns:** Prefer existing helpers, clients, fixtures, page objects, factories, config loaders, and environment handling. Add new helpers only when they remove repeated setup in the tests being added.
- **Write runnable code:** Implement tests in the repository when enough context exists. If direct edits are unsafe or the user asks for a draft, provide complete file contents with paths, assumptions, and run commands.
- **Keep scope tight:** Cover the highest-value happy path plus meaningful failure, edge, or regression cases. Avoid broad tests that only assert existence or duplicate lower-level coverage.
- **Design for determinism:** Prefer stable selectors, public API contracts, deterministic fixtures, isolated data, explicit assertions, and existing test doubles. Avoid sleeps, hidden network dependencies, shared mutable state, and order-dependent tests.
- **Protect secrets:** Keep credentials, tokens, base URLs, and environment-specific values behind existing config helpers or environment variables.

## Working Rules

**Use the bundled helpers for skill maintenance and generated eval scaffolding.**

- **Skill validation:** Run `scripts/validate_evals.py` after editing this skill's eval cases, `scripts/run_eval.py` for trigger/routing checks, `scripts/run_loop.py` for eval/improvement loops, and `scripts/aggregate_benchmark.py` to summarize iterations.
- **AI eval scaffolding:** Use `scripts/scaffold_ai_eval.py` when creating a starter AI eval folder and `scripts/summarize_ai_perf.py` when summarizing AI benchmark `results.jsonl` files.
- **Quality pairing:** For AI evals and benchmarks, measure quality with operational metrics when possible. Latency, tokens, and cost without pass/fail quality mostly show how efficiently the system can be wrong. Annoyingly common, still not useful.
- **Verification:** Run the narrowest relevant test command when feasible. If verification cannot run, state the blocker and provide the exact command the user should run.

## Output Format

**End with the information needed to review and rerun the work.**

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
