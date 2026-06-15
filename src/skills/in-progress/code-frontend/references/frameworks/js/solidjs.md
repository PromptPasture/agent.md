# SolidJS — Framework Adapter

SolidJS uses fine-grained reactivity with signals — no virtual DOM. JSX compiles to direct DOM operations. SolidStart is the meta-framework for SSR/SSG.

---

## Conventions

### File extensions

- `.tsx` — components (JSX)
- `.ts` — utilities, stores, types

### Component structure

```tsx
// components/UserCard.tsx
import { type Component } from 'solid-js';
import type { User } from '@/types/user';

interface UserCardProps {
  user: User;
  featured?: boolean;
  onSelect?: (id: string) => void;
  class?: string;
}

const UserCard: Component<UserCardProps> = (props) => {
  return (
    <article
      class={`user-card${props.featured ? ' featured' : ''} ${props.class ?? ''}`}
      onClick={() => props.onSelect?.(props.user.id)}
    >
      <span class="name">{props.user.name}</span>
    </article>
  );
};

export default UserCard;
```

### Key differences from React

- **Props are NOT destructured at the top level** — destructuring breaks reactivity
- **Signals are accessed by calling them**: `count()` not `count`
- **No re-renders** — DOM updates surgically, only the reactive node changes
- **`createEffect` runs immediately** and tracks dependencies automatically

```tsx
// Bad — destructuring loses reactivity
const { user, featured } = props;

// Good — always access props inline
<span>{props.user.name}</span>
```

---

## Error Handling

### ErrorBoundary

```tsx
import { ErrorBoundary } from 'solid-js';

function App() {
  return (
    <ErrorBoundary
      fallback={(err, reset) => (
        <section role="alert">
          <p>{err.message}</p>
          <button onClick={reset}>Retry</button>
        </section>
      )}
    >
      <Feature />
    </ErrorBoundary>
  );
}
```

### SolidStart — error pages

```tsx
// src/routes/[...404].tsx
export default function NotFound() {
  return <main><h1>Page not found</h1><a href="/">Go home</a></main>;
}
```

---

## Reactivity — Core Primitives

```ts
import { createSignal, createMemo, createEffect, createStore, batch } from 'solid-js';

// Signal — primitive reactive value
const [count, setCount] = createSignal(0);
const [user, setUser]   = createSignal<User | null>(null);

// Access: call the signal
console.log(count()); // 0

// Update
setCount(5);
setCount(prev => prev + 1);

// Memo — derived, cached reactive value (equivalent of computed)
const doubled = createMemo(() => count() * 2);

// Effect — runs when dependencies change
createEffect(() => {
  document.title = `Count: ${count()}`;
});

// Batch — group updates to avoid intermediate renders
batch(() => {
  setCount(10);
  setUser({ id: '1', name: 'Alice' });
});

// Store — reactive object (mutable, nested)
const [store, setStore] = createStore({ items: [] as Item[], loading: false });
setStore('items', prev => [...prev, newItem]);
setStore('loading', true);
```

---

## Motion

SolidJS does not ship animation utilities. Use CSS transitions or **solid-transition-group**:

```tsx
import { TransitionGroup } from 'solid-transition-group';

<TransitionGroup name="fade">
  <For each={items()}>{(item) => <ItemRow item={item} />}</For>
</TransitionGroup>
```

```css
.fade-enter-active, .fade-exit-active { transition: opacity 0.2s ease; }
.fade-enter, .fade-exit-to            { opacity: 0; }

@media (prefers-reduced-motion: reduce) {
  .fade-enter-active, .fade-exit-active { transition: none; }
}
```

---

## Accessibility

Focus management uses DOM refs and `onMount`:

```tsx
import { createSignal, onMount, type JSX } from 'solid-js';

function Dialog(props: { isOpen: boolean; onClose: () => void; children: JSX.Element }) {
  let dialogRef: HTMLDivElement | undefined;

  createEffect(() => {
    if (props.isOpen) dialogRef?.focus();
  });

  return (
    <Show when={props.isOpen}>
      <div ref={dialogRef} role="dialog" tabindex="-1" aria-modal="true">
        {props.children}
      </div>
    </Show>
  );
}
```

---

## Performance

SolidJS is inherently performant — no virtual DOM reconciliation. Optimise by:

- Using `<Show>` over ternary for conditional rendering (avoids recreating DOM)
- Using `<For>` over `.map()` for lists (keyed, minimal DOM operations)
- Using `createMemo` for expensive derivations
- Keeping signals granular — one signal per independent value

