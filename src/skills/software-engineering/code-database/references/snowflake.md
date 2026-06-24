# Snowflake

---

## Core Rules

- Snowflake separates compute (virtual warehouses) from storage — suspend warehouses when not in use to stop billing
- Use `TIMESTAMP_TZ` for all timestamps — it stores timezone offset alongside the value
- Use clustering keys on large tables queried by range or high-cardinality filter columns
- Use parameterized queries (`:param` or `%(name)s` depending on the connector) — never string-interpolate user input
- Prefer `VARIANT` for semi-structured data (JSON, Avro, Parquet) — Snowflake indexes VARIANT columns automatically

---

## Data Types Reference

```sql
id          VARCHAR(36)      -- UUID as string; or use UUID_STRING() to generate
user_id     VARCHAR(36)      NOT NULL
name        VARCHAR(255)     NOT NULL
status      VARCHAR(50)      NOT NULL DEFAULT 'pending'
amount      NUMBER(19,4)     NOT NULL DEFAULT 0
flag        BOOLEAN          NOT NULL DEFAULT FALSE
payload     VARIANT          -- semi-structured JSON / Avro / Parquet
tags        ARRAY            -- Snowflake ARRAY (semi-structured)
created_at  TIMESTAMP_TZ(9)  NOT NULL DEFAULT CURRENT_TIMESTAMP()
updated_at  TIMESTAMP_TZ(9)  NOT NULL DEFAULT CURRENT_TIMESTAMP()
```

---

## Table Design

### Clustering Keys

Snowflake stores data in micro-partitions (approximately 50–500 MB compressed). Natural clustering happens in insertion order. Define a clustering key when queries consistently filter on a column that is not the insertion-order column:

```sql
CREATE TABLE events (
  id          VARCHAR(36)     NOT NULL,
  user_id     VARCHAR(36)     NOT NULL,
  event_type  VARCHAR(100)    NOT NULL,
  payload     VARIANT,
  occurred_at TIMESTAMP_TZ(9) NOT NULL
)
CLUSTER BY (DATE(occurred_at), event_type);
```

Clustering key guidelines:

- Choose 1–3 columns that appear together in `WHERE` filters
- Cardinality should be high enough to create meaningful partitioning (date, user segment)
- Avoid clustering keys on very low-cardinality columns (boolean, 2-value status)
- Monitor with `SYSTEM$CLUSTERING_INFORMATION` and recluster with `ALTER TABLE … RECLUSTER`

### Transient and Temporary Tables

```sql
-- Transient table: no Fail-safe (saves storage cost for staging data)
CREATE TRANSIENT TABLE staging.raw_events (
  id      VARCHAR(36),
  payload VARIANT,
  loaded_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP()
);

-- Temporary table: session-scoped, auto-dropped
CREATE TEMPORARY TABLE temp_user_segment AS
SELECT user_id, segment FROM users WHERE active = TRUE;
```

---

## Semi-Structured Data (VARIANT)

Snowflake natively ingests JSON, Avro, and Parquet into `VARIANT` columns. Querying uses `:` notation for path traversal:

```sql
-- Extract a field (returns VARIANT)
SELECT payload:user_id::STRING AS user_id FROM events;

-- Nested field
SELECT payload:address:city::STRING AS city FROM users;

-- Array element
SELECT payload:items[0]:product_id::STRING AS first_product FROM orders;

-- Filter on semi-structured field
SELECT * FROM events
WHERE payload:event_type::STRING = 'click';

-- Flatten an array into rows
SELECT
  e.id,
  f.value:product_id::STRING AS product_id,
  f.value:quantity::INT AS quantity
FROM orders e,
LATERAL FLATTEN(input => e.payload:items) f;
```

---

## Parameterized Queries

Snowflake connector for Python uses `%(name)s` or `%s` placeholders:

```python
# Python (snowflake-connector-python)
cursor.execute(
    "SELECT id, email FROM users WHERE role = %(role)s AND created_at >= %(since)s",
    {"role": role_value, "since": since_value}
)
```

