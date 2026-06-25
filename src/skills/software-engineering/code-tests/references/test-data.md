# Test Data Reference

Guidance for creating, managing, and cleaning up test data across all test types.

---

## Principles

- **Minimal**: create only what the test requires; no full production snapshots
- **Isolated**: each test owns its data; no cross-test dependencies
- **Realistic**: values should be valid and representative, not `"test"` or `123`
- **Deterministic**: no random values without a seeded generator; tests must be reproducible

---

## Factories

Use factory functions to construct test objects. Factories set sensible defaults and accept overrides:

```typescript
// TypeScript
function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: crypto.randomUUID(),
    email: `user+${Date.now()}@example.com`,
    name: 'Test User',
    role: 'viewer',
    createdAt: new Date(),
    ...overrides,
  };
}

const admin = makeUser({ role: 'admin' });
const banned = makeUser({ status: 'banned' });
```

```python
# Python
def make_user(**overrides) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "email": f"user+{int(time.time())}@example.com",
        "name": "Test User",
        "role": "viewer",
        **overrides,
    }
```

- One factory per domain entity
- Factories live in `tests/factories/` or `tests/helpers/factories/`
- Factories do not persist to the DB — call a separate `createUser(db, makeUser())` helper for that

---

## DB Seed Helpers

Separate factory construction from DB insertion:

```typescript
async function createUser(db: DB, overrides: Partial<User> = {}): Promise<User> {
  const user = makeUser(overrides);
  await db.users.insert(user);
  return user;
}
```

- Returns the created entity so tests can reference its ID
- Accepts overrides to avoid fixture proliferation
- Teardown: either delete by ID in `afterEach`, or use transaction rollback

---

## Fixture Files

Use static fixture files for:

- Complex nested structures that are hard to express in a factory
- Canonical examples from a spec or contract (e.g., an OpenAPI response example)
- Binary blobs (images, PDFs) used in upload tests

Keep fixture files small and named after the scenario, not the data type:

```text
tests/fixtures/
  orders/
    valid-order.json
    oversized-order.json
  uploads/
    sample-receipt.pdf
```

---

## Parameterised Data for Load Tests

For load tests, use CSV or generated data to avoid cache hits:

```javascript
// k6
import { SharedArray } from 'k6/data';
const queries = new SharedArray('queries', () => open('./data/search-queries.csv').split('\n'));

export default function () {
  const query = queries[Math.floor(Math.random() * queries.length)];
  http.get(`${__ENV.BASE_URL}/search?q=${encodeURIComponent(query)}`);
}
```

---

## Avoiding Common Pitfalls

|Pitfall|Fix|
|---|---|
|Hardcoded IDs (`userId: "123"`)|Use factory-generated or DB-returned IDs|
|Shared fixture mutated between tests|Deep-clone fixtures before each test|
|Relying on insertion order for IDs|Query by a unique business key, not by auto-increment ID|
|Large seed scripts run before every test|Seed once in global setup; use transactions per test|
|Real email addresses or phone numbers|Use `@example.com` domains and `+15550000000` numbers|
