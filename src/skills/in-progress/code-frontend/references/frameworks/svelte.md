# SvelteKit — Framework Adapter

SvelteKit-specific implementations for all concerns defined in `references/`. This file is self-contained — it does not depend on the React adapter.

Covers: SvelteKit with Svelte 5 (runes). Svelte 4 store equivalents are noted where different.

---

## Conventions

### File extensions

- `.svelte` — components and routes
- `.server.ts` — server-only modules (never sent to the client)
- `.ts` — shared utilities and types

### File and folder naming

- Route files: SvelteKit convention (`+page.svelte`, `+layout.svelte`, `+page.server.ts`)
- Components: PascalCase (`UserCard.svelte`)
- Utilities/stores: camelCase (`useDebounce.ts`, `authStore.ts`)
- Feature folders: kebab-case (`user-profile/`, `auth/`)

### Component structure — order within a .svelte file

```svelte
<script lang="ts">
  // 1. Imports
  // 2. Props ($props)
  // 3. State ($state, $derived)
  // 4. Effects ($effect)
  // 5. Functions
</script>

<!-- Template -->

<style>
  /* Scoped styles */
</style>
```

### Props — Svelte 5 runes

```svelte
<script lang="ts">
  import type { User } from '$lib/types/user.types';

  interface Props {
    user: User;
    onSelect?: (id: string) => void;
    class?: string;
  }

  let { user, onSelect, class: className }: Props = $props();
</script>
```

---

## Error Handling

### Route error page — +error.svelte

```svelte
<!-- src/routes/+error.svelte -->
<script lang="ts">
  import { page } from '$app/stores';
</script>

<svelte:head>
  <title>Error {$page.status} — MyApp</title>
</svelte:head>

<main>
  <h1>{$page.status}: {$page.error?.message ?? 'Something went wrong'}</h1>
  <a href="/">Go home</a>
</main>
```

### Throwing errors in load functions

```ts
// +page.server.ts
import { error, redirect } from '@sveltejs/kit';

export async function load({ params, locals }) {
  if (!locals.user) redirect(302, '/login');

  const product = await fetchProduct(params.slug);
  if (!product) error(404, 'Product not found');

  return { product };
}
```

### Form action errors — fail()

```ts
// +page.server.ts
import { fail } from '@sveltejs/kit';

export const actions = {
  default: async ({ request }) => {
    const data   = await request.formData();
    const email  = data.get('email') as string;

    if (!email) return fail(400, { email, missing: true });

    try {
      await sendEmail(email);
      return { success: true };
    } catch {
      return fail(500, { email, error: 'Failed to send. Please try again.' });
    }
  },
};
```

### Global error handler — hooks.server.ts

```ts
// src/hooks.server.ts
import type { HandleServerError } from '@sveltejs/kit';

export const handleError: HandleServerError = ({ error, event }) => {
  console.error('Unhandled error:', error, event.url.pathname);
  return { message: 'An unexpected error occurred.' };
};
```

---

## Motion

### Built-in transitions

```svelte
<script lang="ts">
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';

  let visible = $state(true);
</script>

{#if visible}
  <div transition:fade={{ duration: 200 }}>Fade</div>
  <div in:fly={{ y: 12, duration: 200, easing: cubicOut }} out:fade>Fly in</div>
  <div transition:slide={{ duration: 150 }}>Slide</div>
{/if}
```

### Reduced motion

```svelte
<script lang="ts">
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const duration = prefersReduced ? 0 : 200;
</script>

<div transition:fade={{ duration }}>Content</div>
```

### List animation — animate:flip

```svelte
<script lang="ts">
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';

  let items = $state(['a', 'b', 'c']);
</script>

{#each items as item (item)}
  <div animate:flip={{ duration: 200 }} transition:fade>
    {item}
  </div>
{/each}
```

### Tweened and spring stores

```svelte
<script lang="ts">
  import { tweened, spring } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';

  const progress = tweened(0, { duration: 400, easing: cubicOut });
  const coords   = spring({ x: 0, y: 0 }, { stiffness: 0.1, damping: 0.25 });

  function advance() { progress.set(1); }
</script>

<progress value={$progress} />
```

