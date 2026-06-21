---
topic: code-database skill design
method: comparative analysis
date: "2026-06-21"
related:
  - src/skills/in-progress/code-database/SKILL.md
  - src/skills/code-backend/SKILL.md
  - src/skills/code-frontend/SKILL.md
---

# Brainstorm - code-database Skill

## Goal

Design a `code-database` skill that produces production-ready schema, migrations, and queries in the project's detected DB stack, following the same 4-phase workflow already established in `code-frontend` and `code-backend`.

## Context

The skill file exists (`src/skills/in-progress/code-database/SKILL.md`) but is empty — only frontmatter. A set of reference docs was previously deleted (postgres, mysql, sqlite, mssql, oracle, bigquery, snowflake, clickhouse, cockroachdb, migration, schema-design, common, analytics). The skill needs to be built from scratch, consistent in structure and quality with the other two code-* skills.

## Agenda

1. Define skill trigger and scope
2. Design the 4-phase workflow (Discover → Design → Build → Validate)
3. Define reference doc set (engine-specific + concern docs)
4. Define P0–P3 quality checklist

## Ideas Considered

### Scope: Schema & migrations only

- **Description:** Limit the skill to DDL work — table design, migrations, indexes, constraints.
- **Benefits:** Narrow and focused; easy to reason about.
- **Trade-offs:** Leaves out query writing and ORM usage, which are the most common daily DB tasks. Forces users to context-switch to a different skill for DML/DQL.

### Scope: Queries & data access only

- **Description:** Cover SQL queries, ORM calls, stored procedures, views — but not schema changes.
- **Benefits:** High daily utility.
- **Trade-offs:** Schema and queries are tightly coupled. Writing a query without confirming the schema it operates on is fragile.

### Scope: Full DB layer — schema, migrations, and queries (chosen)

- **Description:** Any database work: schema design, migrations, queries, indexes, views, stored procedures.
- **Benefits:** Mirrors how backend engineers actually work. Avoids artificial boundaries between DDL and DML. One skill that covers the full DB surface.
- **Trade-offs:** Broader scope means the Design phase must be adaptive — confirm schema contracts when schema changes are in scope, query contracts when queries are in scope, or both.

### Engine strategy: engine-agnostic

- **Description:** One set of SQL best-practices that applies across all engines.
- **Benefits:** Simpler to maintain.
- **Trade-offs:** Loses engine-specific guidance — Postgres CTEs, MySQL limitations, BigQuery partitioning, Snowflake clustering, etc. These differences matter enough to cause production bugs.

### Engine strategy: engine-specific reference docs (chosen)

- **Description:** Detect the DB engine in Discover, load the matching reference doc in Build — same pattern as `code-backend` loading `persistence.md`, `auth.md`, etc.
- **Benefits:** Precise, actionable guidance per engine. Consistent with the existing reference doc pattern.
- **Trade-offs:** More docs to maintain, but each doc is small and focused.

## Outcomes

### Summary

The skill follows the 4-phase pattern: **Discover → Design → Build → Validate**. Engine detection happens in Discover. Design confirms schema and/or query contracts as needed before any code is written. Build loads engine-specific and concern reference docs, then writes complete SQL, migrations, or ORM code. Validate runs a DB-focused P0–P3 checklist.

### Decisions

**Trigger:** Use when the user asks to design a table, write a migration, add an index, write a query, use an ORM, or produce any database layer code in a real codebase.

**Phase 1 — Discover:**

- Inspect project files to detect: DB engine, ORM/query library, migration tool
- Key signals: `docker-compose.yml` (DB service), `go.mod`/`package.json`/`requirements.txt` (ORM deps), migration directories (`migrations/`, `db/migrate/`, Flyway/Liquibase/Alembic configs)
- Output a confirmed detection summary before proceeding
- Fallback: suggest PostgreSQL + raw SQL if nothing is detected

**Phase 2 — Design:**

- When schema changes needed: draft schema contract (tables, columns, types, constraints, indexes)
- When queries needed: draft query contract (inputs, output shape, performance target)
- Both if applicable
- Wait for explicit confirmation before writing any code

**Phase 3 — Build:**

- Load engine-specific reference doc matching detected engine
- Load concern docs based on task signals (migration, schema-design, analytics, etc.)
- Write complete SQL/migrations/ORM code — no placeholders, no TODOs
- List all files created/modified and wait for confirmation before Validate

**Phase 4 — Validate (P0–P3):**

P0 — Blocking:

- SQL injection: parameterized queries / ORM-safe binding enforced throughout
- Destructive schema changes (DROP TABLE, DROP COLUMN, TRUNCATE) explicitly confirmed before migration is written
- Data loss risk (column removal, type coercion, NOT NULL added to existing column) flagged and confirmed
- Every migration includes a rollback / down migration

P1 — Required:

- Type safety in ORM calls (no untyped raw queries at service boundaries)
- Error handling: every query result checked; no silent discard of errors
- Index correctness: all columns referenced in WHERE/JOIN/ORDER BY have appropriate indexes

P2 — Expected:

- No N+1 queries — related data joined or batch-loaded
- No unbounded queries — LIMIT applied; pagination where result set can grow
- Migration idempotency — safe to re-run; uses IF NOT EXISTS / IF EXISTS guards where applicable
- Missing index noted in migration comment where a query depends on it

P3 — Polish:

- Connection pool sizing noted in config
- Slow query logging / observability hooks noted
- Seed data consistent with schema constraints

**Reference doc set:**

Engine-specific:

- `references/postgres.md`
- `references/mysql.md`
- `references/sqlite.md`
- `references/mssql.md`
- `references/oracle.md`
- `references/bigquery.md`
- `references/snowflake.md`
- `references/clickhouse.md`
- `references/cockroachdb.md`

Concern docs:

- `references/migration.md` — migration patterns, rollback strategy, idempotency
- `references/schema-design.md` — normalization, naming conventions, constraint patterns
- `references/analytics.md` — OLAP-specific patterns (partitioning, clustering, materialized views)
- `references/common.md` — cross-engine patterns (indexes, transactions, NULL handling)

### Open Questions

None — all decisions confirmed by user.

## Next Steps

1. Write `SKILL.md` — 4-phase workflow following the `code-backend` template
2. Write concern reference docs (`migration.md`, `schema-design.md`, `analytics.md`, `common.md`)
3. Write engine-specific reference docs (start with `postgres.md`, `mysql.md`, `sqlite.md`; add others)
4. Update skill description field in frontmatter
5. Move skill from `in-progress/` to published once complete
