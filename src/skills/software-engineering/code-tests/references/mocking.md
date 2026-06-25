# Mocking Reference

Guidance for deciding when to mock and how to keep mocks trustworthy.

---

## The Core Rule

Mock only what you cannot control and cannot afford to call in tests:

|Dependency|Mock?|
|---|---|
|Your own DB|No — use a real test DB or testcontainers|
|Your own cache (Redis)|No — use a real instance or testcontainers|
|Your own internal service (same repo)|No — test through the real code path|
|Third-party payment processor|Yes — side effects are real and irreversible|
|Email / SMS / push notification provider|Yes — would send real messages|
|External analytics or logging API|Yes — flaky, rate-limited, irrelevant to test logic|
|System clock / `Date.now()`|Yes — makes tests deterministic|
|File system (when not the subject under test)|Situational — prefer temp dirs over mocks|

---

## Mock Fidelity

A mock that does not reflect the real contract hides failures:

- Mock the **interface**, not the **implementation** — return realistic shapes, not simplified ones
- Include realistic error responses, not just happy-path returns
- If the real dependency returns a paginated response, the mock must too
- Keep mocks updated when the real contract changes

```typescript
// Bad — oversimplified mock hides real shape
jest.spyOn(paymentService, 'charge').mockResolvedValue({ success: true });

// Good — mock reflects the real contract
jest.spyOn(paymentService, 'charge').mockResolvedValue({
  transactionId: 'txn_abc123',
  status: 'captured',
  amount: 9999,
  currency: 'USD',
  capturedAt: new Date().toISOString(),
});
```

---

## Stub vs Mock vs Spy

|Type|What it does|When to use|
|---|---|---|
|Stub|Returns a fixed value; no verification|Providing test data to the subject|
|Mock|Returns a value AND verifies it was called correctly|Verifying a side effect occurred|
|Spy|Wraps the real implementation; records calls|Verifying call count or args without replacing behaviour|

Do not use mocks to verify that a method was called if the observable outcome (DB state, return value, response body) already proves it.

---

## HTTP Mocking

For external HTTP APIs, use an interceptor rather than mocking the service class:

```typescript
// Node.js — nock
import nock from 'nock';

nock('https://api.stripe.com')
  .post('/v1/charges')
  .reply(200, { id: 'ch_123', status: 'succeeded', amount: 9999 });
```

```python
# Python — responses
import responses

@responses.activate
def test_charge():
    responses.add(responses.POST, 'https://api.stripe.com/v1/charges',
                  json={'id': 'ch_123', 'status': 'succeeded'}, status=200)
```

Interceptors test the HTTP client code as well, whereas mocking the service class skips it entirely.

---

## Teardown

- Reset all mocks after each test to prevent bleed-through
- Use `afterEach(() => jest.restoreAllMocks())` or equivalent
- Verify no unexpected mock calls remain at the end of a test when using strict mocking

---

## Contract Testing

When a mock is used long-term, consider a contract test to keep the mock honest:

- Consumer-driven contract tests (Pact) verify that the real provider still matches what the mock returns
- Run contract tests in CI against a staging or sandbox environment of the real provider
