# SEO

SEO applies to pages, not components. Skip this reference for non-page components unless they render content that affects crawlability.

---

## Core Principles

- **Crawlable content** — critical content must be in the HTML, not injected by JS after load
- **Unique metadata** — every page has a distinct `title` and `meta description`
- **Logical structure** — one `h1` per page, headings in order, no skipped levels
- **Canonical URL** — prevents duplicate content across routes

---

## Next.js App Router — Metadata API

Prefer the Metadata API over manual `<head>` tags. It handles deduplication and streaming correctly.

### Static metadata

```ts
// app/about/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us — MyApp',
  description: 'Learn about MyApp and the team behind it.',
  openGraph: {
    title: 'About Us — MyApp',
    description: 'Learn about MyApp and the team behind it.',
    url: 'https://myapp.com/about',
    siteName: 'MyApp',
    images: [{ url: 'https://myapp.com/og/about.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'About Us — MyApp',
    description: 'Learn about MyApp and the team behind it.',
    images: ['https://myapp.com/og/about.png'],
  },
};
```

### Dynamic metadata

```ts
// app/products/[slug]/page.tsx
import type { Metadata } from 'next';
import { fetchProduct } from '@/api/products';

interface PageProps {
  params: { slug: string };
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const product = await fetchProduct(params.slug).catch(() => null);
  if (!product) return { title: 'Product not found' };

  return {
    title: `${product.name} — MyApp`,
    description: product.description.slice(0, 155),
    openGraph: {
      title: product.name,
      description: product.description.slice(0, 155),
      images: [{ url: product.imageUrl, width: 1200, height: 630 }],
    },
    alternates: {
      canonical: `https://myapp.com/products/${params.slug}`,
    },
  };
}
```

### Title template

Define a title template at the root layout to avoid repeating the site name:

```ts
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: 'MyApp',
    template: '%s — MyApp',
  },
};

// app/about/page.tsx — only provide the page title
export const metadata: Metadata = {
  title: 'About Us', // renders as "About Us — MyApp"
};
```

---

## Next.js Pages Router

```tsx
import Head from 'next/head';

export default function AboutPage() {
  return (
    <>
      <Head>
        <title>About Us — MyApp</title>
        <meta name="description" content="Learn about MyApp and the team behind it." />
        <meta property="og:title" content="About Us — MyApp" />
        <meta property="og:description" content="Learn about MyApp and the team behind it." />
        <meta property="og:image" content="https://myapp.com/og/about.png" />
        <meta property="og:url" content="https://myapp.com/about" />
        <link rel="canonical" href="https://myapp.com/about" />
      </Head>
      <main>...</main>
    </>
  );
}
```

---

## Other Frameworks

For SvelteKit, Nuxt, Astro, and Remix use the framework's native head management:

```svelte
<!-- SvelteKit — +page.svelte -->
<svelte:head>
  <title>About Us — MyApp</title>
  <meta name="description" content="..." />
</svelte:head>
```

```ts
// Nuxt — useSeoMeta composable
useSeoMeta({
  title: 'About Us — MyApp',
  description: '...',
  ogImage: 'https://myapp.com/og/about.png',
});
```

```astro
<!-- Astro — pass to Layout -->
<Layout title="About Us — MyApp" description="...">
  ...
</Layout>
```

```ts
// Remix — meta export
export const meta: MetaFunction = () => [
  { title: 'About Us — MyApp' },
  { name: 'description', content: '...' },
];
```

---

## Structured Data (JSON-LD)

Add structured data for rich results in search — articles, products, breadcrumbs, FAQs.

```tsx
// app/products/[slug]/page.tsx
export default async function ProductPage({ params }: PageProps) {
  const product = await fetchProduct(params.slug);

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.imageUrl,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <ProductView product={product} />
    </>
  );
}
```

Common schema types: `Article`, `Product`, `BreadcrumbList`, `FAQPage`, `Organization`, `WebSite`.

---

## Heading Hierarchy

```tsx
// Good — one h1, logical order
<main>
  <h1>Product Catalogue</h1>       {/* one per page */}
  <section>
    <h2>Featured Products</h2>
    <article>
      <h3>Product Name</h3>
    </article>
  </section>
  <section>
    <h2>All Products</h2>
  </section>
</main>

// Bad — skipped levels, multiple h1
<div>
  <h1>Product Catalogue</h1>
  <h1>Featured</h1>               {/* second h1 */}
  <h4>Product Name</h4>           {/* skipped h2 and h3 */}
</div>
```

---

## Canonical URLs

Set canonical on every page to prevent duplicate content from query parameters, trailing slashes, or alternate domains:

```ts
// Next.js App Router
alternates: {
  canonical: 'https://myapp.com/products/widget',
}

// Next.js Pages Router
<link rel="canonical" href="https://myapp.com/products/widget" />
```

---

## Rendering Strategy and SEO

| Strategy | SEO impact | Use when |
| --- | --- | --- |
| SSR (Server-Side Rendering) | Excellent — full HTML on first request | Dynamic content, personalised pages |
| SSG (Static Generation) | Excellent — pre-rendered HTML | Stable content, blogs, marketing |
| ISR (Incremental Static Regeneration) | Excellent — periodically refreshed | Mostly stable with occasional updates |
| CSR (Client-Side Rendering) | Poor — content missing on first crawl | Authenticated dashboards, internal tools |

Avoid CSR for any content that should be indexed. Use SSR or SSG with a loading skeleton for authenticated content that still needs SEO.

---

## sitemap.xml and robots.txt

```ts
// Next.js App Router — app/sitemap.ts
import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await fetchAllProducts();

  return [
    { url: 'https://myapp.com', lastModified: new Date(), changeFrequency: 'monthly', priority: 1 },
    ...products.map(p => ({
      url: `https://myapp.com/products/${p.slug}`,
      lastModified: p.updatedAt,
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
  ];
}

// app/robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/', disallow: '/api/' },
    sitemap: 'https://myapp.com/sitemap.xml',
  };
}
```
