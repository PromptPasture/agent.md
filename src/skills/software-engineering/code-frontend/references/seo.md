# SEO

SEO applies to pages, not components. Skip this for non-page components unless they affect crawlability.

---

## Core Principles

- **Crawlable content**: critical content must be in the initial HTML, not injected by JS after load
- **Unique metadata**: every page has a distinct `title` and `meta description`
- **Logical structure**: one `h1` per page, headings in order, no skipped levels
- **Canonical URL**: prevents duplicate content across routes with query parameters, trailing slashes, or alternate domains

---

## Required Head Tags

Every public page must include these at minimum:

```html
<title>Page Title — Site Name</title>
<meta name="description" content="One to two sentences, under 155 characters." />
<link rel="canonical" href="https://myapp.com/page-path" />

<!-- Open Graph (social sharing) -->
<meta property="og:title" content="Page Title — Site Name" />
<meta property="og:description" content="Same as meta description." />
<meta property="og:image" content="https://myapp.com/og/page.png" />
<meta property="og:url" content="https://myapp.com/page-path" />
<meta property="og:type" content="website" />

<!-- Twitter / X card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title — Site Name" />
<meta name="twitter:description" content="Same as meta description." />
<meta name="twitter:image" content="https://myapp.com/og/page.png" />
```

### Title pattern

Use a consistent title template across all pages — `[Page] — [Site Name]`:

```
Home page:      Site Name
Inner pages:    Page Title — Site Name
Error pages:    Not Found — Site Name
```

Define the template at the root layout level and let individual pages provide only the page-specific part.

### Meta description

- Under 155 characters — longer descriptions are truncated in search results
- Unique per page — duplicate descriptions are ignored or penalised
- Descriptive and action-oriented — describes what the user will find, not the site

---

## OG Image

- Dimensions: **1200 × 630 px** (standard), **1200 × 1200 px** for square cards
- Include the page title and site branding
- Generate dynamically for content pages (product, article, profile)
- Static fallback for pages without dynamic content

---

## Structured Data (JSON-LD)

Add structured data for rich results — articles, products, breadcrumbs, FAQs, organisation info.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Widget Pro",
  "description": "The best widget for your needs.",
  "image": "https://myapp.com/products/widget-pro.jpg",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

Common schema types: `Article`, `Product`, `BreadcrumbList`, `FAQPage`, `Organization`, `WebSite`, `Person`.

Validate with [Google's Rich Results Test](https://search.google.com/test/rich-results) before shipping.

---

## Heading Hierarchy

```html
<!-- Good — one h1, logical order, no skipped levels -->
<main>
  <h1>Product Catalogue</h1>
  <section>
    <h2>Featured Products</h2>
    <article>
      <h3>Widget Pro</h3>
    </article>
  </section>
  <section>
    <h2>All Products</h2>
  </section>
</main>

<!-- Bad — multiple h1, skipped levels -->
<div>
  <h1>Product Catalogue</h1>
  <h1>Featured</h1>    <!-- second h1 -->
  <h4>Widget Pro</h4>  <!-- skipped h2 and h3 -->
</div>
```

---

## Rendering Strategy and SEO

|Strategy|SEO impact|Use when|
|---|---|---|
|SSR (Server-Side Rendering)|Excellent — full HTML on first request|Dynamic, personalised content|
|SSG (Static Generation)|Excellent — pre-rendered HTML|Stable content, blogs, marketing|
|ISR (Incremental Static Regeneration)|Excellent — periodically refreshed|Mostly stable with occasional updates|
|CSR (Client-Side Rendering)|Poor — content missing on first crawl|Authenticated dashboards, internal tools|

Avoid CSR for any content that should be indexed. Use SSR or SSG with a loading skeleton for authenticated content that still needs SEO.

---

## sitemap.xml

Every public site needs a sitemap. At minimum it must list:

- All static public pages with their canonical URL
- All dynamic content pages (products, articles, profiles) with `lastModified`
- Priority and `changeFrequency` hints for the crawler

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://myapp.com/</loc>
    <lastmod>2025-01-01</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://myapp.com/products/widget-pro</loc>
    <lastmod>2025-06-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

---

## robots.txt

```
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /dashboard/

Sitemap: https://myapp.com/sitemap.xml
```

Disallow pages that should not be indexed: API routes, admin areas, authenticated-only content, duplicate paginated routes.