### View Transitions — SvelteKit wiring

```ts
// app.html or +layout.svelte
// Enable in svelte.config.js:
// kit: { browser: { router: { type: 'hash' } } }

// Or trigger manually:
import { onNavigate } from '$app/navigation';

onNavigate(navigation => {
  if (!('startViewTransition' in document)) return;
  return new Promise(resolve => {
    document.startViewTransition(async () => {
      resolve();
      await navigation.complete;
    });
  });
});
```

---

## Accessibility

### Focus management with tick()

```svelte
<script lang="ts">
  import { tick } from 'svelte';

  let dialogEl: HTMLDivElement;
  let triggerEl: HTMLButtonElement;
  let isOpen = $state(false);

  async function open() {
    isOpen = true;
    await tick(); // wait for DOM update
    dialogEl.focus();
  }

  async function close() {
    isOpen = false;
    await tick();
    triggerEl.focus();
  }
</script>

<button bind:this={triggerEl} onclick={open}>Open</button>

{#if isOpen}
  <div bind:this={dialogEl} role="dialog" tabindex="-1" aria-modal="true">
    <button onclick={close}>Close</button>
  </div>
{/if}
```

### Focus trap action

```ts
// lib/actions/focusTrap.ts
import type { Action } from 'svelte/action';

const FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

export const focusTrap: Action<HTMLElement, boolean> = (node, active = true) => {
  function handleKeyDown(e: KeyboardEvent) {
    if (!active || e.key !== 'Tab') return;
    const els   = Array.from(node.querySelectorAll<HTMLElement>(FOCUSABLE));
    const first = els[0];
    const last  = els[els.length - 1];
    if (e.shiftKey) { if (document.activeElement === first) { e.preventDefault(); last.focus(); } }
    else            { if (document.activeElement === last)  { e.preventDefault(); first.focus(); } }
  }

  node.addEventListener('keydown', handleKeyDown);
  return {
    update(newActive: boolean) { active = newActive; },
    destroy() { node.removeEventListener('keydown', handleKeyDown); },
  };
};
```

```svelte
<div role="dialog" use:focusTrap={isOpen}>...</div>
```

### Svelte a11y compiler warnings

Svelte's compiler flags common a11y issues at build time. Never suppress them with `<!-- svelte-ignore a11y-... -->` without a written justification in a comment.

---

## Performance

### Reactivity is compiled — no manual memoization needed

Svelte compiles reactivity at build time. There is no virtual DOM diffing and no equivalent to `memo`, `useMemo`, or `useCallback`. Derived values update precisely when their dependencies change.

```svelte
<script lang="ts">
  let items = $state<Item[]>([]);

  // Derived — recomputes only when items changes
  const sorted = $derived([...items].sort((a, b) => a.name.localeCompare(b.name)));
  const total  = $derived(items.reduce((sum, i) => sum + i.price, 0));
</script>
```

### Lazy loading routes

SvelteKit splits routes automatically. For component-level lazy loading:

```ts
// Dynamic import — deferred until needed
const HeavyChart = (await import('$lib/components/HeavyChart.svelte')).default;
```

### Efficient list rendering

```svelte
<!-- Always key each blocks for efficient reconciliation -->
{#each items as item (item.id)}
  <ItemRow {item} />
{/each}

<!-- Avoid keying by index for lists that reorder or mutate -->
```

### @sveltejs/kit adapter — output mode

Choose the right adapter for your deployment target:

```ts
// svelte.config.js
import adapter from '@sveltejs/adapter-auto';        // Vercel, Netlify auto-detect
// import adapter from '@sveltejs/adapter-node';     // Node.js server
// import adapter from '@sveltejs/adapter-static';   // SPA / static export
```

---

## Data Fetching

### Server load — +page.server.ts

```ts
// src/routes/products/[slug]/+page.server.ts
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch, locals }) => {
  const product = await fetch(`/api/products/${params.slug}`)
    .then(r => r.ok ? r.json() : null);

  if (!product) error(404, 'Product not found');

  return { product };
};
```

