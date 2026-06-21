# Security Patterns

---

## Core Rules

- Validate all input at entry points — reject before processing
- Never trust client-supplied IDs for ownership — derive identity from the verified token
- Never expose internal error details, stack traces, or SQL to clients
- Secrets never appear in code, logs, or response bodies

---

## Injection Prevention

### SQL Injection

Always use parameterized queries or ORM bindings. Never interpolate user input into query strings.

```pseudocode
-- Bad: string interpolation
query = "SELECT * FROM users WHERE email = '" + email + "'"

-- Good: parameterized
query = "SELECT * FROM users WHERE email = ?"
db.execute(query, params: [email])
```

### Command Injection

Never pass user input to shell commands. If a subprocess is required, use an argument list — not a shell string.

```pseudocode
-- Bad: shell string with user input
shell("convert " + filename)

-- Good: argument list, no shell interpreter
exec("convert", [filename])
```

Validate that `filename` is within the expected directory before use.

### Path Traversal

Never construct file paths from user input without sanitizing. Resolve to an absolute path and confirm it is within the allowed root:

```pseudocode
root = "/var/uploads"
target = resolvePath(root, userSuppliedPath)

if not target.startsWith(root + "/"):
  throw AppError { code: "FORBIDDEN", message: "Invalid path" }
```

### SSRF (Server-Side Request Forgery)

When making outbound HTTP requests with user-controlled URLs:

- Parse and validate the URL before making the request
- Block private IP ranges (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`)
- Whitelist allowed schemes (`https://` only unless HTTP is required)
- Do not follow redirects automatically for user-controlled URLs

---

## Sensitive Data

### In Transit

- Require TLS 1.2+ on all endpoints — no HTTP in production
- Use `Strict-Transport-Security` with a long `max-age` and `includeSubDomains`
- Terminate TLS at the load balancer or reverse proxy, not in application code

### At Rest

- Hash passwords with bcrypt (cost ≥ 12), Argon2id, or scrypt
- Encrypt PII columns (email, phone, SSN) using AES-256-GCM or a DB-level encryption extension
- Never store JWT access tokens — they are bearer credentials

### In Logs

Never log:

- Passwords or raw secrets
- Full JWT tokens or session IDs
- Credit card numbers or bank account numbers
- Full SSNs or government ID numbers
- Raw request bodies when they contain auth fields

---

## Rate Limiting

Apply rate limiting on all public-facing endpoints to prevent brute-force and abuse:

| Endpoint | Limit | Window |
| --- | --- | --- |
| `POST /auth/login` | 5 attempts | 15 minutes per IP |
| `POST /auth/register` | 10 requests | 1 hour per IP |
| `POST /auth/password-reset` | 3 requests | 1 hour per email |
| All other public endpoints | 100 requests | 1 minute per IP |

Return `429 Too Many Requests` with a `Retry-After` header when the limit is exceeded.

---

## Security Headers

Set these on every HTTP response:

```text
X-Content-Type-Options:   nosniff
X-Frame-Options:          DENY
Referrer-Policy:          no-referrer
Content-Security-Policy:  default-src 'none'   (for API-only services)
```

Do not set `X-Powered-By` or `Server` headers — they leak technology stack information.

---

## CSRF

CSRF applies to cookie-based auth. JWT in `Authorization` headers is not vulnerable to CSRF.

For cookie-based sessions:

- Use `SameSite=Strict` or `SameSite=Lax` on session cookies
- Require a CSRF token on all state-mutating requests (`POST`, `PUT`, `PATCH`, `DELETE`)
- Validate the CSRF token against the session before processing the request

---

## Access Control

### Route-level

Every protected route must check authentication before handler logic runs.

### Resource-level

Verify the requesting user owns or is permitted to access the resource — do not rely solely on the ID being hard to guess:

```pseudocode
resource = repo.getOrder(orderID)
if resource.userID != context.claims.userID and context.claims.role != "admin":
  throw AppError { code: "FORBIDDEN", status: 403, message: "Access denied" }
```

### Principle of Least Privilege

- DB user has only the permissions needed by the application — no superuser
- Service accounts have only the IAM roles needed — no wildcard permissions
- API keys are scoped to the minimum set of operations

---

## Dependency Security

- Keep dependencies updated; run the package manager's audit command in CI
- Pin dependency versions in lockfiles
- Review licenses and provenance of new dependencies before adding them
- Run a software composition analysis (SCA) scan in CI (e.g., Snyk, Grype, Trivy)

---

## What NOT to Do

- Do not roll your own crypto — use established libraries
- Do not return 404 when a resource exists but is forbidden — return 403
- Do not log auth tokens, even partially
- Do not expose error details from the DB, ORM, or runtime in API responses
- Do not disable TLS certificate verification in HTTP clients — even in tests
