# Migration Reference

Produce database migrations that are safe to run, clear to review, and aligned with the repository's migration tool.

## Detect the Migration Tool

**Use the repository's migration tool instead of inventing a new format.**

Identify tooling from file names, folders, dependencies, or framework conventions:

| Signal | Tooling |
| --- | --- |
| `V1__name.sql`, `flyway.conf` | Flyway |
| `db/changelog`, XML/YAML change sets | Liquibase |
| `versions/*.py`, `alembic.ini` | Alembic |
| `db/migrate/*.rb` | Rails / ActiveRecord |
| `prisma/migrations`, `schema.prisma` | Prisma |
| `migrations/*.sql`, `up.sql`, `down.sql` | SQL-first migration tool |

Follow the existing repository style before introducing a new migration shape.

## Safety Rules

**Prefer staged, reversible changes that avoid surprise locks and data loss.**

- **Transactional DDL:** Use transaction-wrapped migrations when the dialect and tool support it. Note exceptions such as PostgreSQL `CREATE INDEX CONCURRENTLY`.
- **Reversibility:** Provide a down migration when the tool expects one. If data loss prevents a true rollback, state the forward-fix path.
- **Expand and contract:** For production schema changes, add nullable columns or compatibility structures first, backfill safely, then enforce constraints or remove old columns in a later migration.
- **Backfills:** Batch large updates, make them idempotent, and avoid long exclusive locks.
- **Indexes:** For large PostgreSQL tables, prefer `CREATE INDEX CONCURRENTLY` outside a transaction. For other dialects, call out lock behavior where relevant.
- **Constraints:** Add constraints after data is valid. For PostgreSQL, consider `NOT VALID` plus later validation for large tables.
- **Destructive changes:** Do not drop columns, tables, or data without making the risk explicit and offering a safer staged alternative.

## Output Shape

**Match the project's migration format and make rollback behavior explicit.**

For SQL-first migrations, produce:

```sql
-- Up
BEGIN;

-- schema changes

COMMIT;

-- Down
BEGIN;

-- rollback changes

COMMIT;
```

For framework migrations, use the framework's existing class/function style and include validation notes for generated SQL when the ORM hides important DDL details.

## Verification

**Check both schema application and rollback whenever the project supports it.**

Recommend the narrowest useful checks: migration dry-run, schema diff, rollback test, application tests that touch the changed table, and query-plan review for new indexes.
