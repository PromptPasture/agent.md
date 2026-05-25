# Code Review Checklist

Use this checklist to guide code reviews. It is coverage guidance, not a requirement to produce a finding in every category. Report only concrete risks tied to the reviewed change.

Load a focused reference when the diff needs deeper review:

- **Regressions**: `references/regressions.md` for compatibility, rollout, persistence, or integration risk.
- **Security**: `references/security.md` for changed authentication, authorization, input handling, secrets, privacy, or abuse surfaces.
- **Performance**: `references/performance.md` for hot paths, data access, rendering, payload size, concurrency, or resource-use changes.
- **Test gaps**: `references/test-gaps.md` for missing, weak, flaky, or misleading tests.

---

## Correctness

- **Inputs**: validate input handling, nullability, empty states, boundary values, parsing, serialization, and time zone behavior.
- **Control flow**: check for missed branches, inverted conditions, early returns, retries, and fallback paths.
- **Contracts**: confirm changed return types, error shapes, status codes, events, and public contracts match callers and documented behavior.
- **Assumptions**: look for stale assumptions in callers, mocks, fixtures, generated types, and snapshots.

---

## Regression And Compatibility

Use `references/regressions.md` for deeper guidance.

---

## Tests

Use `references/test-gaps.md` for deeper guidance.

---

## Security

Use `references/security.md` for broader security review concerns when the user asks for OWASP-style review, threat modeling, secrets exposure, abuse resistance, or privacy risk in the reviewed code.

Use `references/security.md` for deeper guidance.

---

## Performance

Use `references/performance.md` for deeper guidance.

---

## Maintainability

- **Duplication**: flag duplicated logic when it can drift and create inconsistent behavior.
- **Contracts**: check whether naming, ownership boundaries, or abstractions make the changed contract hard to use correctly.
- **Local fixes**: prefer local fixes that match repository patterns over broad refactors.
- **Style**: do not elevate style preferences to review findings without a concrete defect or future-risk path.

---

## Operations And Observability

- **Diagnostics**: verify logs, metrics, traces, alerts, audit records, and error handling for changed critical paths.
- **Resilience**: check idempotency, retries, timeout behavior, cancellation, queue semantics, and partial-failure handling.
- **Recovery**: confirm migrations, background jobs, cron tasks, and external calls have safe failure and recovery behavior.
- **Deployment order**: look for deployment-order risks when configuration, schema, and code change together.
