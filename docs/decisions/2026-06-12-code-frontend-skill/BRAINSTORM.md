---
topic: code-frontend skill
method: comparative analysis
date: "2026-06-13"
updated: "2026-06-21"
---

# Brainstorm - code-frontend Skill

## Goal

Design a skill that guides an agent to generate production-ready frontend code
for real project codebases — not artifacts or sandboxes. The skill must detect
the project stack automatically, enforce quality across TypeScript, accessibility,
and performance, and gate output behind an explicit validation checklist.

## Context

- Output target: files written to disk inside an existing (or new) project
- Framework stance: agnostic — detect from `package.json`, `tsconfig.json`, and
  framework-specific files; suggest a stack when the project is empty
- No bespoke config file; all project knowledge comes from the repository itself
- Existing `frontend-design` skill covers aesthetic direction and is a natural
  companion; `code-frontend` covers code correctness and quality, not visual identity
- Skill location: `src/skills/code-frontend/SKILL.md`

## Agenda

1. Define the four phases and their gates
2. Define what "production-ready" means operationally
3. Define stack detection heuristics
4. Define the validation checklist
5. Decide approach structure

## Ideas Considered

### Approach A: Linear workflow

- **Description:** Single fixed sequence — detect → plan → build → validate — no
  branching or skipping.
- **Benefits:** Simple to write, easy to follow.
- **Trade-offs:** Rigid; unhelpful when user is mid-task or iterating on an existing
  component. No room to skip phases the user has already handled.

### Approach B: Phase-gated with decision points ✅ Selected

- **Description:** Four named phases (Discover → Plan → Build → Validate) with
  explicit gates. Each phase produces an artifact (detection summary, component
  plan, written files, checklist result) that must be confirmed before the next
  phase starts. Phases are skippable when the user already provides the relevant
  context.
- **Benefits:** Maps to real development workflow. User stays in control. Validation
  is a natural last phase, not an afterthought. Composable with other skills.
- **Trade-offs:** Slightly more ceremony for trivial components; mitigated by
  skippable phases.

### Approach C: Checklist-driven

- **Description:** The skill is structured as one large quality checklist wrapping
  code generation.
- **Benefits:** Thorough, nothing missed.
- **Trade-offs:** Mechanical, hard to read, gates get ignored in practice.

## Outcomes

### Summary

`code-frontend` is a four-phase, phase-gated skill for writing production-ready
frontend components into real codebases. It auto-detects the project stack and
suggests one when the project is empty. It enforces three quality axes —
TypeScript strictness, accessibility, and performance — through an explicit
inline checklist at the end of each build, before declaring output complete.
No external scripts, no bespoke config file.

### Decisions

- **Structure:** Approach B — phase-gated with skippable phases
- **Phases:** Discover → Plan → Build → Validate
- **Stack detection:** Read `package.json` dependencies, `tsconfig.json`,
  framework config files (`next.config.*`, `vite.config.*`, `svelte.config.*`,
  `nuxt.config.*`). Fall back to suggesting a stack (Next.js + Tailwind + TS)
  if none found, with user confirmation before proceeding.
- **No config file:** Detection is purely from existing project files
- **Validate phase checklist axes:**
  - Security (P0): no unsanitized HTML injection, no `javascript:`/`data:` URL injection,
    external links include `rel="noopener noreferrer"`, CSRF protection on mutating forms,
    no server secrets exposed to the client
  - TypeScript (P1): strict mode respected, no `any`, no unused imports, proper
    return types on all exported functions
  - Accessibility (P0/P1): semantic HTML elements, ARIA only where native semantics
    are insufficient, keyboard navigation, visible focus, no missing alt text
  - Performance (P2): no unnecessary re-renders, lazy loading where applicable,
    no layout-thrashing patterns, images sized appropriately
- **Companion skill:** `frontend-design` handles visual direction;
  `code-frontend` handles code quality — they compose naturally

### Extensibility Model

`SKILL.md` is the stable core — phases and checklist axes never change.
`references/` is the extension surface — adding a new framework, CSS library,
or concern means adding or updating one file only. No changes to `SKILL.md`.

The agent reads only the reference docs relevant to the current task, keeping
context lean regardless of how many references exist.

