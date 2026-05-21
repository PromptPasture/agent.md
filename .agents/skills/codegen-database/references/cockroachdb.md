# CockroachDB Reference

Use CockroachDB-compatible distributed SQL and call out behavior that differs from single-node PostgreSQL.

## Key Patterns

**Treat CockroachDB as distributed SQL with PostgreSQL-like syntax, not as a PostgreSQL clone.**

- **Postgres-like, not Postgres:** CockroachDB supports much PostgreSQL syntax, but extensions, functions, locking behavior, and some types differ.
- **Primary keys:** Prefer keys that avoid hot ranges. Random UUIDs are often safer than monotonic keys for write-heavy tables.
- **Transactions:** Expect serializable isolation. Add retry guidance for transaction conflicts.
- **Regional data:** Use regional tables, locality, and follower reads when geo-distribution is part of the requirement.
- **Indexes:** Use secondary indexes carefully because distributed writes pay extra coordination cost.
- **Sequences:** Avoid sequence-heavy designs for high-scale distributed writes unless the tradeoff is acceptable.

## Example

**Prefer keys and constraints that avoid distributed hot spots.**

```sql
CREATE TABLE accounts (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id  UUID NOT NULL,
    email      STRING NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT accounts_tenant_email_uq UNIQUE (tenant_id, email)
);
```
