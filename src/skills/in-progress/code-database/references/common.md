# Common — Cross-Engine SQL Patterns

---

## Core Rules

- Always use parameterized queries — never interpolate user input into SQL strings
- List columns explicitly in `SELECT` — never use `SELECT *` in application code
- Apply `LIMIT` to every list query — never return an unbounded result set
- Wrap multi-step writes in a transaction — roll back on any error
- Every `NOT NULL` column should have a meaningful default or be required at the application layer

---

## Parameterized Queries

Different engines use different placeholder syntax — use the one that matches your driver:

```sql
-- PostgreSQL, CockroachDB (positional)
SELECT id, email FROM users WHERE email = $1

-- MySQL, SQLite, SQL Server (question mark)
SELECT id, email FROM users WHERE email = ?

-- Oracle, SQL Server (named)
SELECT id, email FROM users WHERE email = :email
```

Never do this:

```sql
-- NEVER: SQL injection vector
SELECT id FROM users WHERE email = '` + userInput + `'
```

---

## Indexes

Add an index whenever a column appears in `WHERE`, `JOIN ON`, or `ORDER BY` on a table expected to grow.

```sql
-- Single-column index (equality lookup)
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Composite index (equality + sort — column order matters)
CREATE INDEX idx_orders_user_status ON orders (user_id, status, created_at DESC);

-- Partial index (sparse condition — only indexes matching rows)
CREATE INDEX idx_orders_pending ON orders (created_at) WHERE status = 'pending';

-- Unique index (enforces uniqueness at the DB level)
CREATE UNIQUE INDEX idx_users_email ON users (email);
```

Index guidelines:

- Leading column of a composite index must match the most selective `WHERE` condition
- Cover columns used in `SELECT` (covering index) to avoid heap lookups on hot queries
- Do not index columns with very low cardinality (e.g., boolean, 2-value enum) on their own

---

## Pagination

### Offset pagination (simple, small datasets)

```sql
SELECT id, name, created_at
FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 40;
```

- Simple to implement and reason about
- Degrades at large offsets — the DB must skip rows it still reads

### Cursor pagination (scalable, large/growing datasets)

```sql
-- First page
SELECT id, name, created_at
FROM users
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Subsequent pages (cursor = last row's created_at + id)
SELECT id, name, created_at
FROM users
WHERE (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

- Consistent under concurrent writes — rows don't shift
- Requires a stable, unique sort key (add `id` as tiebreaker)

---

## Transactions

Wrap multi-step writes in a transaction. Roll back on any error:

```pseudocode
tx = db.begin()
try:
  tx.exec("INSERT INTO orders ...")
  tx.exec("UPDATE inventory SET quantity = quantity - 1 WHERE ...")
  tx.commit()
catch error:
  tx.rollback()
  raise error
```

Transaction guidelines:

- Keep transactions short — long transactions hold locks and block other writers
- Do not perform external calls (HTTP, queue publish) inside a transaction
- Use `READ COMMITTED` isolation unless the task requires stronger guarantees

---

## NULL Handling

- Treat NULL as "unknown", not as empty string or zero
- Comparisons with NULL always use `IS NULL` / `IS NOT NULL`, never `= NULL`
- Aggregates (`COUNT`, `SUM`, `AVG`) silently ignore NULLs — make this explicit in comments when it matters
- Use `COALESCE(col, default)` to substitute a fallback when NULL is possible

```sql
-- Wrong: always returns no rows (NULL != NULL)
WHERE deleted_at = NULL

-- Correct
WHERE deleted_at IS NULL
```

---

## Timestamps

- Always store timestamps in UTC at the DB level
- Use timezone-aware types (`TIMESTAMPTZ` in Postgres, `DATETIME(6)` in MySQL 8, `DATETIMEOFFSET` in SQL Server)
- Set `DEFAULT now()` / `DEFAULT CURRENT_TIMESTAMP` in the column definition — do not rely solely on application code
- Include `created_at` and `updated_at` on every table that tracks state changes

---

## Soft Deletes

When records must be retained for audit or recovery, add a `deleted_at` nullable timestamp instead of issuing `DELETE`.

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;

-- Filter deleted rows in all standard queries
SELECT ... FROM users WHERE deleted_at IS NULL;

-- Partial index keeps the active-row index lean
CREATE INDEX idx_users_active ON users (email) WHERE deleted_at IS NULL;
```

---

## N+1 Prevention

Load related records with a JOIN or a single IN-clause batch query — never in a loop:

```sql
-- Bad: one query per order
for order in orders:
  user = SELECT * FROM users WHERE id = order.user_id   -- N extra queries

-- Good: single JOIN
SELECT o.id, o.total, u.email, u.name
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE o.status = ?;

-- Good: batch fetch with IN
SELECT id, email, name FROM users WHERE id IN (?, ?, ?, ...);
```

---

## What NOT to Do

- Do not put business logic in triggers — they are invisible to application code and hard to test
- Do not use stored procedures for application logic — prefer the application layer for maintainability
- Do not return entire tables to the application for in-memory filtering — filter in the query
- Do not commit partial writes — wrap related inserts/updates in a transaction
