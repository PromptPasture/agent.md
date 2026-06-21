# API Testing Reference

Guidance for writing API tests that verify HTTP endpoints against their contracts (Supertest, httpx, REST Assured, `net/http/httptest`).

---

## Framework Detection

| Signal | Framework |
| --- | --- |
| `supertest` in deps | Supertest (Node.js) |
| `httpx` or `requests` in deps | httpx / requests (Python) |
| `rest-assured` in pom.xml | REST Assured (Java/Kotlin) |
| `net/http/httptest` import | Go stdlib httptest |
| `@nestjs/testing` in deps | NestJS testing module |

---

## Test Plan Format

When drafting the test plan in Phase 2, list each scenario with the full contract:

```text
Endpoint:  POST /api/v1/orders
Auth:      Bearer token (role: customer)

Scenarios:
  Happy path
    Request:  { items: [{ id: "abc", qty: 2 }] }
    Response: 201 { id: string, status: "pending", total: number }

  Validation failure
    Request:  { items: [] }
    Response: 400 { code: "VALIDATION_ERROR", fields: { items: ["required"] } }

  Conflict
    Request:  duplicate idempotency key
    Response: 200, original order body returned

  Unauthenticated
    Auth:     none
    Response: 401 { code: "UNAUTHORIZED" }
```

---

## Assertion Depth

Assert on the full observable contract, not just status codes:

```typescript
const res = await request(app)
  .post('/api/v1/orders')
  .set('Authorization', `Bearer ${token}`)
  .send({ items: [{ id: 'abc', qty: 2 }] });

expect(res.status).toBe(201);
expect(res.body).toMatchObject({
  id: expect.any(String),
  status: 'pending',
  total: expect.any(Number),
});
expect(res.headers['content-type']).toMatch(/application\/json/);
```

- Always assert response body shape, not just presence
- Assert Content-Type header
- Assert error body shape on failure responses — not just status code
- For 4xx/5xx: assert `code` field matches the contract

---

## Auth Setup

- Generate tokens programmatically in test setup — do not hardcode
- Use a dedicated test user seeded in the DB or a mock auth service
- Test both authenticated and unauthenticated paths for every protected endpoint
- Test role boundaries: a lower-privilege token must not access higher-privilege routes

---

## State Setup and Teardown

- Seed required DB state before the test, clean up after
- Use transactions that are rolled back on teardown when the framework supports it
- Do not rely on state left by a previous test

---

## Contract Validation

For endpoints with a published OpenAPI spec, validate responses against the schema:

```typescript
import { validateResponse } from './helpers/openapi';
expect(validateResponse('/api/v1/orders', 'POST', 201, res.body)).toPass();
```

---

## P2 Checklist (API-specific)

- [ ] Every scenario asserts on response body shape, not just status code
- [ ] Error responses assert on `code` or `message` field shape
- [ ] Content-Type header asserted on all responses
- [ ] Auth tested: valid token, missing token, wrong role
- [ ] DB state seeded before each test and cleaned up after
- [ ] No hardcoded tokens or credentials — loaded from env or fixture
