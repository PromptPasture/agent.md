# BigQuery Reference

Use GoogleSQL syntax for BigQuery warehouse SQL.

---

## Key Patterns

- **Types:** Use `ARRAY`, `STRUCT`, `JSON`, `NUMERIC`, `BIGNUMERIC`, `TIMESTAMP`, and `DATETIME` intentionally. Prefer `TIMESTAMP` for absolute instants.
- **Nested data:** Use `UNNEST` with aliases and guard against row multiplication.
- **Partitioning:** Partition large tables by ingestion time or business date. Use `require_partition_filter = TRUE` where appropriate.
- **Clustering:** Cluster on high-cardinality filter or join keys used after partition pruning.
- **Cost control:** Select only needed columns, filter partitions early, and avoid repeated scans of large CTEs when materialization would be cheaper.
- **Parameters:** Use named parameters like `@start_date`.

---

## Example

```sql
SELECT
    DATE(event_timestamp) AS event_date,
    COUNT(DISTINCT user_id) AS active_users
FROM `project.dataset.events`
WHERE DATE(event_timestamp) BETWEEN @start_date AND @end_date
GROUP BY event_date
ORDER BY event_date;
```
