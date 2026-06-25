# CockroachDB

---

## Core Rules

- CockroachDB is PostgreSQL-compatible and distributed. Most Postgres patterns apply, with differences in primary key design and transactions
- Use UUID v4 as primary key with `gen_random_uuid()`. Sequential integers cause write hotspots on the range leader
- Serializable isolation is default. Don't lower it without understanding the trade-offs
- Handle `40001` (serialization failure) errors with exponential backoff. They're expected under contention
- Co-locate related data using interleave or locality optimizations in multi-region setups

---

## Data Types Reference

CockroachDB uses PostgreSQL syntax:

```sql
id          UUID           PRIMARY KEY DEFAULT gen_random_uuid()
user_id     UUID           NOT NULL
email       STRING         NOT NULL      -- STRING is an alias for TEXT in CRDB
name        STRING         NOT NULL
status      STRING         NOT NULL DEFAULT 'pending'
amount      DECIMAL(19,4)  NOT NULL DEFAULT 0
flag        BOOL           NOT NULL DEFAULT false
payload     JSONB                        -- same as Postgres JSONB
tags        STRING[]
created_at  TIMESTAMPTZ    NOT NULL DEFAULT now()
updated_at  TIMESTAMPTZ    NOT NULL DEFAULT now()
```

---

## Primary Key Design (Hotspot Prevention)

In CockroachDB, data is range-partitioned and distributed across nodes by primary key order. Sequential integer PKs (`SERIAL`, `SEQUENCE`) concentrate inserts on one range leader, creating a write hotspot.

Use UUID instead:

```sql
-- Good: random UUID distributes writes across ranges
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- Acceptable: hash-sharded index for high-throughput sequential workloads
CREATE TABLE events (
  id         INT8       DEFAULT unique_rowid() PRIMARY KEY,
  user_id    UUID       NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
) WITH (sql_defaults_explicit_timestamp = true);

-- Better: hash-sharded PK (CRDB 20.2+)
CREATE TABLE events (
  id         INT8        DEFAULT unique_rowid(),
  user_id    UUID        NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (id) USING HASH WITH (bucket_count = 8)
);
```

---

## Indexes

CockroachDB index syntax follows PostgreSQL with one addition — hash-sharded indexes:

```sql
-- Standard B-tree
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Unique
CREATE UNIQUE INDEX uq_users_email ON users (email);

-- Covering index (STORING)
CREATE INDEX idx_orders_user_status ON orders (user_id, status) STORING (total_cents, created_at);

-- Partial index
CREATE INDEX idx_orders_pending ON orders (created_at) WHERE status = 'pending';

-- Hash-sharded index (prevent hotspot on monotonically increasing column)
CREATE INDEX idx_events_created ON events (created_at) USING HASH WITH (bucket_count = 8);

-- Non-blocking index build (CRDB 22.1+)
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders (user_id);
```

---

## Transactions and Serialization Retries

CockroachDB uses Serializable isolation by default. Under contention, transactions may fail with `SQLSTATE 40001` (serialization failure). The application must retry:

```pseudocode
MAX_RETRIES = 5
BACKOFF_BASE = 100ms

function runWithRetry(txnFn):
  for attempt in 1..MAX_RETRIES:
    tx = db.begin()
    try:
      txnFn(tx)
      tx.commit()
      return
    catch err if err.code == "40001":
      tx.rollback()
      sleep(BACKOFF_BASE * 2^attempt + jitter())
    catch err:
      tx.rollback()
      raise err
  raise MaxRetriesExceeded
```

CockroachDB also supports automatic client-side retry using `SAVEPOINT cockroach_restart`:

```sql
BEGIN;
SAVEPOINT cockroach_restart;
-- ... DML statements ...
RELEASE SAVEPOINT cockroach_restart;
COMMIT;

-- On serialization error:
ROLLBACK TO SAVEPOINT cockroach_restart;
-- retry DML statements
RELEASE SAVEPOINT cockroach_restart;
COMMIT;
```

