# Nuxt.js — Framework Adapter

Nuxt is the Vue meta-framework — SSR, SSG, ISR, and SPA modes in one. Read `vue.md` first — this adapter covers only what Nuxt adds or overrides.

---

## Conventions

### File-based routing

```
pages/
  index.vue                   → /
  about.vue                   → /about
  products/
    index.vue                 → /products
    [slug].vue                → /products/:slug
    [...path].vue             → /products/* (catch-all)
components/                   → auto-imported
composables/                  → auto-imported
server/
  api/
    users/[id].get.ts         → GET /api/users/:id
    products.post.ts          → POST /api/products
  middleware/
    auth.ts
```

Everything in `components/` and `composables/` is auto-imported — no import statements needed.

### Component structure

Same as Vue 3 `<script setup>` — see `references/frameworks/vue.md`. No changes from Nuxt.

---

## Error Handling

### error.vue — global error page

```vue
<!-- error.vue -->
<script setup lang="ts">
const props = defineProps<{ error: { statusCode: number; message: string } }>();
const handleError = () => clearError({ redirect: '/' });
</script>

<template>
  <div role="alert">
    <h1>{{ error.statusCode }}: {{ error.message }}</h1>
    <button @click="handleError">Go home</button>
  </div>
</template>
```

### Throw errors in server routes and pages

```ts
// server/api/products/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');
  const product = await fetchProduct(id!);
  if (!product) throw createError({ statusCode: 404, message: 'Product not found' });
  return product;
});
```

```vue
<!-- pages/products/[slug].vue -->
<script setup lang="ts">
const route = useRoute();
const { data: product, error } = await useFetch(`/api/products/${route.params.slug}`);
if (error.value) throw createError({ statusCode: 404, fatal: true });
</script>
```

---

## Data Fetching

### useFetch — SSR-aware, deduped

```vue
<script setup lang="ts">
// Runs on server and client, deduplicates requests
const { data: product, status, refresh } = await useFetch(`/api/products/${slug}`, {
  key: `product-${slug}`,
  transform: (data) => data as Product,
});
</script>
```

### useAsyncData — for custom async logic

```vue
<script setup lang="ts">
const { data: products, status } = await useAsyncData(
  'products',
  () => $fetch<Product[]>('/api/products'),
  { watch: [category] }  // re-fetch when category changes
);
```

### $fetch — client-side or server route calls

```ts
// In composables or event handlers (not in setup unless wrapped)
const product = await $fetch<Product>(`/api/products/${id}`);

// With error handling
try {
  await $fetch('/api/orders', { method: 'POST', body: orderData });
} catch (err) {
  // FetchError with status and data
}
```

### Server routes

```ts
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id   = getRouterParam(event, 'id');
  const user = await db.users.findById(id!);
  if (!user) throw createError({ statusCode: 404 });

  // Auth check
  const session = await getUserSession(event);
  if (!session.user) throw createError({ statusCode: 401 });

  return user;
});
```

---

## State

### useState — SSR-safe reactive state

```ts
// composables/useCounter.ts
export const useCounter = () => useState('counter', () => 0);

// Shared across components, hydrated from server
const count = useCounter();
count.value++;
```

### Pinia — same as Vue, but use `@pinia/nuxt`

```ts
// nuxt.config.ts
modules: ['@pinia/nuxt', '@pinia-plugin-persistedstate/nuxt']
```

Same store definition as in `references/frameworks/vue.md`.

---

## Performance

### Nuxt Image — `@nuxt/image`

```ts
// nuxt.config.ts
modules: ['@nuxt/image']
```

```vue
<NuxtImg src="/hero.jpg" alt="Hero" width="1200" height="600" format="webp" loading="lazy" />
<NuxtPicture src="/hero.jpg" alt="Hero" :imgAttrs="{ class: 'hero-img' }" />
```

### Route-level code splitting

Nuxt splits routes automatically. For component-level:

```vue
<script setup lang="ts">
const HeavyChart = defineAsyncComponent(() => import('@/components/HeavyChart.vue'));
</script>
```

### Rendering modes

```ts
// nuxt.config.ts
routeRules: {
  '/':               { prerender: true },     // SSG
  '/blog/**':        { isr: 3600 },           // ISR — revalidate every hour
  '/dashboard/**':   { ssr: false },          // SPA — client only
  '/api/**':         { cors: true, headers: { 'cache-control': 's-maxage=3600' } },
}
```

---

## SEO — useSeoMeta / useHead

```vue
<script setup lang="ts">
// Type-safe, recommended
useSeoMeta({
  title: () => `${product.value?.name} — MyApp`,
  description: () => product.value?.description.slice(0, 155),
  ogTitle: () => `${product.value?.name} — MyApp`,
  ogImage: () => product.value?.imageUrl,
  twitterCard: 'summary_large_image',
});

// Canonical
useHead({
  link: [{ rel: 'canonical', href: `https://myapp.com/products/${slug}` }],
});
</script>
```

### Default SEO in app.vue or layout

```vue
<!-- app.vue -->
<script setup lang="ts">
useSeoMeta({
  titleTemplate: '%s — MyApp',
  description: 'Default site description.',
});
</script>
```

### Sitemap — @nuxtjs/sitemap

```ts
// nuxt.config.ts
modules: ['@nuxtjs/sitemap'],
site: { url: 'https://myapp.com' },
sitemap: {
  sources: ['/api/__sitemap__/urls'],
},
```

---

## PWA — @vite-pwa/nuxt

```ts
// nuxt.config.ts
modules: ['@vite-pwa/nuxt'],
pwa: {
  registerType: 'autoUpdate',
  manifest: { name: 'MyApp', theme_color: '#6366f1' },
  workbox: { navigateFallback: '/' },
}
```

---

## i18n — @nuxtjs/i18n

```ts
// nuxt.config.ts
modules: ['@nuxtjs/i18n'],
i18n: {
  locales: [
    { code: 'en', file: 'en.json' },
    { code: 'fr', file: 'fr.json' },
    { code: 'ar', file: 'ar.json', dir: 'rtl' },
  ],
  defaultLocale: 'en',
  langDir: 'locales/',
  strategy: 'prefix_except_default',
}
```

```vue
<script setup lang="ts">
const { t, locale, locales, setLocale } = useI18n();
</script>

<template>
  <p>{{ t('product.addToCart') }}</p>
  <button v-for="l in locales" :key="l.code" @click="setLocale(l.code)">
    {{ l.code.toUpperCase() }}
  </button>
</template>
```
