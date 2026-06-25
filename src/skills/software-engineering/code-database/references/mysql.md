# MySQL / MariaDB

---

## Core Rules

- Use `InnoDB` storage engine for all tables — it supports transactions, FK constraints, and row-level locking
- Use `DATETIME(6)` or `TIMESTAMP(6)` for timestamps (microsecond precision); avoid bare `TIMESTAMP` (limited range, auto-update side effects)
- Use `utf8mb4` character set and `utf8mb4_unicode_ci` collation — `utf8` in MySQL is limited to 3 bytes (no emoji support)
- Use `BIGINT UNSIGNED AUTO_INCREMENT` or `CHAR(36)` UUID for primary keys
- Always declare FK constraints — MySQL does not enforce them without explicit definition

---

## Character Set

Set character set and collation at the database, table, and connection level:

```sql
-- Database default
CREATE DATABASE myapp
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Table-level (or inherit from database)
CREATE TABLE users (
  ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

Set `character_set_client`, `character_set_connection`, and `character_set_results` to `utf8mb4` in the connection string:

```
mysql://user:pass@host/db?charset=utf8mb4
```

---

## Data Types Reference

```sql
id          BIGINT UNSIGNED  AUTO_INCREMENT PRIMARY KEY
-- or UUID:
id          CHAR(36)         NOT NULL DEFAULT (UUID()) PRIMARY KEY

email       VARCHAR(320)     NOT NULL
name        VARCHAR(255)     NOT NULL
status      ENUM('pending','paid','cancelled') NOT NULL DEFAULT 'pending'
amount      DECIMAL(19,4)    NOT NULL
flag        TINYINT(1)       NOT NULL DEFAULT 0
payload     JSON             -- MySQL 5.7.8+
tags        JSON             -- store as JSON array
created_at  DATETIME(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
updated_at  DATETIME(6)      NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
              ON UPDATE CURRENT_TIMESTAMP(6)
```

---

## Indexes

```sql
-- Standard B-tree
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Unique
CREATE UNIQUE INDEX uq_users_email ON users (email);

-- Composite
CREATE INDEX idx_orders_user_status ON orders (user_id, status, created_at DESC);

-- Full-text (InnoDB, MySQL 5.6+)
CREATE FULLTEXT INDEX idx_posts_search ON posts (title, body);

-- JSON expression index (MySQL 5.7.9+ / MariaDB 10.2+)
ALTER TABLE events ADD COLUMN event_type VARCHAR(100)
  GENERATED ALWAYS AS (payload->>'$.type') STORED;
CREATE INDEX idx_events_type ON events (event_type);
```

MySQL B-tree indexes have a maximum key prefix of 767 bytes (InnoDB row format `COMPACT`) or 3072 bytes (`DYNAMIC`). Use `ROW_FORMAT=DYNAMIC` for large VARCHAR columns:

```sql
ALTER TABLE posts ROW_FORMAT=DYNAMIC;
CREATE INDEX idx_posts_title ON posts (title(191));  -- prefix index for long columns
```

---

## UUID as Primary Key

UUIDs as random PKs cause index fragmentation in InnoDB (which clusters rows by PK). Use UUID v7 (time-ordered) or store a separate auto-increment surrogate:

```sql
-- Option 1: auto-increment surrogate + UUID natural key
id        BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
uuid      CHAR(36) NOT NULL UNIQUE DEFAULT (UUID())

-- Option 2: ordered UUID (MySQL 8.0 / MariaDB 10.7+)
id        CHAR(36) NOT NULL PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID(), 1))
```

---

## Upsert (INSERT … ON DUPLICATE KEY UPDATE)

```sql
INSERT INTO users (id, email, name)
VALUES (?, ?, ?)
ON DUPLICATE KEY UPDATE
  name       = VALUES(name),
  updated_at = NOW(6);
```

---

## JSON Queries (MySQL 5.7.8+)

```sql
-- Extract
SELECT payload->>'$.user_id' AS user_id FROM events;

-- Filter
SELECT * FROM events WHERE payload->>'$.type' = 'click';

-- Array contains (JSON_CONTAINS)
SELECT * FROM posts WHERE JSON_CONTAINS(tags, '"mysql"');
```

---

## Full-Text Search

```sql
-- NATURAL LANGUAGE mode (ranked relevance)
SELECT id, title,
  MATCH(title, body) AGAINST ('database migration' IN NATURAL LANGUAGE MODE) AS score
FROM posts
WHERE MATCH(title, body) AGAINST ('database migration' IN NATURAL LANGUAGE MODE);

-- BOOLEAN mode (explicit operators)
SELECT id, title FROM posts
WHERE MATCH(title, body) AGAINST ('+database -nosql' IN BOOLEAN MODE);
```

---

## Transactions

```sql
START TRANSACTION;
  INSERT INTO orders (user_id, total_cents) VALUES (?, ?);
  UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?;
COMMIT;

-- On error:
ROLLBACK;
```

MySQL's `AUTOCOMMIT` is `ON` by default — always wrap multi-step writes in an explicit transaction.

---

## Migrations (MySQL-specific)

MySQL acquires a metadata lock for `ALTER TABLE` operations, blocking all reads and writes on the table. For large tables, use **online DDL** or `pt-online-schema-change` / `gh-ost`:

```sql
-- Online DDL (MySQL 5.6+ InnoDB): many operations are in-place and lock-free
ALTER TABLE orders
  ADD COLUMN notes TEXT,
  ALGORITHM=INPLACE, LOCK=NONE;

-- Check if an operation supports ALGORITHM=INPLACE before using it
-- https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html
```

```sql
-- Add column safely without locking
-- 1. Add nullable (no default — immediate on MySQL 8.0+)
ALTER TABLE orders ADD COLUMN notes TEXT;

-- 2. Backfill in batches
UPDATE orders SET notes = '' WHERE notes IS NULL LIMIT 10000;
-- Repeat until 0 rows affected

-- 3. Set NOT NULL in a subsequent migration
ALTER TABLE orders MODIFY COLUMN notes TEXT NOT NULL DEFAULT '';
```

---

## Connection Pooling

```
max_connections (MySQL server) = sum of all application pool max sizes
```

Recommended application pool settings:

|Setting|Value|
|---|---|
|Max pool size|10–25 per app instance|
|Min idle|2–5|
|Connection timeout|30 s|
|Max lifetime|30 min|
|`wait_timeout` (server)|28800 s (8 h) — set in `my.cnf`|

---

## What NOT to Do

- Do not use `MyISAM` — it lacks transactions, FK constraints, and row-level locking
- Do not use `utf8` — use `utf8mb4` to support full Unicode (including emoji)
- Do not use bare `TIMESTAMP` for new columns — it has a 2038 range limit and an implicit `ON UPDATE` behavior that can silently mutate data
- Do not run `ALTER TABLE` without `ALGORITHM=INPLACE, LOCK=NONE` on large live tables — it will lock the table
- Do not use `ENUM` for values that change frequently — `ALTER TABLE` is required to add values
