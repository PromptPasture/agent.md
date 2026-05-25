# Test Gap Review

Use this reference when judging whether tests sufficiently cover the reviewed change.

---

## Review Focus

Promote a test gap to a severity finding only when the absence or weakness of the test hides a concrete bug, makes a risky migration untrustworthy, or creates a likely false positive in CI.

---

## Missing Coverage

- **New behavior**: should have at least one test that fails against the old behavior.
- **Risky paths**: changed validation, authorization, migrations, retries, feature flags, and error handling need negative or edge-case coverage.
- **Frontend flows**: should cover loading, empty, error, disabled, permission, and responsive states when those states changed.
- **Backend flows**: should cover input boundaries, persistence effects, external failures, idempotency, and transaction behavior when relevant.

---

## Weak Tests

- **Assertions**: watch for assertions that only check existence, snapshots without behavioral intent, excessive mocking, and tests coupled to implementation details.
- **Mocks**: check whether mocks match real contracts, including error shapes, timing, optional fields, and side effects.
- **Interfaces**: prefer stable public interfaces and observable outcomes over private helper calls.
- **Failure mode**: verify tests fail for the intended reason, not because setup is brittle.

---

## Flaky Patterns

- **Timing and state**: flag sleeps, timing races, test-order dependence, shared mutable state, hidden network calls, random data without seeds, timezone dependence, and reliance on local machine state.
- **Cleanup**: check cleanup for databases, queues, browser storage, temporary files, fake timers, event listeners, and global config.
- **Async behavior**: for retries and async workers, verify tests control time, retries, and queue state deterministically.

---

## CI And Maintenance

- **Wiring**: check whether new tests are wired into existing scripts and CI jobs.
- **Fixtures**: verify fixtures, factories, and helpers follow repository patterns.
- **Signal**: avoid broad low-signal tests that slow CI without proving the changed behavior.
