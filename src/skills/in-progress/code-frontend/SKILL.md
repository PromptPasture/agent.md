---
name: code-frontend
description: You use this when user asks to build a component, create a page, implement UI, scaffold a form, or produce any frontend code in a real codebase. It generates production-ready code with auto-detected stack, interface contracts, decomposition heuristics, and a P0–P3 quality checklist covering a11y, TypeScript, SEO, performance, and error handling.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "2.1.2"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: web-development
  tags: [frontend, typescript, javascript, css, a11y, seo, pwa, i18n]
---

# Doing Frontend

Generates production-ready frontend code in the project's existing stack.
Four phases: **Discover → Plan → Build → Validate**. Each phase produces a confirmed output before the next begins. Phases are skippable when the user already provides the relevant context.

---

## Phase 1 — Discover

**Goal:** Establish the project stack before writing a single line of code.

### 1.1 Read project files

Inspect the following in order. Stop reading a file once the needed signal is found.

| File | Signal to extract |
| --- | --- |
| `package.json` | Framework, CSS lib, language, key deps (query, router, i18n, etc.) |
| `tsconfig.json` | TypeScript presence, `strict` mode on/off, path aliases |
| `next.config.*` | Next.js — check `app/` dir for App Router, `pages/` for Pages Router |
| `vite.config.*` | Vite — check plugins for React (`@vitejs/plugin-react`), Preact (`@preact/preset-vite`), Vue, Lit, Svelte, Solid (`vite-plugin-solid`) |
| `svelte.config.*` | SvelteKit |
| `nuxt.config.*` | Nuxt |
| `astro.config.*` | Astro |
| `remix.config.*` / `vite.config.*` with Remix plugin | Remix |
| `angular.json` | Angular |
| `pnpm-workspace.yaml` / `turbo.json` / `nx.json` | Monorepo; note which workspace the task targets |

### 1.2 Detect CSS approach

From `package.json` dependencies and config files:

- **TailwindCSS** — `tailwindcss` dep + `tailwind.config.*`
- **Bootstrap** — `bootstrap` dep
- **CSS Modules** — `.module.css` files or framework default
- **Plain CSS** — none of the above
- **Vue Scoped Styles** — `vue` dep present and no other CSS lib found
- **Other** — note the library name (Chakra, MUI, shadcn/ui, etc.)

### 1.3 Output a detection summary

Present a concise summary and wait for confirmation before proceeding:

```
Stack detected:
  Framework:  Next.js 14 (App Router)
  Language:   TypeScript (strict: true)
  CSS:        TailwindCSS
  State:      Zustand
  Fetching:   React Query
  Monorepo:   no
```

If the user corrects any item, update and re-confirm.

### 1.4 Empty project fallback

If no framework config is found, suggest a default stack and wait for explicit user confirmation before proceeding:

```
No framework detected. Suggested stack:
  Framework:  Next.js 15 (App Router)
  Language:   TypeScript (strict)
  CSS:        TailwindCSS

Confirm, or tell me what stack to use instead.
```

Do not proceed to Plan until the stack is confirmed.

---

## Phase 2 — Plan

**Goal:** Produce a component interface contract the user confirms before any code is written.

### 2.1 Ask clarifying questions (if needed)

Before drafting the contract, resolve any ambiguity with a single focused question. Do not ask more than one question at a time. Skip this step if the user's request is already specific enough.

Common gaps to check:

- Is this a new component or extending an existing one?
- Where does it live in the file tree?
- Does it fetch its own data or receive it via props?
- Any specific a11y, i18n, or animation requirements for this component?

### 2.2 Draft the interface contract

Produce the contract in this format. Omit sections that are genuinely not applicable (e.g. no events, no slots).

```
Component:   UserCard
File:        src/components/UserCard/UserCard.{tsx,svelte,vue}
Index:       src/components/UserCard/index.ts

Props:
  user        User        required   User object to display
  onSelect?   () => void  optional   Called when card is clicked
  class?      string      optional   Additional CSS classes

Events / Callbacks:
  onSelect    Fires on click and Enter/Space keypress

Children / Slots:
  none

Dependencies:
  Internal:   src/types/User.ts
  External:   none

Notes:
  Keyboard accessible. Renders a link when href is provided, button otherwise.
```

### 2.3 Identify which reference docs apply

Load the framework adapter that matches the detected stack — always load exactly one:

