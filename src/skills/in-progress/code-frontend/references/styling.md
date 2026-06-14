# Styling

Apply the approach that matches the detected stack. Never mix approaches within a single component — pick one and be consistent across the feature.

---

## TailwindCSS

### Core conventions

```tsx
// Readable class order: layout → box model → typography → visual → interactive → responsive
<div className="flex flex-col gap-4 p-6 text-sm font-medium bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow md:flex-row">

// Conditional classes — use clsx or cn (shadcn/ui utility)
import { clsx } from 'clsx';

<button
  className={clsx(
    'px-4 py-2 rounded-lg font-medium transition-colors',
    isPrimary && 'bg-blue-600 text-white hover:bg-blue-700',
    !isPrimary && 'bg-gray-100 text-gray-900 hover:bg-gray-200',
    disabled && 'opacity-50 cursor-not-allowed',
  )}
>
  {label}
</button>
```

### Extract repeated patterns to components — not to `@apply`

`@apply` defeats the purpose of utility classes and makes refactoring harder.

```tsx
// Bad — @apply in CSS
// .btn { @apply px-4 py-2 rounded-lg font-medium; }

// Good — extract to a typed React component
interface ButtonProps {
  variant: 'primary' | 'secondary';
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}

const variantClasses: Record<ButtonProps['variant'], string> = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
};

export function Button({ variant, disabled, children, onClick }: ButtonProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={clsx(
        'px-4 py-2 rounded-lg font-medium transition-colors',
        variantClasses[variant],
        disabled && 'opacity-50 cursor-not-allowed',
      )}
    >
      {children}
    </button>
  );
}
```

### Design tokens

Define custom values in `tailwind.config.ts`, not as arbitrary values in class strings:

```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          50:  '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      spacing: {
        '18': '4.5rem',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
};
```

```tsx
// Good — uses token
<div className="bg-brand-500 p-18">

// Bad — arbitrary value for something that should be a token
<div className="bg-[#3b82f6] p-[4.5rem]">
```

### Dark mode

```tsx
// Use Tailwind's dark: variant — class strategy (add 'dark' class to html)
<div className="bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-50">
```

---

## Bootstrap

### Component patterns

```tsx
// Use Bootstrap class names directly; avoid mixing with Tailwind
<div className="card shadow-sm">
  <div className="card-body">
    <h5 className="card-title">{title}</h5>
    <p className="card-text">{description}</p>
    <button className="btn btn-primary">{cta}</button>
  </div>
</div>
```

### Customise via Sass variables — never override compiled CSS

```scss
// styles/bootstrap-custom.scss
// Override before importing Bootstrap
$primary:   #6366f1;
$font-size-base: 1rem;
$border-radius: 0.5rem;

@import 'bootstrap/scss/bootstrap';
```

### Avoid Bootstrap's JavaScript for interactive components in React

Use React state instead of Bootstrap's JS plugins to avoid DOM conflicts:

```tsx
// Bad — Bootstrap JS manipulates DOM directly, conflicts with React
// <button data-bs-toggle="collapse" data-bs-target="#menu">

// Good — React-controlled
const [isOpen, setIsOpen] = useState(false);
<button onClick={() => setIsOpen(prev => !prev)} aria-expanded={isOpen}>
  Menu
</button>
<div className={clsx('collapse', isOpen && 'show')} id="menu">
  ...
</div>
```

---

## CSS Modules

Co-locate the module file with the component:

```
UserCard/
  UserCard.tsx
  UserCard.module.css
```

```css
/* UserCard.module.css */
.root {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 0.75rem;
  background: var(--color-surface);
}

.name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.root:hover {
  box-shadow: var(--shadow-md);
}
```

```tsx
import styles from './UserCard.module.css';
import { clsx } from 'clsx';

export function UserCard({ user, className }: UserCardProps) {
  return (
    <article className={clsx(styles.root, className)}>
      <span className={styles.name}>{user.name}</span>
    </article>
  );
}
```

### CSS custom properties for theming

```css
/* styles/tokens.css — global */
:root {
  --color-surface:      #ffffff;
  --color-text-primary: #111827;
  --color-text-muted:   #6b7280;
  --color-brand:        #6366f1;
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

[data-theme='dark'] {
  --color-surface:      #0f172a;
  --color-text-primary: #f1f5f9;
  --color-text-muted:   #94a3b8;
}
```

---

## Plain CSS

Use BEM naming to prevent collisions in global scope:

```css
/* Block */
.user-card { }

/* Element */
.user-card__name { }
.user-card__avatar { }

/* Modifier */
.user-card--featured { }
.user-card__name--truncated { }
```

Scope to a root selector to reduce collision risk further:

```css
.user-card { display: flex; gap: 1rem; }
.user-card .user-card__name { font-weight: 600; }
```

---

## Component Libraries (Chakra UI, MUI, shadcn/ui, Radix)

### shadcn/ui (Radix + Tailwind)

```tsx
// Add components via CLI — they live in your codebase
// npx shadcn@latest add button card

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>{title}</CardTitle>
  </CardHeader>
  <CardContent>
    <Button variant="outline">{cta}</Button>
  </CardContent>
</Card>
```

Customise via `cn()` and Tailwind classes — never edit the generated component files directly unless the change is permanent.

### MUI (Material UI)

```tsx
import { Button, Card, CardContent, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

// Prefer styled() over sx prop for reusable overrides
const StyledCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: theme.shape.borderRadius * 2,
}));

// Use sx only for one-off adjustments
<Button sx={{ mt: 2 }} variant="contained">Submit</Button>
```

### Chakra UI

```tsx
import { Box, Button, Text } from '@chakra-ui/react';

<Box p={6} bg="white" borderRadius="xl" boxShadow="md">
  <Text fontWeight="semibold">{label}</Text>
  <Button colorScheme="blue" mt={4}>Submit</Button>
</Box>
```

---

## Animation in Styles

Keep animation utilities alongside the component that owns them. See `references/motion.md` for patterns.

```css
/* Prefer transform and opacity for animations — compositor-only */
.fade-in {
  animation: fadeIn 0.2s ease forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .fade-in { animation: none; }
}
```

---

## Responsive Design

Mobile-first in all approaches:

```tsx
// Tailwind — mobile default, larger breakpoints override
<div className="flex-col md:flex-row lg:gap-8">

// CSS — mobile default, min-width queries override
// .grid { grid-template-columns: 1fr; }
// @media (min-width: 768px) { .grid { grid-template-columns: repeat(2, 1fr); } }
```

Common breakpoints (Tailwind defaults, adapt for other approaches):

| Name | Width | Use |
| --- | --- | --- |
| `sm` | 640px | Large phones landscape |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small desktops |
| `xl` | 1280px | Standard desktops |
| `2xl` | 1536px | Wide screens |
