# BigQuery

---

## Core Rules

- BigQuery is a columnar, serverless OLAP engine — it is not a transactional database; do not use it as one
- Always specify column lists in `SELECT` — scanning unused columns costs money and time on a columnar engine
- Partition large tables by date or ingestion time — most queries filter on a time range
- Cluster tables on the columns most used in `WHERE` and `JOIN` conditions after partitioning
- Use parameterized queries (`@param`) — never string-interpolate user input into SQL

---

## Data Types Reference

```sql
-- BigQuery Standard SQL types
id          STRING        -- UUID stored as STRING; no native UUID type
user_id     STRING        NOT NULL
amount      NUMERIC       -- exact 29-digit decimal with 9 decimal places
amount_big  BIGNUMERIC    -- 76-digit decimal with 38 decimal places
flag        BOOL
payload     JSON          -- native JSON type (GA 2022)
-- or:
payload     STRING        -- JSON stored as STRING for older compatibility
tags        ARRAY<STRING>
address     STRUCT<street STRING, city STRING, country STRING>
created_at  TIMESTAMP     -- UTC, microsecond precision
event_date  DATE
```

---

## Parameterized Queries

BigQuery uses `@param` syntax:

```sql
SELECT id, email, name
FROM `project.dataset.users`
WHERE role = @role
  AND created_at >= @since
LIMIT @page_size;
```

In the client library:

```python
# Python (google-cloud-bigquery)
query = """
  SELECT id, email FROM `project.dataset.users`
  WHERE role = @role
"""
job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("role", "STRING", role_value),
    ]
)
client.query(query, job_config=job_config)
```

---

## Table Design

### Partitioning

Partition by a `DATE` or `TIMESTAMP` column, or by ingestion time. BigQuery prunes partitions automatically when the partition column is filtered:

```sql
CREATE TABLE `project.dataset.events`
(
  id         STRING    NOT NULL,
  user_id    STRING    NOT NULL,
  event_type STRING    NOT NULL,
  payload    JSON,
  occurred_at TIMESTAMP NOT NULL
)
PARTITION BY DATE(occurred_at)
OPTIONS (
  partition_expiration_days = 365,
  require_partition_filter = true   -- reject unfiltered full scans
);
```

Always include the partition column in `WHERE`:

```sql
-- Good: partition pruning applied
SELECT * FROM `project.dataset.events`
WHERE DATE(occurred_at) = '2024-06-21';

-- Bad: full table scan (rejected if require_partition_filter = true)
SELECT * FROM `project.dataset.events`
WHERE event_type = 'click';
```

### Clustering

Cluster on up to 4 columns to sort data within each partition block. Clustering reduces bytes scanned on high-cardinality filter columns:

```sql
CREATE TABLE `project.dataset.events`
(
  id          STRING    NOT NULL,
  user_id     STRING    NOT NULL,
  event_type  STRING    NOT NULL,
  occurred_at TIMESTAMP NOT NULL
)
PARTITION BY DATE(occurred_at)
CLUSTER BY user_id, event_type;
```

Good clustering columns: those used in `WHERE`, `JOIN ON`, or `GROUP BY` that are not the partition column.

---

## Query Patterns

### Always list columns

```sql
-- Bad: scans every column (expensive)
SELECT * FROM `project.dataset.orders`;

-- Good: only the needed columns are scanned
SELECT order_id, user_id, total_cents, created_at
FROM `project.dataset.orders`
WHERE DATE(created_at) = CURRENT_DATE();
```

### Avoid `SELECT DISTINCT` on large tables

`DISTINCT` forces a full shuffle across workers. Filter earlier or use `GROUP BY`:

```sql
-- Prefer GROUP BY over DISTINCT for aggregation context
SELECT user_id, COUNT(*) AS event_count
FROM `project.dataset.events`
WHERE DATE(occurred_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY user_id;
```

### Approximate aggregation

Use `APPROX_COUNT_DISTINCT` for cardinality estimates on billions of rows:

```sql
SELECT APPROX_COUNT_DISTINCT(user_id) AS approx_users
FROM `project.dataset.events`
WHERE DATE(occurred_at) >= '2024-06-01';
```

### Joining large tables

Put the larger table first (left side) in a JOIN — BigQuery's distributed join optimizer benefits from this ordering. Use `INNER JOIN` where possible — `LEFT JOIN` cannot be broadcast as efficiently.

```sql
SELECT e.user_id, u.email, COUNT(*) AS events
FROM `project.dataset.events` e    -- large table: left
JOIN `project.dataset.users` u     -- smaller dimension: right
  ON u.id = e.user_id
WHERE DATE(e.occurred_at) = '2024-06-21'
GROUP BY 1, 2;
```

---

## Arrays and Structs

```sql
-- Unnest an array column into rows
SELECT user_id, tag
FROM `project.dataset.posts`,
UNNEST(tags) AS tag;

-- Access struct fields
SELECT address.city, COUNT(*) AS count
FROM `project.dataset.users`
GROUP BY 1;

-- Build an array in a query
SELECT user_id, ARRAY_AGG(DISTINCT event_type) AS event_types
FROM `project.dataset.events`
GROUP BY user_id;
```

---

## JSON Support

```sql
-- Extract scalar (native JSON type, BigQuery 2022+)
SELECT JSON_VALUE(payload, '$.user_id') AS user_id FROM `project.dataset.events`;

-- Extract object
SELECT JSON_QUERY(payload, '$.address') AS address FROM `project.dataset.users`;

-- Unnest JSON array
SELECT user_id, item
FROM `project.dataset.orders`,
UNNEST(JSON_QUERY_ARRAY(payload, '$.items')) AS item;
```

---

## Materialized Views

```sql
CREATE MATERIALIZED VIEW `project.dataset.daily_revenue`
OPTIONS (enable_refresh = true, refresh_interval_minutes = 60)
AS
SELECT
  DATE(created_at) AS day,
  SUM(total_cents) AS total_cents,
  COUNT(*) AS order_count
FROM `project.dataset.orders`
WHERE status = 'paid'
GROUP BY 1;
```

Materialized views in BigQuery are refreshed automatically and serve cached results when the base table is unchanged — zero extra cost for frequently-run dashboards.

---

## Cost Control

- Use `require_partition_filter = true` on large tables to block accidental full scans
- Preview byte estimate in the BigQuery console before running expensive queries
- Use `CREATE TABLE … AS SELECT` for intermediate results rather than repeating subqueries in production jobs
- Set project-level and dataset-level `maxBytesBilled` query limit via the API/SDK

---

## What NOT to Do

- Do not use BigQuery as a transactional store — it has no row-level locking and DML (`INSERT`/`UPDATE`/`DELETE`) has quota limits
- Do not use `SELECT *` — scanning all columns multiplies cost on a columnar engine
- Do not skip partitioning on tables expected to exceed 1 GB — full scans become expensive
- Do not `JOIN` two large unpartitioned tables directly — pre-filter both sides before the join
- Do not store sensitive PII in BigQuery without column-level access controls (BigQuery column masking or authorized views)