| Detected stack | Adapter |
| --- | --- |
| Next.js (App Router or Pages Router) | `references/frameworks/js/nextjs.md` + `references/frameworks/js/react.md` |
| Vite + React / CRA / Remix | `references/frameworks/js/react.md` |
| Preact | `references/frameworks/js/preact.md` |
| SvelteKit | `references/frameworks/js/svelte.md` |
| Vue (Vite SPA) | `references/frameworks/js/vue.md` |
| Nuxt | `references/frameworks/js/nuxt.md` + `references/frameworks/js/vue.md` |
| Astro | `references/frameworks/js/astro.md` |
| Angular | `references/frameworks/js/angular.md` |
| SolidJS / SolidStart | `references/frameworks/js/solidjs.md` |
| Other | No adapter available — apply concern docs only; note the gap to the user |

Then load the CSS framework adapter that matches the detected CSS approach — load exactly one:

| Detected CSS | Adapter |
| --- | --- |
| TailwindCSS | `references/frameworks/css/tailwind.md` |
| Bootstrap | `references/frameworks/css/bootstrap.md` |
| CSS Modules | `references/frameworks/css/css-modules.md` |
| shadcn/ui or shadcn-svelte | `references/frameworks/css/shadcn.md` + `references/frameworks/css/tailwind.md` |
| MUI | `references/frameworks/css/mui.md` |
| Plain CSS / none detected | `references/styling.md` |

Then load concern docs based on the task:

| Signal | Load |
| --- | --- |
| Form inputs present | `references/forms.md` |
| Data fetched inside component | `references/data-fetching.md` |
| Animation or transition required | `references/motion.md` |
| User-visible copy or labels present | `references/i18n.md` |
| State shared across components | `references/state.md` |
| Persistence across reloads or tabs needed | `references/storage.md` |
| Page component (not shared UI) | `references/seo.md` |
| PWA in manifest or scope | `references/pwa.md` |
| No existing project conventions found | `references/conventions.md` |
| Any a11y complexity beyond basics | `references/a11y.md` |
| Any async operation or heavy dependency | `references/performance.md` |
| Error states or boundaries needed | `references/error-handling.md` |

### 2.4 Wait for confirmation

Present the contract and the list of reference docs to load. Do not proceed to Build until the user confirms or requests changes.

---

## Phase 3 — Build

**Goal:** Write production-ready files that match the confirmed contract and detected stack.

### 3.1 Load reference docs

Load every reference doc identified in Phase 2 before writing any file. Apply its guidance throughout the Build phase.

### 3.2 Apply decomposition heuristics

Before writing, state the decomposition rationale out loud. Split into smaller components when any of the following is true:

- Props exceed 5–7 on a single component
- Markup or template exceeds ~150 lines
- A distinct visual or logical unit repeats more than once
- A section has its own independent state or data dependency
- A piece could be reused elsewhere without modification

Prefer flat hierarchies. Do not create abstractions that exist only to satisfy a single use case.

### 3.3 File and folder conventions

Follow the project's existing conventions if present. When no convention is established, apply these defaults:

```
src/components/ComponentName/
  ComponentName.{tsx,svelte,vue}   # Component implementation
  ComponentName.types.ts           # Props and local types (if non-trivial)
  index.ts                         # Barrel export
```

- One component per file
- Named exports only — no default exports from component files
- Barrel `index.ts` re-exports from every component folder
- Co-locate types with the component that owns them
- Feature folders over type folders (`src/features/auth/` not `src/components/forms/`)

### 3.4 Code standards

Apply these unconditionally, regardless of what exists in the project:

#### TypeScript

- `strict: true` — never widen to `any`; use `unknown` and narrow explicitly
- Explicit return types on all exported functions and components
- No unused imports, variables, or parameters
- Prefer `type` over `interface` for props and local types; use `interface` for extendable contracts

#### Component structure

Write in this order:

1. Imports (external → internal → types → styles)
2. Types and interfaces
3. Constants and helpers local to the file
4. Component function
5. Sub-components (if small and tightly coupled)

#### Error handling

- Wrap async operations in try/catch with typed errors
- Provide a visible fallback UI for every error state — never silently swallow
- Use error boundaries at route and feature boundaries; see `references/error-handling.md` for patterns

#### Accessibility

- Prefer semantic HTML over ARIA — use ARIA only where native semantics are insufficient
- Every interactive element is keyboard reachable and has a visible focus state
- No click handler on a non-interactive element without the appropriate `role` and keyboard event handler
- See `references/a11y.md` for patterns beyond the basics

