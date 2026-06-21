# Backend Error Handling

---

## Core Rules

- Never silently discard an error — propagate it or log it with context, never both
- Wrap errors with context at each layer boundary so the chain is readable at the top
- Return typed errors from services; map to HTTP status codes in handlers
- Error responses must match the API contract exactly

---

## Error Type

Define a single application error type used throughout the service layer:

```pseudocode
AppError:
  code    string   -- machine-readable constant: "NOT_FOUND", "CONFLICT", "FORBIDDEN"
  message string   -- human-readable; safe to send to clients
  cause   error    -- original error; logged but never sent to client
  status  integer  -- HTTP status code to use in the response

methods:
  error()  → string   -- returns message
  unwrap() → error    -- returns cause (for error chain inspection)
```

---

## Error Response Shape

Every error response uses the same envelope:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Email is required",
  "fields": {
    "email": ["must not be blank"]
  }
}
```

- `code` — machine-readable constant; stable across versions
- `message` — human-readable; never contains internal stack traces or SQL
- `fields` — present only for validation errors; maps field names to error lists

---

## Layer Responsibilities

| Layer | Responsibility |
| --- | --- |
| Handler | Map `AppError` → HTTP status + JSON body; log unexpected (5xx) errors |
| Service | Return `AppError` for domain failures; wrap lower-layer errors with context |
| Repository | Return `AppError` for DB failures (not found, constraint violation); wrap driver errors |

The handler is the only place that touches HTTP. Services and repositories never write HTTP responses.

---

## Wrapping Errors

Wrap with context at each boundary so the log chain is complete:

```pseudocode
// at each layer boundary, wrap the error with the operation name
error = wrap("UserService.CreateUser", cause)
```

The wrapper preserves the original error for logging while adding context for tracing the call path.

---

## Handler Error Mapping

```pseudocode
function handleError(response, error):
  if error is AppError:
    writeJSON(response, error.status, { code: error.code, message: error.message })
  else:
    -- Unexpected error: log internally, return generic 500
    log.error("unexpected error", error)
    writeJSON(response, 500, { code: "INTERNAL_ERROR", message: "An unexpected error occurred" })
```

Centralise this logic in a single error-handling middleware or helper — do not repeat it in every handler.

---

## Common Error Codes

| Code | Status | When to use |
| --- | --- | --- |
| `VALIDATION_ERROR` | 400 | Input fails schema or business rule validation |
| `UNAUTHORIZED` | 401 | No valid auth token present |
| `FORBIDDEN` | 403 | Token valid but insufficient permission |
| `NOT_FOUND` | 404 | Resource does not exist |
| `CONFLICT` | 409 | Unique constraint violation, optimistic lock conflict |
| `UNPROCESSABLE` | 422 | Semantically invalid but structurally correct input |
| `INTERNAL_ERROR` | 500 | Unexpected failure — never expose cause to client |

---

## What Never Goes in an Error Response

- Stack traces
- SQL query text or table names
- Internal error messages from drivers or ORMs
- Secrets, tokens, or PII
- File paths or internal service names
