# PostgreSQL

---

## Core Rules

- Use `TIMESTAMPTZ` (not `TIMESTAMP`) — always store timezone-aware timestamps
- Use `TEXT` over `VARCHAR(n)` unless you need a hard length limit enforced at the DB level
- Use `JSONB` (not `JSON`) — it is stored binary, indexed, and queryable
- Use `gen_random_uuid()` for UUID generation (built-in since Postgres 13; use `pgcrypto` on older versions)
- Use `BIGINT GENERATED ALWAYS AS IDENTITY` or `UUID` for primary keys — avoid `SERIAL`

---

## Data Types Reference

```sql
-- Preferred types
id           UUID        PRIMARY KEY DEFAULT gen_random_uuid()
count        BIGINT      NOT NULL DEFAULT 0
amount       NUMERIC(19,4) NOT NULL
flag         BOOLEAN     NOT NULL DEFAULT false
payload      JSONB
tags         TEXT[]
created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
```

---

## UUID Generation

```sql
-- Postgres 13+ (built-in)
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- Postgres < 13 (requires pgcrypto extension)
CREATE EXTENSION IF NOT EXISTS pgcrypto;
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

---

## Indexes

```sql
-- B-tree (default, equality and range)
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Partial index (only index matching rows)
CREATE INDEX idx_orders_pending ON orders (created_at)
  WHERE status = 'pending';

-- Covering index (include extra columns to avoid heap fetch)
CREATE INDEX idx_orders_user_status ON orders (user_id, status)
  INCLUDE (total_cents, created_at);

-- GIN index for JSONB and array containment
CREATE INDEX idx_events_payload ON events USING GIN (payload);
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);

-- GiST index for full-text search (tsvector)
CREATE INDEX idx_posts_search ON posts USING GIN (to_tsvector('english', title || ' ' || body));

-- Non-blocking index build on live tables
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_id ON orders (user_id);
```

---

## Full-Text Search

```sql
-- Add a generated tsvector column for search
ALTER TABLE posts ADD COLUMN search_vector TSVECTOR
  GENERATED ALWAYS AS (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(body, ''))) STORED;

CREATE INDEX idx_posts_search ON posts USING GIN (search_vector);

-- Query
SELECT id, title
FROM posts
WHERE search_vector @@ plainto_tsquery('english', 'database migration');
```

---

## JSONB Queries

```sql
-- Extract a field
SELECT payload->>'user_id' AS user_id FROM events;

-- Filter by nested field
SELECT * FROM events WHERE payload->>'type' = 'click';

-- Containment query (uses GIN index)
SELECT * FROM events WHERE payload @> '{"source": "mobile"}';

-- Check key existence (uses GIN index)
SELECT * FROM events WHERE payload ? 'error_code';
```

---

## Common Table Expressions (CTEs)

```sql
-- Standard CTE
WITH active_users AS (
  SELECT id, email FROM users WHERE deleted_at IS NULL
),
recent_orders AS (
  SELECT user_id, COUNT(*) AS order_count
  FROM orders
  WHERE created_at > now() - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT u.email, o.order_count
FROM active_users u
JOIN recent_orders o ON o.user_id = u.id;
```

Use CTEs to name intermediate results — they are not always optimised as subqueries in older Postgres versions (prior to 12, CTEs were optimisation fences).

---

## Window Functions

```sql
SELECT
  user_id,
  amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY created_at)  AS running_total,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS row_num,
  LAG(amount, 1) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_amount
FROM orders;
```

---

## Upsert (INSERT … ON CONFLICT)

```sql
INSERT INTO users (id, email, name)
VALUES ($1, $2, $3)
ON CONFLICT (email) DO UPDATE
  SET name       = EXCLUDED.name,
      updated_at = now();

-- Ignore duplicates silently
INSERT INTO user_events (user_id, event_type)
VALUES ($1, $2)
ON CONFLICT DO NOTHING;
```

---

## Transactions and Savepoints

```sql
BEGIN;
  INSERT INTO orders (id, user_id, total_cents) VALUES ($1, $2, $3);

  SAVEPOINT after_order;
  INSERT INTO order_items (order_id, product_id, quantity) VALUES ($1, $4, $5);

  -- Roll back only the item insert if it fails
  ROLLBACK TO SAVEPOINT after_order;

COMMIT;
```

---

## Row-Level Security (Multi-tenancy)

```sql
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY projects_tenant_isolation ON projects
  USING (tenant_id = current_setting('app.tenant_id')::UUID);
```

Set the tenant context at the start of each DB session:

```pseudocode
db.exec("SET app.tenant_id = ?", tenantID)
```

---

## Partitioning

```sql
CREATE TABLE events (
  id          BIGINT      NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL,
  payload     JSONB
) PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2024_06
  PARTITION OF events
  FOR VALUES FROM ('2024-06-01') TO ('2024-07-01');

-- Indexes must be created on each partition or the parent (Postgres 11+)
CREATE INDEX ON events (occurred_at);
```

---

## Migrations (Postgres-specific)

```sql
-- Add column safely (nullable first)
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url TEXT;

-- Set default without rewriting the table (Postgres 11+, constant default)
ALTER TABLE users ALTER COLUMN role SET DEFAULT 'viewer';

-- Non-blocking index
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users (email);

-- Rename safely (expand-contract pattern — never direct rename on live table)
ALTER TABLE users ADD COLUMN display_name TEXT;
UPDATE users SET display_name = username;
-- (Deploy new code, verify, then drop old column in a subsequent migration)
ALTER TABLE users DROP COLUMN username;
```

---

## Connection Pooling

Postgres does not natively support connection multiplexing — use PgBouncer in transaction mode between the application and Postgres:

```
App → PgBouncer (transaction mode) → Postgres
```

Application pool settings (with PgBouncer):

- Max connections to PgBouncer: determined by your app instances × max_pool_size
- PgBouncer pool_size per database: 10–25 (tune under load)
- `server_idle_timeout`: 600 s
- `client_idle_timeout`: 0 (let the app manage)

---

## What NOT to Do

- Do not use `SERIAL` or `BIGSERIAL` for new tables — prefer `GENERATED ALWAYS AS IDENTITY`
- Do not use `JSON` — use `JSONB` for all JSON storage
- Do not use `TIMESTAMP` without timezone — use `TIMESTAMPTZ`
- Do not run `CREATE INDEX` (without `CONCURRENTLY`) on a live table with active writes — it takes a full table lock
- Do not use `SELECT *` in views or materialized views that other queries rely on — adding columns breaks them
