# Backend Code Conventions

Apply these when no existing project conventions are found. When conventions exist, follow them instead.

---

## Project Layout

Organize by layer, then by domain:

```text
src/
  handlers/       # HTTP handlers (thin — parse, validate, delegate, respond)
  services/       # Business logic (fat — owns domain rules)
  repository/     # DB access (owns all queries)
  models/         # Domain types, entities, DTOs
  middleware/     # HTTP middleware (auth, logging, rate limiting)
  workers/        # Background jobs and queue consumers
  config/         # Config loading and validation
  main            # Entry point — wire dependencies, start server
db/
  migrations/     # SQL migration files
```

Feature folders override layer folders when a domain is large enough to warrant its own subtree:

```text
src/
  users/
    handler
    service
    repository
    model
```

---

## Naming

|Artifact|Convention|Example|
|---|---|---|
|Types / classes|`PascalCase`|`UserService`|
|Functions / methods|Follow language convention|`createUser`, `CreateUser`, `create_user`|
|Constants|`UPPER_SNAKE_CASE`|`MAX_PAGE_SIZE`|
|DB tables|`snake_case`, plural|`users`, `refresh_tokens`|
|DB columns|`snake_case`|`created_at`, `user_id`|
|Endpoints|`kebab-case`, plural nouns|`/api/v1/users`, `/api/v1/refresh-tokens`|

---

## Handler Conventions

Handlers are thin. The only logic in a handler:

1. Parse and bind the request (path params, query params, body)
2. Validate input — reject early with a 400 before calling any service
3. Call the service
4. Map the result to the response shape
5. Write the response with the correct status code

No business logic. No DB calls. No conditional branching on domain rules.

---

## Service Conventions

Services own domain logic. Each service:

- Depends on a repository interface (not a concrete type) — allows testing without a real DB
- Returns domain types plus a typed error — never raw strings
- Never accesses HTTP context directly
- Is stateless — all state lives in the repository or the DB

---

## Repository Conventions

Repositories own all DB access:

- Named after the table or aggregate: `UserRepository`, `OrderRepository`
- Accept a cancellation context as the first argument on every method
- Return domain models, not raw DB rows
- Never contain business logic — only query, insert, update, delete

---

## Error Conventions

Use a consistent error type at service boundaries:

```pseudocode
AppError:
  code    string   -- machine-readable: "NOT_FOUND", "VALIDATION_ERROR"
  message string   -- human-readable, safe to expose to clients
  status  integer  -- HTTP status to map to at the handler layer
```

Map `AppError` to HTTP responses in the handler, not in the service. Service errors are domain errors; HTTP is the transport.

---

## File Size Limits

- Handler file: one handler group per file; ~60 lines per handler method
- Service file: one domain per file; split when the file exceeds ~300 lines
- Repository file: one domain per file; split when the file exceeds ~300 lines

---

## Exports

- Export only what callers need — keep internal helpers private
- Group exports by type: types first, then constructors, then methods
