# Test Gap Review

Use this reference when judging whether tests sufficiently cover the reviewed change.

## Review Focus

Test gaps usually belong under `Test gaps`, not `Findings`. Promote a test gap to a severity finding only when the absence or weakness of the test hides a concrete bug, makes a risky migration untrustworthy, or creates a likely false positive in CI.

## Missing Coverage

- New behavior should have at least one test that fails against the old behavior.
- Changed validation, authorization, migrations, retries, feature flags, and error handling need negative or edge-case coverage.
- Frontend flows should cover loading, empty, error, disabled, permission, and responsive states when those states changed.
- Backend flows should cover input boundaries, persistence effects, external failures, idempotency, and transaction behavior when relevant.

## Weak Tests

- Watch for assertions that only check existence, snapshots without behavioral intent, excessive mocking, and tests coupled to implementation details.
- Check whether mocks match real contracts, including error shapes, timing, optional fields, and side effects.
- Prefer stable public interfaces and observable outcomes over private helper calls.
- Verify tests fail for the intended reason, not because setup is brittle.

## Flaky Patterns

- Flag sleeps, timing races, test-order dependence, shared mutable state, hidden network calls, random data without seeds, timezone dependence, and reliance on local machine state.
- Check cleanup for databases, queues, browser storage, temporary files, fake timers, event listeners, and global config.
- For retries and async workers, verify tests control time, retries, and queue state deterministically.

## CI And Maintenance

- Check whether new tests are wired into existing scripts and CI jobs.
- Verify fixtures, factories, and helpers follow repository patterns.
- Avoid broad low-signal tests that slow CI without proving the changed behavior.
