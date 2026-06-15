# Astro — Framework Adapter

Astro is a server-first, content-focused framework using an island architecture. Most content renders as static HTML; interactive islands opt in to client-side JS with `client:*` directives.

---

## Conventions

### File extensions

- `.astro` — pages, layouts, and Astro components
- `.ts` — server endpoints, middleware, utilities
- Framework component files (`.tsx`, `.svelte`, `.vue`) — used as islands

### Component structure — .astro files

```astro
---
// Frontmatter (server-side, runs at build or request time)
import Layout from '@/layouts/Layout.astro';
import UserCard from '@/components/UserCard.tsx';
import { fetchUser } from '@/lib/api';

const { id } = Astro.params;
const user = await fetchUser(id);
if (!user) return Astro.redirect('/404');

interface Props { title: string; }
const { title } = Astro.props;
---

<!-- Template (static HTML by default) -->
<Layout {title}>
  <!-- Island — hydrates on load -->
  <UserCard user={user} client:load />
</Layout>

<style>
  /* Scoped to this component */
</style>
```

### Client directives — choose the least expensive one

| Directive | Hydrates when |
| --- | --- |
| `client:load` | Immediately on page load |
| `client:idle` | Browser is idle |
| `client:visible` | Component enters the viewport |
| `client:media="(max-width: 768px)"` | Media query matches |
| `client:only="react"` | Client-only, no SSR |

---

## Error Handling

### 404 and custom error pages

```astro
---
// src/pages/404.astro
---
<Layout title="Not found">
  <h1>Page not found</h1>
  <a href="/">Go home</a>
</Layout>
```

### Error in data fetching

```astro
---
const { id } = Astro.params;
let product = null;
let error = null;

try {
  product = await fetchProduct(id);
} catch (err) {
  error = err instanceof Error ? err.message : 'Failed to load product';
}

if (!product && !error) return Astro.redirect('/404');
---

{error ? (
  <ErrorMessage message={error} />
) : (
  <ProductView product={product!} />
)}
```

### Server endpoint errors

```ts
// src/pages/api/products/[id].ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ params }) => {
  try {
    const product = await fetchProduct(params.id!);
    if (!product) return new Response('Not found', { status: 404 });
    return new Response(JSON.stringify(product), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch {
    return new Response('Internal server error', { status: 500 });
  }
};
```

---

## Motion

Astro renders static HTML — animations run inside framework islands or via CSS. Apply CSS animations directly on `.astro` components; Framer Motion and Svelte transitions work inside their respective islands.

```astro
---
// View Transitions — built-in Astro support
import { ViewTransitions } from 'astro:transitions';
---
<head>
  <ViewTransitions />
</head>
```

```astro
<!-- Persist elements across navigations -->
<header transition:persist>
  <nav>...</nav>
</header>

<!-- Animate specific elements -->
<h1 transition:animate="slide">Page Title</h1>
<img transition:name={`product-${id}`} src={product.image} />
```

See `references/motion.md` for CSS animation principles.

---

## Accessibility

Astro renders semantic HTML by default — the same rules from `references/a11y.md` apply. Interactive a11y (focus traps, live regions) is implemented inside framework islands using the island framework's adapter.

---

## Performance

### Static by default

Astro ships zero JS by default. Only islands hydrate. Keep islands small and defer hydration.

### Image optimisation — astro:assets

```astro
---
import { Image, Picture } from 'astro:assets';
import heroImage from '@/assets/hero.jpg';
---

<!-- Optimised, resized, WebP/AVIF output -->
<Image src={heroImage} alt="Hero" width={1200} height={600} />

<!-- Responsive with multiple formats -->
<Picture
  src={heroImage}
  formats={['avif', 'webp']}
  alt="Hero"
  widths={[400, 800, 1200]}
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

### Prefetch

```astro
---
import { prefetch } from 'astro:prefetch';
---
<!-- Enable globally in astro.config.mjs -->
<!-- prefetch: true -->

