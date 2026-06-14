# Error Handling

Every error state must be visible to the user. Never swallow errors silently.

---

## Error Boundaries

Place error boundaries at route and feature boundaries — not around every component.

```tsx
// app/dashboard/error.tsx (Next.js App Router)
'use client';

import { useEffect } from 'react';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DashboardError({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log to error reporting service
    console.error(error);
  }, [error]);

  return (
    <section role="alert" aria-live="assertive">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </section>
  );
}
```

For non-Next.js projects, use a class-based `ErrorBoundary` or a library such as `react-error-boundary`:

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function FeatureFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <section role="alert">
      <p>Failed to load: {error.message}</p>
      <button onClick={resetErrorBoundary}>Retry</button>
    </section>
  );
}

export function FeatureRoot() {
  return (
    <ErrorBoundary FallbackComponent={FeatureFallback}>
      <Feature />
    </ErrorBoundary>
  );
}
```

---

## Async Error Handling

Always handle the three states: loading, error, success.

```tsx
// Good — all three states explicit
function UserProfile({ id }: { id: string }) {
  const { data, isLoading, error } = useUserProfile(id);

  if (isLoading) return <UserProfileSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return <UserProfileView user={data} />;
}
```

Never rely on the component tree to catch async errors — catch at the call site:

```ts
// Good
async function saveUser(user: User): Promise<Result<User, ApiError>> {
  try {
    const saved = await api.users.save(user);
    return { ok: true, data: saved };
  } catch (err) {
    const error = toApiError(err);
    return { ok: false, error };
  }
}

// Bad — error propagates uncaught to the caller
async function saveUser(user: User): Promise<User> {
  return api.users.save(user);
}
```

---

## Result Type Pattern

Use a `Result` type for operations that are expected to fail:

```ts
type Result<T, E = Error> =
  | { ok: true; data: T }
  | { ok: false; error: E };
```

Prefer this over throwing for domain errors (validation failures, not-found, permission denied). Reserve thrown errors for truly unexpected conditions.

---

## Empty States

Treat empty as a distinct state — not a subset of success:

```tsx
function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <EmptyState
        icon={<CheckCircleIcon />}
        title="No tasks yet"
        description="Create your first task to get started."
        action={<CreateTaskButton />}
      />
    );
  }

  return <ul>{tasks.map(task => <TaskItem key={task.id} task={task} />)}</ul>;
}
```

---

## User-Facing Error Messages

- Use plain language — no stack traces, error codes, or technical jargon visible to users
- Always offer a recovery action (retry, go back, contact support)
- Use `role="alert"` and `aria-live="assertive"` so screen readers announce the error

```tsx
// Reusable error message component
interface ErrorMessageProps {
  error: Error | string;
  onRetry?: () => void;
}

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  const message = typeof error === 'string' ? error : error.message;

  return (
    <div role="alert" aria-live="assertive" className="error-message">
      <p>{message}</p>
      {onRetry && (
        <button onClick={onRetry} type="button">
          Try again
        </button>
      )}
    </div>
  );
}
```

---

## Toast / Notification Errors

Use toasts only for non-blocking, transient errors (e.g. a background sync failed). Always pair with a persistent fallback UI for blocking errors.

```ts
// Good — toast for background operation
async function syncData() {
  try {
    await api.sync();
  } catch (err) {
    toast.error('Sync failed. Your changes are saved locally.');
  }
}

// Bad — toast as the only signal for a blocking error
// The user may miss it; there is no recovery path visible
```

---

## Form Validation Errors

Handle at the field level, not only at submit. See `references/forms.md` for patterns.
