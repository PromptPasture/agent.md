---
name: code-backend
description: You use this when the user asks to build an API endpoint, implement a service, add middleware, create a worker or queue consumer, write a migration, or produce any backend code in a real codebase. It generates production-ready code with auto-detected stack (Go, Node.js, Python, Java, Kotlin, Rust, and more), confirmed API contracts and DB schema before writing, and a P0–P3 quality checklist covering security, API correctness, observability, and performance.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "2.0.2"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: development
  tags: [codegen, backend, api, engineering]
---

# Doing Backend

Generates production-ready backend code in the project's existing stack.
Four phases: **Discover → Design → Build → Validate**. Each phase produces a confirmed output before the next begins. Phases are skippable when the user already provides the relevant context.

---

## Phase 1 — Discover

**Goal:** Identify the project stack before writing any code.

### 1.1 Read project files

Inspect the following in order. Stop reading a file once the needed signal is found.

| File | Signal to extract |
| --- | --- |
| `go.mod` | Go version; inspect imports for Gin, Echo, Fiber, Chi, or `net/http` |
| `package.json` | Node.js; inspect deps for Express, Fastify, NestJS, Hono, Nitro |
| `requirements.txt` / `pyproject.toml` / `Pipfile` | Python; inspect for FastAPI, Django, Flask |
| `pom.xml` / `build.gradle` / `build.gradle.kts` | Java/Kotlin; inspect for Spring Boot, Quarkus, Micronaut, Ktor |
| `Cargo.toml` | Rust; inspect for Axum, Actix-web, Warp |
| `go.sum` / `package-lock.json` / `poetry.lock` / `Cargo.lock` | Confirm dependency versions |
| ORM/query files | Detect GORM, sqlx, Prisma, TypeORM, SQLAlchemy, Hibernate, SeaORM, etc. |
| Migration files | Detect Flyway, Liquibase, Alembic, golang-migrate, Prisma migrations |
| Auth files | Detect JWT libs, OAuth clients, Passport, Spring Security, etc. |
| Queue/worker files | Detect BullMQ, Celery, Kafka clients, RabbitMQ, Sidekiq, etc. |
| Observability config | Detect OpenTelemetry, Prometheus, Datadog, structlog, Zap, etc. |
| `docker-compose.yml` / `docker-compose.yaml` | DB type, cache, queue services in use |

### 1.2 Output a detection summary

Present a concise summary and wait for confirmation before proceeding:

```text
Stack detected:
  Language:      <detected language and version>
  Framework:     <detected framework>
  ORM:           <detected ORM or query library>
  DB:            <detected database>
  Auth:          <detected auth library or "none">
  Queue:         <detected queue library or "none">
  Observability: <detected logging/tracing libs or "none">
  Monorepo:      yes/no
```

If the user corrects any item, update and re-confirm.

### 1.3 Empty project fallback

If no stack files are found, suggest a default stack and wait for explicit user confirmation before proceeding:

```text
No stack detected. Suggested stack:
  Language:   Go 1.22
  Framework:  net/http (stdlib)
  ORM:        sqlx
  DB:         PostgreSQL

Confirm, or tell me what stack to use instead.
```

Do not proceed to Design until the stack is confirmed.

---

## Phase 2 — Design

**Goal:** Produce confirmed API contracts, DB schema changes, and service interface signatures before any code is written.

### 2.1 Ask clarifying questions (if needed)

Before drafting contracts, resolve any ambiguity with a single focused question. Do not ask more than one question at a time. Skip this step if the user's request is already specific enough.

Common gaps to check:

- Is this a new endpoint/service or modifying an existing one?
- Where does it live in the file tree?
- What authentication/authorization does this route require?
- Are there DB schema changes (new tables, columns, indexes)?
- Any async/background work required?

### 2.2 Draft API contracts

For every endpoint added or changed, produce the contract in this format. Omit sections that are genuinely not applicable.

