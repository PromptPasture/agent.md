# TailwindCSS

---

## Setup

### Vite (React, SvelteKit)

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```ts
// tailwind.config.ts
export default {
  content: ['./src/**/*.{html,js,ts,jsx,tsx,svelte,vue}'],
  theme: { extend: {} },
  plugins: [],
};
```

### Next.js

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```ts
// tailwind.config.ts
export default {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: { extend: {} },
  plugins: [],
};
```

### SvelteKit — via svelte-add

```bash
npx svelte-add@latest tailwindcss
```

---

## Class Order Convention

Write classes in this order — layout → box model → typography → visual → interactive → responsive:

```html
<div class="flex flex-col gap-4 p-6 text-sm font-medium bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow md:flex-row">
```

---

## Conditional Classes — always use clsx

```ts
import { clsx } from 'clsx';
// or: import { cn } from '$lib/utils'; // shadcn projects

<button class={clsx(
  'px-4 py-2 rounded-lg font-medium transition-colors',
  isPrimary  && 'bg-blue-600 text-white hover:bg-blue-700',
  !isPrimary && 'bg-gray-100 text-gray-900 hover:bg-gray-200',
  disabled   && 'opacity-50 cursor-not-allowed',
)}>
```

---

## Design Tokens — extend config, never use arbitrary values

```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        brand: { 50: '#eff6ff', 500: '#6366f1', 900: '#1e3a8a' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
      },
    },
  },
};
```

```html
<!-- Good — uses token -->
<div class="bg-brand-500 p-18">

<!-- Bad — arbitrary value for something that should be a token -->
<div class="bg-[#6366f1] p-[4.5rem]">
```

---

## Extract to Components — never to @apply

`@apply` defeats the purpose of utility classes and makes refactoring harder. Extract repeated patterns to a typed component instead.

```ts
// Bad
// .btn { @apply px-4 py-2 rounded-lg font-medium; }

// Good — typed component with variant map
const variantClasses = {
  primary:   'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
  ghost:     'text-gray-600 hover:bg-gray-100',
} as const;
```

---

## Dark Mode

Use the `class` strategy for user-controlled toggle:

```ts
// tailwind.config.ts
export default { darkMode: 'class' };
```

Apply by toggling the `dark` class on `<html>`. See `references/styling.md` for the full three-way (light / dark / system) toggle implementation.

```html
<div class="bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-50">
```

---

## RTL

Use the `rtl:` variant for direction-specific overrides:

```html
<div class="ml-4 rtl:ml-0 rtl:mr-4">

<!-- Or use logical property utilities (Tailwind v3.3+) -->
<div class="ms-4">  <!-- margin-inline-start -->
<div class="ps-6">  <!-- padding-inline-start -->
```

---

## Typography Plugin

```bash
npm install -D @tailwindcss/typography
```

```ts
// tailwind.config.ts
plugins: [require('@tailwindcss/typography')]
```

```html
<article class="prose prose-lg dark:prose-invert max-w-none">
  <!-- Rendered markdown content -->
</article>
```
