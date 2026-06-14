# Performance

Measure before optimising. Never add complexity for a problem that does not exist yet. Apply these patterns when there is a concrete reason — a slow render, a large bundle, a visible layout shift.

---

## Rendering

### Avoid unnecessary re-renders

```tsx
// Memoize expensive child components only when the parent re-renders frequently
// and the child's props are stable
const UserCard = memo(function UserCard({ user }: UserCardProps) {
  return <div>{user.name}</div>;
});

// Stabilise callbacks passed as props
const handleSelect = useCallback((id: string) => {
  setSelected(id);
}, []); // deps must be exhaustive

// Memoize expensive derived values
const sorted = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

Rules:

- Do not `memo` every component — measure first
- `useCallback` is only useful when the function is a dependency of another hook or passed to a memoized child
- `useMemo` is only useful when the computation is demonstrably expensive (> ~1ms)

### Avoid derived state in render

```tsx
// Bad — recalculated on every render
function List({ items }: { items: Item[] }) {
  const total = items.reduce((sum, i) => sum + i.value, 0); // runs every render
  return <div>Total: {total}</div>;
}

// Good — memoized
function List({ items }: { items: Item[] }) {
  const total = useMemo(() => items.reduce((sum, i) => sum + i.value, 0), [items]);
  return <div>Total: {total}</div>;
}
```

### Virtualise long lists

Render only visible rows for lists exceeding ~100 items:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 56, // estimated row height in px
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map(row => (
          <div
            key={row.key}
            style={{ position: 'absolute', top: row.start, width: '100%' }}
          >
            <ItemRow item={items[row.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Code Splitting and Lazy Loading

### Lazy-load routes

```tsx
// Next.js App Router — automatic per-segment code splitting
// No manual action needed; each segment is its own bundle

// Vite + React — manual lazy loading for routes
import { lazy, Suspense } from 'react';
const Dashboard = lazy(() => import('./pages/Dashboard'));

<Suspense fallback={<PageSkeleton />}>
  <Dashboard />
</Suspense>
```

### Lazy-load heavy components

```tsx
// Load only when needed — charts, editors, maps, date pickers
const RichTextEditor = dynamic(() => import('@/components/RichTextEditor'), {
  loading: () => <EditorSkeleton />,
  ssr: false, // disable SSR for browser-only libs
});
```

### Avoid importing entire libraries

```ts
// Bad — imports full library
import _ from 'lodash';
const result = _.groupBy(items, 'category');

// Good — imports only the function needed
import groupBy from 'lodash/groupBy';
const result = groupBy(items, 'category');
```

---

## Layout and Paint

### Prevent layout shift (CLS)

```tsx
// Always set explicit width and height on images
<img
  src={src}
  alt={alt}
  width={400}
  height={300}
  style={{ aspectRatio: '4/3', width: '100%', height: 'auto' }}
/>

// Reserve space for dynamic content with min-height
<div style={{ minHeight: '200px' }}>
  {isLoading ? <Skeleton /> : <Content />}
</div>
```

### Avoid layout thrash

Reading then writing DOM dimensions in the same frame forces the browser to recalculate layout twice:

```ts
// Bad — read, then write, forces two layout calculations
const width = element.offsetWidth;  // read — triggers layout
element.style.width = width + 'px'; // write — invalidates layout

// Good — batch reads, then batch writes
// Or use ResizeObserver which fires after layout
const observer = new ResizeObserver(entries => {
  for (const entry of entries) {
    const { width } = entry.contentRect; // read after layout
    doSomethingWith(width);
  }
});
observer.observe(element);
```

Prefer `transform` over `top`/`left` for animation — transforms run on the compositor thread and do not trigger layout.

---

## Images

```tsx
// Next.js — always use next/image for automatic optimisation
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority // add for above-the-fold images; omit for below
  sizes="(max-width: 768px) 100vw, 50vw"
/>

// Non-Next.js — use modern formats and lazy loading
<img
  src="hero.webp"
  alt="Hero image"
  width={1200}
  height={600}
  loading="lazy"     // omit for above-the-fold
  decoding="async"
/>
```

Use `loading="eager"` and `fetchpriority="high"` for the largest above-the-fold image (LCP candidate).

---

## Fonts

```css
/* Prevent invisible text during font load (FOIT) */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap; /* show fallback immediately, swap when loaded */
}
```

In Next.js, use `next/font` — it inlines font CSS, eliminates layout shift, and self-hosts automatically:

```ts
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'], display: 'swap' });
```

---

## Network

### Prefetch on intent

```tsx
// Next.js Link prefetches on hover by default
<Link href="/dashboard">Dashboard</Link>

// Prefetch programmatically on hover or focus
const router = useRouter();
<button
  onMouseEnter={() => router.prefetch('/dashboard')}
  onClick={() => router.push('/dashboard')}
>
  Go to dashboard
</button>
```

### Debounce and throttle user input

```ts
import { useMemo } from 'react';
import debounce from 'lodash/debounce';

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const debouncedSearch = useMemo(
    () => debounce(onSearch, 300),
    [onSearch]
  );

  return <input onChange={e => debouncedSearch(e.target.value)} />;
}
```

---

## Measuring

Use these tools before and after optimisation — never guess:

| Tool | What it measures |
| --- | --- |
| React DevTools Profiler | Component render time and frequency |
| Chrome DevTools Performance | Paint, layout, scripting, long tasks |
| Lighthouse | LCP, CLS, FID/INP, bundle size, a11y |
| `web-vitals` library | Real-user Core Web Vitals in production |
| `next build` output | Bundle size per route (Next.js) |
| `vite-bundle-visualizer` | Bundle composition (Vite) |
