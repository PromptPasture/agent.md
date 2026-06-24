---
name: code-database
description: Use when the user asks to design a table, write a migration, add an index, write a query, use an ORM, or produce any database layer code in a real codebase. Generates production-ready SQL, migrations, and ORM code with auto-detected engine, confirmed schema and query contracts before writing, and a P0–P3 quality checklist covering SQL injection, destructive change safety, performance, and migration correctness.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "2.0.2"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: database
  tags: [codegen, database, sql, migration, schema, orm]
---

# Doing Database

Generates production-ready schema, migrations, and queries in the project's existing DB stack.
Four phases: **Discover → Design → Build → Validate**. Each phase produces a confirmed output before the next begins. Skip phases when you already have the context.

---

## Phase 1 — Discover

**Goal:** Establish the DB stack before writing a single line of code.

### 1.1 Read project files

Inspect the following in order. Stop reading a file once the needed signal is found.

| File | Signal to extract |
| --- | --- |
| `docker-compose.yml` / `docker-compose.yaml` | DB engine and version in service image (e.g. `postgres:16`, `mysql:8`) |
| `go.mod` | ORM/query lib: GORM, sqlx, pgx, go-pg, ent, bun |
| `package.json` | ORM/query lib: Prisma, TypeORM, Drizzle, Knex, Sequelize, Kysely |
| `requirements.txt` / `pyproject.toml` / `Pipfile` | ORM: SQLAlchemy, Django ORM, Tortoise, Peewee |
| `pom.xml` / `build.gradle` | ORM: Hibernate, Spring Data JPA, jOOQ, MyBatis |
| `Cargo.toml` | ORM: Diesel, SeaORM, SQLx |
| `prisma/schema.prisma` | Engine (`provider`), models, migration history |
| `alembic.ini` / `alembic/` | Python migration tool; infer engine from connection string |
| `flyway.conf` / `V*.sql` files | Flyway migration tool and dialect |
| `liquibase.properties` / `changelog*` | Liquibase migration tool |
| `migrations/` / `db/migrate/` / `database/migrations/` | Migration files — infer engine from SQL dialect or ORM config |
| `.env` / `.env.example` | `DATABASE_URL` — parse engine prefix (`postgresql://`, `mysql://`, `sqlite:`) |

### 1.2 Output a detection summary

Present a concise summary and wait for confirmation before proceeding:

```text
Stack detected:
  Engine:    <detected DB engine and version>
  ORM:       <detected ORM or query library, or "raw SQL">
  Migrations: <detected migration tool or "none">
  Schema:    <detected schema/database name if available>
```

If the user corrects any item, update and re-confirm.

### 1.3 Empty project fallback

If no stack files are found, suggest a default stack and wait for explicit user confirmation:

```text
No DB stack detected. Suggested stack:
  Engine:    PostgreSQL 16
  ORM:       raw SQL with parameterized queries
  Migrations: plain SQL migration files

Confirm, or tell me what stack to use instead.
```

Do not proceed to Design until the stack is confirmed.

---

## Phase 2 — Design

**Goal:** Produce confirmed schema contracts and/or query contracts before any code is written.

### 2.1 Ask clarifying questions (if needed)

Before drafting contracts, resolve any ambiguity with a single focused question. Do not ask more than one question at a time. Skip if the request is already specific.

Common gaps to check:

- Is this a new table/query or modifying an existing one?
- What are the cardinality and access patterns (point lookup, range scan, aggregation)?
- Are there schema changes (new tables, columns, indexes, constraints)?
- What is the expected row volume? (affects index strategy and pagination approach)
- Any soft-delete, audit log, or multi-tenancy requirements?

### 2.2 Draft schema contract (when schema changes are in scope)

For every table added or changed, produce the contract in this format:

```text
Table:   users
Action:  CREATE

Columns:
  id           UUID         PK   DEFAULT gen_random_uuid()
  email        TEXT         NOT NULL UNIQUE
  name         TEXT         NOT NULL
  role         TEXT         NOT NULL DEFAULT 'viewer'
  created_at   TIMESTAMPTZ  NOT NULL DEFAULT now()
  updated_at   TIMESTAMPTZ  NOT NULL DEFAULT now()

Indexes:
  idx_users_email   UNIQUE on (email)

Constraints:
  role must be one of: 'viewer', 'editor', 'admin'

Rollback:
  DROP TABLE users;
```

