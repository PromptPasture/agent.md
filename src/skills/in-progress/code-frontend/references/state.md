# State Management

Choose the simplest state solution that covers the need. Add complexity only when a simpler tool genuinely cannot do the job. For framework-specific implementations, fetch current docs via Context7.

---

## Decision Tree

```
Is the state used by only one component?
  └─ Yes → Local reactive primitive (useState, ref, local store)

Is the state shared between a few nearby components?
  └─ Yes → Lift to the nearest common ancestor

Is the state server data (fetched, cached, synchronised)?
  └─ Yes → Framework data layer (see references/data-fetching.md)

Is the state shared across distant components or the whole app?
  └─ Yes → Is it simple (a few values, infrequent updates)?
              └─ Yes → Framework context / provide-inject / shared store
            Is it complex (many slices, frequent updates, devtools needed)?
              └─ Yes → Dedicated state library (Zustand, Pinia, Jotai, NgRx)
```

---

## Local State

Default for component-scoped state that does not need to be shared. Keep state as close to where it is used as possible.

**Principles:**

- Keep independent values in separate reactive primitives — do not bundle unrelated state into one object
- Group values that always change together into a single object
- When next state depends on previous state, always derive it from the current value — never read stale state

For framework-specific primitives (`useState`, `ref`/`reactive`, Svelte runes), fetch current docs via Context7.

---

## Complex Local State — State Machines

Use a reducer or state machine pattern when component state has multiple sub-values with defined transitions — particularly for async sequences (idle → loading → success | error).

**When to use:**

- State logic is scattered across many event handlers
- Invalid state combinations are possible and need to be prevented
- The same transition (e.g. reset) must fire from multiple places

**Structure:**

- Define a closed set of states (e.g. `idle | loading | success | error`)
- Define a closed set of actions
- Each action maps exactly one state to a next state — no implicit transitions

```ts
// Framework-agnostic shape — implement with the framework's reducer or store
type State =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: User }
  | { status: 'error'; error: string };

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; payload: string }
  | { type: 'RESET' };
```

For framework-specific reducer implementations (`useReducer`, Svelte stores with update functions), fetch current docs via Context7.

---

## Shared State — Context / Provide-Inject

Use for low-frequency global values: theme, locale, authenticated user, feature flags.

**Do not use for high-frequency updates** (mouse position, scroll position, form fields) — every consumer re-evaluates on every change.

**Rules:**

- Always wrap the raw context in a typed accessor function — never expose it directly
- Throw a clear error if the accessor is called outside the provider
- Split contexts by update frequency — read-only values and write actions should be separate so reading one does not cause re-evaluation when the other changes

For framework-specific context APIs (`createContext`/`useContext`, `provide`/`inject`, Svelte context), fetch current docs via Context7.

---

## Global State — Dedicated Libraries

Use when shared state is too complex for context or updates too frequently for it to be performant.

**Choosing a library:**

| Need | Library |
| --- | --- |
| React — simple global store | Zustand |
| React — atomic subscriptions | Jotai |
| React — large app, team conventions | Redux Toolkit |
| Vue / Nuxt | Pinia |
| Svelte | Svelte stores (built-in) |
| Any framework | Nano Stores (framework-agnostic) |

**Slice pattern for large stores** — split by domain, compose into one store:

```
store/
  slices/
    uiSlice.ts       → sidebar, modals, toasts
    cartSlice.ts     → items, totals, checkout state
  useAppStore.ts     → composed store
```

For framework-specific store implementations, fetch current docs via Context7.

---

## URL State

Treat the URL as state for anything the user should be able to bookmark, share, or navigate back to.

**Use URL state for:**

- Filters, sort order, search query
- Pagination (current page, page size)
- Selected tab or panel
- Modal open/closed (when linkable)

**Principles:**

- Parse URL params defensively — always provide a default for missing or invalid values
- Reset pagination when filters change
- Use `URLSearchParams` to build and update query strings — never string-concatenate

```ts
// Framework-agnostic URLSearchParams update
function setParam(key: string, value: string): string {
  const params = new URLSearchParams(window.location.search);
  params.set(key, value);
  if (key !== 'page') params.set('page', '1'); // reset pagination
  return `?${params.toString()}`;
}
```

For framework-specific router integration (`useSearchParams`, SvelteKit `$page.url`, Vue Router `query`), fetch current docs via Context7.

---

## Framework Reference

| Framework | Local | Shared | Global library |
| --- | --- | --- | --- |
| React | `useState` / `useReducer` | Context | Zustand / Jotai / Redux Toolkit |
| SvelteKit | Runes (`$state`) | Svelte context | Svelte stores (built-in) |
| Nuxt / Vue | `ref` / `reactive` | `provide` / `inject` | Pinia |
| Remix | `useState` | Context | Zustand |
| Astro | Component state | Nano Stores | Nano Stores |

---

## Common Mistakes

```
❌ Deriving state from props on initialisation — gets out of sync when props change
✅ Derive directly in the render/template; memoize only if the computation is expensive

❌ Storing server data in local state with a manual fetch in a lifecycle hook
✅ Use the framework's data layer or a fetching library — see references/data-fetching.md

❌ Using context/provide-inject for high-frequency values (mouse position, scroll)
✅ Use a ref or a dedicated high-frequency state library

❌ One giant global store for everything
✅ Split by domain; keep unrelated state in separate stores or local state
```