### Universal load — +page.ts (runs on server and client)

```ts
// src/routes/products/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const category = url.searchParams.get('category') ?? 'all';
  const products = await fetch(`/api/products?category=${category}`).then(r => r.json());
  return { products, category };
};
```

### Layout load — +layout.server.ts

```ts
// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  return { user: locals.user ?? null };
};
```

### Streaming with promises

```ts
// +page.server.ts — stream slow data
export const load: PageServerLoad = async () => {
  return {
    product: fetchProduct(),               // awaited immediately
    reviews: fetchReviews(),               // streamed — page renders without it
  };
};
```

```svelte
<!-- +page.svelte -->
{#await data.reviews}
  <ReviewsSkeleton />
{:then reviews}
  <ReviewsList {reviews} />
{:catch error}
  <p>Failed to load reviews.</p>
{/await}
```

### Form actions

```ts
// +page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  login: async ({ request, cookies }) => {
    const data     = await request.formData();
    const email    = data.get('email') as string;
    const password = data.get('password') as string;

    const user = await authenticate(email, password);
    if (!user) return fail(401, { email, error: 'Invalid credentials' });

    cookies.set('session', createSession(user), { path: '/', httpOnly: true, secure: true, sameSite: 'strict' });
    redirect(302, '/dashboard');
  },
};
```

```svelte
<!-- Progressive enhancement — works without JS -->
<form method="POST" action="?/login" use:enhance>
  <input name="email" type="email" required />
  <input name="password" type="password" required />
  <button type="submit">Log in</button>
</form>
```

### useFetch — client-side fetching

For client-side data that doesn't fit `load`, use TanStack Query or a writable store:

```ts
// lib/stores/userStore.ts
import { writable } from 'svelte/store';

function createUserStore() {
  const { subscribe, set } = writable<User | null>(null);

  return {
    subscribe,
    async load(id: string) {
      const user = await fetchUser(id);
      set(user);
    },
  };
}

export const userStore = createUserStore();
```

---

## Forms — Superforms + Zod

### Schema

```ts
// lib/schemas/login.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email:    z.string().min(1, 'Required').email('Enter a valid email'),
  password: z.string().min(8, 'At least 8 characters'),
});
```

### Server action

```ts
// +page.server.ts
import { superValidate, message } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { loginSchema } from '$lib/schemas/login';

export const load = async () => ({ form: await superValidate(zod(loginSchema)) });

export const actions = {
  default: async ({ request }) => {
    const form = await superValidate(request, zod(loginSchema));
    if (!form.valid) return fail(400, { form });

    const user = await authenticate(form.data.email, form.data.password);
    if (!user) return message(form, 'Invalid credentials', { status: 401 });

    redirect(302, '/dashboard');
  },
};
```

### Form component

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { superForm } from 'sveltekit-superforms';

  let { data } = $props();
  const { form, errors, enhance, submitting, message } = superForm(data.form);
</script>

