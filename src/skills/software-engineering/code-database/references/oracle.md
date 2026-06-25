# Oracle Database

---

## Core Rules

- Use `NUMBER`, `VARCHAR2`, and `TIMESTAMP WITH TIME ZONE` — avoid legacy `CHAR`, `DATE` (it includes time), and `LONG`
- Every table should have a surrogate PK using a sequence + default or `GENERATED AS IDENTITY` (12c+)
- Oracle identifiers are case-insensitive by default and uppercased internally — use consistent lowercase in code and quote only when necessary
- Always prefix schema name in queries when the connected user is not the table owner: `schema.table`
- Use bind variables (`:name`) in all dynamic SQL — never string-concatenate user input

---

## Data Types Reference

```sql
id          NUMBER(19)         GENERATED ALWAYS AS IDENTITY PRIMARY KEY
-- or with sequence:
id          NUMBER(19)         DEFAULT seq_users.NEXTVAL PRIMARY KEY

email       VARCHAR2(320)      NOT NULL
name        VARCHAR2(255)      NOT NULL
status      VARCHAR2(50)       DEFAULT 'pending' NOT NULL
amount      NUMBER(19,4)       NOT NULL
flag        NUMBER(1)          DEFAULT 0 NOT NULL   -- 0=false, 1=true (no BOOLEAN in Oracle < 23c)
payload     CLOB               DEFAULT '{}' NOT NULL  -- JSON as CLOB; or JSON type in 21c+
created_at  TIMESTAMP(6) WITH TIME ZONE  DEFAULT SYSTIMESTAMP NOT NULL
updated_at  TIMESTAMP(6) WITH TIME ZONE  DEFAULT SYSTIMESTAMP NOT NULL
```

Oracle 23c adds a native `BOOLEAN` type and `JSON` column type. For earlier versions use `NUMBER(1)` and `CLOB`.

---

## Sequences and Identity Columns

```sql
-- Oracle 12c+: GENERATED AS IDENTITY (preferred)
CREATE TABLE users (
  id    NUMBER(19) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email VARCHAR2(320) NOT NULL
);

-- Pre-12c: manual sequence
CREATE SEQUENCE seq_users START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE TABLE users (
  id    NUMBER(19) DEFAULT seq_users.NEXTVAL PRIMARY KEY,
  email VARCHAR2(320) NOT NULL
);
```

---

## Bind Variables (Parameterized Queries)

Oracle uses named bind variables with a `:` prefix:

```sql
-- Named bind variable
SELECT id, email FROM users WHERE email = :email;

-- In PL/SQL
EXECUTE IMMEDIATE
  'SELECT id FROM users WHERE email = :1'
  INTO v_id USING p_email;
```

Never use string concatenation in dynamic SQL:

```sql
-- NEVER: SQL injection vector
v_sql := 'SELECT id FROM users WHERE email = ''' || p_email || '''';
```

---

## Indexes

```sql
-- B-tree (default)
CREATE INDEX idx_orders_user_id ON orders (user_id);

-- Unique
CREATE UNIQUE INDEX uq_users_email ON users (email);

-- Composite
CREATE INDEX idx_orders_user_status ON orders (user_id, status, created_at DESC);

-- Function-based index (for case-insensitive search)
CREATE INDEX idx_users_email_lower ON users (LOWER(email));
SELECT id FROM users WHERE LOWER(email) = LOWER(:email);

-- Partial index via function-based (Oracle has no WHERE clause on indexes pre-12c)
-- Oracle 12c+ supports partial with invisible rows trick; use function-based approach instead

-- Online index build (no DML lock)
CREATE INDEX idx_orders_user_id ON orders (user_id) ONLINE;
```

---

## Pagination (Oracle 12c+)

```sql
-- OFFSET-FETCH (Oracle 12c+, preferred)
SELECT id, email, created_at
FROM users
ORDER BY created_at DESC
OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY;

-- ROWNUM approach (pre-12c)
SELECT * FROM (
  SELECT t.*, ROWNUM AS rn FROM (
    SELECT id, email, created_at
    FROM users
    ORDER BY created_at DESC
  ) t WHERE ROWNUM <= 60
) WHERE rn > 40;
```

---

## JSON Support (Oracle 12c+)

```sql
-- Extract scalar
SELECT JSON_VALUE(payload, '$.user_id') AS user_id FROM events;

-- Extract object
SELECT JSON_QUERY(payload, '$.address') AS address FROM users;

-- Filter (uses function-based index for performance)
SELECT * FROM events WHERE JSON_VALUE(payload, '$.type') = 'click';

-- JSON_TABLE: project JSON into relational rows
SELECT jt.user_id, jt.action
FROM events,
     JSON_TABLE(payload, '$'
       COLUMNS (
         user_id VARCHAR2(36) PATH '$.user_id',
         action  VARCHAR2(50) PATH '$.action'
       )
     ) jt;
```

---

## PL/SQL Transactions

```sql
BEGIN
  INSERT INTO orders (user_id, total_cents) VALUES (:user_id, :total_cents);
  UPDATE inventory SET quantity = quantity - :qty WHERE product_id = :product_id;
  COMMIT;
EXCEPTION
  WHEN OTHERS THEN
    ROLLBACK;
    RAISE;
END;
/
```

Oracle does not auto-commit — every session must `COMMIT` or `ROLLBACK` explicitly. JDBC/OCI drivers default to `autoCommit=false`.

---

## Migrations (Oracle-specific)

Online DDL is available but some operations require extra steps:

```sql
-- Add nullable column (fast — metadata only in 11g+)
ALTER TABLE users ADD avatar_url VARCHAR2(2048);

-- Add NOT NULL column with default (Oracle 11g+ stores default efficiently)
ALTER TABLE users ADD role VARCHAR2(50) DEFAULT 'viewer' NOT NULL;

-- Rename column (Oracle 9i+)
ALTER TABLE users RENAME COLUMN username TO display_name;

-- Online index build
CREATE INDEX idx_orders_user_id ON orders (user_id) ONLINE;

-- Check for column before adding (PL/SQL)
DECLARE
  v_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_count
  FROM user_tab_columns
  WHERE table_name = 'USERS' AND column_name = 'AVATAR_URL';

  IF v_count = 0 THEN
    EXECUTE IMMEDIATE 'ALTER TABLE users ADD avatar_url VARCHAR2(2048)';
  END IF;
END;
/
```

---

## Connection Pooling

Use UCP (Universal Connection Pool) or HikariCP for Java, or cx_Oracle session pool for Python:

|Setting|Recommended|
|---|---|
|`initialPoolSize`|2–5|
|`minPoolSize`|2|
|`maxPoolSize`|20–50|
|`connectionWaitTimeout`|30 s|
|`inactiveConnectionTimeout`|300 s|

Enable `validateConnectionOnBorrow = true` to discard stale connections caused by firewall timeouts.

---

## What NOT to Do

- Do not use `DATE` for timestamps — Oracle `DATE` includes hours/minutes/seconds but has no timezone; use `TIMESTAMP WITH TIME ZONE`
- Do not use `CHAR` for text — it pads with spaces, causing subtle comparison bugs; use `VARCHAR2`
- Do not use `LONG` or `LONG RAW` — they are deprecated; use `CLOB` / `BLOB`
- Do not use `ROWNUM` for pagination in new code — use `OFFSET … FETCH NEXT` (Oracle 12c+)
- Do not commit inside a loop — commit after the batch completes to avoid partial commits and excessive redo log pressure
- Do not use `SELECT *` — Oracle stores `ROWID` and virtual columns that may appear unexpectedly
