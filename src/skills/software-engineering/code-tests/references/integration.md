# Integration Testing Reference

Guidance for writing integration tests that verify service behaviour against real dependencies — databases, queues, caches, or downstream services.

---

## Scope Definition

Integration tests sit between unit tests and E2E tests. They:

- Spin up or connect to real infrastructure (DB, cache, queue)
- Test a service or repository boundary end-to-end, without going through HTTP
- Do not mock infrastructure — mock only third-party APIs outside your control

If the test mocks the database, it is a unit test. If it goes through an HTTP client to the service, it is an API test.

---

## Infrastructure Strategy

|Approach|When to use|
|---|---|
|Docker Compose (testcontainers)|Portable, CI-safe; preferred default|
|Shared dev DB (seeded schema)|Acceptable if CI has a dedicated DB instance|
|In-memory substitute (SQLite, H2)|Only when dialect differences are low-risk|

Use testcontainers when available in the project's language:

```typescript
// Node.js
import { PostgreSqlContainer } from '@testcontainers/postgresql';
const db = await new PostgreSqlContainer().start();
```

```go
// Go
container, _ := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{...})
```

---

## Test Plan Format

When drafting the test plan in Phase 2, describe the service boundary and dependencies:

```text
Target:       OrderService.createOrder()
Dependencies: PostgreSQL (real), PaymentService (stubbed — external)
State before: product catalogue seeded, user exists

Scenarios:
  Happy path
    Input:  CreateOrderInput{ userId, items }
    Assert: order persisted in DB with status "pending"
    Assert: inventory decremented for each item

  Insufficient stock
    Input:  item quantity exceeds available stock
    Assert: error returned, no order persisted, inventory unchanged

  Payment service unavailable
    Stub:   PaymentService.charge() throws NetworkError
    Assert: error returned, no partial state committed
```

---

## State Management

- Run each test in a transaction and roll it back on teardown when possible
- Alternatively, truncate only the tables touched by the test in teardown
- Never leave state that affects subsequent tests
- Seed the minimum data required — not a full production snapshot

```typescript
beforeEach(async () => { await db.beginTransaction(); });
afterEach(async () => { await db.rollbackTransaction(); });
```

---

## What to Mock

Mock only what you cannot control:

- Third-party HTTP APIs (payment processors, email providers, SMS gateways)
- Non-deterministic external clocks or random generators
- Services that would send real side effects (email, SMS, push notifications)

Do not mock:

- Your own database
- Your own cache (Redis)
- Your own message queue
- Internal services within the same repository

---

## Assertion Depth

Assert on persistent state, not just return values:

```typescript
const order = await orderService.createOrder(input);

// Assert return value
expect(order.id).toBeDefined();
expect(order.status).toBe('pending');

// Assert DB state
const dbOrder = await db.orders.findById(order.id);
expect(dbOrder).toMatchObject({ status: 'pending', userId: input.userId });

// Assert side effects
const inventory = await db.inventory.findByProductId(input.items[0].productId);
expect(inventory.reserved).toBe(input.items[0].quantity);
```

---

## P2 Checklist (Integration-specific)

- [ ] Real infrastructure used — no mocked DB, cache, or queue
- [ ] Each test cleans up its state (transaction rollback or targeted truncation)
- [ ] Only truly external third-party services are mocked
- [ ] Assertions cover both return values and persistent DB/queue state
- [ ] Container or DB connection lifecycle managed in global setup/teardown — not per test
- [ ] Tests can run in parallel without conflicting on shared rows (use isolated data per test)
