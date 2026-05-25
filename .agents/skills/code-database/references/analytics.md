# Analytics SQL Reference

Write warehouse-oriented SQL for metrics, cohorts, funnels, retention, denormalized reporting tables, and transformation models.

---

## Analytics Rules

- **Define the grain:** State the row grain for every result or model, such as one row per user per day or one row per order item.
- **Separate facts and dimensions:** Keep event/fact measures separate from descriptive dimensions unless a denormalized output is explicitly requested.
- **Use stable time windows:** Make timezone, date truncation, inclusive/exclusive boundaries, and late-arriving data assumptions explicit.
- **Avoid silent fanout:** Pre-aggregate before joining one-to-many relationships when metrics can multiply.
- **Prefer named CTEs:** Use CTEs to make metric definitions auditable, then collapse only if the target engine needs it for performance.
- **Partition and cluster:** Tie partitioning, clustering, or sort keys to common filters and joins.
- **Validate metrics:** Include sanity checks such as row counts, distinct keys, duplicate detection, and null-rate checks for important dimensions.

---

## Output Shape

Return the query or model definition, followed by short notes for grain, assumptions, performance, and validation.

```sql
WITH base_events AS (
    SELECT
        user_id,
        event_name,
        occurred_at
    FROM events
    WHERE occurred_at >= :start_at
      AND occurred_at < :end_at
)
SELECT
    DATE_TRUNC('day', occurred_at) AS event_day,
    COUNT(DISTINCT user_id)       AS active_users
FROM base_events
GROUP BY 1;
```

---

## Warehouse Routing

Use dialect references for engine-specific details when present. If no warehouse-specific reference exists, keep SQL ANSI-oriented and flag any syntax assumptions.