<!-- Or per-link -->
<a href="/dashboard" data-astro-prefetch>Dashboard</a>
```

---

## Data Fetching

### Static — at build time

```astro
---
// Runs once at build time
const posts = await fetch('https://api.example.com/posts').then(r => r.json());
---
{posts.map(post => <PostCard {post} />)}
```

### Server-side — on every request

```ts
// astro.config.mjs
export default defineConfig({ output: 'server' }); // or 'hybrid'
```

```astro
---
export const prerender = false; // opt out of static for this page
const data = await fetchDynamicData(Astro.request);
---
```

### Content Collections

```ts
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

export const collections = {
  blog: defineCollection({
    type: 'content',
    schema: z.object({
      title:       z.string(),
      publishDate: z.date(),
      tags:        z.array(z.string()),
    }),
  }),
};
```

```astro
---
import { getCollection, getEntry } from 'astro:content';

const posts = await getCollection('blog');
const post  = await getEntry('blog', 'my-post');
const { Content } = await post.render();
---
<Content />
```

### Dynamic routes

```astro
---
// src/pages/products/[slug].astro
import type { GetStaticPaths } from 'astro';

export const getStaticPaths: GetStaticPaths = async () => {
  const products = await fetchAllProducts();
  return products.map(p => ({ params: { slug: p.slug }, props: { product: p } }));
};

const { product } = Astro.props;
---
```

---

## Forms

Astro supports native HTML form actions (Astro 4+) or API routes.

### Astro actions (v4+)

```ts
// src/actions/index.ts
import { defineAction, z } from 'astro:actions';

export const server = {
  contact: defineAction({
    input: z.object({ email: z.string().email(), message: z.string().min(10) }),
    handler: async ({ email, message }) => {
      await sendEmail({ email, message });
      return { success: true };
    },
  }),
};
```

```astro
---
import { actions } from 'astro:actions';
const result = Astro.getActionResult(actions.contact);
---

<form method="POST" action={actions.contact}>
  <input name="email" type="email" required />
  <textarea name="message" required></textarea>
  {result?.error && <p role="alert">{result.error.message}</p>}
  <button type="submit">Send</button>
</form>
```

---

## State

Islands are isolated — they do not share state by default. Use **Nano Stores** for cross-island state.

```ts
// src/stores/cart.ts
import { atom, map } from 'nanostores';

export const cartCount = atom(0);
export const cartItems = map<Record<string, CartItem>>({});

export function addToCart(item: CartItem) {
  cartItems.setKey(item.id, item);
  cartCount.set(Object.keys(cartItems.get()).length);
}
```

```tsx
// React island
import { useStore } from '@nanostores/react';
import { cartCount } from '@/stores/cart';

export function CartBadge() {
  const count = useStore(cartCount);
  return <span>{count}</span>;
}
```

```svelte
<!-- Svelte island -->
<script>
  import { cartCount } from '@/stores/cart';
</script>
<span>{$cartCount}</span>
```

---

## SEO

```astro
---
// src/layouts/Layout.astro
interface Props {
  title: string;
  description?: string;
  ogImage?: string;
  canonical?: string;
}
const {
  title,
  description = 'Default site description.',
  ogImage = '/og/default.png',
  canonical = new URL(Astro.url.pathname, Astro.site).toString(),
} = Astro.props;
---
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width" />
  <title>{title} — MyApp</title>
  <meta name="description" content={description} />
  <link rel="canonical" href={canonical} />
  <meta property="og:title" content={`${title} — MyApp`} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content={ogImage} />
  <meta name="twitter:card" content="summary_large_image" />
</head>
<body><slot /></body>
</html>
```

### Sitemap

```ts
// astro.config.mjs
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://myapp.com',
  integrations: [sitemap()],
});
```

---

## PWA

```ts
// astro.config.mjs
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  vite: {
    plugins: [VitePWA({ registerType: 'autoUpdate', manifest: { name: 'MyApp', theme_color: '#6366f1' } })],
  },
});
```

---

## i18n — Built-in (Astro 4+)

```ts
// astro.config.mjs
export default defineConfig({
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr', 'ar'],
    routing: { prefixDefaultLocale: false },
  },
});
```

```astro
---
import { getRelativeLocaleUrl } from 'astro:i18n';
const frUrl = getRelativeLocaleUrl('fr', Astro.url.pathname);
---
<a href={frUrl}>Français</a>
```
