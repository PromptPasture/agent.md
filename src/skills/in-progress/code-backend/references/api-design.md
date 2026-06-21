# API Design — REST Conventions, Versioning, Pagination

---

## Core Rules

- Resources are plural nouns — not verbs
- HTTP methods carry the action — not the URL
- Status codes are semantic — 2xx success, 4xx client error, 5xx server error
- Every error response uses the same envelope shape
- Versioning is in the URL path — not the header

---

## URL Structure

```text
/api/{version}/{resource}/{id}/{sub-resource}

/api/v1/users
/api/v1/users/{id}
/api/v1/users/{id}/orders
/api/v1/orders/{id}/items
```

- Lowercase, hyphen-separated words: `/refresh-tokens`, not `/refreshTokens`
- No trailing slashes
- No file extensions (`.json`, `.xml`)
- No verbs: `/api/v1/users/{id}` not `/api/v1/getUser/{id}`

---

## HTTP Method Semantics

| Method | Semantics | Body | Idempotent | Safe |
| --- | --- | --- | --- | --- |
| `GET` | Fetch resource(s) | No | Yes | Yes |
| `POST` | Create resource | Yes | No | No |
| `PUT` | Replace resource (full update) | Yes | Yes | No |
| `PATCH` | Partial update | Yes | No | No |
| `DELETE` | Delete resource | No | Yes | No |

Use `POST` for actions that do not map cleanly to CRUD:

```text
POST /api/v1/orders/{id}/cancel
POST /api/v1/auth/refresh
POST /api/v1/emails/verify
```

---

## Status Codes

Use the most specific status code that applies:

| Code | Meaning | Use when |
| --- | --- | --- |
| `200 OK` | Success with body | GET, PUT, PATCH responses |
| `201 Created` | Resource created | POST creates a new resource |
| `204 No Content` | Success, no body | DELETE, action endpoints |
| `400 Bad Request` | Client error — malformed request | Invalid JSON, missing field |
| `401 Unauthorized` | No valid auth | No token or invalid token |
| `403 Forbidden` | Auth valid, insufficient permission | Token valid but wrong role |
| `404 Not Found` | Resource does not exist | ID not in DB |
| `409 Conflict` | Conflict with existing state | Duplicate unique field, optimistic lock |
| `422 Unprocessable` | Semantically invalid | Valid JSON but business rule violation |
| `429 Too Many Requests` | Rate limited | Add `Retry-After` header |
| `500 Internal Server Error` | Unexpected server error | Unhandled exception |
| `503 Service Unavailable` | Temporarily unable to serve | Add `Retry-After` header |

---

## Request and Response Shapes

### Successful single resource

```json
{
  "id":         "uuid",
  "email":      "user@example.com",
  "name":       "Jane Doe",
  "role":       "viewer",
  "created_at": "2024-06-21T12:00:00Z"
}
```

### Successful list

```json
{
  "items": [...],
  "total": 142,
  "page":  1,
  "limit": 20
}
```

Or for cursor pagination:

```json
{
  "items":       [...],
  "next_cursor": "2024-06-20T11:59:00Z",
  "has_more":    true
}
```

### Error

```json
{
  "code":    "VALIDATION_ERROR",
  "message": "Request validation failed",
  "fields": {
    "email": ["must be a valid email address"]
  }
}
```

`fields` is present only for validation errors.

---

## Versioning

Version in the URL path:

```text
/api/v1/users
/api/v2/users
```

- `v1`, `v2` — integer major versions only
- Introduce a new version when a breaking change is unavoidable
- Maintain the previous version until consumers have migrated
- Deprecate by adding a `Deprecation` and `Sunset` header to responses

Do not version via request headers or query params — URL versioning is explicit and cacheable.

---

## Pagination

### Offset Pagination

Use for admin tools and datasets that do not grow under concurrent writes.

Query params: `?page=1&limit=20` (default limit: 20, max: 100)

```json
{
  "items": [...],
  "total": 142,
  "page":  1,
  "limit": 20
}
```

### Cursor Pagination

Use for feeds and datasets that change frequently.

Query params: `?after=<cursor>&limit=20`

```json
{
  "items":       [...],
  "next_cursor": "2024-06-20T11:59:00Z",
  "has_more":    true
}
```

The cursor is opaque to the client — do not expose raw IDs or timestamps unless the sort is stable.

---

## Filtering and Sorting

Accept filters as query params:

```text
GET /api/v1/orders?status=pending&user_id=uuid&created_after=2024-01-01
GET /api/v1/users?sort=created_at:desc
```

- Whitelist allowed filter and sort fields — do not pass arbitrary column names to the DB
- Return 400 with `VALIDATION_ERROR` for unknown or disallowed query params

---

## Response Headers

Set these on every response:

```text
Content-Type:  application/json; charset=utf-8
X-Request-ID:  <request id>
```

Set these on list responses:

```text
X-Total-Count: 142
```

Set on deprecated endpoints:

```text
Deprecation: true
Sunset:      Sat, 01 Jan 2025 00:00:00 GMT
```
