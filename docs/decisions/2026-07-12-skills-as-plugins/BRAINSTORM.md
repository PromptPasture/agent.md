---
topic: Skills as Claude Code Plugins
method: comparative analysis
date: "2026-07-12"
related:
  - src/skills/
  - src/skills/README.md
  - .plugins/.codex-plugin/plugin.json
  - plugins/
  - docs/decisions/2026-06-11-skill-catalog/BRAINSTORM.md
---

# Brainstorm - Skills as Claude Code Plugins

## Goal

Reorganize the skill library so it can be installed as a set of Claude Code
plugins under `plugins/`, replacing or supplementing the current
category-based layout under `src/skills/`.

## Context

`src/skills/` groups skills into catalogs (`lifestyle/`, `product/`,
`software-engineering/`, `productivity/`, `utility/`, `deprecated/`,
`in-progress/`) designed around content topic, not installability. The
repository already exports the full library to OpenAI Codex through
`.plugins/.codex-plugin/plugin.json`, which points its `skills` field at
`../src/skills/` without copying files, keeping `src/skills/` the single
source of truth (see the
[Skill Catalog brainstorm](../2026-06-11-skill-catalog/BRAINSTORM.md)).

Claude Code's plugin format does not support that reference-only pattern.
Plugin manifest paths must start with `./` and cannot traverse outside the
plugin's own directory: `../` references are dropped at install/cache time,
and even symlinks to sibling plugins in the same marketplace are dereferenced
and copied rather than kept as pointers. Any Claude Code plugin must
therefore contain its skill files physically within its own tree.

An empty `plugins/` folder has been created as the destination for this new
structure.

## Agenda

1. Decide the grouping logic for splitting the skill library into plugins.
2. Decide whether `src/skills/` remains canonical with `plugins/` generated
   from it, or whether skill content moves into `plugins/` directly.
3. Decide how `plugins/` interacts with the existing Codex export and any
   future `dist/` artifacts.
4. Decide handling for `deprecated/` and `in-progress/` skills.

## Ideas Considered

### One plugin per existing category

- **Description:** Map `lifestyle/`, `product/`, `software-engineering/`,
  `productivity/`, `utility/` directly onto five plugins.
- **Benefits:** No re-categorization work; matches the current
  `src/skills/README.md` structure.
- **Trade-offs:** Categories were designed around content topic, not
  install-time cohesion; several categories mix unrelated workflows.
- **Outcome:** Rejected. Categories do not map cleanly onto install-worthy
  plugins.

### Domain/workflow-bundle grouping (Anthropic precedent)

- **Description:** Researched `anthropics/claude-plugins-official`.
  Anthropic groups its own plugins by domain or workflow tool (one `github`
  plugin, one `code-review` plugin, one `plugin-dev` plugin bundling several
  related skill-authoring skills), not by persona and not one-skill-per-plugin.
  Official guidance is to "bundle related operations into a cohesive
  toolkit" with no fixed granularity rule.
- **Benefits:** Real precedent from the platform this is being built for.
- **Trade-offs:** Still requires deciding where the actual boundaries fall.
- **Outcome:** Adopted as the grouping philosophy for further discussion.

### Persona-based grouping

- **Description:** Group by who installs a plugin (engineer vs. PM vs.
  writer vs. personal use).
- **Trade-offs:** Not selected as the primary lens for the remaining skills.
- **Outcome:** Rejected in favor of lifecycle-stage grouping.

### Lifecycle-stage grouping

- **Description:** Group the remaining (non-git, non-skill-toolkit) skills
  by where they sit in the work lifecycle: discover -> build -> ship, with
  `lifestyle` kept separate as a non-lifecycle bucket.
- **Benefits:** Matches the preferred mental model; groups skills by when
  they get reached for rather than by who reaches for them.
- **Trade-offs:** A few skills straddle two stages (see Open Questions).
- **Outcome:** Selected as the working draft for the four remaining plugins.

## Outcomes

### Summary

The skill library will be split into plugins using domain/workflow-bundle
logic, following Anthropic's own official marketplace conventions. Two
plugins are settled: `git-workflow` and `skill-toolkit`. The remaining
skills are drafted into a discover/build/ship lifecycle model, with
`lifestyle` staying as its own non-lifecycle plugin. Because Claude Code
plugins cannot reference files outside their own directory, skill content
will need to physically live inside each plugin; the exact source-of-truth
mechanism is still open.

### Decisions

- Use domain/workflow-bundle grouping (Anthropic's own convention), not
  persona-based or one-skill-per-plugin grouping.
- `git-workflow` plugin: `git-branch`, `git-commit`.
- `skill-toolkit` plugin (meta: building/auditing the skill library itself):
  `to-skill`, `audit-skill-security`, `adapt`, `dry`, `yagni`.
- Remaining skills grouped by lifecycle stage, plus a separate `lifestyle`
  plugin for non-lifecycle skills:
  - `discover` (draft): `brainstorm`, `plan`, `review`, `wiki`, `to-notes`,
    `manage`, `to-prd`, `to-ticket`, `write-spec`, `markitdown`.
  - `build` (draft): `code-backend`, `code-database`, `code-frontend`,
    `code-tests`, `review-code`, `design-api`.
  - `ship` (draft): `write-api-docs`, `write-changelog`,
    `write-release-notes`, `write-runbook`, `write-readme`,
    `avoid-ai-writing`.
  - `lifestyle` (unchanged): `landscape-design`, `lawyer`.
- Claude Code plugin manifests cannot point outside their own directory
  (confirmed: no `../` traversal; symlinks to sibling plugins are
  dereferenced/copied at install) — ruling out the reference-only pattern
  used for the Codex export.

### Open Questions

- Final placement of three skills that straddle stages:
  - `write-spec` — drafted under `discover` (spec precedes build); could
    instead belong to `ship` as a doc artifact.
  - `design-api` — drafted under `build` (produces the contract code is
    written against); could instead belong to `discover`.
  - `markitdown` — drafted under `discover` (reading/converting reference
    material); it is a generic utility that does not cleanly belong to any
    single stage.
- Whether `src/skills/` remains the canonical source with `plugins/`
  generated from it via a build step, or whether skill content physically
  moves into `plugins/` and `src/skills/` is retired.
- How the new `plugins/` structure coexists with the existing
  `.plugins/.codex-plugin/plugin.json` export and any `dist/` build
  artifacts.
- Whether `deprecated/` skills (`write-user-story`, `remember`) are excluded
  from all plugins, and whether `in-progress/` skills are excluded until
  stable, mirroring the precedent set in the
  [Skill Catalog brainstorm](../2026-06-11-skill-catalog/BRAINSTORM.md).
- Final plugin names — `discover`/`build`/`ship`/`lifestyle` are working
  drafts, not confirmed.

## Next Steps

1. Edit this document directly to finalize plugin composition and names.
2. Resolve the open questions above (source-of-truth strategy, stage
   boundaries for the three straddling skills, deprecated/in-progress
   handling).
3. Review and approve the finalized brainstorm notes.
4. Create an implementation plan covering plugin manifests, the
   migration/build mechanism, and how `plugins/` coexists with the Codex
   export.
