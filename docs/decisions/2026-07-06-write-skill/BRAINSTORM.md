---
topic: to-skill meta-skill
method: comparative analysis
date: "2026-07-06"
related:
  - src/AGENTS.md
  - pages/BUILDING_SKILLS.md
  - src/skills/in-progress/writing-great-skills/SKILL.md
---

# Brainstorm - to-skill meta-skill

## Goal

Design `src/skills/utility/to-skill/SKILL.md`: a skill that helps author
skills in this repo, replacing the need to manually cross-reference
`AGENTS.md`, `pages/BUILDING_SKILLS.md`, and `writing-great-skills` every time
a skill is created, edited, or restructured.

## Context

An earlier attempt drafted this skill directly as a 7-step workflow that
pointed at the three governing sources instead of doing the work of applying
them. The user stopped that draft to brainstorm the design first. Along the
way, the user also confirmed they intend to retire `writing-great-skills`
once `to-skill` ships, since its useful vocabulary will live inside
`to-skill` instead.

`writing-great-skills` is itself a close rendering of a talk — "Building
Great Agent Skills - The Missing Manual" — whose central contribution is a
four-part skill checklist: **Trigger** (invocation), **Structure**
(information hierarchy), **Steering** (leading words, leg work), and
**Pruning** (single source of truth, sediment, no-ops, sprawl). The user
directed that this checklist should be the main design idea driving
`to-skill`, not just background vocabulary it happens to embed.

## Agenda

1. What should `to-skill` cover — create-only, or also edit/audit/split?
2. Model-invoked or user-invoked?
3. One skill with branches, or a router to separate skills?
4. Does the "audit" branch clash with the existing `audit-skill-security` skill?
5. Should `to-skill` point at `AGENTS.md`, or embed its rules?
6. Should `to-skill` point at `writing-great-skills`, or embed its vocabulary?
7. Should `to-skill` point at `pages/BUILDING_SKILLS.md`, or embed its mechanics?
8. How should the embedded content be laid out inside the skill?
9. Should the workflow be ad hoc branches, or the source talk's own checklist?

## Ideas Considered

### Scope

- **Create-only:** Narrowest. Editing or auditing an existing skill would be
  out of scope or a separate skill.
- **Create + edit:** Adds revising an existing skill under the same workflow.
- **Create + edit + audit/split (chosen):** Also owns detecting when a skill
  has grown bloated and needs splitting — the "By sequence" / "By invocation"
  cuts `writing-great-skills` describes. (How this is implemented in the
  workflow — as separate branches vs. as outcomes of one shared checklist —
  is resolved separately below, in **Workflow shape**.)
  - **Benefits:** One skill covers the full authoring lifecycle instead of
    leaving restructuring as an unaddressed gap.
  - **Trade-offs:** More surface area to keep coherent than a create-only skill.

### Invocation

- **Model-invoked:** Matches other repo utility skills (`git-commit`,
  `git-branch`, `audit-skill-security`), fires automatically on authoring
  requests, but adds permanent context load for an infrequent, deliberate
  task.
- **User-invoked (chosen):** Zero context load; authoring a skill is a
  deliberate act, not an ambient one, so the cognitive cost of remembering
  the skill's name is acceptable.

### Shape

- **Router to separate skills** (e.g. `create-skill`, `edit-skill`,
  `split-skill`): each skill stays minimal, but the three would duplicate
  the same rule-checking machinery three times, and adds more names for the
  user to remember.
- **Single skill with branches (chosen):** One `to-skill` whose steps
  branch on new-vs-existing and healthy-vs-bloated. The branches share the
  same underlying rule set, so splitting them apart would only fragment one
  meaning across three files.

### Naming clash with audit-skill-security

- `audit-skill-security` audits third-party skills for trust/security before
  installing them. `to-skill`'s audit branch checks structural/quality
  compliance (repo naming/frontmatter rules, information hierarchy, no-ops,
  sprawl) for skills authored in this repo. Different concerns, different
  skills — **no rename needed**, as long as `to-skill` never uses "audit"
  ambiguously without the quality/structure qualifier.

### Source of truth: AGENTS.md

- **Point at `AGENTS.md`:** Keeps one canonical location for the rules, but
  a skill that depends on a specific repo file at a specific path is not
  standalone — it breaks if the skill folder is ever copied or shipped
  elsewhere.
- **Embed the rules (chosen):** `to-skill` inlines the actual rule content
  it needs to act, the same way `git-commit` inlines the Conventional Commits
  spec directly rather than pointing elsewhere. `AGENTS.md` remains the
  compact governance statement for humans skimming it; `to-skill` is the
  operational form of the same rules. The resulting duplication is accepted,
  same as it would be for any standalone skill capturing a spec.

### Vocabulary source: writing-great-skills

- `writing-great-skills` has `disable-model-invocation: true`. Per its own
  glossary, a user-invoked skill has no description, so **no other skill can
  fire it** — a pointer from `to-skill` to it would not reliably resolve.
- **Embed the needed vocabulary (chosen):** `to-skill` inlines the specific
  concepts it actually applies — completion criteria, the information
  hierarchy (steps / in-skill reference / disclosed reference), leading
  words, and the pruning failure modes (duplication, sediment, no-op,
  sprawl). The user will retire `writing-great-skills` once `to-skill`
  ships, so there is no long-term duplication between the two.

