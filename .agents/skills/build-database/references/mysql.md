# MySQL / MariaDB Reference

## Key types

**Use dialect-native types and call out portability tradeoffs.**

- **Rule:** `BIGINT UNSIGNED AUTO_INCREMENT` — primary keys (or `CHAR(36)` for UUID)
- **Rule:** `VARCHAR(n)` — always specify length (required by MySQL)
- **Rule:** `DECIMAL(p,s)` — exact decimals (not FLOAT for money)
- **Rule:** `DATETIME` / `TIMESTAMP` — TIMESTAMP auto-converts to UTC; DATETIME stores as-is
- **Rule:** `JSON` — native JSON type (MySQL 5.7.8+, MariaDB 10.2+)
- **Rule:** `TEXT` / `MEDIUMTEXT` / `LONGTEXT` — for large text (no indexes without prefix)
- **Rule:** `TINYINT(1)` — booleans (MySQL has no native BOOLEAN, maps to TINYINT)

## Upsert

**Use the dialect-native upsert form and state the required uniqueness constraint.**

```sql
INSERT INTO users (email, name, updated_at)
VALUES (?, ?, NOW())
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    updated_at = NOW();
```

## Auto-increment and UUIDs

**Choose identifiers based on distribution, ordering, and write patterns.**

```sql
-- Integer PK (simpler, better performance)
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ...
);

-- UUID PK (distributed-safe)
CREATE TABLE users (
    id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
    ...
) ENGINE=InnoDB;
```

## Storage engines

**Choose storage engines that preserve transactions and referential integrity.**

- **Rule:** Always use `ENGINE=InnoDB` (transactions, foreign keys, row-level locking)
- **Rule:** `ENGINE=MyISAM` is legacy — never use for new tables

## Character set

**Use Unicode-safe defaults unless the repository already requires otherwise.**

```sql
-- Database level
CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Table level (always explicit)
CREATE TABLE articles (
    ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

`utf8mb4` is required for emoji and full Unicode support. `utf8` in MySQL is 3-byte only.

## JSON columns

**Use JSON columns for flexible attributes while preserving queryable constraints where needed.**

```sql
CREATE TABLE events (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payload JSON NOT NULL,
    -- Virtual columns for JSON key indexing:
    event_type VARCHAR(50) AS (JSON_UNQUOTE(payload->>'$.type')) STORED,
    INDEX idx_events_type (event_type)
);

-- Query
SELECT * FROM events WHERE JSON_UNQUOTE(payload->>'$.userId') = ?;
```

## Full-text search

**Use built-in full-text search syntax and indexes for search workloads.**

```sql
-- Index (MyISAM supports this; InnoDB from 5.6+)
ALTER TABLE articles ADD FULLTEXT(title, body);

-- Query
SELECT *, MATCH(title, body) AGAINST (? IN BOOLEAN MODE) AS score
FROM articles
WHERE MATCH(title, body) AGAINST (? IN BOOLEAN MODE)
ORDER BY score DESC;
```

## EXPLAIN

**Use execution plans to confirm whether indexes and joins behave as expected.**

```sql
EXPLAIN FORMAT=JSON
SELECT * FROM orders WHERE user_id = ?;
```

## Pagination — keyset preferred

**Use keyset pagination when offsets would scan too much data.**

```sql
-- Offset (avoid on large tables)
SELECT * FROM orders ORDER BY created_at DESC LIMIT ? OFFSET ?;

-- Keyset
SELECT * FROM orders
WHERE created_at < ?  -- cursor
ORDER BY created_at DESC
LIMIT ?;
```

## Common gotchas

**Call out dialect behavior that commonly changes query results or safety.**

- **Rule:** `GROUP BY` in MySQL 5.7+ with `ONLY_FULL_GROUP_BY` mode: all non-aggregate SELECT columns must be in GROUP BY
- **Rule:** `ENUM` type: changes to ENUM values require ALTER TABLE (expensive on large tables); prefer VARCHAR + CHECK constraint or a lookup table
- **Rule:** String comparison is case-insensitive by default (depends on collation)
- **Rule:** No `RETURNING` clause — use `LAST_INSERT_ID()` after INSERT
