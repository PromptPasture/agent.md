# Persistence — ORM, Queries, Migrations

---

## Core Rules

- All DB access lives in the repository layer. No raw queries in services or handlers.
- Always use parameterized queries or ORM bindings. Never use string interpolation.
- Every query accepts a cancellation context to enable timeout and cancellation.
- Migrations are the source of truth for schema. No DDL outside migration files.

---

## Repository Interface

Define an interface in the service layer; the concrete implementation lives in `repository/`:

```pseudocode
interface UserRepository:
  create(input: CreateUserInput) → User | error
  getByID(id: string) → User | error
  getByEmail(email: string) → User | error
  update(id: string, input: UpdateUserInput) → User | error
  delete(id: string) → error
  list(filter: UserFilter) → { items: User[], total: integer } | error
```

The service depends on the interface, not the concrete type — this allows testing with a mock repository.

---

## Query Patterns

### Parameterized queries (raw SQL)

```sql
-- Always list columns explicitly; never SELECT *
SELECT id, email, name, role, created_at
FROM users
WHERE id = ?            -- use the placeholder syntax for your DB driver ($1, ?, :id)
```

```pseudocode
// In application code
user = db.queryOne(
  "SELECT id, email, name, role, created_at FROM users WHERE id = ?",
  params: [id]
)
if notFound:
  throw AppError { code: "NOT_FOUND", status: 404, message: "User not found" }
```

### ORM queries

```pseudocode
// Use ORM bindings — never interpolate user input into query strings
user = orm.users.findOne(where: { id: id })
if not found:
  throw AppError { code: "NOT_FOUND", status: 404, message: "User not found" }
```

### Pagination

Always paginate unbounded queries. Use cursor-based pagination for large or frequently-updated sets; offset-based for admin/internal tools.

```sql
-- Offset pagination (simple)
SELECT ... FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?

-- Cursor pagination (scalable)
SELECT ... FROM users WHERE created_at < ? ORDER BY created_at DESC LIMIT ?
```

Return total count alongside items only when required — it adds a separate COUNT query cost.

---

## N+1 Prevention

Never load related records in a loop. Join or batch-load instead:

```pseudocode
-- Bad: triggers one query per order
for each order in orders:
  order.user = repo.getUser(order.userID)   -- N extra queries
```

```sql
-- Good: single JOIN
SELECT orders.*, users.email, users.name
FROM orders
JOIN users ON users.id = orders.user_id
WHERE orders.status = ?
```

---

## Migrations

- One migration file per schema change
- File names include timestamp and description: `20240621_create_users.sql`
- Migrations are irreversible by default — write a down migration only if rollback is needed
- Never modify a migration that has been applied to production — create a new one

```sql
-- 20240621_create_users.sql
CREATE TABLE users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  name       TEXT NOT NULL,
  role       TEXT NOT NULL DEFAULT 'viewer',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users (email);
```

---

## Connection Pool

Set pool size explicitly — do not rely on defaults in production:

| Setting | Recommended starting value |
| --- | --- |
| Max open connections | `(num_cores × 2) + effective_spindle_count` or start at 10–25 |
| Max idle connections | Half of max open |
| Connection max lifetime | 5–30 minutes |
| Connection max idle time | 5 minutes |

Log pool exhaustion events and add a metric so you can tune under load.

---

## Transactions

Wrap multi-step writes in a transaction. Always roll back on error:

```pseudocode
transaction = db.beginTransaction()
try:
  insertUser(transaction, user)
  insertAuditLog(transaction, event)
  transaction.commit()
catch error:
  transaction.rollback()
  throw error
```

---

## Soft Deletes

Add a `deleted_at` timestamp column when records must be retained for audit or recovery. Filter `WHERE deleted_at IS NULL` in all standard queries. Create a partial index on `deleted_at` when the table is large.

---

## What NOT to Do

- Do not use `SELECT *` in application queries. List columns explicitly.
- Do not load entire tables into memory for processing. Stream or paginate.
- Do not put retry logic inside the repository. Retry at the service or handler level.
- Do not swallow not-found errors. Surface them as a typed `NOT_FOUND` error.