```tsx
// Good — Show only mounts/unmounts once
<Show when={isLoggedIn()} fallback={<Login />}>
  <Dashboard />
</Show>

// Good — For is keyed and minimal
<For each={items()}>{(item) => <ItemRow item={item} />}</For>

// Avoid index as key implicitly — For handles this correctly
```

### Lazy loading

```tsx
import { lazy, Suspense } from 'solid-js';

const Dashboard = lazy(() => import('./Dashboard'));

<Suspense fallback={<Skeleton />}>
  <Dashboard />
</Suspense>
```

---

## Data Fetching — createResource

```tsx
import { createResource, Suspense } from 'solid-js';

// Basic resource
const [user, { refetch }] = createResource(() => userId(), fetchUser);

// Use with Suspense
<Suspense fallback={<Skeleton />}>
  <Show when={!user.error} fallback={<ErrorMessage error={user.error} />}>
    <UserProfile user={user()!} />
  </Show>
</Suspense>
```

### SolidStart — server data

```tsx
// src/routes/products/[id].tsx
import { createAsync } from '@solidjs/router';

const getProduct = cache(async (id: string) => {
  'use server';
  const product = await db.products.findById(id);
  if (!product) throw new Error('Not found');
  return product;
}, 'product');

export default function ProductPage() {
  const params  = useParams();
  const product = createAsync(() => getProduct(params.id));

  return (
    <Suspense fallback={<Skeleton />}>
      <ProductView product={product()} />
    </Suspense>
  );
}
```

---

## Forms — Modular Forms

```tsx
import { createForm, valiForm } from '@modular-forms/solid';
import * as v from 'valibot'; // or Zod

const loginSchema = v.object({
  email:    v.pipe(v.string(), v.email('Invalid email')),
  password: v.pipe(v.string(), v.minLength(8, 'At least 8 characters')),
});

function LoginForm() {
  const [form, { Form, Field }] = createForm({
    validate: valiForm(loginSchema),
  });

  const handleSubmit = async (values: LoginInput) => {
    await authService.login(values);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Field name="email">
        {(field, props) => (
          <div>
            <label for={field.name}>Email</label>
            <input {...props} id={field.name} type="email"
              aria-invalid={!!field.error} aria-describedby={field.error ? `${field.name}-error` : undefined} />
            {field.error && <p id={`${field.name}-error`} role="alert">{field.error}</p>}
          </div>
        )}
      </Field>
      <button type="submit" disabled={form.submitting} aria-busy={form.submitting}>
        {form.submitting ? 'Logging in…' : 'Log in'}
      </button>
    </Form>
  );
}
```

---

## State — Global Signals and Stores

```ts
// stores/cart.ts — module-level signals are global
import { createSignal, createMemo } from 'solid-js';
import { createStore } from 'solid-js/store';

const [cartItems, setCartItems] = createStore<CartItem[]>([]);
export const cartTotal = createMemo(() =>
  cartItems.reduce((sum, i) => sum + i.price * i.quantity, 0)
);

export const cartStore = {
  items: cartItems,
  total: cartTotal,
  addItem(item: CartItem) {
    setCartItems(prev => [...prev, item]);
  },
  removeItem(id: string) {
    setCartItems(prev => prev.filter(i => i.id !== id));
  },
};
```

### URL state — @solidjs/router

```tsx
import { useSearchParams } from '@solidjs/router';

function ProductFilters() {
  const [searchParams, setSearchParams] = useSearchParams();

  const category = () => searchParams.category ?? 'all';

  function setFilter(key: string, value: string) {
    setSearchParams({ [key]: value, page: '1' });
  }

  return <select value={category()} onChange={e => setFilter('category', e.target.value)}>...</select>;
}
```

---

## SEO — SolidStart

```tsx
import { Title, Meta, Link } from '@solidjs/meta';

export default function ProductPage() {
  const product = createAsync(() => getProduct(params.id));

  return (
    <>
      <Title>{() => `${product()?.name} — MyApp`}</Title>
      <Meta name="description" content={product()?.description} />
      <Meta property="og:image" content={product()?.imageUrl} />
      <Link rel="canonical" href={`https://myapp.com/products/${params.id}`} />
      <ProductView product={product()} />
    </>
  );
}
```

---

## i18n — @solid-primitives/i18n

```ts
import { createI18nContext, useI18n } from '@solid-primitives/i18n';

const en = { product: { addToCart: 'Add to cart' }, cart: { items: '{count} items' } };
const fr = { product: { addToCart: 'Ajouter au panier' }, cart: { items: '{count} articles' } };

const I18nContext = createI18nContext({ en, fr }, 'en');

// Usage
function ProductButton() {
  const [t, { locale, setLocale }] = useI18n();
  return <button>{t('product.addToCart')}</button>;
}
```
