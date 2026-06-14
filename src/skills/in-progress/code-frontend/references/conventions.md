# Code Conventions

Apply these conventions when no project-level standard exists. When one does exist, follow the project — note any deviation.

---

## Naming

| Thing | Convention | Example |
| --- | --- | --- |
| Component | PascalCase | `UserCard`, `NavigationMenu` |
| Hook | camelCase, `use` prefix | `useUserProfile`, `useDebounce` |
| Utility function | camelCase, verb-first | `formatDate`, `parseSearchParams` |
| Type / Interface | PascalCase | `UserCardProps`, `ApiResponse` |
| Constant | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_LOCALE` |
| CSS class (plain) | kebab-case | `user-card`, `nav-menu-item` |
| File (component) | PascalCase | `UserCard.tsx` |
| File (hook/util) | camelCase | `useDebounce.ts`, `formatDate.ts` |
| File (type-only) | camelCase, `.types.ts` | `user.types.ts` |
| Folder (component) | PascalCase | `UserCard/` |
| Folder (feature) | kebab-case | `auth/`, `user-profile/` |

---

## File Structure

### Component folder (default)

```
src/components/UserCard/
  UserCard.tsx            # Implementation
  UserCard.types.ts       # Props and local types (omit if trivial — inline instead)
  index.ts                # Barrel export
```

### Feature folder

Group by feature, not by file type:

```
src/features/auth/
  components/
    LoginForm/
      LoginForm.tsx
      index.ts
  hooks/
    useAuth.ts
  utils/
    validatePassword.ts
  auth.types.ts
  index.ts
```

Never organise by type at the top level (`components/`, `hooks/`, `utils/` as siblings at `src/`) in a feature-rich codebase — it does not scale.

### Shared code

```
src/shared/
  components/   # Truly generic UI (Button, Modal, Badge)
  hooks/        # Generic hooks (useDebounce, useLocalStorage)
  utils/        # Pure functions with no framework dependency
  types/        # Shared domain types
```

---

## Exports

- **Named exports only** from component and utility files — no default exports
- **Barrel `index.ts`** in every component folder — re-export the component and its types
- **Do not barrel-export everything** at `src/index.ts` — it creates circular dependency risk and slows bundlers

```ts
// UserCard/index.ts
export { UserCard } from './UserCard';
export type { UserCardProps } from './UserCard.types';
```

---

## Import Order

Enforce this order (configure with `eslint-plugin-import` or Prettier if available):

1. Node built-ins (`node:path`, `node:fs`)
2. External packages (`react`, `next/link`, `zod`)
3. Internal aliases (`@/components`, `@/features`)
4. Relative imports (`./UserCard`, `../utils`)
5. Type-only imports (`import type { ... }`)
6. Style imports (`./UserCard.module.css`)

Separate each group with a blank line.

---

## Props

- Destructure props at the function signature — not inside the body
- Group optional props at the end
- Use explicit `undefined` checks — never rely on falsy coercion for optional callbacks

```ts
// Good
function UserCard({ user, onSelect, className }: UserCardProps) { ... }

// Bad
function UserCard(props: UserCardProps) {
  const { user, onSelect } = props;
}
```

---

## Hooks

- One responsibility per hook — extract when a hook handles more than one concern
- Return named objects, not positional arrays (exception: hooks that mirror `useState`)
- Never call hooks conditionally — keep all hook calls at the top of the function

```ts
// Good
const { data, isLoading, error } = useUserProfile(id);

// Bad
const [data, setData, isLoading, error] = useUserProfile(id);
```

---

## Constants and Magic Values

- No inline magic strings or numbers — extract to named constants
- Co-locate constants with the component that owns them; move to `src/shared/` only when used in two or more places

```ts
// Good
const MAX_VISIBLE_TAGS = 5;
const tags = allTags.slice(0, MAX_VISIBLE_TAGS);

// Bad
const tags = allTags.slice(0, 5);
```
