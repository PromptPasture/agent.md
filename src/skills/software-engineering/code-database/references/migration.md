# Migration — Schema Change Patterns

---

## Core Rules

- Migrations are the source of truth for schema — no DDL outside migration files
- One migration = one logical change
- Every migration must have a rollback (down migration) unless rollback is provably impossible
- Never modify a migration that has already been applied to any environment — create a new one
- Migrations must be safe to run on a live database with concurrent traffic

---

## File Naming

Use a timestamp prefix and a descriptive name:

```
YYYYMMDDHHMMSS_<description>.up.sql
YYYYMMDDHHMMSS_<description>.down.sql
```

Examples:

```
20240621120000_create_users.up.sql
20240621120000_create_users.down.sql
20240622090000_add_users_role_index.up.sql
20240622090000_add_users_role_index.down.sql
```

Avoid generic names like `update.sql` or `fix.sql` — the name is the only documentation for what a migration does at a glance.

---

## Up / Down Pair

Every migration has a matching rollback:

```sql
-- 20240621120000_create_users.up.sql
CREATE TABLE IF NOT EXISTS users (
  id         UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT        NOT NULL,
  name       TEXT        NOT NULL,
  role       TEXT        NOT NULL DEFAULT 'viewer',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users (email);
```

```sql
-- 20240621120000_create_users.down.sql
DROP TABLE IF EXISTS users;
```

When rollback is impossible (e.g., data was transformed and original cannot be recovered), document it:

```sql
-- 20240622_backfill_slugs.down.sql
-- ROLLBACK NOT POSSIBLE: slug data was generated from title at migration time.
-- To undo, restore from a backup taken before this migration ran.
SELECT 1; -- no-op to satisfy migration runner
```

---

## Idempotency

Use `IF NOT EXISTS` / `IF EXISTS` guards wherever the engine supports them:

```sql
-- Creating objects
CREATE TABLE IF NOT EXISTS ...
CREATE INDEX IF NOT EXISTS ...
CREATE SEQUENCE IF NOT EXISTS ...

-- Dropping objects
DROP TABLE IF EXISTS ...
DROP INDEX IF EXISTS ...

-- Adding columns (Postgres 9.6+)
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url TEXT;
```

For engines that do not support `IF NOT EXISTS` on `ALTER TABLE`, wrap in a conditional:

```sql
-- MySQL / MariaDB: check information_schema before adding
SET @exists = (
  SELECT COUNT(*) FROM information_schema.columns
  WHERE table_schema = DATABASE()
    AND table_name = 'users'
    AND column_name = 'avatar_url'
);
SET @sql = IF(@exists = 0,
  'ALTER TABLE users ADD COLUMN avatar_url TEXT',
  'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
```

---

## Safe Schema Changes (zero-downtime)

### Adding a nullable column

Always safe — existing rows get NULL automatically:

```sql
ALTER TABLE orders ADD COLUMN notes TEXT;
```

### Adding a NOT NULL column

**Unsafe on large tables with live traffic** — requires a default or a multi-step approach:

```sql
-- Step 1: Add nullable
ALTER TABLE orders ADD COLUMN priority TEXT;

-- Step 2: Backfill (do in batches if table is large)
UPDATE orders SET priority = 'normal' WHERE priority IS NULL;

-- Step 3: Add NOT NULL constraint + default (separate migration)
ALTER TABLE orders ALTER COLUMN priority SET NOT NULL;
ALTER TABLE orders ALTER COLUMN priority SET DEFAULT 'normal';
```

### Renaming a column

**Never rename directly on a live table.** Use the expand–contract pattern:

```sql
-- Migration 1: add new column
ALTER TABLE users ADD COLUMN display_name TEXT;

-- Migration 2: backfill (deploy new app code that writes both columns)
UPDATE users SET display_name = username WHERE display_name IS NULL;

-- Migration 3: drop old column (after old code is fully retired)
ALTER TABLE users DROP COLUMN username;
```

### Dropping a column

Confirm with the user before writing. Drop in a separate migration after verifying no application code references the column:

```sql
-- Ensure no application code reads this column before running
ALTER TABLE users DROP COLUMN legacy_token;
```

### Adding an index to a large table

Use `CONCURRENTLY` in Postgres to avoid locking:

```sql
-- Postgres: non-blocking index build
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_id ON orders (user_id);
```

For MySQL, use `pt-online-schema-change` or `gh-ost` for large tables. Note this in a migration comment.

---

## Data Migrations

When a migration transforms existing data, keep it separate from DDL migrations:

```
20240623000000_add_slug_column.up.sql        -- DDL only
20240623000001_backfill_slugs.up.sql         -- data only
```

Data migration guidelines:

- Batch updates to avoid long-running transactions and lock contention:

```sql
-- Backfill in batches of 1000
UPDATE posts
SET slug = lower(replace(title, ' ', '-'))
WHERE slug IS NULL
LIMIT 1000;
-- Run until 0 rows affected
```

- Add a `WHERE` clause that makes the migration idempotent — safe to re-run
- Estimate row count and expected duration before running on production

---

## Locking Reference

|Operation|Lock level|Safe on large live table?|
|---|---|---|
|`CREATE TABLE`|None on existing tables|Yes|
|`CREATE INDEX`|Share lock (blocks writes)|No — use CONCURRENTLY|
|`CREATE INDEX CONCURRENTLY`|No table lock|Yes (Postgres)|
|`ALTER TABLE ADD COLUMN` (nullable)|Brief metadata lock|Yes|
|`ALTER TABLE ADD COLUMN NOT NULL`|Full table lock|No — use multi-step|
|`ALTER TABLE DROP COLUMN`|Full table lock|No on large tables|
|`TRUNCATE`|Full lock|Only after explicit confirmation|
|`DROP TABLE`|Full lock|Only after explicit confirmation|

---

## What NOT to Do

- Do not write raw DDL in application startup code — use migration files
- Do not skip down migrations with "we'll never roll back" — you will need them in staging
- Do not run long `UPDATE` statements without batching — they hold locks and grow the transaction log
- Do not modify a shared migration file that teammates have already applied
