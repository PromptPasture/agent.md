# Backend Performance

---

## Core Rules

- Measure before optimising — profile first, don't guess
- No N+1 queries — join or batch-load related data
- No unbounded queries — always apply LIMIT; paginate where the result set can grow
- No synchronous blocking in hot paths — offload to workers or use async where the stack supports it

---

## Query Performance

### N+1 Detection and Fix

An N+1 occurs when a loop triggers a query per iteration. Always identify the root query and either join or batch-load.

```pseudocode
-- Bad: N+1 — one extra query per order
for each order in orders:
  order.user = repo.getUser(order.userID)
```

```sql
-- Good: single JOIN
SELECT orders.id, orders.total, orders.status,
       users.id AS user_id, users.email, users.name
FROM orders
JOIN users ON users.id = orders.user_id
WHERE orders.status = ?
```

### Index Strategy

Add an index whenever a column appears in a `WHERE`, `ORDER BY`, or `JOIN ON` clause on a table that will grow.

```sql
-- Single-column index for equality lookups
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Composite index for equality + sort
CREATE INDEX idx_orders_user_status ON orders (user_id, status, created_at DESC);

-- Partial index for sparse queries
CREATE INDEX idx_orders_pending ON orders (created_at) WHERE status = 'pending';
```

Note missing indexes in migration comments when adding them would be too expensive in a single migration.

### Pagination

Always paginate list endpoints. Choose the pattern based on access pattern:

```sql
-- Offset pagination (admin tools, small datasets)
SELECT ... FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?

-- Cursor pagination (feeds, large/growing datasets)
SELECT ... FROM orders WHERE user_id = ? AND created_at < ? ORDER BY created_at DESC LIMIT ?
```

Cursor pagination avoids the row-skip cost of large offsets and stays consistent under concurrent writes.

---

## Caching

Cache results that are expensive to compute and change infrequently. Cache at the service layer, not the handler.

```pseudocode
function getProduct(id):
  cacheKey = "product:" + id
  cached = cache.get(cacheKey)
  if cached is found:
    return cached

  product = repo.getProduct(id)
  cache.set(cacheKey, product, ttl: 5 minutes)
  return product
```

Cache invalidation: invalidate on write, not on a timer alone. Use short TTLs (< 5 min) for user-visible data.

Never cache:

- Auth tokens or sessions (use a dedicated session store)
- Sensitive PII
- Data that must be strongly consistent

---

## Connection Pooling

Reuse connections — do not open a new connection per request. Configure the pool explicitly:

| Setting | Recommended starting value |
| --- | --- |
| Max open connections | 10–25 (tune under load) |
| Max idle connections | Half of max open |
| Connection max lifetime | 5–30 minutes |
| Connection max idle time | 5 minutes |

Apply the same principle to HTTP clients used for outbound calls — reuse a shared client with a connection pool rather than creating one per request.

---

## Concurrency

Use parallel execution for independent work that does not depend on each other:

```pseudocode
// Run independent lookups in parallel
[user, prefs] = await parallel(
  userRepo.get(id),
  prefsRepo.get(id)
)
```

Limit concurrency explicitly — do not spawn unlimited parallel tasks. Use a semaphore or worker pool with a fixed size, tuned to the DB connection pool and downstream rate limits.

---

## Timeouts

Set timeouts on every external call. Never leave a call with no timeout.

```pseudocode
// Wrap every external call with a timeout
result = withTimeout(5 seconds):
  httpClient.get(url)
```

| Call type | Recommended timeout |
| --- | --- |
| DB query (simple) | 3–5 s |
| DB query (complex/report) | 30–60 s |
| Outbound HTTP (user-facing) | 5–10 s |
| Outbound HTTP (background) | 30–60 s |
| Queue publish | 5 s |

---

## Response Size

- Never return more fields than the client needs — shape the response to the use case
- Stream large responses rather than buffering them in memory
- Compress responses ≥ 1 KB with gzip/brotli via middleware — do not compress per-handler

---

## Profiling

When a performance issue is suspected:

1. Add a tracing span around the suspected operation
2. Check the slow query log (`log_min_duration_statement` in PostgreSQL; slow query log in MySQL)
3. Use `EXPLAIN ANALYZE` on the slow query
4. Profile the process with the language's profiling tool only if the query is fast but the handler is slow

Do not add caching or indexes speculatively — measure first.
