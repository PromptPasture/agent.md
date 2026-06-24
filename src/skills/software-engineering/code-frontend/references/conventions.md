# Code Conventions

Apply these when no project standard exists. If one does, follow it and note any deviations.

---

## Naming

| Thing | Convention | Example |
| --- | --- | --- |
| Component | PascalCase | `UserCard`, `NavigationMenu` |
| Composable / store / hook | camelCase, framework-idiomatic prefix | `useUserProfile`, `createAuthStore` |
| Utility function | camelCase, verb-first | `formatDate`, `parseSearchParams` |
| Type / Interface | PascalCase | `UserCardProps`, `ApiResponse` |
| Constant | SCREAMING_SNAKE_CASE | `MAX_RETRIES`, `DEFAULT_LOCALE` |
| CSS class (plain) | kebab-case (BEM for global scope — see `references/styling.md`) | `user-card`, `user-card__name`, `user-card--featured` |
| File (component) | PascalCase | `UserCard.tsx`, `UserCard.svelte` |
| File (util/composable) | camelCase | `formatDate.ts`, `useDebounce.ts` |
| File (type-only) | camelCase, `.types.ts` | `user.types.ts` |
| Folder (component) | PascalCase | `UserCard/` |
| Folder (feature) | kebab-case | `auth/`, `user-profile/` |

---

## File Structure

### Component folder (default)

```
src/components/UserCard/
  UserCard.{tsx,svelte,vue}   # Implementation
  UserCard.types.ts            # Props and local types (omit if trivial — inline instead)
  index.ts                     # Barrel export
```

### Feature folder

Group by feature, not by file type:

```
src/features/auth/
  components/
    LoginForm/
  composables/        # or hooks/, stores/ — framework-idiomatic
  utils/
  auth.types.ts
  index.ts
```

Never organise by type at the top level (`components/`, `utils/` as siblings at `src/`) in a feature-rich codebase — it does not scale.

### Shared code

```
src/shared/
  components/     # Truly generic UI (Button, Modal, Badge)
  composables/    # Generic reactive logic — name varies by framework
  utils/          # Pure functions with no framework dependency
  types/          # Shared domain types
```

---

## Exports

- **Named exports only** from component and utility files — no default exports (unless the framework requires it, e.g. SvelteKit route files)
- **Barrel `index.ts`** in every component folder — re-export the component and its types
- **Do not barrel-export everything** at `src/index.ts` — it creates circular dependency risk and slows bundlers

```ts
// UserCard/index.ts
export { UserCard } from './UserCard';
export type { UserCardProps } from './UserCard.types';
```

---

## Import Order

Enforce this order (configure with `eslint-plugin-import` or the framework's preferred linter):

1. Node built-ins (`node:path`, `node:fs`)
2. External packages (`zod`, `date-fns`, framework imports)
3. Internal aliases (`$lib/`, `@/components`, `~~/`)
4. Relative imports (`./UserCard`, `../utils`)
5. Type-only imports (`import type { ... }`)
6. Style imports (`./UserCard.module.css`)

Separate each group with a blank line.

---

## Component Props

- Destructure or bind props at the component boundary — not deep inside the implementation
- Group required props before optional ones
- Use explicit checks for optional callbacks — never rely on falsy coercion

---

## Reactive Logic (Composables / Hooks / Stores)

- One responsibility per unit — extract when it handles more than one concern
- Return named objects, not positional arrays, when returning multiple values
- Never invoke reactive logic conditionally

---

## Constants and Magic Values

- No inline magic strings or numbers — extract to named constants
- Co-locate constants with the component that owns them; promote to `src/shared/` only when used in two or more places

```ts
// Good
const MAX_VISIBLE_TAGS = 5;
const tags = allTags.slice(0, MAX_VISIBLE_TAGS);

// Bad
const tags = allTags.slice(0, 5);
```
