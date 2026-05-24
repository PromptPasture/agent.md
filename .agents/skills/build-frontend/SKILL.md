---
name: build-frontend
description: Generate production-ready frontend code. Use for components, pages, routes, client state, forms, styling, accessibility, performance, PWA behavior, and data visualization.
license: MIT
version: 1.1.0
tags:
  - codegen
  - frontend
  - ui
author: Oleg Shulyakov
metadata:
  catalog: software-team-roles
---

# build-frontend

Implement production frontend work by routing to the smallest relevant reference set, matching the repository's existing architecture, and verifying the user-facing behavior.

## Variant Detection

**Classify the work from explicit user intent first, then confirm it against the repository.**

- **User signals:** Look for framework names, route or page names, component libraries, state libraries, CSS systems, test tools, file paths, file extensions, and requested user-facing behavior.
- **Repository signals:** Inspect `package.json`, lockfiles, framework configs, `tsconfig.json`, source folders, imports, routing structure, design tokens, Storybook, test setup, and CI jobs before choosing an implementation path.
- **Frontend scope:** Use this skill for components, pages, layouts, routes, loaders/actions, forms, stores, queries, charts, responsive styling, accessibility fixes, PWA behavior, and frontend performance work.
- **Route away:** Use `write-tests` for test-only work, `design-api` for API contract design, `build-backend` for backend implementation, and `write-spec` or a design skill for UI/UX specification when no code is requested.
- **Clarify rarely:** If the framework, styling system, or target surface remains genuinely ambiguous after inspection, ask one short question naming the likely options.

## Reference Routing

**Read only the references needed for the current implementation.**

Start with one language or markup reference:

| Signal | Reference |
| --- | --- |
| HTML, templates, server-rendered views, static pages, Web Components markup, `.html`, `.htm` | `references/html.md` |
| TypeScript, `.ts`, `.tsx`, strict typing, typed components, `tsconfig.json` | `references/typescript.md` |
| JavaScript, `.js`, `.jsx`, no TypeScript configuration | `references/javascript.md` |

Then read one framework reference when detected:

| Signal | Reference |
| --- | --- |
| React, JSX, hooks, React Query, Redux, Zustand | `references/javascript-react.md` |
| Next.js, App Router, Pages Router, RSC, server actions | `references/javascript-react-nextjs.md` |
| Remix, React Router data APIs, loaders, actions | `references/javascript-react-remix.md` |
| Vue, Composition API, Pinia, Vue Router | `references/javascript-vue.md` |
| Nuxt, Nitro, auto-imported composables, file routes | `references/javascript-vue-nuxt.md` |
| Angular, standalone components, services, RxJS, signals | `references/javascript-angular.md` |
| Svelte | `references/javascript-svelte.md` |
| SvelteKit | `references/javascript-svelte-sveltekit.md` |
| Astro, islands, content collections | `references/javascript-astro.md` |
| SolidJS, signals, SolidStart | `references/javascript-solidjs.md` |

Add capability references only when the task needs them:

| Signal | Reference |
| --- | --- |
| CSS modules, vanilla CSS, Sass, design tokens, layout, responsive styling | `references/css.md` |
| Tailwind, utility classes, variants, `tailwind.config.*` | `references/css-tailwind.md` |
| Bootstrap, React-Bootstrap, Bootstrap grid/utilities | `references/css-bootstrap.md` |
| MUI, Chakra, Mantine, Ant Design, Radix, shadcn/ui, Headless UI, design-system component APIs | `references/css-component-libraries.md` |
| WCAG, keyboard UX, focus, semantics, screen readers | `references/accessibility.md` |
| Locales, ICU messages, formatting, RTL, locale routing | `references/internationalization.md` |
| Validation, complex inputs, dirty state, error display | `references/forms.md` |
| Client/server state, caching, stores, optimistic UX | `references/state.md` |
| Bundle size, rendering, Core Web Vitals | `references/performance.md` |
| Service workers, manifest, offline mode, installability | `references/pwa.md` |
| Charts, dashboards, dense tables, interactive data | `references/visualization.md` |

## Implementation Workflow

**Build the real workflow in the local style before polishing edge cases.**

- **Inspect first:** Identify the existing component boundaries, route conventions, data-fetching layer, state model, styling approach, design tokens, lint rules, and accessibility patterns before editing.
- **Keep scope tight:** Make the smallest change that completes the requested behavior. Avoid new providers, stores, component layers, UI kits, icon sets, chart libraries, or form libraries unless the request or repository already points there.
- **Place code deliberately:** Put reusable primitives near the existing design system, route-specific composition near routes or pages, and side effects in the established data, loader, action, hook, service, or store layer.
- **Model states explicitly:** Implement applicable loading, empty, error, success, disabled, optimistic, validation, permission, and offline states. Do not ship decorative placeholders for requested product behavior.
- **Preserve visual language:** Match existing typography, spacing, color tokens, icon conventions, motion, density, and component APIs. Prefer project-owned abstractions when they already fit.
- **Design for change:** Keep components cohesive, props explicit, dependencies local or injected through existing mechanisms, and shared logic extracted only when it removes meaningful duplication.

## Working Rules

**Treat frontend quality as behavior, accessibility, resilience, and maintainability together.**

- **Accessibility:** Use semantic elements, labels, keyboard navigation, visible focus, reduced-motion behavior, useful alt text, and status announcements where needed. Accessibility is implementation work, not a final checklist.
- **Responsive layout:** Use stable constraints such as grid tracks, flex rules, aspect ratios, min/max sizes, and explicit wrapping. Avoid text overlap, layout shift, viewport-scaled typography, and controls that resize unpredictably.
- **Forms:** Validate at the UI boundary, expose errors accessibly, preserve dirty and pending state, and keep client-side validation consistent with server constraints. Never rely on frontend checks as the only enforcement for authorization or sensitive rules.
- **State:** Keep local state local. Use existing query, cache, store, loader, action, or context patterns for shared state, server state, optimistic updates, and invalidation.
- **Performance:** Avoid unnecessary client JavaScript, repeated expensive renders, unbounded lists, layout thrashing, oversized assets, and avoidable bundle growth. Defer deeper optimization until measurement or risk justifies it.
- **Tests:** Add or update focused tests when the repository has a frontend test setup. Prefer component, interaction, route, accessibility, or visual-regression coverage that exercises behavior over shallow render-only tests.
- **Verification:** Run the narrowest relevant formatter, linter, typecheck, build, and tests available. For browser-visible changes, inspect the running UI when practical and check responsive breakpoints that matter.

## Output Format

**Report what changed, how it was checked, and any remaining risk.**

When editing a repository, finish with changed files, commands run, and verification status. Mention commands that could not be run and why.

When only drafting code, use this structure:

```text
Assumptions:
- ...

Files:
- path/to/file

Run:
- command

Notes:
- ...
```