<form method="POST" use:enhance>
  <label for="email">Email</label>
  <input id="email" name="email" type="email" bind:value={$form.email}
    aria-invalid={!!$errors.email} aria-describedby={$errors.email ? 'email-error' : undefined} />
  {#if $errors.email}
    <p id="email-error" role="alert">{$errors.email}</p>
  {/if}

  <label for="password">Password</label>
  <input id="password" name="password" type="password" bind:value={$form.password}
    aria-invalid={!!$errors.password} />
  {#if $errors.password}
    <p role="alert">{$errors.password}</p>
  {/if}

  {#if $message}
    <div role="alert">{$message}</div>
  {/if}

  <button type="submit" disabled={$submitting} aria-busy={$submitting}>
    {$submitting ? 'Logging in…' : 'Log in'}
  </button>
</form>
```

---

## State

### Svelte 5 — runes

```svelte
<script lang="ts">
  // Local state
  let count = $state(0);
  let items = $state<Item[]>([]);

  // Derived state — recomputes when dependencies change
  const doubled = $derived(count * 2);
  const total   = $derived(items.reduce((sum, i) => sum + i.price, 0));

  // Side effects — run when dependencies change
  $effect(() => {
    document.title = `Count: ${count}`;
    return () => { document.title = 'MyApp'; }; // cleanup
  });
</script>
```

### Svelte 4 — writable / readable / derived stores

```ts
// lib/stores/cart.ts
import { writable, derived, get } from 'svelte/store';

const items = writable<CartItem[]>([]);

export const cartStore = {
  subscribe: items.subscribe,
  addItem:    (item: CartItem) => items.update(prev => [...prev, item]),
  removeItem: (id: string)    => items.update(prev => prev.filter(i => i.id !== id)),
  clear:      ()               => items.set([]),
};

export const cartTotal = derived(items, $items =>
  $items.reduce((sum, i) => sum + i.price * i.quantity, 0)
);
```

```svelte
<script>
  import { cartStore, cartTotal } from '$lib/stores/cart';
</script>

<p>Total: {$cartTotal}</p>
```

### Context API — component tree sharing

```ts
// lib/context/auth.ts
import { setContext, getContext } from 'svelte';
import type { User } from '$lib/types';

const AUTH_KEY = Symbol('auth');

export function setAuthContext(user: User | null) {
  setContext(AUTH_KEY, { user });
}

export function getAuthContext(): { user: User | null } {
  return getContext(AUTH_KEY);
}
```

```svelte
<!-- +layout.svelte -->
<script lang="ts">
  import { setAuthContext } from '$lib/context/auth';
  let { data, children } = $props();
  setAuthContext(data.user);
</script>
{@render children()}

<!-- Any child component -->
<script lang="ts">
  import { getAuthContext } from '$lib/context/auth';
  const { user } = getAuthContext();
</script>
```

### URL state — $page.url

```svelte
<script lang="ts">
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';

  const category = $derived($page.url.searchParams.get('category') ?? 'all');

  function setFilter(key: string, value: string) {
    const params = new URLSearchParams($page.url.searchParams);
    params.set(key, value);
    params.set('page', '1');
    goto(`?${params.toString()}`, { replaceState: false, keepFocus: true });
  }
</script>
```

---

## Styling

Svelte components are scoped by default — styles in a `<style>` block apply only to that component.

### Scoped styles — default

```svelte
<div class="card">
  <span class="card__name">{user.name}</span>
</div>

<style>
  /* Scoped by default — no collision risk */
  .card {
    display: flex;
    gap: var(--space-4);
    padding: var(--space-6);
    background: var(--color-surface);
    border-radius: var(--radius-lg);
  }

  .card__name {
    font-weight: 600;
    color: var(--color-text-primary);
  }
</style>
```

### Global styles

```svelte
<style>
  /* Target elements outside this component */
  :global(.prose h2) { font-size: 1.5rem; }

  /* Or in a dedicated global stylesheet */
  /* src/app.css — imported in +layout.svelte */
</style>
```

For app-wide globals, use `src/app.css` imported once in `+layout.svelte`.

### CSS framework adapters

Load the adapter that matches the detected CSS stack:

| Detected CSS | Adapter |
| --- | --- |
| TailwindCSS | `references/frameworks/tailwind.md` |
| Bootstrap | `references/frameworks/bootstrap.md` |
| CSS Modules | `references/frameworks/css-modules.md` |
| shadcn-svelte | `references/frameworks/shadcn.md` + `references/frameworks/tailwind.md` |
| Plain CSS | `references/styling.md` (tokens, layout, BEM) |

MUI is React-only and not available for SvelteKit.

---

## SEO — svelte:head

```svelte
<!-- +page.svelte or +layout.svelte -->
<svelte:head>
  <title>{data.product.name} — MyApp</title>
  <meta name="description" content={data.product.description.slice(0, 155)} />
  <meta property="og:title" content="{data.product.name} — MyApp" />
  <meta property="og:image" content={data.product.imageUrl} />
  <link rel="canonical" href="https://myapp.com/products/{data.product.slug}" />
</svelte:head>
```

### Root layout — title template

```svelte
<!-- src/routes/+layout.svelte -->
<svelte:head>
  <title>MyApp</title>
</svelte:head>

<!-- Individual pages override with their own svelte:head -->
```

### Sitemap — +server.ts

```ts
// src/routes/sitemap.xml/+server.ts
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async () => {
  const products = await fetchAllProducts();

  const urls = [
    { loc: 'https://myapp.com/', priority: '1.0', changefreq: 'monthly' },
    ...products.map(p => ({
      loc: `https://myapp.com/products/${p.slug}`,
      priority: '0.8',
      changefreq: 'weekly',
      lastmod: p.updatedAt.toISOString(),
    })),
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url>
    <loc>${u.loc}</loc>
    <priority>${u.priority}</priority>
    <changefreq>${u.changefreq}</changefreq>
    ${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : ''}
  </url>`).join('\n')}
</urlset>`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
};
```

---

## PWA — SvelteKit Service Worker

SvelteKit has built-in service worker support. Place `src/service-worker.ts` in the project root — it is automatically registered.

```ts
// src/service-worker.ts
/// <reference types="@sveltejs/kit" />
/// <reference no-default-lib="true"/>
/// <reference lib="esnext" />
/// <reference lib="webworker" />

import { build, files, version } from '$service-worker';

const CACHE = `cache-${version}`;
const ASSETS = [...build, ...files];

// Precache on install
self.addEventListener('install', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS))
  );
});

