# Preact — Framework Adapter

Preact is a 3KB React-compatible alternative with the same API. Use `preact/compat` for full React ecosystem compatibility. Read `react.md` first — this adapter covers only what differs from React.

---

## Conventions

Identical to React — same hook naming, file structure, props patterns. See `references/frameworks/react.md`.

File extensions: `.tsx` / `.ts`.

---

## Setup

### Vite + Preact

```bash
npm create vite@latest my-app -- --template preact-ts
```

### Preact with React compatibility (preact/compat)

Use when adopting React libraries (React Query, React Hook Form, Framer Motion, shadcn/ui):

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [preact()],
  resolve: {
    alias: {
      'react':     'preact/compat',
      'react-dom': 'preact/compat',
      'react/jsx-runtime': 'preact/jsx-runtime',
    },
  },
});
```

With `preact/compat` enabled, all React libraries work without modification.

---

## Signals — @preact/signals

Preact ships its own signal primitive — finer-grained than React's useState, no re-render of the full component.

```ts
import { signal, computed, effect, batch } from '@preact/signals';

// Global signals — live outside components
const count   = signal(0);
const doubled = computed(() => count.value * 2);

effect(() => { console.log('Count:', count.value); });

// Update
count.value++;
count.value = 10;

// Batch
batch(() => { count.value = 5; name.value = 'Alice'; });
```

```tsx
import { signal } from '@preact/signals';

const cartCount = signal(0);

// Signals used directly in JSX — only that text node re-renders
function CartBadge() {
  return <span>{cartCount}</span>; // no .value needed in JSX
}

// Signals in hooks — use @preact/signals/react for compat mode
import { useSignal, useComputed } from '@preact/signals';

function Counter() {
  const count  = useSignal(0);
  const double = useComputed(() => count.value * 2);
  return <button onClick={() => count.value++}>{count} × 2 = {double}</button>;
}
```

---

## Key Differences from React

| Concern | React | Preact |
| --- | --- | --- |
| Bundle size | ~45KB (min+gz) | ~3KB (min+gz) |
| Signals | `@preact/signals` (opt-in) | `@preact/signals` (native) |
| Concurrent Mode | ✓ (React 18+) | ✗ |
| `useId` | ✓ | ✓ (Preact 10.11+) |
| `useDeferredValue` | ✓ | ✗ |
| `useTransition` | ✓ | ✗ |
| Server Components | ✓ (Next.js) | ✗ |
| `startTransition` | ✓ | ✗ |

Avoid React 18+ concurrent features (`useTransition`, `useDeferredValue`, `startTransition`) — they are not implemented in Preact.

---

## Error Handling

```tsx
import { Component } from 'preact';
import type { ComponentChildren } from 'preact';

interface Props { children: ComponentChildren; fallback?: (err: Error, reset: () => void) => ComponentChildren; }
interface State { error: Error | null; }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State { return { error }; }

  reset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      return this.props.fallback?.(this.state.error, this.reset) ?? (
        <section role="alert">
          <p>{this.state.error.message}</p>
          <button onClick={this.reset}>Retry</button>
        </section>
      );
    }
    return this.props.children;
  }
}
```

---

## Performance

### Signals over useState for frequently updating values

```tsx
// Prefer signals for high-frequency state (input values, counters, scroll position)
// Only the bound DOM node re-renders — not the component

const inputValue = useSignal('');
<input value={inputValue} onInput={e => inputValue.value = e.currentTarget.value} />
```

### PureComponent / memo

```tsx
import { memo } from 'preact/compat';

// Same as React.memo
const UserCard = memo(function UserCard({ user }: { user: User }) {
  return <div>{user.name}</div>;
});
```

### Lazy loading

```tsx
import { lazy, Suspense } from 'preact/compat';

const Dashboard = lazy(() => import('./Dashboard'));
<Suspense fallback={<Skeleton />}><Dashboard /></Suspense>
```

---

## Data Fetching

With `preact/compat`, use React Query or SWR identically to React. See `references/frameworks/react.md`.

Without compat, use native fetch with signals:

```ts
import { signal } from '@preact/signals';

export function createFetch<T>(url: string) {
  const data    = signal<T | null>(null);
  const loading = signal(true);
  const error   = signal<Error | null>(null);

  fetch(url)
    .then(r => r.json())
    .then(d  => { data.value = d; loading.value = false; })
    .catch(e => { error.value = e; loading.value = false; });

  return { data, loading, error };
}
```

---

## Forms

With `preact/compat`, use React Hook Form identically to React. See `references/frameworks/react.md`.

Without compat, use signals for controlled inputs:

```tsx
import { useSignal } from '@preact/signals';

function LoginForm({ onSubmit }: { onSubmit: (email: string, password: string) => void }) {
  const email    = useSignal('');
  const password = useSignal('');

  return (
    <form onSubmit={e => { e.preventDefault(); onSubmit(email.value, password.value); }}>
      <input type="email" value={email} onInput={e => email.value = e.currentTarget.value} />
      <input type="password" value={password} onInput={e => password.value = e.currentTarget.value} />
      <button type="submit">Log in</button>
    </form>
  );
}
```

---

## State

With `preact/compat`, Zustand and Jotai work identically to React. See `references/frameworks/react.md`.

For signal-based global state without a library:

```ts
// stores/cart.ts
import { signal, computed } from '@preact/signals';

const _items = signal<CartItem[]>([]);

export const cartItems = _items; // read-only exposure
export const cartTotal = computed(() =>
  _items.value.reduce((sum, i) => sum + i.price * i.quantity, 0)
);

export function addItem(item: CartItem) {
  _items.value = [..._items.value, item];
}
export function removeItem(id: string) {
  _items.value = _items.value.filter(i => i.id !== id);
}
```

---

## SEO

Preact does not have an SSR meta-framework equivalent to Next.js. For SSR, use **Preact's official SSR** or a Vite SSR setup.

For SPA, use `preact-helmet` or inject directly:

```tsx
import { Helmet } from 'react-helmet-async'; // works with preact/compat

<Helmet>
  <title>{product.name} — MyApp</title>
  <meta name="description" content={product.description} />
</Helmet>
```

---

## PWA

Same as Vite + React — use `vite-plugin-pwa`. See `references/frameworks/react.md` PWA section.

---

## i18n

With `preact/compat`, use `react-i18next` identically to React. See `references/frameworks/react.md`.

Without compat, use `@solid-primitives/i18n` pattern or a framework-agnostic library like `typesafe-i18n`.
