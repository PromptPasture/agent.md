# ClickHouse

---

## Core Rules

- ClickHouse is a columnar OLAP engine for append-only, high-throughput analytics. It's not a transactional database
- Choose the table engine carefully. `MergeTree` works for almost all production cases
- ClickHouse primary keys are sparse indexes (not uniqueness constraints). Design for query patterns, not data integrity
- Inserts batch server-side. Send large batches (≥ 1000 rows), not single rows
- Use parameterized queries (`{param:Type}`). Never interpolate user input

---

## Table Engines

| Engine | Use case |
| --- | --- |
| `MergeTree` | General-purpose OLAP; append-only |
| `ReplicatedMergeTree` | HA replication across nodes |
| `SummingMergeTree` | Pre-aggregate numeric columns on merge |
| `AggregatingMergeTree` | Store partial aggregation states |
| `ReplacingMergeTree` | Deduplicate rows by version on merge (eventual) |
| `CollapsingMergeTree` | Delete rows via sign column (-1/+1) |
| `Distributed` | Shard queries across a cluster |

For most use cases: `MergeTree` (single node) or `ReplicatedMergeTree` (cluster).

---

## Table Design

```sql
CREATE TABLE events
(
  id          UUID          DEFAULT generateUUIDv4(),
  user_id     UUID          NOT NULL,
  event_type  LowCardinality(String),   -- dictionary-encode low-cardinality strings
  payload     String,                   -- JSON stored as String
  occurred_at DateTime64(3, 'UTC')      -- millisecond precision, UTC
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(occurred_at)      -- monthly partitions
ORDER BY (user_id, occurred_at)         -- primary key = sparse index for queries
SETTINGS index_granularity = 8192;     -- default: 1 index entry per 8192 rows
```

### ORDER BY (Primary Key)

The `ORDER BY` clause defines the sort order within parts and is the sparse index:

- Put the most selective filter column first only if it is frequently used in `WHERE`
- For time-series data, put a low-cardinality dimension first (user_id, tenant_id), then time
- Do not put UUID in the primary key unless queries always filter on it — high-cardinality PK first reduces compression

### PARTITION BY

Partition by time for most workloads:

```sql
PARTITION BY toYYYYMM(occurred_at)    -- monthly (recommended for most)
PARTITION BY toYYYYMMDD(occurred_at)  -- daily (for high-volume, short-retention)
PARTITION BY toYear(occurred_at)      -- yearly (for low-volume, long-retention)
```

Avoid creating too many partitions — each partition adds overhead. Monthly is a safe default.

---

## Data Types

```sql
-- Use exact numeric types
UInt8, UInt16, UInt32, UInt64      -- unsigned integers (prefer over Int when always positive)
Int8, Int16, Int32, Int64
Float32, Float64                   -- avoid for money; use Decimal
Decimal(P, S)                      -- exact decimal: Decimal(19,4) for financial
String                             -- variable-length bytes (UTF-8 text or binary)
FixedString(N)                     -- fixed-width, padded with null bytes
LowCardinality(String)             -- dictionary encoding for < 10k distinct values
UUID                               -- 128-bit, stored efficiently
Date, Date32                       -- date only
DateTime, DateTime64(precision, tz) -- DateTime64(3, 'UTC') for milliseconds
Array(T)                           -- typed array
Nullable(T)                        -- avoid Nullable in ORDER BY columns — it disables sparse index
```

Avoid `Nullable` in `ORDER BY` columns — it prevents the sparse index from being used.

---

## Parameterized Queries

ClickHouse uses `{name:Type}` syntax for HTTP interface and client libraries:

```sql
SELECT id, user_id, event_type
FROM events
WHERE user_id = {user_id:UUID}
  AND occurred_at >= {since:DateTime}
  AND event_type = {type:String}
LIMIT {limit:UInt32};
```

In the Go client:

```go
rows, err := conn.Query(ctx,
    "SELECT id FROM events WHERE user_id = {user_id:UUID}",
    clickhouse.Named("user_id", userID),
)
```

---

## Inserts (Batching)

ClickHouse merges insert batches asynchronously. Insert single rows only in development:

```sql
-- Good: batch insert
INSERT INTO events (user_id, event_type, payload, occurred_at)
VALUES
  ('uuid1', 'click', '{}', now()),
  ('uuid2', 'view',  '{}', now()),
  -- ... thousands of rows
;
```

For high-throughput ingestion use the `Buffer` engine as an intermediate layer, or Kafka table engine:

```sql
CREATE TABLE events_buffer AS events
ENGINE = Buffer(
  currentDatabase(), events,
  16,          -- num_layers
  10, 100,     -- min_time, max_time (seconds)
  10000, 1000000, -- min_rows, max_rows
  10000000, 1000000000 -- min_bytes, max_bytes
);
```

---

## JSON Queries

ClickHouse stores JSON as `String` and provides extraction functions:

```sql
-- Extract scalar
SELECT JSONExtractString(payload, 'user_id') AS user_id FROM events;

-- Extract int
SELECT JSONExtractInt(payload, 'quantity') AS qty FROM orders;

-- Filter
SELECT * FROM events
WHERE JSONExtractString(payload, 'type') = 'click';

-- ClickHouse 22.6+: JSON type (experimental)
-- payload JSON   -- enables dot-notation access: payload.user_id
```

---

## Aggregation Patterns

```sql
-- uniqExact: exact distinct count (memory-intensive)
SELECT uniqExact(user_id) AS users FROM events WHERE toDate(occurred_at) = today();

-- uniq: approximate distinct count (HLL, much faster)
SELECT uniq(user_id) AS approx_users FROM events WHERE toDate(occurred_at) = today();

-- topK: most frequent values
SELECT topK(10)(event_type) AS top_events FROM events WHERE toDate(occurred_at) = today();

-- quantile: percentile (approximate)
SELECT quantile(0.95)(response_ms) AS p95 FROM requests WHERE toDate(created_at) = today();

-- Window function (ClickHouse 23.x+)
SELECT user_id, occurred_at,
  runningAccumulate(sumState(1)) OVER (PARTITION BY user_id ORDER BY occurred_at) AS row_num
FROM events;
```

---

## Materialized Views

ClickHouse materialized views are triggers — they run on insert, not on schedule:

```sql
-- Target table (AggregatingMergeTree for partial states)
CREATE TABLE daily_event_counts
(
  day        Date,
  event_type LowCardinality(String),
  count      AggregateFunction(count, UInt64)
)
ENGINE = AggregatingMergeTree()
ORDER BY (day, event_type);

-- Materialized view (inserts into target on each batch insert to events)
CREATE MATERIALIZED VIEW mv_daily_event_counts TO daily_event_counts AS
SELECT
  toDate(occurred_at) AS day,
  event_type,
  countState() AS count
FROM events
GROUP BY day, event_type;

-- Query: merge partial states
SELECT day, event_type, countMerge(count) AS total
FROM daily_event_counts
GROUP BY day, event_type
ORDER BY day DESC;
```

---

## Mutations (UPDATE / DELETE)

ClickHouse mutations are heavy asynchronous operations — they rewrite parts on disk. Use sparingly:

```sql
-- Async mutation (runs in background)
ALTER TABLE events DELETE WHERE occurred_at < now() - INTERVAL 1 YEAR;
ALTER TABLE events UPDATE status = 'archived' WHERE occurred_at < now() - INTERVAL 6 MONTH;

-- Check mutation status
SELECT * FROM system.mutations WHERE table = 'events' AND is_done = 0;
```

For soft deletes, use `CollapsingMergeTree` with a sign column instead of `DELETE`.

---

## What NOT to Do

- Do not use ClickHouse for OLTP workloads — no row-level locking, single-row inserts are slow
- Do not insert rows one by one — always batch (minimum 100–1000 rows per insert)
- Do not put high-cardinality columns (UUID, random string) at the start of `ORDER BY` unless queries always filter on them
- Do not use `Nullable` on `ORDER BY` columns — it breaks the sparse index
- Do not run frequent `UPDATE`/`DELETE` — mutations rewrite data and are expensive; design for append-only
- Do not skip `PARTITION BY` on tables that will hold months or years of data
