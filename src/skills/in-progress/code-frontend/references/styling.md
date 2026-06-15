# Styling

CSS principles that apply regardless of framework or CSS library. For CSS library-specific usage (Tailwind, Bootstrap, CSS Modules, shadcn/ui, MUI, Chakra UI), fetch current docs via Context7.

Never mix styling approaches within a single component — pick one and be consistent across the feature.

---

## Design Tokens

Define all visual constants as named tokens before writing component styles. Never use raw hex values, magic numbers, or hardcoded pixel values in component CSS.

```css
/* tokens.css — define once, reference everywhere */
:root {
  /* Colour */
  --color-brand:        #6366f1;
  --color-surface:      #ffffff;
  --color-text-primary: #111827;
  --color-text-muted:   #6b7280;
  --color-border:       #e5e7eb;
  --color-error:        #dc2626;
  --color-success:      #16a34a;

  /* Spacing scale */
  --space-1:  0.25rem;
  --space-2:  0.5rem;
  --space-4:  1rem;
  --space-6:  1.5rem;
  --space-8:  2rem;
  --space-12: 3rem;
  --space-16: 4rem;

  /* Typography */
  --font-sans:   'Inter', system-ui, sans-serif;
  --font-mono:   'JetBrains Mono', monospace;
  --text-sm:     0.875rem;
  --text-base:   1rem;
  --text-lg:     1.125rem;
  --text-xl:     1.25rem;
  --leading-tight:  1.25;
  --leading-normal: 1.5;

  /* Radius */
  --radius-sm:  0.25rem;
  --radius-md:  0.5rem;
  --radius-lg:  0.75rem;
  --radius-full: 9999px;

  /* Shadow */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* Transition */
  --duration-fast:   100ms;
  --duration-normal: 200ms;
  --duration-slow:   300ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
}
```

---

## Dark Mode

Use `prefers-color-scheme` for automatic switching and `data-theme` for user-controlled override:

```css
/* Automatic — follows OS preference */
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface:      #0f172a;
    --color-text-primary: #f1f5f9;
    --color-text-muted:   #94a3b8;
    --color-border:       #1e293b;
  }
}

/* Manual override — applied via JS toggle */
[data-theme='dark'] {
  --color-surface:      #0f172a;
  --color-text-primary: #f1f5f9;
  --color-text-muted:   #94a3b8;
  --color-border:       #1e293b;
}

[data-theme='light'] {
  --color-surface:      #ffffff;
  --color-text-primary: #111827;
}
```

Toggle via JS — always support three values: `light`, `dark`, and `system` (follows OS). Store preference in `localStorage` (see `references/storage.md`):

```ts
type Theme = 'system' | 'light' | 'dark';

function applyTheme(theme: Theme): void {
  const resolved = theme === 'system'
    ? window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    : theme;
  document.documentElement.setAttribute('data-theme', resolved);
}

function setTheme(theme: Theme): void {
  localStorage.setItem('theme', theme);
  applyTheme(theme);
}

// Re-apply when OS preference changes (relevant when theme === 'system')
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  const stored = (localStorage.getItem('theme') as Theme) ?? 'system';
  if (stored === 'system') applyTheme('system');
});

// On page load — restore preference before first paint to avoid flash
const stored = (localStorage.getItem('theme') as Theme) ?? 'system';
applyTheme(stored);
```

---

## Layout

### Flexbox — for one-dimensional layout

```css
/* Row with gap, wrapping on small screens */
.card-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

/* Centering */
.centered {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Sidebar + main — sidebar fixed, main grows */
.layout {
  display: flex;
  gap: var(--space-8);
}
.layout__sidebar { flex: 0 0 240px; }
.layout__main    { flex: 1 1 0; min-width: 0; } /* min-width: 0 prevents overflow */
```

### Grid — for two-dimensional layout

```css
/* Responsive grid — no media queries needed */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-6);
}

/* Named areas for page layout */
.page {
  display: grid;
  grid-template-areas:
    'header header'
    'nav    main'
    'footer footer';
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
}
.page__header { grid-area: header; }
.page__nav    { grid-area: nav; }
.page__main   { grid-area: main; }
.page__footer { grid-area: footer; }
```

---

## Responsive Design

**Mobile-first** — write styles for the smallest screen first, then override at larger breakpoints with `min-width` queries:

```css
/* Mobile default */
.card { flex-direction: column; padding: var(--space-4); }

/* Tablet and up */
@media (min-width: 768px) {
  .card { flex-direction: row; padding: var(--space-6); }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .card { padding: var(--space-8); }
}
```

### Common breakpoints

| Name | Min-width | Target |
| --- | --- | --- |
| `sm` | 640px | Large phones landscape |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small desktops |
| `xl` | 1280px | Standard desktops |
| `2xl` | 1536px | Wide screens |

Use `dvh` (`100dvh`) instead of `vh` (`100vh`) for full-height layouts on mobile — `vh` does not account for the browser chrome.

---

## Typography

```css
/* Base scale — set on :root or body */
body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--color-text-primary);
  -webkit-font-smoothing: antialiased;
}

/* Fluid type scale — scales between viewport sizes without breakpoints */
h1 {
  font-size: clamp(1.75rem, 4vw, 3rem);
  line-height: var(--leading-tight);
  font-weight: 700;
}

h2 { font-size: clamp(1.375rem, 3vw, 2rem); font-weight: 600; }
h3 { font-size: clamp(1.125rem, 2vw, 1.5rem); font-weight: 600; }
```

Rules:

- Set `font-size` on `:root` in `rem` — never override the user's browser default font size
- Use `rem` for font sizes, `em` for spacing relative to font size, `px` for borders only
- Maximum line length: 60–75 characters (`max-width: 65ch`) for body text

---

## Logical Properties

Use logical properties for layouts that must work in both LTR and RTL (see `references/i18n.md`):

```css
/* Physical — breaks in RTL */
.card { margin-left: 1rem; padding-left: 1.5rem; text-align: left; }

/* Logical — works in both LTR and RTL */
.card {
  margin-inline-start: 1rem;
  padding-inline: 1.5rem;
  text-align: start;
}
```

| Physical | Logical equivalent |
| --- | --- |
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` / `padding-right` | `padding-inline` |
| `border-left` | `border-inline-start` |
| `text-align: left` | `text-align: start` |
| `top` / `bottom` | `inset-block-start` / `inset-block-end` |

---

## Animation

Prefer `transform` and `opacity` — compositor-only properties that never trigger layout:

```css
.fade-in {
  animation: fadeIn var(--duration-normal) var(--ease-out) forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .fade-in { animation: none; }
}
```

See `references/motion.md` for full animation patterns and timing guidelines.

---

## Naming — BEM for Global CSS

When not using CSS Modules or a utility library, use BEM to prevent class collisions in the global scope:

```css
/* Block */            .user-card { }
/* Element */          .user-card__name { }
/* Modifier */         .user-card--featured { }
/* Element modifier */ .user-card__name--truncated { }
```