#### Performance

- Memoize only when a concrete re-render problem exists — not by default
- Lazy-load routes and heavy components with dynamic imports
- No expensive computation in the render or template path — compute outside or use the framework's reactive primitive
- See `references/performance.md` for deeper patterns

### 3.5 Write files

Write each file in full. No placeholders, no TODOs, no stub implementations. If a piece is genuinely out of scope for this task, omit it and state why — do not leave it half-written.

After writing all files, list every file created or modified:

```
Created:
  src/components/UserCard/UserCard.tsx
  src/components/UserCard/UserCard.types.ts
  src/components/UserCard/index.ts

Modified:
  src/components/index.ts   (added UserCard export)
```

Present this list and wait for the user to confirm before proceeding to Validate.

---

## Phase 4 — Validate

**Goal:** Work through every checklist item before declaring the output complete. Fix any issue found — do not report and skip.

Items are ordered by severity. P0 failures block delivery. P1–P3 failures must be resolved before closing but do not require re-confirmation from the user unless the fix changes the interface contract.

---

### P0 — Blocking

These issues make the output unsafe or broken. Stop and fix before anything else.

- [ ] No `dangerouslySetInnerHTML` with unsanitized input
- [ ] No secrets or environment variables exposed to the client that should be server-only
- [ ] All props match the confirmed interface contract exactly — no added, removed, or renamed props without re-confirming Plan
- [ ] Every interactive element is reachable by keyboard and has a visible focus state
- [ ] No missing `alt` on `img` elements (use `alt=""` for decorative images)
- [ ] Component renders without runtime errors in the happy path

---

### P1 — Required

These issues violate production standards. Fix before closing.

#### TypeScript

- [ ] `strict: true` respected — no `any`, no `ts-ignore`, no `as` casts without a comment explaining why
- [ ] All exported functions and components have explicit return types
- [ ] No unused imports or variables

#### Error handling

- [ ] Every async operation has a catch path with a visible fallback — no silent failures
- [ ] Error boundary present at the nearest route or feature boundary
- [ ] Loading and empty states are handled explicitly, not left as `undefined`

#### SEO (skip for non-page components)

- [ ] Page has a unique `title` and `meta description`
- [ ] Headings follow a logical hierarchy — one `h1`, no skipped levels
- [ ] Canonical URL set where applicable

#### Accessibility

- [ ] Semantic HTML used throughout — no `div` or `span` where a native element exists
- [ ] Form inputs have associated `label` elements
- [ ] ARIA attributes used only where native semantics are insufficient, and used correctly

---

### P2 — Expected

These issues reduce quality below senior standards. Fix before closing.

#### Performance

- [ ] No unnecessary re-renders — derived values computed outside the render path or via the framework's reactive primitive
- [ ] Heavy components or routes lazy-loaded with dynamic imports
- [ ] No layout-thrashing patterns (reading then writing DOM dimensions in the same frame)
- [ ] Images have explicit `width` and `height` to prevent layout shift

#### Data fetching (if applicable)

- [ ] Loading, error, and success states all handled and visible to the user
- [ ] No fetch calls inside a reactive lifecycle without a cancellation or cleanup path
- [ ] Caching strategy is explicit — not left to default behaviour

#### Code quality

- [ ] No component exceeds ~150 lines of markup/template — split if so
- [ ] No prop list exceeds 7 — extract a sub-component or group into an object
- [ ] No logic duplicated across files that could be a shared utility or composable

---

### P3 — Polish

Nice-to-have. Fix if the effort is small; note and defer otherwise.

- [ ] Motion respects `prefers-reduced-motion` (if animations are present)
- [ ] i18n strings are externalised — no hardcoded user-visible copy (if i18n is in use)
- [ ] PWA offline behaviour tested for this route (if PWA is in scope)
- [ ] Bundle impact noted for any new heavy dependency added

---

### Completion summary

After all items are resolved, output:

```
Validate complete.

P0  ✓ all passed
P1  ✓ all passed
P2  ✓ all passed      (or: 1 deferred — [item] — [reason])
P3  ✓ all passed      (or: 1 deferred — [item] — [reason])

Files delivered:
  src/components/UserCard/UserCard.tsx
  src/components/UserCard/UserCard.types.ts
  src/components/UserCard/index.ts
```

If any P2 or P3 item was deferred, state the reason and confirm it is acceptable before closing.
