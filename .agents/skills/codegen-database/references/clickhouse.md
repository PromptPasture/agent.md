# ClickHouse Reference

Use ClickHouse patterns for high-volume analytical tables and queries.

## Key Patterns

**Design ClickHouse tables around scan pruning, append-heavy writes, and explicit aggregation.**

- **Engines:** Choose `MergeTree` family engines deliberately. State the `ORDER BY` key because it drives data skipping and query performance.
- **Partitioning:** Partition by coarse time windows or stable lifecycle boundaries. Avoid high-cardinality partitions.
- **Materialized views:** Use materialized views for incremental aggregation when raw-event scans are too expensive.
- **Primary key:** In ClickHouse, primary key is sparse index metadata, not a uniqueness guarantee.
- **Types:** Prefer concrete numeric and datetime types; use `LowCardinality(String)` for repeated low-cardinality text.
- **Mutations:** Treat updates and deletes as expensive asynchronous mutations.

## Example

**Choose partition and order keys from the most common query filters.**

```sql
CREATE TABLE events
(
    occurred_at DateTime,
    user_id     UUID,
    event_name  LowCardinality(String)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(occurred_at)
ORDER BY (event_name, occurred_at, user_id);
```
