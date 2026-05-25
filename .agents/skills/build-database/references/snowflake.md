# Snowflake Reference

Use Snowflake SQL for warehouse transformations, semi-structured data, tasks, and analytical queries.

---

## Key Patterns

- **Semi-structured data:** Use `VARIANT`, `OBJECT`, `ARRAY`, `:` path access, and `LATERAL FLATTEN` for nested values.
- **Time travel:** Mention retention and recovery implications when changing or replacing tables.
- **Clustering:** Recommend clustering only when pruning materially improves repeated large-table queries.
- **Tasks and streams:** Use streams for change capture and tasks for scheduled transformations when requested.
- **Identifiers:** Avoid quoted mixed-case identifiers unless the existing warehouse already uses them.
- **Parameters:** Use bind variables or session variables according to the execution context.

---

## Example

```sql
SELECT
    payload:user_id::STRING AS user_id,
    COUNT(*)               AS event_count
FROM analytics.raw_events,
    LATERAL FLATTEN(input => payload:events) event
GROUP BY user_id;
```