### Plan Phase Confirmation

Phase 2 confirms only the interface contract before Build starts. The list of
concern docs to load is an internal implementation detail — it is not presented
to the user for approval. This reduces friction without hiding anything meaningful.

### Language and Framework Scope (initial)

- **Languages:** JavaScript, TypeScript (strict mode preferred)
- **CSS:** TailwindCSS, Bootstrap, other utility/component frameworks, plain CSS
- **JS Frameworks:** Next.js, Vite+React, SvelteKit, Nuxt, Astro, Remix

### Validate Checklist Priority Levels

Validate phase items are tiered so the agent works through them in severity order:

- **P0 — Blocking:** Security (XSS, URL injection, CSRF, secrets), a11y critical (missing alt, no keyboard nav), broken contracts
- **P1 — Required:** TypeScript strict violations, error boundaries absent, SEO missing meta
- **P2 — Expected:** Performance patterns, decomposition heuristics, data fetching patterns
- **P3 — Polish:** Animation/motion, image sizing, bundle hints

### Component Interface Contracts (Plan Phase)

The Plan phase output must include a structured interface contract before Build
starts — minimum fields: component name, file path, props interface (name,
type, required, description), emitted events or callback signatures, slots/children
API, and external dependencies. This prevents the agent writing code against
wrong assumptions.

### Decomposition Heuristics (Build Phase)

The Build phase must apply explicit decomposition rules before writing any file:
single responsibility per component, extract when props exceed 5-7, split when
JSX exceeds ~150 lines, colocate styles/tests with component, prefer feature
folders over type folders. The agent states its decomposition rationale before
writing.

### Coverage Map

|Concern|Delivery|Location|
|---|---|---|
|Language (JS/TS)|Inline — Discover + Validate (P1)|`SKILL.md`|
|Framework detection|Inline — Discover phase|`SKILL.md`|
|Interface contracts|Inline — Plan phase|`SKILL.md`|
|Decomposition heuristics|Inline — Build phase|`SKILL.md`|
|Validate checklist (P0–P3)|Inline — Validate phase|`SKILL.md`|
|Code conventions|Reference doc|`references/conventions.md`|
|Error handling|Reference doc|`references/error-handling.md`|
|Data fetching|Reference doc|`references/data-fetching.md`|
|Animation / motion|Reference doc|`references/motion.md`|
|Accessibility patterns|Reference doc|`references/a11y.md`|
|Performance patterns|Reference doc|`references/performance.md`|
|SEO|Reference doc|`references/seo.md`|
|Styling (Tailwind, Bootstrap, plain, etc.)|Reference doc|`references/styling.md`|
|Forms|Reference doc|`references/forms.md`|
|State management|Reference doc|`references/state.md`|
|PWA|Reference doc|`references/pwa.md`|
|i18n|Reference doc|`references/i18n.md`|

New frameworks, CSS libraries, or concerns → add a file to `references/`.
No other changes required.

### Open Questions

None.

## Next Steps

1. ✅ Write `src/skills/code-frontend/SKILL.md` — 4 phases, interface contracts, decomposition heuristics, P0–P3 validate checklist
2. ✅ Write `src/skills/code-frontend/references/conventions.md`
3. ✅ Write `src/skills/code-frontend/references/error-handling.md`
4. ✅ Write `src/skills/code-frontend/references/data-fetching.md`
5. ✅ Write `src/skills/code-frontend/references/motion.md`
6. ✅ Write `src/skills/code-frontend/references/a11y.md`
7. ✅ Write `src/skills/code-frontend/references/performance.md`
8. ✅ Write `src/skills/code-frontend/references/seo.md`
9. ✅ Write `src/skills/code-frontend/references/styling.md`
10. ✅ Write `src/skills/code-frontend/references/forms.md`
11. ✅ Write `src/skills/code-frontend/references/state.md`
12. ✅ Write `src/skills/code-frontend/references/pwa.md`
13. ✅ Write `src/skills/code-frontend/references/i18n.md`
14. ✅ Verify frontmatter passes all field rules
15. ✅ Write `src/skills/code-frontend/references/testing.md`
16. ⬜ Graduate from `in-progress/` to `published/`
