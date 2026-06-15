# Performance

Measure before optimising. Never add complexity for a problem that does not exist yet. Apply these patterns when there is a concrete reason — a slow render, a large bundle, a visible layout shift. For framework-specific implementations, fetch current docs via Context7.

---

## Rendering

### Avoid unnecessary re-renders

Only memoize when a measured problem exists. Memoization adds complexity and is only useful when:

- A child component re-renders frequently with stable inputs
- A derived value computation is demonstrably expensive (> ~1ms)
- A callback is a dependency of another reactive unit or passed to a memoized child

**Do not memoize by default.** Premature memoization increases code weight and can hide real issues. Measure with browser or framework DevTools first.

For framework-specific memoization APIs (`memo`, `useMemo`, `useCallback`, `$derived`, `computed`), fetch current docs via Context7.

### Avoid expensive computation in the render path

Computation that runs on every render must be cheap. If a derived value is expensive to compute:

- Memoize it using the framework's reactive primitive
- Move it to a server or build step if the data is static
- Compute it once on input change rather than on every render pass

### Virtualise long lists

Render only the visible portion of lists exceeding ~100 items. Mount and unmount rows as the user scrolls rather than rendering the full list.

**Requirements for a virtual list:**

- A fixed-height scroll container
- A known or estimated row height
- Absolute positioning of rows within a full-height inner container

For framework-specific virtual list implementations, fetch current docs via Context7.

---

## Code Splitting and Lazy Loading

### Split at route and feature boundaries

Load only the code needed for the current view. Defer heavy components (charts, rich text editors, maps, date pickers) until they are needed.

**Principles:**

- Split at route level first — this gives the largest gains with the least complexity
- Split at component level only for components that are rarely shown or are genuinely heavy
- Always provide a loading fallback (skeleton, spinner) while deferred code loads
- For SSR: disable server-side rendering for browser-only libraries

For framework-specific lazy loading (`lazy`/`Suspense`, `dynamic()`, `import()`, SvelteKit route splitting), fetch current docs via Context7.

### Avoid importing entire libraries

```ts
// Bad — entire library in the bundle
import _ from 'lodash';
const result = _.groupBy(items, 'category');

// Good — only the function needed
import groupBy from 'lodash/groupBy';
const result = groupBy(items, 'category');
```

Prefer libraries with native ESM tree-shaking (`date-fns`, `radix-ui`, etc.) over CommonJS bundles where possible.

---

## Layout and Paint

### Prevent layout shift (CLS)

Set explicit dimensions on all media before it loads:

```html
<!-- Always set width and height — browser reserves the space before load -->
<img
  src="hero.webp"
  alt="Hero image"
  width="1200"
  height="600"
  style="width: 100%; height: auto; aspect-ratio: 2/1;"
/>
```

Reserve space for dynamic content that appears after load:

```css
.content-placeholder {
  min-height: 200px; /* matches expected content height */
}
```

### Avoid layout thrash

Reading then writing DOM dimensions in the same frame forces the browser to recalculate layout twice:

```ts
// Bad — read, then write, two layout calculations
const width = element.offsetWidth;   // read — forces layout
element.style.width = width + 'px';  // write — invalidates layout

// Good — use ResizeObserver, which fires after layout
const observer = new ResizeObserver(entries => {
  for (const entry of entries) {
    const { width } = entry.contentRect;
    doSomethingWith(width);
  }
});
observer.observe(element);
```

Prefer `transform` over `top`/`left` for animation — transforms run on the compositor thread and never trigger layout.

---

## Images

```html
<!-- Above-the-fold (LCP candidate) — eager, high priority -->
<img
  src="hero.webp"
  alt="Hero image"
  width="1200"
  height="600"
  loading="eager"
  fetchpriority="high"
  decoding="async"
/>

<!-- Below-the-fold — lazy load -->
<img
  src="product.webp"
  alt="Product photo"
  width="400"
  height="400"
  loading="lazy"
  decoding="async"
/>
```

- Use modern formats: WebP first, AVIF where supported
- Always provide `width` and `height` to prevent layout shift
- Use `srcset` and `sizes` for responsive images

For framework-specific image components (`next/image`, SvelteKit `enhanced:img`), fetch current docs via Context7.

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

- Use `woff2` — best compression, supported everywhere
- Self-host fonts when possible — eliminates third-party DNS lookup
- Preload the primary font file in `<head>`:

```html
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin />
```

For framework-specific font optimisation (`next/font`, Vite font plugins), fetch current docs via Context7.

---

## Network

### Prefetch on intent

Start loading the next destination when the user signals intent (hover, focus) — not speculatively on page load.

```ts
// Generic prefetch on pointer enter
element.addEventListener('pointerenter', () => {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = '/dashboard';
  document.head.appendChild(link);
});
```

For framework router prefetch APIs (`<Link prefetch>`, `router.prefetch()`), fetch current docs via Context7.

### Debounce user input

Delay expensive operations triggered by fast input (search, filter, resize):

```ts
function debounce<T extends (...args: unknown[]) => void>(fn: T, delay: number): T {
  let timer: ReturnType<typeof setTimeout>;
  return ((...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  }) as T;
}

// Usage — works in any framework
const search = debounce((query: string) => fetchResults(query), 300);
input.addEventListener('input', e => search((e.target as HTMLInputElement).value));
```

---

## Measuring

Always measure before and after. Never optimise by intuition alone.

| Tool | What it measures |
| --- | --- |
| Framework DevTools (Profiler/Inspector) | Component render time and frequency |
| Chrome DevTools → Performance | Paint, layout, scripting, long tasks |
| Lighthouse | LCP, CLS, FID/INP, bundle size, a11y score |
| `web-vitals` library | Real-user Core Web Vitals in production |
| `vite-bundle-visualizer` / `@next/bundle-analyzer` | Bundle composition per route |
| `rollup-plugin-visualizer` | Bundle composition (Rollup/Vite) |