### Mechanics source: pages/BUILDING_SKILLS.md

- This is a 952-line reference doc, not a skill, so pointing at it doesn't
  have the same "unreachable pointer" problem as `writing-great-skills`. But
  it is still a repo-external file a standalone skill shouldn't depend on.
- **Embed only the operative mechanics (chosen):** required frontmatter
  fields, file/folder layout, naming rules, and the triggering/functional
  testing checklist move into `to-skill` directly. `pages/BUILDING_SKILLS.md`
  stays available as deeper background for a human reading it once.

### Content layout inside the skill

- **Everything inline in one `SKILL.md`:** Simplest to read in one pass, but
  the file would run long once rules from three sources are embedded —
  exactly the sprawl failure mode the skill is meant to help authors avoid.
- **SKILL.md + `references/` (chosen):** `SKILL.md` stays a short branching
  workflow (create / edit / audit-and-split), each step ending on a
  completion criterion. The bulky, look-up-only material — frontmatter field
  rules, naming conventions, the information-hierarchy/leading-words/pruning
  checklist — moves into `references/` files bundled inside `to-skill/`'s
  own folder. Nothing outside the skill folder is required at runtime.
- **SKILL.md + references/ + a validator script:** Same as above plus a
  bundled script that mechanically checks required fields, naming pattern,
  and the no-`README.md` rule during the audit branch. More reliable than
  prose-only checking, but adds a language/runtime dependency and a file to
  maintain. Deferred — no evidence yet that prose checking is insufficient
  (YAGNI).

### Workflow shape

- **Keep the create/edit/audit-split branches, checklist as reference:**
  The three branches stay as the top-level workflow; Trigger/Structure/
  Steering/Pruning move into `references/` that each branch consults as
  needed.
  - **Trade-offs:** Three branches that partly overlap (an "edit" often
    needs the same pruning pass as an "audit"), and splitting stays a
    separately-maintained branch instead of falling naturally out of the
    Pruning step that already detects sprawl.
- **The checklist IS the workflow (chosen):** `SKILL.md`'s steps become the
  talk's own four items — Trigger, Structure, Steering, Pruning — applied
  the same way whether the skill is new or existing. Drafting a new skill
  walks all four to build it; revising an existing one walks the same four
  to evaluate and fix it. Splitting a bloated skill is no longer a separate
  branch — it falls out of the Pruning step (sprawl → split by branch or
  sequence) and the Structure step (branch-only reference → disclosed
  reference), exactly as the talk describes them.
  - **Benefits:** One workflow instead of three overlapping ones; "audit"
    and "split" stop being separate concerns and become natural outcomes of
    running the same checklist against existing content. Directly matches
    the source material the user wants this skill to embody.
  - **Trade-offs:** "New vs. existing" is no longer a first-class branch in
    the workflow structure — it becomes framing context the agent carries
    into the same four steps, not a fork with different steps.

## Outcomes

### Summary

`to-skill` will be a standalone, shippable, **user-invoked** skill at
`src/skills/utility/to-skill/`, covering the full skill-authoring
lifecycle in this repo — creating a new skill and revising an existing one
(including detecting when it needs to be split). Its workflow is the source
talk's own four-part checklist — **Trigger, Structure, Steering, Pruning** —
applied the same way whether the skill is new or existing; splitting a
bloated skill falls out of the Pruning and Structure steps rather than being
a separate branch. It embeds the operative rules and vocabulary it needs —
repo naming/frontmatter/README-index rules (currently in `AGENTS.md`),
file-layout and testing mechanics (currently in `pages/BUILDING_SKILLS.md`),
and the Trigger/Structure/Steering/Pruning vocabulary (currently in
`writing-great-skills`, which will be retired once `to-skill` ships) —
rather than pointing at those sources at runtime. `SKILL.md` stays the short
four-step checklist with a completion criterion per step; the embedded detail
lives in bundled `references/` files so the skill folder is self-contained.

### Decisions

- Scope: create + edit, with splitting handled as an outcome of the
  checklist rather than a separate branch.
- Invocation: user-invoked (`disable-model-invocation: true`).
- Shape: single skill, not a router.
- Workflow: the talk's own checklist — Trigger → Structure → Steering →
  Pruning — is the workflow itself, not just embedded reference.
- No naming change needed against `audit-skill-security`.
- `to-skill` embeds rules/vocabulary/mechanics from `AGENTS.md`,
  `writing-great-skills`, and `pages/BUILDING_SKILLS.md` instead of pointing
  at them.
- Layout: `SKILL.md` (short, four-step checklist, completion-criterion-per-
  step) + `references/` for the bulky embedded material. No validator script
  in v1.
- `writing-great-skills` will be retired after `to-skill` ships.

### Open Questions

- Exact `references/` file breakdown (e.g. one file per rule category, or
  fewer, larger files) — left to the implementation plan.
- Whether retiring `writing-great-skills` also requires updates elsewhere
  (e.g. `src/skills/README.md`'s In-Progress table) — left to the
  implementation plan.

### Next Steps

Turn these decisions into an implementation plan covering: the `SKILL.md`
four-step checklist workflow and its completion criteria, the `references/`
file breakdown, updating `src/skills/README.md`'s Utility Skills table, and
removing `writing-great-skills` (and its README entry) once `to-skill` is
verified to cover its useful content.
