# Next.js — Framework Adapter

Next.js-specific patterns on top of `references/frameworks/react.md`. Read the React adapter first — this file covers only what Next.js adds or overrides.

Covers: App Router (primary), Pages Router (noted where different).

---

## Error Handling

### App Router — error.tsx

```tsx
// app/dashboard/error.tsx
'use client';

import { useEffect } from 'react';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function DashboardError({ error, reset }: ErrorProps) {
  useEffect(() => {
    console.error(error); // send to error reporting service
  }, [error]);

  return (
    <section role="alert" aria-live="assertive">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </section>
  );
}
```

### App Router — not-found.tsx

```tsx
// app/not-found.tsx
export default function NotFound() {
  return (
    <main>
      <h1>Page not found</h1>
      <p>The page you requested does not exist.</p>
      <a href="/">Go home</a>
    </main>
  );
}
```

### App Router — global-error.tsx

```tsx
// app/global-error.tsx — catches errors in the root layout
'use client';
export default function GlobalError({ reset }: { reset: () => void }) {
  return (
    <html><body>
      <section role="alert">
        <h2>Something went wrong</h2>
        <button onClick={reset}>Try again</button>
      </section>
    </body></html>
  );
}
```

---

## Routing

```tsx
import Link from 'next/link';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';
import { redirect, notFound } from 'next/navigation';

// Prefetch on hover (default for Link)
<Link href="/dashboard">Dashboard</Link>

// Programmatic navigation
const router = useRouter();
router.push('/dashboard');
router.prefetch('/dashboard');   // prefetch on hover/focus
router.replace('/login');        // no back history entry

// Server-side redirect / not found
redirect('/login');              // in Server Component or action
notFound();                      // triggers not-found.tsx
```

---

## Data Fetching

### Server Components (App Router)

```tsx
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation';
import { fetchUser } from '@/api/users';

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id).catch(() => null);
  if (!user) notFound();
  return <UserProfile user={user} />;
}
```

Cache control:

```ts
fetch(url);                                        // cached (default)
fetch(url, { next: { revalidate: 60 } });          // ISR — revalidate every 60s
fetch(url, { cache: 'no-store' });                 // SSR — always fresh
fetch(url, { next: { tags: ['user'] } });          // tag for on-demand revalidation
```

On-demand revalidation:

```ts
// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache';
export async function POST() {
  revalidateTag('user');
  return Response.json({ revalidated: true });
}
```

### generateStaticParams (App Router)

```ts
// app/products/[slug]/page.tsx
export async function generateStaticParams() {
  const products = await fetchAllProducts();
  return products.map(p => ({ slug: p.slug }));
}
```

### Pages Router — getServerSideProps / getStaticProps

```ts
// SSR
export async function getServerSideProps({ params }: GetServerSidePropsContext) {
  const user = await fetchUser(params!.id as string);
  if (!user) return { notFound: true };
  return { props: { user } };
}

// SSG
export async function getStaticProps({ params }: GetStaticPropsContext) {
  const product = await fetchProduct(params!.slug as string);
  return { props: { product }, revalidate: 60 }; // ISR
}

export async function getStaticPaths() {
  const products = await fetchAllProducts();
  return { paths: products.map(p => ({ params: { slug: p.slug } })), fallback: 'blocking' };
}
```

### URL state — App Router

```ts
import { useRouter, useSearchParams, usePathname } from 'next/navigation';

export function useFilters() {
  const router       = useRouter();
  const pathname     = usePathname();
  const searchParams = useSearchParams();

  const filters = {
    category: searchParams.get('category') ?? 'all',
    page:     Number(searchParams.get('page') ?? '1'),
  };

  function setFilter(key: string, value: string) {
    const params = new URLSearchParams(searchParams.toString());
    params.set(key, value);
    params.set('page', '1');
    router.push(`${pathname}?${params.toString()}`);
  }

  return { filters, setFilter };
}
```

---

## Performance

### next/image

```tsx
import Image from 'next/image';

// Above-the-fold (LCP) — priority
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority sizes="100vw" />

// Below-the-fold — lazy (default)
<Image src="/product.jpg" alt="Product" width={400} height={400} sizes="(max-width: 768px) 100vw, 400px" />
```

### next/font

```ts
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html className={inter.className}>{children}</html>;
}
```

### dynamic() — code splitting

```tsx
import dynamic from 'next/dynamic';

const RichTextEditor = dynamic(() => import('@/components/RichTextEditor'), {
  loading: () => <EditorSkeleton />,
  ssr: false,                      // browser-only libraries
});
```

### Bundle analyser

```ts
// next.config.ts
import withBundleAnalyzer from '@next/bundle-analyzer';
export default withBundleAnalyzer({ enabled: process.env.ANALYZE === 'true' })({ /* config */ });
// Run: ANALYZE=true next build
```