```text
Endpoint:   POST /api/v1/users
Auth:       Bearer token (role: admin)

Request:
  Content-Type: application/json
  Body: {
    email:    string  required  Valid email address
    name:     string  required  Display name
    role:     string  optional  Default: "viewer"
  }

Response 201:
  Content-Type: application/json
  Body: {
    id:         string  UUID
    email:      string
    name:       string
    role:       string
    created_at: string  ISO 8601
  }

Errors:
  400  { code: "VALIDATION_ERROR", message: string, fields: { field: string[] } }
  401  { code: "UNAUTHORIZED",     message: string }
  403  { code: "FORBIDDEN",        message: string }
  409  { code: "CONFLICT",         message: string }
  500  { code: "INTERNAL_ERROR",   message: string }
```

### 2.3 Draft DB schema changes

List every schema change required. Use DDL or migration pseudocode — match the project's existing migration format.

```sql
CREATE TABLE users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  name       TEXT NOT NULL,
  role       TEXT NOT NULL DEFAULT 'viewer',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users (email);
```

Omit this section if no schema changes are required.

### 2.4 Draft service interface contracts

List the service-layer signatures that back the endpoints above.

```pseudocode
UserService:
  createUser(input: CreateUserInput) → User | error
  getUser(id: string) → User | error

CreateUserInput:
  email  string  required
  name   string  required
  role   string  optional  default: "viewer"

User:
  id         string
  email      string
  name       string
  role       string
  created_at datetime
```

### 2.5 Identify concern docs to load

Load concern docs based on the task:

| Signal | Load |
| --- | --- |
| DB queries, ORM, migrations required | `references/persistence.md` |
| Auth/authz on any route | `references/auth.md` |
| Input validation at entry points | `references/validation.md` |
| Worker, queue, or background job | `references/workers.md` |
| Logging, tracing, or metrics | `references/observability.md` |
| Config or secrets management | `references/config.md` |
| Unit, integration, or contract tests required | `references/testing.md` |
| Query performance or caching concern | `references/performance.md` |
| REST design, versioning, or pagination | `references/api-design.md` |
| Security patterns beyond basic auth | `references/security.md` |
| Error handling patterns required | `references/error-handling.md` |
| No existing project conventions found | `references/conventions.md` |

### 2.6 Wait for confirmation

Present the API contracts, schema changes, and service interfaces from steps 2.2–2.4, then wait for explicit confirmation before proceeding to Build. If the user corrects any item, update and re-confirm.

---

## Phase 3 — Build

**Goal:** Write production-ready files that match the confirmed Design contracts and detected stack.

### 3.1 Load reference docs

Load every concern doc identified in Phase 2 before writing any file. Apply its guidance throughout the Build phase.

### 3.2 Apply decomposition heuristics

Before writing, state the decomposition rationale out loud. Split into smaller units when any of the following is true:

- A handler or service method exceeds ~60 lines
- A file exceeds ~300 lines
- A function has more than 4–5 parameters — group into a struct/object
- A service touches more than one domain boundary
- A piece of logic is used in more than one place

Prefer thin handlers and fat services. Do not create abstractions that exist only to satisfy a single use case.

### 3.3 File and folder conventions

Follow the project's existing conventions if present. When no convention is established, apply these defaults:

```text
internal/
  handlers/       # HTTP handler functions or controllers
  services/       # Business logic, one file per domain
  repository/     # DB access layer, one file per domain
  models/         # Domain types / entities
  middleware/     # HTTP middleware
  config/         # App config loading and validation
```

- One domain per file in `services/` and `repository/`
- Handlers delegate to services — no business logic in handlers
- Repository layer owns all DB access — no raw queries in services
- Feature folders over type folders where the project already uses them

### 3.4 Code standards

Apply these unconditionally, regardless of what exists in the project:

#### Types and safety

- No untyped boundaries — no dynamic/untyped values at service or handler edges
- Explicit return types on all exported or public functions
- Errors as typed values — no raw strings at service boundaries
- Null/nil safety: check before dereference; return explicit zero values or errors

#### Handler structure

Write handlers in this order:

1. Parse and bind request
2. Validate input (reject early, before any DB or service call)
3. Call service
4. Map service result to response
5. Write response with correct status code

#### Error handling

- Never swallow errors silently — propagate or log with context
- Return typed error responses that match the Design contract exactly
- Wrap errors with context at each layer boundary; see `references/error-handling.md`

#### Security

