# Data Fetching

Choose the fetching layer that matches the detected stack. Apply it consistently — do not mix patterns within a single feature.

---

## Choosing a Strategy

| Context | Preferred approach |
| --- | --- |
| Next.js App Router | Server Components + `fetch` with cache options |
| Next.js Pages Router | `getServerSideProps` / `getStaticProps` + React Query for client |
| SvelteKit | `load` functions in `+page.server.ts` / `+page.ts` |
| Nuxt | `useFetch`, `useAsyncData` |
| Astro | `fetch` in frontmatter for static; API routes for dynamic |
| Remix | `loader` / `action` functions |
| Vite + React (SPA) | React Query or SWR |

---

## React Query

Preferred client-side fetching library for React projects without a full-stack framework fetching layer.

### Query

```ts
// hooks/useUser.ts
import { useQuery } from '@tanstack/react-query';
import { fetchUser } from '@/api/users';
import type { User } from '@/types/user.types';

export function useUser(id: string) {
  return useQuery<User, Error>({
    queryKey: ['users', id],
    queryFn: () => fetchUser(id),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}
```

### Mutation

```ts
// hooks/useUpdateUser.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { updateUser } from '@/api/users';
import type { User, UpdateUserInput } from '@/types/user.types';

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation<User, Error, UpdateUserInput>({
    mutationFn: updateUser,
    onSuccess: (updated) => {
      queryClient.setQueryData(['users', updated.id], updated);
    },
    onError: (error) => {
      // Surface via toast or inline — never swallow
      console.error('Update failed:', error.message);
    },
  });
}
```

### Key conventions

- Query keys are arrays — `['users', id]` not `'users/' + id`
- Set explicit `staleTime` — never rely on default (0) in production
- Invalidate or update cache in `onSuccess` — do not rely on refetch
- Wrap mutations in a custom hook; never call `useMutation` in a component directly

---

## SWR

Lighter alternative for simple read-heavy cases.

```ts
import useSWR from 'swr';
import { fetcher } from '@/lib/fetcher';
import type { User } from '@/types/user.types';

export function useUser(id: string) {
  const { data, error, isLoading } = useSWR<User>(
    `/api/users/${id}`,
    fetcher,
    { revalidateOnFocus: false }
  );

  return { data, error, isLoading };
}

// lib/fetcher.ts
export async function fetcher<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Fetch failed: ${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}
```

---

## Next.js Server Components

Fetch on the server by default. No loading state needed — use `Suspense` and `loading.tsx` for streaming.

```tsx
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation';
import { fetchUser } from '@/api/users';

interface PageProps {
  params: { id: string };
}

export default async function UserPage({ params }: PageProps) {
  const user = await fetchUser(params.id).catch(() => null);

  if (!user) notFound();

  return <UserProfile user={user} />;
}

export async function generateMetadata({ params }: PageProps) {
  const user = await fetchUser(params.id).catch(() => null);
  return { title: user ? `${user.name} — MyApp` : 'User not found' };
}
```

Cache control:

```ts
// Static — cached indefinitely (default)
fetch(url);

// Revalidate every 60 seconds
fetch(url, { next: { revalidate: 60 } });

// No cache — always fresh
fetch(url, { cache: 'no-store' });
```

---

## Loading States

Always render a skeleton, not a spinner, for content-shaped loading:

```tsx
// Good — skeleton matches the content shape
if (isLoading) return <UserCardSkeleton />;

// Acceptable — spinner for indeterminate background operations only
if (isLoading) return <Spinner aria-label="Loading user" />;
```

Skeleton components must match the dimensions and layout of the loaded content to prevent layout shift.

---

## Optimistic Updates

Apply when the operation is low-risk and the expected result is predictable:

```ts
onMutate: async (input) => {
  await queryClient.cancelQueries({ queryKey: ['users', input.id] });
  const previous = queryClient.getQueryData<User>(['users', input.id]);
  queryClient.setQueryData(['users', input.id], { ...previous, ...input });
  return { previous };
},
onError: (_err, input, context) => {
  // Roll back on failure
  queryClient.setQueryData(['users', input.id], context?.previous);
},
```

Do not apply optimistic updates to destructive operations (delete, payment, publish).

---

## Cancellation and Cleanup

Cancel in-flight requests when a component unmounts or query key changes:

```ts
// Native fetch with AbortController (useEffect pattern)
useEffect(() => {
  const controller = new AbortController();

  async function load() {
    try {
      const data = await fetchUser(id, { signal: controller.signal });
      setUser(data);
    } catch (err) {
      if ((err as Error).name !== 'AbortError') setError(err as Error);
    }
  }

  load();
  return () => controller.abort();
}, [id]);
```

React Query and SWR handle cancellation automatically when query keys change.

---

## API Layer

Never call `fetch` directly from a component or hook. Route through a typed API module:

```ts
// api/users.ts
import { api } from '@/lib/api-client';
import type { User, UpdateUserInput } from '@/types/user.types';

export const fetchUser = (id: string): Promise<User> =>
  api.get(`/users/${id}`);

export const updateUser = (input: UpdateUserInput): Promise<User> =>
  api.patch(`/users/${input.id}`, input);
```

The API client handles base URL, auth headers, error normalisation, and response parsing in one place.