Omit this section if no schema changes are required.

### 2.3 Draft query contract (when queries are in scope)

For every query added or changed, produce the contract in this format:

```text
Query:    getUsersByRole
Purpose:  List all users with a given role, paginated

Inputs:
  role    string  required  Filter by role
  limit   int     required  Page size (max 100)
  cursor  string  optional  Pagination cursor (created_at of last row)

Output columns:
  id, email, name, role, created_at

Ordering:   created_at DESC
Pagination: cursor-based on created_at
Indexes:    idx_users_role_created (role, created_at DESC) — must exist
```

Omit this section if no new queries are required.

### 2.4 Reconcile missing indexes

For every index listed in a query contract under "Indexes required", check whether it already exists in the schema. If it does not:

- Add it to the schema contract (section 2.2) as an `ALTER TABLE … ADD INDEX` or `CREATE INDEX` action
- It will be written as a migration in Phase 3 alongside any other schema changes

Do not write a query that depends on an index that is not confirmed to exist.

### 2.5 Identify concern docs to load

Load concern docs based on the task:

| Signal | Load |
| --- | --- |
| New tables, columns, or constraints | `references/schema-design.md` |
| Migration files being written | `references/migration.md` |
| OLAP, reporting, or analytical queries | `references/analytics.md` |
| Cross-engine or engine-agnostic patterns needed | `references/common.md` |
| PostgreSQL engine detected | `references/postgres.md` |
| MySQL / MariaDB engine detected | `references/mysql.md` |
| SQLite engine detected | `references/sqlite.md` |
| SQL Server / MSSQL engine detected | `references/mssql.md` |
| Oracle engine detected | `references/oracle.md` |
| BigQuery engine detected | `references/bigquery.md` |
| Snowflake engine detected | `references/snowflake.md` |
| ClickHouse engine detected | `references/clickhouse.md` |
| CockroachDB engine detected | `references/cockroachdb.md` |

### 2.6 Wait for confirmation

Present the schema and/or query contracts from steps 2.2–2.4, then wait for explicit confirmation before proceeding to Build. If the user corrects any item, update and re-confirm.

---

## Phase 3 — Build

**Goal:** Write production-ready files that match the confirmed Design contracts and detected stack.

### 3.1 Load reference docs

Load every concern doc identified in Phase 2 before writing any file. Apply its guidance throughout the Build phase.

### 3.2 State decomposition rationale

Before writing, briefly state what files will be created and why they are split that way. Split into separate files when:

- A migration file contains more than one schema change (split by change)
- An ORM model file exceeds ~200 lines
- A query file covers more than one domain

### 3.3 File and folder conventions

Follow the project's existing conventions if present. When no convention is established, apply these defaults:

```text
migrations/
  YYYYMMDDHHMMSS_<description>.up.sql      # forward migration
  YYYYMMDDHHMMSS_<description>.down.sql    # rollback migration

db/
  queries/        # Named SQL query files (one file per domain)
  models/         # ORM model definitions
  repository/     # Repository implementations
```

### 3.4 Code standards

Apply these unconditionally:

#### Queries

- Never use `SELECT *` in application queries — list columns explicitly
- Always use parameterized queries or ORM-safe bindings — never string interpolation
- Every query accepts a cancellation context (timeout / deadline)
- Apply `LIMIT` on every list query — no unbounded result sets
- No N+1: load related data with JOIN or batch query, never in a loop

#### Schema

- Use explicit column types — no generic `TEXT` for everything if a narrower type fits
- Every column has a `NOT NULL` constraint unless NULL is semantically meaningful
- Every foreign key has an index unless the table is tiny (< 1000 rows and never queried by that column)
- Default values declared in DDL, not only in application code
- Timestamps use timezone-aware types (`TIMESTAMPTZ`, `DATETIME WITH TIME ZONE`, etc.)

#### Migrations

- One migration = one logical change
- Every migration has a rollback (down migration) unless rollback is impossible (e.g., irreversible data transform)
- Never modify an applied migration — create a new one
- Use `IF NOT EXISTS` / `IF EXISTS` guards where the engine supports it

