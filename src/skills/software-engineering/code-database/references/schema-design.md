# Schema Design

---

## Core Rules

- Design for the access pattern, not for theoretical purity
- Every table has a single-column surrogate primary key (UUID or auto-increment integer)
- Every column has a `NOT NULL` constraint unless NULL is semantically meaningful
- Foreign keys are declared at the DB level — do not rely only on application-level referential integrity
- Every foreign key column has an index

---

## Naming Conventions

| Object | Convention | Example |
| --- | --- | --- |
| Tables | `snake_case`, plural | `users`, `order_items` |
| Columns | `snake_case` | `email`, `created_at` |
| Primary key | `id` | `id UUID PRIMARY KEY` |
| Foreign key | `<referenced_table_singular>_id` | `user_id`, `order_id` |
| Indexes | `idx_<table>_<columns>` | `idx_orders_user_id` |
| Unique indexes | `uq_<table>_<columns>` | `uq_users_email` |
| Check constraints | `chk_<table>_<column>` | `chk_orders_status` |
| Enums / types | `snake_case` | `order_status`, `user_role` |

---

## Primary Keys

**UUID (preferred for distributed systems):**

```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()   -- Postgres / CockroachDB
id CHAR(36) PRIMARY KEY DEFAULT (UUID())         -- MySQL 8+
```

**Auto-increment integer (preferred for high-insert-rate, single-node):**

```sql
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY   -- SQL standard
id BIGSERIAL PRIMARY KEY                              -- Postgres shorthand
id BIGINT AUTO_INCREMENT PRIMARY KEY                  -- MySQL
```

Do not use natural keys (email, username, slug) as primary keys — they change and cause cascading updates.

---

## Column Types

Choose the narrowest type that fits:

| Use case | Postgres | MySQL | SQLite |
| --- | --- | --- | --- |
| Short text (< 255 chars) | `VARCHAR(n)` or `TEXT` | `VARCHAR(n)` | `TEXT` |
| Long text | `TEXT` | `TEXT` | `TEXT` |
| Integer (small) | `INTEGER` | `INT` | `INTEGER` |
| Integer (large) | `BIGINT` | `BIGINT` | `INTEGER` |
| Decimal (money) | `NUMERIC(19,4)` | `DECIMAL(19,4)` | `NUMERIC` |
| Boolean | `BOOLEAN` | `TINYINT(1)` | `INTEGER` (0/1) |
| UTC timestamp | `TIMESTAMPTZ` | `DATETIME(6)` | `TEXT` (ISO 8601) |
| Date only | `DATE` | `DATE` | `TEXT` |
| JSON document | `JSONB` | `JSON` | `TEXT` |
| UUID | `UUID` | `CHAR(36)` | `TEXT` |
| Binary | `BYTEA` | `BLOB` | `BLOB` |

Avoid `FLOAT` and `DOUBLE` for monetary values — use `NUMERIC`/`DECIMAL`.

---

## Constraints

Declare all constraints at the column and table level — do not rely solely on application validation:

```sql
CREATE TABLE orders (
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID        NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
  status      TEXT        NOT NULL DEFAULT 'pending',
  total_cents BIGINT      NOT NULL CHECK (total_cents >= 0),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),

  CONSTRAINT chk_orders_status CHECK (status IN ('pending', 'paid', 'cancelled', 'refunded'))
);
```

### ON DELETE behaviour

| Option | Use when |
| --- | --- |
| `RESTRICT` (default) | Child rows must be deleted first — safest default |
| `CASCADE` | Child rows should auto-delete with parent (audit logs, line items) |
| `SET NULL` | FK can be nullable; nullify when parent is deleted |
| `SET DEFAULT` | Rare — set a fallback FK value |

Prefer `RESTRICT` as the default; use `CASCADE` only when child rows are meaningless without the parent.

---

## Standard Audit Columns

Include on every table that tracks state changes:

```sql
created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
created_by  UUID        REFERENCES users(id),   -- optional: when user attribution needed
updated_by  UUID        REFERENCES users(id)    -- optional
```

Keep `updated_at` current by updating it on every `UPDATE`. In Postgres, use a trigger:

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

---

## Many-to-Many Relationships

Use a join table with its own PK and audit columns:

```sql
CREATE TABLE user_roles (
  id         UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id    UUID        NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  granted_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  granted_by UUID        REFERENCES users(id),

  CONSTRAINT uq_user_roles UNIQUE (user_id, role_id)
);

CREATE INDEX idx_user_roles_user_id ON user_roles (user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles (role_id);
```

---

## Enumerations

Prefer a `CHECK` constraint over a DB enum type for values that change:

```sql
-- Flexible: add values without a schema migration
status TEXT NOT NULL DEFAULT 'pending'
  CONSTRAINT chk_orders_status CHECK (status IN ('pending', 'paid', 'cancelled'));

-- Rigid: requires ALTER TYPE to add values (Postgres)
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'cancelled');
status order_status NOT NULL DEFAULT 'pending';
```

Use `ENUM` types only when the value set is truly stable and the engine's tooling benefits outweigh the migration cost.

---

## Multi-Tenancy

When multiple tenants share a single database, add a `tenant_id` column to every tenant-scoped table:

```sql
CREATE TABLE projects (
  id         UUID NOT NULL,
  tenant_id  UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  name       TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  PRIMARY KEY (tenant_id, id)   -- composite PK keeps tenant data clustered
);

CREATE INDEX idx_projects_tenant_id ON projects (tenant_id);
```

Always include `tenant_id` in the `WHERE` clause of every query. Row-level security (Postgres) can enforce this at the DB level.

---

## What NOT to Do

- Do not store comma-separated lists in a column — use a join table
- Do not use `TEXT` for everything — choose typed columns for numbers, booleans, and dates
- Do not store passwords in plaintext — hash at the application layer before writing
- Do not use reserved words as column or table names (`order`, `user`, `group`, `index`)
- Do not design for theoretical 3NF purity at the cost of query performance — denormalize deliberately where access patterns require it, and document why
