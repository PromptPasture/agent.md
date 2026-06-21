# Data Fetching

Choose the fetching layer that matches the detected stack. Apply it consistently — do not mix patterns within a single feature.

---

## Choosing a Strategy

| Context | Preferred approach |
| --- | --- |
| Next.js App Router | Server Components + `fetch` with cache options |
| Next.js Pages Router | `getServerSideProps` / `getStaticProps` + client library |
| SvelteKit | `load` in `+page.server.ts` / `+page.ts` |
| Nuxt | `useFetch` / `useAsyncData` |
| Astro | `fetch` in frontmatter for static; API routes for dynamic |
| Remix | `loader` / `action` functions |
| Vite SPA | Client fetching library (React Query, SWR, TanStack Query) |

**Prefer server fetching over client fetching** when the framework supports it — it reduces client bundle size, eliminates loading flicker, and keeps sensitive logic off the client.

---

## Core Principles

### Always handle three states

Every data dependency must render three states explicitly — missing one is a bug:

```
loading → skeleton or spinner
error   → error message + retry action
success → content
```

Never let undefined data reach the rendering layer. Guard at the top of the component or route handler.

### Never fetch directly in a component

Route all fetch calls through a typed API module. Components should not know about URLs, headers, or response shapes.

```ts
// api/users.ts — the only place that knows the endpoint
import { api } from '@/lib/api-client';
import type { User, UpdateUserInput } from '@/types/user.types';

export const fetchUser = (id: string): Promise<User> =>
  api.get(`/users/${id}`);

export const updateUser = (input: UpdateUserInput): Promise<User> =>
  api.patch(`/users/${input.id}`, input);
```

The API client centralises base URL, auth headers, error normalisation, and response parsing. Components import from `api/`, never from `fetch`.

### Use an explicit cache strategy

Never leave caching to chance. For every data dependency, decide:

| Question | Decision |
| --- | --- |
| How stale can this data be? | Set a `staleTime` or `revalidate` interval |
| Should this refetch on window focus? | Explicit on/off |
| Does a mutation invalidate this? | Explicit invalidation or cache update |

---

## Loading States

Prefer skeletons over spinners for content-shaped data — a skeleton that matches the content dimensions prevents layout shift and sets the user's expectation correctly.

```
Content-shaped (list, card, table) → skeleton matching the layout
Indeterminate background operation → spinner with aria-label
Full page navigation → framework router loading indicator
```

Skeleton components must match the dimensions and layout of the loaded content. A mismatched skeleton is worse than a spinner.

---

## Optimistic Updates

Apply optimistic updates when:

- The operation is low-risk (edit, toggle, reorder)
- The expected result is predictable from the input alone
- A rollback on failure is straightforward

**Never apply to destructive operations** (delete, payment, publish, send) — the cost of a failed rollback is too high.

Required parts of every optimistic update:

1. Apply the expected result to local state immediately
2. Fire the real request
3. On success: confirm or reconcile with the server response
4. On failure: roll back to the previous state and surface an error

---

## Cancellation and Cleanup

Cancel in-flight requests when a component unmounts or its inputs change. Leaving requests running after unmount causes state updates on unmounted components and can produce race conditions.

Use `AbortController` — supported natively in all modern browsers and Node.js:

```ts
// Framework-agnostic cancellation
async function loadUser(id: string, signal: AbortSignal): Promise<User> {
  const res = await fetch(`/api/users/${id}`, { signal });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

// Usage — caller owns the controller
const controller = new AbortController();
loadUser(id, controller.signal).catch(err => {
  if (err.name === 'AbortError') return; // expected — ignore
  handleError(err);
});

// Cancel when no longer needed
controller.abort();
```

Client fetching libraries (React Query, SWR, TanStack Query) handle cancellation automatically when query keys change.