#### Error handling

- Surface not-found as a typed error, not nil/null silently returned
- Surface constraint violations (unique, FK) as typed errors the caller can handle
- Never swallow DB errors — propagate with context

### 3.5 Write files

Write each file in full. No placeholders, no TODOs, no stub implementations.

After writing all files, list every file created or modified:

```text
Created:
  migrations/20240621120000_create_users.up.sql
  migrations/20240621120000_create_users.down.sql
  db/models/user.go
  db/repository/user_repository.go

```

Present this list and wait for the user to confirm before proceeding to Validate.

---

## Phase 4 — Validate

**Goal:** Work through every checklist item before declaring the output complete. Fix any issue found — do not report and skip.

Items are ordered by severity. P0 failures block delivery. P1–P3 failures must be resolved before closing but do not require re-confirmation from the user unless the fix changes the Design contracts.

---

### P0 — Blocking

These issues make the output unsafe or destructive. Stop and fix before anything else.

- [ ] No SQL injection: all user-controlled values go through parameterized queries or ORM-safe bindings — no string concatenation in query construction
- [ ] Destructive schema changes (`DROP TABLE`, `DROP COLUMN`, `TRUNCATE`) were explicitly confirmed with the user before the migration was written
- [ ] Data loss risk identified and confirmed: column removal, column type coercion, adding `NOT NULL` to an existing column without a default — all flagged and acknowledged before writing
- [ ] Every migration has a rollback (down migration) unless rollback is provably impossible
- [ ] All queries and schema match the confirmed Design contracts exactly

---

### P1 — Required

These issues violate production standards. Fix before closing.

#### Type safety

- [ ] ORM model fields are typed — no untyped/dynamic field maps at repository boundaries
- [ ] Query result columns are mapped to typed structs/objects — no raw `map[string]interface{}` or `any[]` returned from the repository

#### Error handling

- [ ] Every query result is checked for errors — no silent discard
- [ ] Not-found condition returns a typed error, not a nil/null value
- [ ] Constraint violations (unique, FK) are caught and returned as typed errors the caller can handle

#### Index correctness

- [ ] Every column referenced in `WHERE`, `JOIN ON`, or `ORDER BY` on a table expected to grow has an index (or one is noted as a follow-up)
- [ ] Foreign key columns have an index unless the referencing table is static/tiny

---

### P2 — Expected

These issues reduce quality below senior standards. Fix before closing.

#### Query performance

- [ ] No N+1 queries — related data joined or batch-loaded
- [ ] No unbounded list queries — `LIMIT` applied; pagination in place where result set can grow
- [ ] `EXPLAIN` output considered for any non-trivial query on a large table (note findings in a comment if EXPLAIN is not runnable locally)

#### Migration quality

- [ ] Migration is idempotent where the engine supports it (`IF NOT EXISTS`, `IF EXISTS`)
- [ ] Migration timestamp and filename are descriptive and unique
- [ ] Large-table migrations note the locking strategy (e.g., concurrent index build in Postgres, `pt-online-schema-change` for MySQL)

#### Observability

- [ ] Query tracing span created if the project uses OpenTelemetry or equivalent

---

### P3 — Polish

Nice-to-have. Fix if the effort is small; note and defer otherwise.

- [ ] Connection pool sizing noted in config (max connections, idle timeout, lifetime)
- [ ] Seed data consistent with all schema constraints (not null, FK, unique, check)
- [ ] Soft-delete pattern (`deleted_at`) considered when hard delete would affect referential integrity
- [ ] Audit columns (`created_at`, `updated_at`, `created_by`) present on tables that need an audit trail

---

### Completion summary

After all items are resolved, output:

```text
Validate complete.

P0  ✓ all passed
P1  ✓ all passed
P2  ✓ all passed      (or: 1 deferred — [item] — [reason])
P3  ✓ all passed      (or: 1 deferred — [item] — [reason])

Files delivered:
  migrations/20240621120000_create_users.up.sql
  migrations/20240621120000_create_users.down.sql
  db/models/user.go
  db/repository/user_repository.go
```

If any P2 or P3 item was deferred, state the reason and confirm it is acceptable before closing.
