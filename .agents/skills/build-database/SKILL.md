---
name: build-database
description: >
  Generate or modify database code: schemas, DDL, SQL queries, migrations, analytics SQL,
  indexes, stored procedures, and dialect-specific database scripts.
license: MIT
tags:
  - codegen
  - database
  - data
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-team-roles
  category: database
  references:
    - classify-content
---

# build-database

Generate production-ready database code for schemas, DDL, OLTP queries, analytics SQL, migrations, indexes, stored procedures, and dialect-specific scripts. Use this as a router: classify the database artifact first, detect the dialect from context or repository evidence, then read only the relevant references.

---

## Variant Detection

- **Schema design:** Requests for entities, tables, relationships, normalization, constraints, ERD-to-DDL, or "what tables do I need" route to `references/schema-design.md`.
- **Migrations:** Requests for up/down migrations, Flyway, Liquibase, Rails/ActiveRecord migrations, Alembic, Prisma migrations, rollback, data backfills, or deployment-safe DDL route to `references/migration.md`.
- **OLTP SQL:** Requests for queries, DML, views, indexes, transactions, upserts, stored procedures, or query optimization route to `references/common.md`, then the dialect reference.
- **Analytics SQL:** Requests for warehouses, metrics, cohorts, funnels, retention, partitioned fact tables, dbt-like transformations, BigQuery, Snowflake, or ClickHouse route to `references/analytics.md`, then any matching warehouse reference.
- **Adjacent skills:** Use `report-db-health` for database health findings from existing telemetry. Use `plan-backup` for backup and recovery policy. Use `write-spec` for data contracts when the output is prose rather than executable database code.
- **Ambiguity:** If the artifact type or database remains genuinely ambiguous after inspecting context, ask one short question naming the likely choices.

---

## Dialect Routing

| Signal | Reference |
| --- | --- |
| PostgreSQL, Postgres, `JSONB`, `TIMESTAMPTZ`, `ON CONFLICT`, `pg`, `psql` | `references/postgres.md` |
| MySQL, MariaDB, `AUTO_INCREMENT`, `ON DUPLICATE KEY`, `mysql2` | `references/mysql.md` |
| SQL Server, MSSQL, T-SQL, `pyodbc`, `OFFSET-FETCH`, `MERGE` | `references/mssql.md` |
| SQLite, embedded/mobile/local database, FTS5, WAL mode | `references/sqlite.md` |
| Oracle, PL/SQL, sequences, `DUAL`, Oracle hints | `references/oracle.md` |
| BigQuery, GoogleSQL, ARRAY/STRUCT, partitioned warehouse tables | `references/bigquery.md` |
| Snowflake, VARIANT, streams/tasks, clustering, time travel | `references/snowflake.md` |
| ClickHouse, MergeTree, materialized views, sparse indexes | `references/clickhouse.md` |
| CockroachDB, distributed SQL, follower reads, regional tables | `references/cockroachdb.md` |

If the user asks for portable SQL, use `references/common.md` and avoid dialect-specific syntax unless you clearly mark alternatives.

---

## Working Rules

- **Inspect first:** Read existing migrations, schema files, ORM models, query builders, naming conventions, fixtures, and migration tooling before editing repository files.
- **Prefer structural guarantees:** Encode business rules with constraints, foreign keys, uniqueness, checks, generated columns, and transaction boundaries before relying on application-only enforcement.
- **Keep migrations safe:** Make destructive DDL explicit, separate schema changes from risky data rewrites when needed, and include rollback or forward-fix guidance when true rollback is unsafe.
- **Use parameters:** Never generate SQL that interpolates user input into executable statements. Use the placeholder style for the target dialect or framework.
- **Index deliberately:** Tie each recommended index to a query, constraint, or access pattern. Avoid adding write-costly indexes without a reason.
- **Handle concurrency:** Use transactions, locks, isolation levels, uniqueness, idempotency keys, or retry notes when the database operation can race.
- **Respect dialect limits:** Do not mix syntax across engines. If the dialect is unknown and syntax materially differs, ask once instead of producing decorative nonsense in SQL clothing.
- **Verify locally:** Run the narrowest relevant migration check, SQL parser, formatter, test, or application test available. If no database is available, state what was reviewed statically.

---

## Implementation Flow

1. Identify artifact type and dialect, then read the selected artifact reference and dialect reference.
2. Inspect the closest existing schema, migration, query, model, and tests.
3. Plan the minimal database surface: tables, columns, constraints, indexes, migrations, queries, and tests or fixtures.
4. Edit using project naming and migration conventions.
5. Add or update focused tests, fixtures, or migration assertions when the repository supports them.
6. Run focused verification and fix regressions within scope.

---

## Output

When editing a repository, finish with changed files, commands run, and verification status.

When drafting code only, include:

```text
Assumptions:
- ...

SQL / Migration:
- ...

Performance:
- ...

Rollback / Safety:
- ...
```

---

## Verification

Use the narrowest relevant migration check, SQL parser, formatter, test, or application test available. If no database is available, report the static checks performed and the remaining runtime risk.
