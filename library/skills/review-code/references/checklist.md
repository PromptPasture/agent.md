# Code Review Checklist

Use this checklist to guide code reviews. It is coverage guidance, not a requirement to produce a finding in every category. Report only concrete risks tied to the reviewed change.

Load a focused reference when the diff needs deeper review:

- `references/regressions.md` for compatibility, rollout, persistence, or integration risk.
- `references/security.md` for changed authentication, authorization, input handling, secrets, privacy, or abuse surfaces.
- `references/performance.md` for hot paths, data access, rendering, payload size, concurrency, or resource-use changes.
- `references/test-gaps.md` for missing, weak, flaky, or misleading tests.
- `references/agent-skill.md` for created or revised agent skills, including trigger descriptions, scope, progressive disclosure, and eval coverage.

## Correctness

Check whether the change preserves the intended behavior under normal and edge-case inputs.

- Validate input handling, nullability, empty states, boundary values, parsing, serialization, and time zone behavior.
- Check control flow for missed branches, inverted conditions, early returns, retries, and fallback paths.
- Confirm changed return types, error shapes, status codes, events, and public contracts match callers and documented behavior.
- Look for stale assumptions in callers, mocks, fixtures, generated types, and snapshots.

## Regression And Compatibility

Check whether the change breaks existing users, integrations, data, or deployment flows.

Use `references/regressions.md` for deeper guidance.

## Tests

Check whether tests prove the changed behavior and can fail for the right reason.

Use `references/test-gaps.md` for deeper guidance.

## Security

Check security-sensitive changes for concrete exposure. Use `references/security.md` for broader security review concerns when the user asks for OWASP-style review, threat modeling, secrets exposure, abuse resistance, or privacy risk in the reviewed code.

Use `references/security.md` for deeper guidance.

## Performance

Check whether the change creates avoidable work or changes scaling behavior.

Use `references/performance.md` for deeper guidance.

## Maintainability

Check maintainability only where it affects change safety.

- Flag duplicated logic when it can drift and create inconsistent behavior.
- Check whether naming, ownership boundaries, or abstractions make the changed contract hard to use correctly.
- Prefer local fixes that match repository patterns over broad refactors.
- Do not elevate style preferences to review findings without a concrete defect or future-risk path.

## Skill Design

Check created or revised skills for agent usability. Use `references/agent-skill.md` for deeper guidance.

## Operations And Observability

Check whether production behavior remains diagnosable and recoverable.

- Verify logs, metrics, traces, alerts, audit records, and error handling for changed critical paths.
- Check idempotency, retries, timeout behavior, cancellation, queue semantics, and partial-failure handling.
- Confirm migrations, background jobs, cron tasks, and external calls have safe failure and recovery behavior.
- Look for deployment-order risks when configuration, schema, and code change together.
