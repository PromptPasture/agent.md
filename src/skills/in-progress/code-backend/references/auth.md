# Auth and Authorization

---

## Core Rules

- Authentication (who are you?) is verified in middleware — before any handler logic
- Authorization (are you allowed?) is verified at the start of the handler or service — before any data access
- Never mix auth logic with business logic
- Reject unauthenticated requests with 401; authorized but insufficient permission with 403

---

## Authentication Patterns

### JWT (stateless)

Verify the token signature and claims in middleware. Attach the parsed claims to the request context.

```pseudocode
middleware jwtAuth(request, next):
  header = request.headers["Authorization"]
  if header is missing or does not start with "Bearer ":
    return 401, { code: "UNAUTHORIZED", message: "Missing or invalid Authorization header" }

  claims = verifyJWT(token: header.removePrefix("Bearer "))
  if verifyError:
    return 401, { code: "UNAUTHORIZED", message: "Invalid or expired token" }

  request.context.claims = claims
  return next(request)
```

### Session (stateful)

Load the session from the session store in middleware. Verify the session is active and not expired. Attach the user ID to the request context. Rotate the session ID after login and after privilege escalation.

### API Keys

Compare the key from the `Authorization` header (or `X-API-Key`) against a hashed value stored in the DB. Never store plaintext API keys. Use a constant-time comparison to prevent timing attacks.

---

## Authorization Patterns

### Role-based (RBAC)

Check the role from the parsed token/session before any data access:

```pseudocode
function requireRole(context, requiredRole):
  claims = context.claims
  if claims is missing or claims.role != requiredRole:
    throw AppError { code: "FORBIDDEN", message: "Insufficient permissions", status: 403 }
```

### Resource ownership

Verify the requesting user owns the resource before returning or modifying it:

```pseudocode
resource = repo.getOrder(id)
if resource.userID != context.claims.userID:
  throw AppError { code: "FORBIDDEN", message: "Access denied", status: 403 }
```

### Scope-based (OAuth)

Check the `scope` claim in the token against the required scope for the operation:

```pseudocode
if "orders:write" not in context.claims.scopes:
  throw AppError { code: "FORBIDDEN", message: "Insufficient scope", status: 403 }
```

---

## Token Security

- Set short expiry on access tokens (15 min – 1 hour)
- Use refresh tokens for long-lived sessions; rotate refresh tokens on use
- Store refresh tokens hashed in the DB
- Set `Secure; HttpOnly; SameSite=Strict` on session and refresh token cookies
- Never log tokens or include them in error responses
- Validate `iss`, `aud`, `exp`, and `nbf` claims on every JWT

---

## Password Handling

- Hash with bcrypt (cost ≥ 12), Argon2id, or scrypt — never MD5, SHA-1, or unsalted SHA-256
- Never store plaintext passwords
- Never log passwords
- Apply rate limiting on login endpoints to slow brute-force attacks

---

## OAuth / OIDC (third-party auth)

- Validate the `state` parameter to prevent CSRF on the callback
- Verify the `id_token` signature against the provider's JWKS endpoint
- Use PKCE when the client is a browser or mobile app
- Store only the stable provider subject ID (`sub`) — not the access token

---

## What NOT to Do

- Do not check auth inside repository methods. Auth lives above the data layer.
- Do not return 404 when the resource exists but is forbidden. Return 403.
- Do not expose user IDs as sequential integers. Use UUIDs or opaque slugs.
- Do not trust client-supplied user IDs. Always derive identity from the verified token or session.
