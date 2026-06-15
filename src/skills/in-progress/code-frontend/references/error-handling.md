# Error Handling

Every error state must be visible to the user. Never swallow errors silently. For framework-specific implementations, fetch current docs via Context7.

---

## Error Containment

Contain errors at route and feature boundaries — not around every component. This limits the blast radius: a failure in one feature does not crash the entire page.

**Placement rules:**

- One boundary per route or page
- One boundary per independently loadable feature within a page
- Never wrap every leaf component — that defeats the purpose

When an error is caught at a boundary, always provide:

1. A human-readable message explaining what failed
2. A recovery action (retry, reload, go back, contact support)
3. A screen-reader announcement (`role="alert"`)

---

## Async Error Handling

Always handle three states explicitly: **loading**, **error**, **success**. A missing error or loading state is a bug, not an acceptable default.

**Principles:**

- Catch at the call site — never rely on the component tree to surface async errors
- Return errors as values for expected failures; throw only for truly unexpected conditions
- Do not let an unhandled promise rejection reach the user as a blank screen

**Result type pattern** — use for operations that are expected to fail:

```ts
type Result<T, E = Error> =
  | { ok: true;  data: T }
  | { ok: false; error: E };
```

Use `Result` for domain errors (validation failures, not-found, permission denied). Reserve thrown errors for programmer mistakes and unrecoverable conditions.

```ts
// Good — error is a value, caller decides what to do
async function saveUser(user: User): Promise<Result<User, ApiError>> {
  try {
    const saved = await api.users.save(user);
    return { ok: true, data: saved };
  } catch (err) {
    return { ok: false, error: toApiError(err) };
  }
}

// Bad — error propagates uncaught; caller has no typed signal
async function saveUser(user: User): Promise<User> {
  return api.users.save(user);
}
```

---

## Empty States

Treat empty as a distinct state — not a subset of success. An empty list after a successful fetch is different from a list that has not loaded yet.

**Every empty state must include:**

- A clear explanation of why it is empty
- A primary action to move forward (create, import, invite, etc.)

```
States to handle explicitly:
  loading  → skeleton or spinner
  error    → error message + retry
  empty    → empty state + primary action
  success  → content
```

---

## User-Facing Error Messages

- Plain language — no stack traces, error codes, or internal identifiers visible to users
- Always offer a recovery action — never a dead end
- Announce errors to screen readers via `role="alert"` or `aria-live="assertive"`
- Distinguish recoverable errors ("Try again") from unrecoverable ones ("Contact support")

---

## Toast / Notification Errors

Use toasts only for **non-blocking, transient** errors (e.g. a background sync failed, a non-critical action timed out). Always pair with a persistent fallback UI for blocking errors.

```
Good use of toast:
  Background sync failed → toast("Sync failed. Changes saved locally.")

Bad use of toast:
  Form submission failed → toast only (user may miss it; no recovery path visible)
  Page failed to load → toast only (content is gone; user is stuck)
```

---

## Form Validation Errors

Handle at the field level, not only at submit. See `references/forms.md` for patterns.
