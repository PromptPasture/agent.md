# SQL Server (MSSQL)

---

## Core Rules

- Use `NVARCHAR` for all text that may contain non-ASCII characters — `VARCHAR` is limited to the database collation's code page
- Use `DATETIME2` (not `DATETIME`) — it has a larger range, higher precision, and is ISO 8601 compatible
- Use `UNIQUEIDENTIFIER` (UUID) or `BIGINT IDENTITY` for primary keys
- Always specify a schema prefix (`dbo.TableName`) — relying on the default schema leads to ambiguous resolution
- Set `SET NOCOUNT ON` in stored procedures and triggers to suppress row-count messages

---

## Data Types Reference

```sql
id          UNIQUEIDENTIFIER  PRIMARY KEY DEFAULT NEWSEQUENTIALID()
-- or:
id          BIGINT            IDENTITY(1,1) PRIMARY KEY

email       NVARCHAR(320)     NOT NULL
name        NVARCHAR(255)     NOT NULL
status      NVARCHAR(50)      NOT NULL DEFAULT N'pending'
amount      DECIMAL(19,4)     NOT NULL DEFAULT 0
flag        BIT               NOT NULL DEFAULT 0
payload     NVARCHAR(MAX)     NOT NULL DEFAULT N'{}'   -- JSON (SQL Server 2016+)
created_at  DATETIME2(7)      NOT NULL DEFAULT SYSUTCDATETIME()
updated_at  DATETIME2(7)      NOT NULL DEFAULT SYSUTCDATETIME()
```

Use `NEWSEQUENTIALID()` instead of `NEWID()` for UUID PKs — sequential UUIDs avoid index fragmentation.

---

## T-SQL Syntax Reference

```sql
-- Top N rows (SQL Server equivalent of LIMIT)
SELECT TOP (20) id, email FROM dbo.users ORDER BY created_at DESC;

-- Pagination with OFFSET-FETCH
SELECT id, email, created_at
FROM dbo.users
ORDER BY created_at DESC
OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;

-- String concatenation
SELECT N'Hello, ' + name AS greeting FROM dbo.users;

-- NULL-safe coalesce
SELECT COALESCE(display_name, email) AS name FROM dbo.users;

-- Current UTC timestamp
SELECT SYSUTCDATETIME();   -- DATETIME2 precision
SELECT GETUTCDATE();       -- DATETIME precision (avoid for new code)
```

---

## Indexes

```sql
-- Clustered index (one per table, usually the PK)
CREATE CLUSTERED INDEX cidx_orders_id ON dbo.orders (id);

-- Non-clustered index
CREATE NONCLUSTERED INDEX idx_orders_user_id ON dbo.orders (user_id);

-- Covering index (INCLUDE columns avoid key lookups)
CREATE NONCLUSTERED INDEX idx_orders_user_status
ON dbo.orders (user_id, status)
INCLUDE (total_cents, created_at);

-- Filtered index (partial)
CREATE NONCLUSTERED INDEX idx_orders_pending
ON dbo.orders (created_at)
WHERE status = N'pending';

-- Unique
CREATE UNIQUE NONCLUSTERED INDEX uq_users_email ON dbo.users (email);

-- Online index build (Enterprise / Developer edition)
CREATE NONCLUSTERED INDEX idx_orders_user_id ON dbo.orders (user_id)
WITH (ONLINE = ON);
```

---

## JSON Support (SQL Server 2016+)

```sql
-- Validate JSON
SELECT ISJSON(payload) AS is_valid FROM dbo.events;

-- Extract scalar value
SELECT JSON_VALUE(payload, '$.user_id') AS user_id FROM dbo.events;

-- Extract object/array
SELECT JSON_QUERY(payload, '$.address') AS address FROM dbo.users;

-- Filter by JSON field (use a computed column + index for performance)
SELECT * FROM dbo.events
WHERE JSON_VALUE(payload, '$.type') = N'click';

-- Add computed column for frequently-queried JSON field
ALTER TABLE dbo.events
  ADD event_type AS JSON_VALUE(payload, '$.type') PERSISTED;

CREATE INDEX idx_events_type ON dbo.events (event_type);
```