- Validate all inputs at the entry point before any processing
- Never log secrets, tokens, or PII
- Apply authentication and authorization checks before handler logic runs
- See `references/security.md` for patterns beyond the basics

#### Performance

- No N+1 queries — join or batch-load related data
- No unbounded queries — always apply LIMIT; add pagination where the result set can grow
- See `references/performance.md` for deeper patterns

### 3.5 Write files

Write each file in full. No placeholders, no TODOs, no stub implementations. If a piece is genuinely out of scope for this task, omit it and state why — do not leave it half-written.

After writing all files, list every file created or modified:

```text
Created:
  <handler file>
  <service file>
  <repository file>
  <model/schema file>
  <migration file>

Modified:
  <router/entry file>   (registered POST /api/v1/users)
```

Present this list and wait for the user to confirm before proceeding to Validate.

---

## Phase 4 — Validate

**Goal:** Work through every checklist item before declaring the output complete. Fix any issue found — do not report and skip.

Items are ordered by severity. P0 failures block delivery. P1–P3 failures must be resolved before closing but do not require re-confirmation from the user unless the fix changes the Design contracts.

---

### P0 — Blocking

These issues make the output insecure or broken. Stop and fix before anything else.

- [ ] Every protected route verifies authentication before handler logic runs
- [ ] Authorization (role/scope check) applied on every route that requires it
- [ ] All input validated at entry points — reject before any DB or service call
- [ ] No SQL injection: parameterized queries or ORM-safe binding used throughout
- [ ] No command injection: no `exec` / `os.system` / shell calls with user-controlled values
- [ ] No path traversal: file paths constructed from user input are sanitized and bounded
- [ ] No secrets, tokens, or PII written to logs or response bodies
- [ ] All endpoints match the confirmed API contract exactly — method, path, request schema, response schema, status codes
- [ ] No broken API contract: added, removed, or renamed fields re-confirmed with user

---

### P1 — Required

These issues violate production standards. Fix before closing.

#### Type safety

- [ ] No `any` / `interface{}` / untyped `object` at service or handler boundaries
- [ ] All exported functions have explicit return types
- [ ] Errors are typed values — not raw strings at service boundaries

#### Error handling

- [ ] Every error is either returned or logged with context — no silent discard
- [ ] Error responses match the contract shape from Design phase exactly
- [ ] All error status codes are correct and documented in the contract

#### API correctness

- [ ] All response fields present and correctly typed
- [ ] Pagination applied wherever the result set is unbounded
- [ ] Content-Type headers set correctly on all responses

---

### P2 — Expected

These issues reduce quality below senior standards. Fix before closing.

#### Observability

- [ ] Structured log entry on every request (method, path, status, latency)
- [ ] Structured log entry on every error with enough context to reproduce
- [ ] Tracing span created for every external call (DB, HTTP, queue, cache)
- [ ] Metrics recorded for request count, error rate, and latency where instrumentation exists

#### Query performance

- [ ] No N+1 queries — related data joined or batch-loaded
- [ ] No unbounded queries — LIMIT applied; pagination where result set can grow
- [ ] Missing index hints noted in migration comments where applicable

#### Boundary validation

- [ ] Input validated at service entry points as well as handler entry points
- [ ] Output sanitized before writing to external systems (DB, queue, downstream API)

#### Code quality

- [ ] No handler exceeds ~60 lines — extract to service if so
- [ ] No file exceeds ~300 lines — split by domain if so
- [ ] No logic duplicated across files that could be a shared utility or middleware

---

### P3 — Polish

Nice-to-have. Fix if the effort is small; note and defer otherwise.

- [ ] Config values are loaded from environment — no hardcoded ports, DB URLs, or secrets
- [ ] Rate limiting applied on public-facing endpoints where abuse is plausible

---

### Completion summary

After all items are resolved, output:

```text
Validate complete.

P0  ✓ all passed
P1  ✓ all passed
P2  ✓ all passed      (or: 1 deferred — [item] — [reason])
P3  ✓ all passed      (or: 1 deferred — [item] — [reason])

Files delivered:
  <handler file>
  <service file>
  <repository file>
  <model/schema file>
  <migration file>
```

If any P2 or P3 item was deferred, state the reason and confirm it is acceptable before closing.