---

## SEO — Metadata API (App Router)

### Title template

```ts
// app/layout.tsx — define template once
export const metadata: Metadata = {
  title: { default: 'MyApp', template: '%s — MyApp' },
};

// app/about/page.tsx — only the page title
export const metadata: Metadata = {
  title: 'About Us',   // renders: "About Us — MyApp"
  description: 'Learn about MyApp.',
  openGraph: {
    title: 'About Us — MyApp',
    description: 'Learn about MyApp.',
    images: [{ url: 'https://myapp.com/og/about.png', width: 1200, height: 630 }],
  },
  alternates: { canonical: 'https://myapp.com/about' },
};
```

### Dynamic metadata

```ts
// app/products/[slug]/page.tsx
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const product = await fetchProduct(params.slug).catch(() => null);
  if (!product) return { title: 'Not found' };
  return {
    title: product.name,
    description: product.description.slice(0, 155),
    openGraph: { images: [{ url: product.imageUrl, width: 1200, height: 630 }] },
    alternates: { canonical: `https://myapp.com/products/${params.slug}` },
  };
}
```

### Sitemap and robots

```ts
// app/sitemap.ts
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
    rules: { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] },
    sitemap: 'https://myapp.com/sitemap.xml',
  };
}
```

### Pages Router — Head

```tsx
import Head from 'next/head';

export default function AboutPage() {
  return (
    <>
      <Head>
        <title>About Us — MyApp</title>
        <meta name="description" content="Learn about MyApp." />
        <meta property="og:title" content="About Us — MyApp" />
        <meta property="og:image" content="https://myapp.com/og/about.png" />
        <link rel="canonical" href="https://myapp.com/about" />
      </Head>
      <main>...</main>
    </>
  );
}
```

---

## PWA — next-pwa

```ts
// next.config.ts
import withPWA from 'next-pwa';

export default withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
      handler: 'CacheFirst',
      options: { cacheName: 'google-fonts', expiration: { maxEntries: 4, maxAgeSeconds: 31536000 } },
    },
    {
      urlPattern: /^https:\/\/api\./,
      handler: 'NetworkFirst',
      options: { cacheName: 'api-cache', expiration: { maxEntries: 100, maxAgeSeconds: 86400 } },
    },
  ],
})({ /* next config */ });
```

---

## i18n — next-intl (App Router)

### Setup

```ts
// next.config.ts
import createNextIntlPlugin from 'next-intl/plugin';
export default createNextIntlPlugin()({ /* next config */ });

// middleware.ts
import createMiddleware from 'next-intl/middleware';
export default createMiddleware({
  locales: ['en', 'fr', 'ar'],
  defaultLocale: 'en',
  localePrefix: 'always',
});
export const config = { matcher: ['/((?!api|_next|.*\\..*).*)'] };
```

### Root layout

```tsx
// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({
  children,
  params: { locale },
}: { children: React.ReactNode; params: { locale: string } }) {
  const messages = await getMessages();
  const dir = ['ar', 'he', 'fa', 'ur'].includes(locale) ? 'rtl' : 'ltr';
  return (
    <html lang={locale} dir={dir}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### Usage

```tsx
// Server Component
import { getTranslations } from 'next-intl/server';
const t = await getTranslations('product');
return <h1>{t('addToCart')}</h1>;

// Client Component
'use client';
import { useTranslations } from 'next-intl';
const t = useTranslations('nav');
return <button>{t('cart', { count })}</button>;
```

### Locale switcher

```ts
import { useRouter, usePathname } from 'next/navigation';

export function useLocaleSwitcher() {
  const router   = useRouter();
  const pathname = usePathname();

  function setLocale(locale: string) {
    document.cookie = `locale=${locale}; path=/; max-age=${60 * 60 * 24 * 365}; SameSite=Lax`;
    const newPath = pathname.replace(/^\/[a-z]{2}(-[A-Z]{2})?/, `/${locale}`);
    router.push(newPath);
  }

  return { setLocale };
}
```

---

## Middleware

```ts
// middleware.ts
import { NextResponse, type NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value;

  // Protect routes
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};
```

---

## Server Actions (App Router)

```ts
// app/actions/user.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const updateSchema = z.object({ name: z.string().min(1) });

export async function updateUser(formData: FormData) {
  const parsed = updateSchema.safeParse({ name: formData.get('name') });
  if (!parsed.success) return { error: parsed.error.flatten() };

  await db.users.update({ name: parsed.data.name });
  revalidatePath('/profile');
}
```

```tsx
// Usage in a Client Component
import { updateUser } from '@/app/actions/user';

<form action={updateUser}>
  <input name="name" required />
  <button type="submit">Save</button>
</form>
```
