# Input Validation

---

## Core Rules

- Validate at the entry point — reject before any service or DB call
- Validate again at service boundaries when input crosses a trust boundary
- Never trust data arriving from external systems (HTTP, queue, webhook)
- Return all validation errors in one response — do not fail-fast on the first field

---

## Validation Checklist

For every input field, check:

- [ ] Present (required fields)
- [ ] Correct type (string, number, boolean, etc.)
- [ ] Within bounds (min/max length, min/max value, allowed enum values)
- [ ] Correct format (email, UUID, ISO 8601 date, phone number)
- [ ] Safe content (no null bytes, no control characters in string fields)

---

## Validation Error Shape

Collect all field errors and return them together:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "fields": {
    "email": ["must be a valid email address"],
    "name":  ["must not be blank", "must not exceed 100 characters"]
  }
}
```

---

## Handler Validation Pattern

```pseudocode
function createUser(request):
  input = parseJSON(request.body)
  if parseError:
    return 400, { code: "VALIDATION_ERROR", message: "Invalid request body" }

  errors = validate(input, rules: {
    email: [required, format:email],
    name:  [required, minLength:1, maxLength:100],
    role:  [optional, oneOf:["admin","viewer","editor"]]
  })

  if errors not empty:
    return 400, { code: "VALIDATION_ERROR", message: "Validation failed", fields: errors }

  return service.createUser(input)
```

Use the validation library available in the project's stack. The pattern — parse, validate, collect all errors, reject before calling the service — is the same regardless of library.

---

## Sanitization

After validation, sanitize before use:

- **SQL:** Always use parameterized queries or ORM bindings — never string interpolation
- **File paths:** Resolve to an absolute path and confirm it is within the allowed directory
- **HTML:** If storing user content that will be rendered, strip tags at write time — never at read time
- **URLs:** Parse and validate the scheme before making outbound requests or storing
- **Email:** Normalize to lowercase before storage and lookup

---

## What NOT to Do

- Do not rely on the DB to catch missing required fields — validate before the query
- Do not silently coerce invalid types — return an error
- Do not truncate oversized input — reject it
- Do not log raw request bodies — they may contain secrets or PII
