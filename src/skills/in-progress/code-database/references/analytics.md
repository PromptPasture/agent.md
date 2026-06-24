# Analytics — OLAP and Reporting Patterns

---

## Core Rules

- Run analytical queries against OLAP engines or read replicas, not the primary OLTP replica
- Partition large tables by time. Most analytical queries filter on date ranges
- Pre-aggregate where possible. Materialised views or summary tables beat repeated full scans
- Avoid row-by-row processing. Set-based operations are orders of magnitude faster at scale

---

## OLTP vs OLAP

| Concern | OLTP | OLAP |
| --- | --- | --- |
| Query type | Point lookups, small updates | Full scans, aggregations, joins |
| Row volume per query | 1–100 | Millions to billions |
| Indexes | Many, narrow | Few, wide (columnar) |
| Write pattern | Frequent, small | Batch / append-only |
| Schema style | Normalised (3NF) | Denormalised (star / snowflake) |
| Engine examples | Postgres, MySQL, SQL Server | BigQuery, Snowflake, ClickHouse, Redshift |

Route analytical workloads to a dedicated OLAP engine or read replica. Don't run full-table aggregations on the primary OLTP database.

---

## Partitioning

Partition large fact tables by the column most queries filter on (usually a date):

```sql
-- Postgres: range partitioning by month
CREATE TABLE events (
  id         BIGINT      NOT NULL,
  user_id    UUID        NOT NULL,
  event_type TEXT        NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL,
  payload    JSONB
) PARTITION BY RANGE (occurred_at);

CREATE TABLE events_2024_01
  PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE events_2024_02
  PARTITION OF events
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```

Partition pruning: include the partition key in every `WHERE` clause so the planner skips irrelevant partitions.

---

## Star Schema

Design analytical schemas around fact tables and dimension tables:

```sql
-- Fact table: append-only, high volume
CREATE TABLE fact_orders (
  order_id    BIGINT      NOT NULL,
  user_key    INT         NOT NULL REFERENCES dim_users(user_key),
  product_key INT         NOT NULL REFERENCES dim_products(product_key),
  date_key    INT         NOT NULL REFERENCES dim_date(date_key),
  quantity    INT         NOT NULL,
  revenue_usd NUMERIC(12,2) NOT NULL
);

-- Dimension table: slowly changing, low volume
CREATE TABLE dim_users (
  user_key    INT         PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id     UUID        NOT NULL UNIQUE,   -- natural key from OLTP
  email       TEXT        NOT NULL,
  name        TEXT        NOT NULL,
  valid_from  DATE        NOT NULL,
  valid_to    DATE,       -- NULL = current record
  is_current  BOOLEAN     NOT NULL DEFAULT true
);
```

---

## Aggregation Patterns

### Window functions (avoid self-joins)

```sql
-- Running total per user
SELECT
  user_id,
  order_date,
  amount,
  SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS running_total
FROM orders;

-- Rank within group
SELECT
  product_id,
  category,
  revenue,
  RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category
FROM product_revenue;

-- Month-over-month change
SELECT
  month,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY month) AS prev_month,
  revenue - LAG(revenue, 1) OVER (ORDER BY month) AS change
FROM monthly_revenue;
```

### Grouping sets (multiple rollup levels in one query)

```sql
SELECT region, product, SUM(revenue)
FROM sales
GROUP BY GROUPING SETS (
  (region, product),   -- detail
  (region),            -- subtotal by region
  (product),           -- subtotal by product
  ()                   -- grand total
);
```

---

## Materialised Views

Pre-compute expensive aggregations and refresh on a schedule:

```sql
-- Postgres
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT
  date_trunc('day', created_at) AS day,
  SUM(amount_cents) AS total_cents,
  COUNT(*) AS order_count
FROM orders
WHERE status = 'paid'
GROUP BY 1;

CREATE UNIQUE INDEX ON daily_revenue (day);

-- Refresh (run via cron or trigger)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;
```

Use `CONCURRENTLY` so reads are not blocked during refresh. Requires a unique index.

---

## Query Optimisation for Analytics

### Filter early, aggregate late

```sql
-- Bad: aggregate everything, then filter
SELECT user_id, SUM(amount) AS total
FROM orders
GROUP BY user_id
HAVING user_id = ?;

-- Good: filter first, then aggregate
SELECT user_id, SUM(amount) AS total
FROM orders
WHERE user_id = ?
GROUP BY user_id;
```

### Avoid `COUNT(DISTINCT ...)` on large tables

`COUNT(DISTINCT col)` is expensive — it requires deduplication before counting. Use HyperLogLog approximations for cardinality estimates at scale:

```sql
-- Postgres: exact (expensive at scale)
SELECT COUNT(DISTINCT user_id) FROM events;

-- Postgres with pg_hll extension: approximate (fast)
SELECT hll_cardinality(hll_add_agg(hll_hash_bigint(user_id))) FROM events;
```

### Avoid `SELECT *` in analytical queries

Columnar engines (BigQuery, Snowflake, ClickHouse) scan only the requested columns. Selecting unused columns multiplies I/O cost:

```sql
-- Bad: scans all columns
SELECT * FROM fact_orders WHERE date_key = 20240621;

-- Good: scan only needed columns
SELECT order_id, user_key, revenue_usd FROM fact_orders WHERE date_key = 20240621;
```

---

## ETL / ELT Patterns

**ELT (preferred for cloud OLAP):** load raw data first, transform inside the warehouse.

```
Source → ingest raw → staging table → dbt / SQL transform → mart table
```

**ETL (preferred for constrained targets):** transform before loading.

```
Source → extract → transform in application → load to target
```

Use **incremental loads** where possible — only process rows changed since the last run:

```sql
-- Watermark-based incremental load
INSERT INTO fact_orders
SELECT ...
FROM source_orders
WHERE updated_at > (SELECT MAX(loaded_at) FROM etl_watermarks WHERE table_name = 'fact_orders');
```

---

## What NOT to Do

- Do not run analytical queries on the OLTP primary — use a read replica or dedicated OLAP engine
- Do not use `SELECT *` — list columns explicitly, especially on columnar engines
- Do not `JOIN` large fact tables to each other without filtering first — join fact to dimension, not fact to fact
- Do not schedule refreshes more frequently than the source data changes — it wastes compute
- Do not store intermediate aggregation results in application memory — push the aggregation to the DB
