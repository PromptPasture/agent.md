# CSS Modules

---

## Setup

CSS Modules work out of the box with Vite, Next.js, and SvelteKit. No additional configuration required.

Name files with the `.module.css` (or `.module.scss`) suffix:

```
UserCard/
  UserCard.tsx          # or .svelte, .vue
  UserCard.module.css
  index.ts
```

---

## Usage

### React / Next.js

```tsx
import styles from './UserCard.module.css';
import { clsx } from 'clsx';

interface UserCardProps {
  user: User;
  className?: string;
  featured?: boolean;
}

export function UserCard({ user, className, featured }: UserCardProps) {
  return (
    <article className={clsx(styles.root, featured && styles.featured, className)}>
      <span className={styles.name}>{user.name}</span>
      <span className={styles.role}>{user.role}</span>
    </article>
  );
}
```

### SvelteKit

```svelte
<script lang="ts">
  import styles from './UserCard.module.css';
  import { clsx } from 'clsx';

  let { user, class: className, featured = false } = $props();
</script>

<article class={clsx(styles.root, featured && styles.featured, className)}>
  <span class={styles.name}>{user.name}</span>
</article>
```

---

## CSS File Conventions

```css
/* UserCard.module.css */

/* Use camelCase for class names — they become JS object properties */
.root {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-6);
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  transition: box-shadow var(--duration-normal) var(--ease-out);
}

.root:hover {
  box-shadow: var(--shadow-md);
}

.featured {
  border: 2px solid var(--color-brand);
}

.name {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.role {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
```

Rules:

- **camelCase class names** — they are accessed as JS properties (`styles.cardTitle`, not `styles['card-title']`)
- **Reference design tokens** via CSS custom properties — never raw hex or pixel values
- **No global selectors** — CSS Modules scope everything locally by default

---

## Global Styles

Use `:global()` sparingly — only for styling third-party components or targeting elements outside the module's scope:

```css
/* Target a child that is rendered by a third-party library */
.root :global(.third-party-class) {
  color: var(--color-brand);
}
```

For truly global styles, use a dedicated `src/styles/globals.css` (imported once in the root layout) rather than `:global()` inside a module.

---

## Composition

Compose classes from other modules without duplication:

```css
/* base.module.css */
.button {
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: background var(--duration-fast) var(--ease-out);
}

/* PrimaryButton.module.css */
.button {
  composes: button from './base.module.css';
  background: var(--color-brand);
  color: white;
}
```

---

## Theming

CSS Modules pair naturally with CSS custom properties for theming. Define tokens globally (see `references/styling.md`) and reference them inside module files — the scoping and the theming remain independent.

```css
/* Tokens in globals.css — available everywhere */
:root { --color-surface: #ffffff; }
[data-theme='dark'] { --color-surface: #0f172a; }

/* Module file references the token — theme switch is automatic */
.card { background: var(--color-surface); }
```