// Delete old caches on activate
self.addEventListener('activate', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
});

// Serve from cache, fall back to network
self.addEventListener('fetch', (event: FetchEvent) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cached => cached ?? fetch(event.request))
  );
});
```

For more complex caching strategies, use `@vite-pwa/sveltekit` (Workbox-backed):

```ts
// vite.config.ts
import { sveltekit } from '@sveltejs/kit/vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    sveltekit(),
    VitePWA({
      strategies: 'injectManifest',
      srcDir: 'src',
      filename: 'service-worker.ts',
    }),
  ],
});
```

---

## i18n — Paraglide.js

### Setup

```ts
// project.inlang/settings.json
{
  "sourceLanguageTag": "en",
  "languageTags": ["en", "fr", "ar"],
  "modules": ["@inlang/plugin-message-format"]
}
```

```ts
// vite.config.ts
import { paraglide } from '@inlang/paraglide-sveltekit/vite';

export default defineConfig({
  plugins: [sveltekit(), paraglide({ project: './project.inlang', outdir: './src/lib/paraglide' })],
});
```

### Usage

```svelte
<!-- messages compiled to typed functions — zero runtime overhead -->
<script lang="ts">
  import * as m from '$lib/paraglide/messages';
  import { languageTag } from '$lib/paraglide/runtime';
</script>

<p>{m.welcomeBack({ name: user.name })}</p>
<p>{m.itemCount({ count: items.length })}</p>
<p>Language: {languageTag()}</p>
```

### Locale routing — hooks.server.ts

```ts
// src/hooks.server.ts
import { i18n } from '$lib/i18n';
export const handle = i18n.handle();
```

### Locale switcher

```svelte
<script lang="ts">
  import { availableLanguageTags, languageTag } from '$lib/paraglide/runtime';
  import { i18n } from '$lib/i18n';
  import { page } from '$app/stores';
</script>

{#each availableLanguageTags() as lang}
  <a href={i18n.route($page.url.pathname)} hreflang={lang}
    aria-current={lang === languageTag() ? 'true' : undefined}>
    {lang.toUpperCase()}
  </a>
{/each}
```

### RTL

```svelte
<!-- +layout.svelte -->
<script lang="ts">
  import { languageTag } from '$lib/paraglide/runtime';
  const RTL = ['ar', 'he', 'fa', 'ur'];
  const dir = $derived(RTL.includes(languageTag()) ? 'rtl' : 'ltr');
</script>

<svelte:head>
  <html lang={languageTag()} {dir} />
</svelte:head>
```