---

## Full-Text Search

```sql
-- Create a full-text catalog
CREATE FULLTEXT CATALOG ft_catalog AS DEFAULT;

-- Create a full-text index
CREATE FULLTEXT INDEX ON dbo.posts (title, body)
  KEY INDEX PK_posts ON ft_catalog;

-- CONTAINS (exact / prefix / phrase / boolean)
SELECT id, title FROM dbo.posts
WHERE CONTAINS((title, body), '"database migration"');

-- FREETEXT (natural language)
SELECT id, title FROM dbo.posts
WHERE FREETEXT((title, body), 'database migration');
```

---

## Transactions

```sql
BEGIN TRANSACTION;
  INSERT INTO dbo.orders (user_id, total_cents)
  VALUES (@user_id, @total_cents);

  UPDATE dbo.inventory
  SET quantity = quantity - @qty
  WHERE product_id = @product_id;

  IF @@ERROR <> 0
    ROLLBACK TRANSACTION;
  ELSE
    COMMIT TRANSACTION;
```

Use `TRY…CATCH` for structured error handling:

```sql
BEGIN TRY
  BEGIN TRANSACTION;
    INSERT INTO dbo.orders ...;
    UPDATE dbo.inventory ...;
  COMMIT TRANSACTION;
END TRY
BEGIN CATCH
  IF @@TRANCOUNT > 0
    ROLLBACK TRANSACTION;
  THROW;
END CATCH;
```

---

## Migrations (SQL Server-specific)

SQL Server supports online DDL on Enterprise edition only. On Standard/Express, `ALTER TABLE` takes a schema modification lock.

```sql
-- Add nullable column (fast — metadata-only)
ALTER TABLE dbo.users ADD avatar_url NVARCHAR(2048);

-- Add NOT NULL column (requires a default for existing rows)
ALTER TABLE dbo.users
  ADD role NVARCHAR(50) NOT NULL CONSTRAINT DF_users_role DEFAULT N'viewer';

-- Drop column (must drop constraints first)
ALTER TABLE dbo.users DROP CONSTRAINT DF_users_legacy_col;
ALTER TABLE dbo.users DROP COLUMN legacy_col;

-- Check for column existence before adding
IF NOT EXISTS (
  SELECT 1 FROM sys.columns
  WHERE object_id = OBJECT_ID(N'dbo.users') AND name = N'avatar_url'
)
BEGIN
  ALTER TABLE dbo.users ADD avatar_url NVARCHAR(2048);
END;
```

---

## Connection Pooling

SQL Server uses connection pooling via ADO.NET / JDBC by default. Key settings:

|Setting|Recommended|
|---|---|
|`Max Pool Size`|100 (ADO.NET default) — tune down under low concurrency|
|`Min Pool Size`|0–5|
|`Connect Timeout`|30 s|
|`Connection Lifetime`|0 (pool manages)|

Set `MultipleActiveResultSets=True` (MARS) in the connection string only if the ORM requires it — MARS adds overhead.

---

## What NOT to Do

- Do not use `DATETIME` for new columns — use `DATETIME2` (higher precision, larger range)
- Do not use `NEWID()` as a clustered PK — random UUIDs cause severe page fragmentation; use `NEWSEQUENTIALID()`
- Do not use `VARCHAR` when text may contain Unicode — use `NVARCHAR`
- Do not use `SELECT *` in views — adding columns to the base table does not automatically update the view's column list (requires `sp_refreshview`)
- Do not use cursors for row-by-row processing — rewrite as set-based operations
- Do not rely on `@@IDENTITY` — use `SCOPE_IDENTITY()` or `OUTPUT INSERTED.id` to avoid trigger interference
