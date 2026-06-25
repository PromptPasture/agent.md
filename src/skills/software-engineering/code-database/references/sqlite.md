# SQLite

---

## Core Rules

- SQLite is a file-based, serverless database — one writer at a time (WAL mode allows concurrent readers)
- Enable WAL mode for all production use — it dramatically improves concurrent read performance
- Enable foreign key enforcement explicitly with `PRAGMA foreign_keys = ON` — it is OFF by default
- SQLite uses dynamic typing — column type affinity is a hint, not a constraint; validate types in the application
- Do not use SQLite for high-write-concurrency workloads — a single write lock serialises all writes

---

## Connection Setup (required PRAGMAs)

Run these on every new connection before the first query:

```sql
PRAGMA journal_mode = WAL;          -- concurrent reads, serialised writes
PRAGMA foreign_keys = ON;           -- enforce FK constraints
PRAGMA busy_timeout = 5000;         -- wait up to 5 s for a lock before returning SQLITE_BUSY
PRAGMA synchronous = NORMAL;        -- safe with WAL; FULL is slower, OFF risks corruption
PRAGMA cache_size = -64000;         -- 64 MB page cache per connection (negative = kibibytes)
PRAGMA temp_store = MEMORY;         -- store temp tables in memory
```

---

## Type Affinity

SQLite has five storage classes: `NULL`, `INTEGER`, `REAL`, `TEXT`, `BLOB`. Column type names are mapped to affinity rules:

|Declared type contains|Affinity|
|---|---|
|`INT`|INTEGER|
|`CHAR`, `TEXT`, `CLOB`|TEXT|
|`BLOB` or none|BLOB|
|`REAL`, `FLOA`, `DOUB`|REAL|
|anything else|NUMERIC|

Use explicit column names that signal intent, even though SQLite does not enforce them:

```sql
id          INTEGER PRIMARY KEY   -- auto-assigns ROWID alias
email       TEXT    NOT NULL
amount      NUMERIC NOT NULL      -- stored as integer cents; use NUMERIC, not REAL
flag        INTEGER NOT NULL DEFAULT 0   -- 0 = false, 1 = true
created_at  TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
payload     TEXT    NOT NULL DEFAULT '{}'  -- JSON stored as TEXT
```

---

## Primary Keys and ROWID

Every table without `WITHOUT ROWID` has an implicit 64-bit `ROWID`. A column declared `INTEGER PRIMARY KEY` is an alias for `ROWID`:

```sql
-- INTEGER PRIMARY KEY = ROWID alias (most efficient)
CREATE TABLE users (
  id    INTEGER PRIMARY KEY,   -- auto-increment, alias for ROWID
  email TEXT    NOT NULL UNIQUE,
  name  TEXT    NOT NULL
);

-- UUID primary key (not ROWID alias — slightly slower but portable)
CREATE TABLE sessions (
  id         TEXT    PRIMARY KEY,   -- store UUID as TEXT
  user_id    INTEGER NOT NULL REFERENCES users(id),
  created_at TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
```

---

## Indexes

```sql
CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE UNIQUE INDEX uq_users_email ON users (email);

-- Partial index
CREATE INDEX idx_orders_pending ON orders (created_at)
  WHERE status = 'pending';

-- Covering index (include extra columns for index-only scans)
CREATE INDEX idx_orders_user_status ON orders (user_id, status, created_at);
```

---

## JSON (SQLite 3.38+)

```sql
-- Extract a field
SELECT json_extract(payload, '$.user_id') AS user_id FROM events;

-- Filter
SELECT * FROM events WHERE json_extract(payload, '$.type') = 'click';

-- Modify
UPDATE events
SET payload = json_set(payload, '$.processed', 1)
WHERE id = ?;
```

For older SQLite versions (< 3.38), use the `JSON1` extension (usually compiled in).

---

## Full-Text Search (FTS5)

```sql
-- Create a virtual FTS5 table
CREATE VIRTUAL TABLE posts_fts USING fts5(
  title,
  body,
  content='posts',
  content_rowid='id'
);

-- Populate
INSERT INTO posts_fts (rowid, title, body)
SELECT id, title, body FROM posts;

-- Query
SELECT rowid, rank FROM posts_fts
WHERE posts_fts MATCH 'database migration'
ORDER BY rank;
```

Keep the FTS table in sync with the source table using triggers or application-level inserts.

---

## Transactions

SQLite serialises all writes. Keep transactions short:

```sql
BEGIN;
  INSERT INTO orders (user_id, total_cents) VALUES (?, ?);
  UPDATE inventory SET quantity = quantity - ? WHERE product_id = ?;
COMMIT;
```

For bulk inserts, wrap in a single transaction — inserting rows one at a time without a transaction is dramatically slower:

```sql
BEGIN;
  INSERT INTO events VALUES (?, ?, ?);
  INSERT INTO events VALUES (?, ?, ?);
  -- ... thousands of rows
COMMIT;
```

---

## Migrations

SQLite has limited `ALTER TABLE` support:

- `ADD COLUMN` — supported (nullable only without a default requiring evaluation)
- `DROP COLUMN` — supported since SQLite 3.35
- `RENAME TABLE` — supported
- `RENAME COLUMN` — supported since SQLite 3.25
- `MODIFY COLUMN`, `ADD CONSTRAINT`, `DROP CONSTRAINT` — **not supported**

For unsupported operations, use the 12-step table-rebuild pattern:

```sql
-- 1. Create new table with the desired schema
CREATE TABLE users_new (
  id    INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name  TEXT NOT NULL,
  role  TEXT NOT NULL DEFAULT 'viewer'  -- new column with default
);

-- 2. Copy data
INSERT INTO users_new (id, email, name)
SELECT id, email, name FROM users;

-- 3. Drop old table
DROP TABLE users;

-- 4. Rename new table
ALTER TABLE users_new RENAME TO users;
```

Wrap the entire rebuild in a transaction with `PRAGMA foreign_keys = OFF` temporarily:

```sql
PRAGMA foreign_keys = OFF;
BEGIN;
  -- rebuild steps here
COMMIT;
PRAGMA foreign_keys = ON;
```

---

## Concurrency and WAL

WAL (Write-Ahead Log) allows one writer and multiple concurrent readers. Key behaviour:

- Readers never block writers; writers never block readers
- Only one writer at a time — concurrent writes queue and may return `SQLITE_BUSY`
- Set `busy_timeout` so the application retries automatically instead of failing immediately
- WAL file grows until a checkpoint occurs — checkpoints happen automatically at 1000 pages by default

```sql
-- Force a checkpoint manually (e.g., during a maintenance window)
PRAGMA wal_checkpoint(TRUNCATE);
```

---

## What NOT to Do

- Do not use SQLite for high-concurrency write workloads — one writer at a time is a hard limit
- Do not use `REAL` for monetary values — use `INTEGER` (store cents) or `NUMERIC` (exact decimal)
- Do not skip `PRAGMA foreign_keys = ON` — FK constraints are silent no-ops without it
- Do not run SQLite in a shared network filesystem (NFS, SMB) — file locking is unreliable
- Do not skip WAL mode in production — default journal mode (`DELETE`) blocks all readers during a write