Snowpark (DataFrame API) handles parameterization automatically — use it for complex transformations.

---

## Virtual Warehouses

```sql
-- Create a warehouse for ETL (separate from analytics queries)
CREATE WAREHOUSE etl_wh
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60        -- suspend after 60 s of inactivity
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- Use a specific warehouse for a session
USE WAREHOUSE etl_wh;
```

Warehouse sizing guidance:

| Workload | Starting size |
| --- | --- |
| Simple queries, dashboards | X-SMALL or SMALL |
| Complex analytics, large joins | MEDIUM or LARGE |
| Heavy ETL, data loading | LARGE or X-LARGE |
| ML feature engineering | X-LARGE or 2X-LARGE |

Scale up for a single large query; scale out (multi-cluster) for many concurrent users.

---

## Data Loading

```sql
-- Stage an S3 file
CREATE STAGE my_stage
  URL = 's3://my-bucket/data/'
  CREDENTIALS = (AWS_ROLE = 'arn:aws:iam::123:role/snowflake');

-- Load from stage into table
COPY INTO events
FROM @my_stage/events/
FILE_FORMAT = (TYPE = 'PARQUET')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
ON_ERROR = 'CONTINUE';

-- Check load history
SELECT * FROM information_schema.load_history
WHERE table_name = 'EVENTS'
ORDER BY last_load_time DESC
LIMIT 10;
```

---

## Transactions

Snowflake supports multi-statement transactions:

```sql
BEGIN;
  INSERT INTO orders (id, user_id, total_cents) VALUES (:id, :user_id, :total);
  UPDATE inventory SET quantity = quantity - :qty WHERE product_id = :product_id;
COMMIT;

-- On error:
ROLLBACK;
```

Snowflake's default isolation level is `READ COMMITTED`. DML operations are atomic per statement even without an explicit transaction.

---

## Time Travel and Fail-Safe

Snowflake retains historical data for querying (Time Travel) and disaster recovery (Fail-Safe):

```sql
-- Query data as of a past timestamp
SELECT * FROM orders AT (TIMESTAMP => '2024-06-20 00:00:00'::TIMESTAMP_TZ);

-- Query data before a specific statement
SELECT * FROM orders BEFORE (STATEMENT => '8e5d0ca9-005e-44e6-b858-a8f5b37c5726');

-- Restore a dropped table (within data_retention_time_in_days)
UNDROP TABLE orders;
```

Set retention period (default 1 day, max 90 days on Enterprise):

```sql
ALTER TABLE orders SET DATA_RETENTION_TIME_IN_DAYS = 7;
```

---

## Migrations (Snowflake-specific)

Snowflake DDL is mostly online — most `ALTER TABLE` operations do not lock the table:

```sql
-- Add column (instant)
ALTER TABLE users ADD COLUMN avatar_url VARCHAR(2048);

-- Set default on existing column
ALTER TABLE users ALTER COLUMN role SET DEFAULT 'viewer';

-- Drop column (instant in Snowflake)
ALTER TABLE users DROP COLUMN legacy_token;

-- Rename column (Snowflake 2023+)
ALTER TABLE users RENAME COLUMN username TO display_name;

-- Idempotent DDL
CREATE TABLE IF NOT EXISTS users (...);
CREATE OR REPLACE TABLE staging.raw_events (...);   -- for staging tables
```

---

## What NOT to Do

- Do not leave virtual warehouses running without `AUTO_SUSPEND` — idle warehouses bill per second
- Do not use `SELECT *` on VARIANT-heavy tables — Snowflake must parse all VARIANT paths
- Do not run large queries on X-SMALL warehouses — scale the warehouse size to the query, then suspend
- Do not store sensitive PII without column masking policies (`CREATE MASKING POLICY`)
- Do not use Snowflake as a low-latency OLTP store — query latency floors at ~1–2 s due to warehouse startup and micro-partition scanning
