# Code Review Checklist

Use this checklist to guide code reviews. It is coverage guidance, not a requirement to produce a finding in every category. Report only concrete risks tied to the reviewed change.

## Correctness

Check whether the change preserves the intended behavior under normal and edge-case inputs.

- Validate input handling, nullability, empty states, boundary values, parsing, serialization, and time zone behavior.
- Check control flow for missed branches, inverted conditions, early returns, retries, and fallback paths.
- Confirm changed return types, error shapes, status codes, events, and public contracts match callers and documented behavior.
- Look for stale assumptions in callers, mocks, fixtures, generated types, and snapshots.

## Regression And Compatibility

Check whether the change breaks existing users, integrations, data, or deployment flows.

- Compare old and new behavior for public APIs, CLI flags, configuration, schemas, environment variables, and feature flags.
- Check backwards compatibility for persisted data, migrations, message formats, cache keys, URLs, and external integrations.
- Verify rollout and rollback behavior when new and old code may run together.
- Watch for dependency updates that change transitive behavior, runtime requirements, or lockfile consistency.

## Tests

Check whether tests prove the changed behavior and can fail for the right reason.

- Prefer tests that exercise observable behavior through stable public interfaces.
- Look for missing negative cases, permission failures, validation errors, migration cases, concurrency cases, and frontend loading or error states.
- Flag weak assertions, excessive mocking, order dependence, shared mutable state, hidden network calls, sleeps, random data without seeds, and tests that only verify implementation details.
- Put missing coverage under `Test gaps` unless the missing test hides a concrete bug or high-risk behavior.

## Security

Check security-sensitive changes for concrete exposure. Route broad audits, OWASP reviews, and threat models to `audit-security`.

- Review authorization, authentication, tenant boundaries, role checks, object-level access, and privilege escalation paths.
- Check input validation, output encoding, path handling, SQL or command construction, SSRF surfaces, file uploads, redirects, and deserialization.
- Confirm secrets, tokens, credentials, PII, logs, telemetry, and error messages are not exposed.
- Verify cryptography, session, cookie, CORS, CSRF, rate-limit, and webhook signature changes against established project patterns.

## Performance

Check whether the change creates avoidable work or changes scaling behavior.

- Look for new N+1 queries, unbounded loops, repeated network calls, inefficient selectors, large payloads, blocking I/O, and unnecessary serialization.
- Check indexes, query plans, pagination, streaming, batching, caching, and invalidation when data access changes.
- For frontend changes, check bundle growth, render loops, expensive derived state, unnecessary re-renders, layout shifts, and image or asset loading.
- Avoid speculative performance comments unless the input size, call frequency, or runtime path makes the risk plausible.

## Maintainability

Check maintainability only where it affects change safety.

- Flag duplicated logic when it can drift and create inconsistent behavior.
- Check whether naming, ownership boundaries, or abstractions make the changed contract hard to use correctly.
- Prefer local fixes that match repository patterns over broad refactors.
- Do not elevate style preferences to review findings without a concrete defect or future-risk path.

## Operations And Observability

Check whether production behavior remains diagnosable and recoverable.

- Verify logs, metrics, traces, alerts, audit records, and error handling for changed critical paths.
- Check idempotency, retries, timeout behavior, cancellation, queue semantics, and partial-failure handling.
- Confirm migrations, background jobs, cron tasks, and external calls have safe failure and recovery behavior.
- Look for deployment-order risks when configuration, schema, and code change together.