---

## Multi-Region Deployments

```sql
-- Set database locality (survivability goal)
ALTER DATABASE myapp SET PRIMARY REGION 'us-east1';
ALTER DATABASE myapp ADD REGION 'eu-west1';
ALTER DATABASE myapp SURVIVE ZONE FAILURE;  -- or REGION FAILURE

-- Global table: reads served locally in every region (low-latency reads, higher write latency)
ALTER TABLE reference_data SET LOCALITY GLOBAL;

-- Regional-by-row: each row is pinned to a region via a crdb_region column
ALTER TABLE users SET LOCALITY REGIONAL BY ROW;
-- CockroachDB adds crdb_region column automatically; set it on insert:
INSERT INTO users (crdb_region, id, email) VALUES ('us-east1', gen_random_uuid(), 'a@b.com');
```

---

## JSON (JSONB)

CockroachDB supports the same JSONB operators as PostgreSQL:

```sql
-- Extract
SELECT payload->>'user_id' AS user_id FROM events;

-- Filter (uses GIN index)
SELECT * FROM events WHERE payload->>'type' = 'click';

-- Containment
SELECT * FROM events WHERE payload @> '{"source": "mobile"}';

-- GIN index
CREATE INVERTED INDEX idx_events_payload ON events (payload);
```

---

## Upsert

```sql
-- INSERT … ON CONFLICT (PostgreSQL-compatible)
INSERT INTO users (id, email, name)
VALUES ($1, $2, $3)
ON CONFLICT (email) DO UPDATE
  SET name       = EXCLUDED.name,
      updated_at = now();

-- CockroachDB UPSERT shorthand (updates all non-PK columns on conflict)
UPSERT INTO users (id, email, name)
VALUES ($1, $2, $3);
```

---

## Migrations (CockroachDB-specific)

Most PostgreSQL migration patterns apply. Key differences:

```sql
-- Add nullable column (online — no table lock)
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url STRING;

-- Add NOT NULL column: must provide a default (CRDB backfills existing rows)
ALTER TABLE users ADD COLUMN IF NOT EXISTS role STRING NOT NULL DEFAULT 'viewer';

-- Non-blocking index (CRDB 22.1+)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_id ON orders (user_id);

-- Column backfill is automatic and online in CockroachDB — no manual batching needed
-- for ADD COLUMN with DEFAULT on large tables
```

CockroachDB performs schema changes online — most DDL does not block reads or writes.

---

## Observability

```sql
-- Active queries
SELECT query, start, application_name
FROM crdb_internal.cluster_queries
WHERE start < now() - INTERVAL '30s';

-- Statement statistics
SELECT statement, mean_latency_seconds, execution_count
FROM crdb_internal.statement_statistics
ORDER BY mean_latency_seconds DESC
LIMIT 20;

-- Range distribution (check for hotspots)
SELECT range_id, start_pretty, end_pretty, replicas
FROM crdb_internal.ranges
WHERE table_name = 'orders';
```

---

## Connection Pooling

CockroachDB recommends **PgBouncer in session mode** (not transaction mode) due to the use of prepared statements and the `SAVEPOINT cockroach_restart` pattern.

Recommended settings:

|Setting|Value|
|---|---|
|Pool mode|Session|
|Max pool size|4 × num_cores per node (start)|
|`server_idle_timeout`|600 s|
|Application max connections|Tune to < 4× node count|

CockroachDB Serverless manages connection pooling automatically.

---

## What NOT to Do

- Do not use `SERIAL` or sequential integer PKs on high-write tables — they create range hotspots
- Do not ignore `40001` serialization errors — they must be retried with backoff
- Do not lower transaction isolation to `READ COMMITTED` without understanding that it breaks serializability guarantees
- Do not run `CREATE INDEX` (without `CONCURRENTLY`) in production — it takes a schema change lock
- Do not use `SELECT *` in interleaved or multi-region table joins — column projection reduces cross-region data movement
