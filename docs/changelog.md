# Changelog

## 2026-07-06

- Removed `handoff` skill from the Productivity catalog.

## 2026-06-25

- Added `wiki` skill and deprecated `remember`.
- Normalized Markdown table formatting and updated linter rule.
- **Ingest**: Processed `docs/` PRDs/BRAINSTORMs, `.agents/memory/`, and git log — wiki initialized.
  - **Create**: Added [Agent Playbook](agent-playbook.md) — AGENTS.md convention and skill layout.
  - **Create**: Added [Skills](skills.md) — complete skill index with all catalogs.
  - **Create**: Added [skills/skill-system.md](skills/skill-system.md) — naming, structure, quality bar.
  - **Create**: Added [skills/skill-catalog.md](skills/skill-catalog.md) — 56-skill catalog and distribution model.
  - **Create**: Added [skills/productivity.md](skills/productivity.md) — adapt, brainstorm, dry, handoff, plan, review, wiki, yagni.
  - **Create**: Added [skills/software-engineering.md](skills/software-engineering.md) — code-* and review-code skills.
  - **Create**: Added [skills/product.md](skills/product.md) — write-prd, write-spec, write-user-story, ticket routing.
  - **Create**: Added [skills/utility.md](skills/utility.md) — audit-skill-security, avoid-ai-writing, git-branch, git-commit.
  - **Create**: Added [skills/lifestyle.md](skills/lifestyle.md) — lawyer, landscape-design.
  - **Create**: Added [skills/documentation.md](skills/documentation.md) — in-progress documentation skills.
  - **Create**: Added [Engineering principles](engineering-principles.md) — SOLID, DRY, KISS, YAGNI in agent context.
  - **Create**: Added [Conventions](conventions.md) — naming, memory, docs, skill-authoring conventions.

## 2026-06-24

- Added `avoid-ai-writing` skill for auditing and removing AI-isms.
- Added returning-session support with memo awareness to `lawyer` skill.
- Graduated `code-backend`, `code-frontend`, `code-database`, `code-tests` from in-progress to `software-engineering` catalog.
- Graduated remaining in-progress skills to categorized directories.
- Removed in-progress stubs: `ask`, `choose`, `classify`, `explain`, `investigate`.
- Removed AI-isms from skill documentation across the library.
- Improved cross-referencing between `write-spec` and `write-prd`.
- Fixed punctuation and formatting across `code-frontend`, `code-tests`, `code-backend`, `code-database`, and `landscape-design` skills.

## 2026-06-23

- Added `yagni` skill for catching speculative additions before they are built.
- Added `dry` skill for catching duplicated knowledge, logic, or structure.

## 2026-06-22

- Added `lawyer` skill for legal document review and drafting.

## 2026-06-21

- Overhauled `code-backend` with 4-phase workflow (Discover → Plan → Build → Validate).
- Overhauled `code-database` with 4-phase workflow and expanded DB references.
- Overhauled `code-tests` with 4-phase workflow and new reference docs.
- Added testing reference for component and unit tests to `code-frontend`.
- Removed Context7 MCP dependency from `code-frontend`; simplified skill docs.
- Synced `AGENTS.md` from template.

## 2026-06-15

- Made `code-frontend` framework-agnostic with adapter files per framework.
- Added framework adapters for Angular, Astro, Nuxt, Preact, SolidJS, Vue.
- Replaced bundled reference docs with Context7 MCP fetch in `code-frontend`.
- Reorganized JS and CSS framework adapters into subdirectories.
- Added `handoff` skill for compacting conversations into agent handoff documents.

## 2026-06-14

- Redesigned `code-frontend` with phase-gated architecture (Discover → Plan → Build → Validate).
- Enhanced `code-frontend` detection, reference docs, and added confirmation step.

## 2026-06-13

- Revised skill catalog distribution: tagged releases publish one installable ZIP per stable skill and one complete library ZIP for bulk use.
- Implemented `markitdown` skill with read/convert modes.
- Added `landscape-design` skill with brainstorming docs and reference formats.
- Migrated YAML tags from list to inline array format across all skills.

## 2026-06-12

- Added `landscape-design` skill with brainstorming docs and reference formats.
- Added `BRAINSTORM.md` as an optional task-folder document type.

## 2026-06-11

- Updated `brainstorm` skill output contract: `BRAINSTORM.md` uses required `topic`, `method`, `date` frontmatter fields plus optional `related`; skill writes the document but does not commit.
- Rewrote `write-ticket` skill with full templates and self-review process.
- Reframed `brainstorm` skill from design-spec to brainstorm-exploration paradigm.
- Moved `ask`, `choose`, `classify`, `explain`, `investigate`, `manage`, `markitdown`, `write-changelog`, `write-readme`, `write-ticket` to in-progress.

## 2026-06-10

- Split `write-user-story` and `write-ticket` into independent skills. `write-ticket` handles bug, feature, task, and spike; `write-user-story` is limited to user stories. Conversion between the two requires an explicit user request.

## 2026-06-09

- Consolidated `review-code` into a self-contained skill covering workflow, risk areas, finding standards, three-pass process, and verification checklists.
- Added `markitdown` user story: CLI-only, single local file, temporary model output, session-local reuse, dependency consent, failure handling.
- Replaced `write-tech-docs` router with five standalone documentation skills: `write-api-docs`, `write-changelog`, `write-readme`, `write-release-notes`, `write-runbook`.

## 2026-06-08

- Updated `plan` skill: discussion drafts stay conversational; plans saved to `docs/YYYY-MM-DD-[topic]/PLAN.md` only after explicit approval. Bumped to `1.4.0`.
- Completed `audit-skill-security` with read-only audit workflow, severity model, and install verdicts.
- Split `manage-git` into focused `git-branch` and `git-commit` utility skills.
- Moved `write-prd`, `write-spec`, `write-user-story` into `product` catalog; `write-tech-docs` into `documentation` catalog.
- Completed `write-user-story` with workflow, output template, writing rules, and verification; made Context, Scope, Developer Tasks, and Dependencies optional.

## 2026-06-05

- Restructured skills into `productivity/`, `software-engineering/`, and `utility/` subdirectories.
- Overhauled `brainstorm` skill with new superpowers; simplified by removing inter-skill dependencies.
- Updated skill catalog metadata from `software-team-roles` to `software-engineering`.
- Reorganized skill index by category; removed `HOWTO.md`.
- Relicensed all skills from MIT to Apache-2.0.
- Added complete guide to building skills (`pages/BUILDING_SKILLS.md`).

## 2026-06-04

- Clarified docs folder naming convention: UTC date prefix is required.

## 2026-06-02

- Changed project license from MIT to Apache 2.0.

## 2026-06-06

- Strengthened root `AGENTS.md` with mandatory session-start memory loading, UTC daily-note creation, pre-edit scope gate, and self-review-and-fix completion gate.
- Strengthened `docs/AGENTS.md`, `pages/AGENTS.md`, and `src/AGENTS.md` with domain-specific mandatory gates.
- Completed `plan`, `review`, `ask`, `remember`, and `adapt` productivity skills with compact workflow, output, boundaries, error paths, and verification sections.
- Made `remember`/`memory` skill agent-agnostic; separated private cross-repo memory (`~/.agents/`) from repo-scoped `.agents/memory/`.
- Updated skill authoring to select purposeful body sections from patterns instead of applying a fixed section template.

## 2026-05-31

- Split monolithic `AGENTS.md` into directory-scoped files (`docs/`, `pages/`, `src/`).
- Updated GitHub labels configuration.

## 2026-05-30

- Added `HOWTO.md` guide for writing Agent Skills.

## 2026-05-27

- Moved library content from `.agents/` to `src/`.
- Converted `Boundaries`, `Error Paths`, and `Verification` sections to Gherkin/scenario format across skills.
- Added `review` skill with retrospective board format.
- Restructured `brainstorm`, `ask`, and `adapt` skills into Given/Then scenario format.

## 2026-05-25

- Renamed all skills to shorter verb-first names; renamed `explore` to `investigate`.
- Enforced verb-first naming convention in `create-skill` authoring instructions.
- Added versioning guidelines (semantic version bumps) to `create-skill`.
- Migrated `create-skill` evals from JSON to YAML with suites/cases format.
- Enhanced `create-skill` eval and authoring references with assertion design and teaching format guidance.
- Removed bold principle sentences; added `Verification` sections across skills.

## 2026-05-24

- Renamed skills to verb-first convention (`write-tests` → `code-tests`).
- Added general utility skills: `ask`, `classify`, `manage`, `choose`, `investigate`, `plan`, `brainstorm`, `remember`, `adapt`.
- Moved `author`, `version`, `source` under `metadata`; added `metadata.category` to all maintained skills, rules, and commands.
- Replaced `Scope` sections with `Boundaries` after `Workflow` in skills.
- Moved generated document metadata from body tables into YAML frontmatter across `write-prd`, `write-spec`, `write-tech-docs`, `write-user-story`.

## 2026-05-23

- Added SPEC and user stories for general-purpose agent skills covering authoring, evals, validation, and handoff.
- Restructured team-roles-as-skills PRD/SPEC with formal sections, decisions, release gates, quality criteria, and implementation stats.
- Rewrote agent-playbook PRD around `AGENTS.md` and Agent Skills specification.

## 2026-05-21

- Added and refined PRD for general agent skills.
- Expanded `writer-sql` into `codegen-database`.
- Added eval coverage requirements to `create-skill`.
- Added pre-commit hook with Markdown lint.

## 2026-05-20

- Reworked `create-skill`, `create-rule`, `codegen-backend`, `codegen-frontend`, `codegen-test`, and `explain-codebase`.
- Restructured PRD and user-story templates including AI output guidance.
- Added section delimiter rules to `create-skill` authoring docs.

## 2026-05-19

- Moved library content under `.agents/`.
- Added `audit-skill-security` for pre-install security vetting.
- Expanded `review-code` and `create-skill` with agent-skill review, grounding, and eval methodology.
- Overhauled `write-prd` and expanded `write-spec` with product-spec, role, release-readiness, and scope templates.
- Renamed `how` to `explain-codebase`.

## 2026-05-18

- Added `src/rules/formatting-markdown.md` scoped to Markdown files.
- Consolidated Markdown tooling into `.devops/js-tools`; renamed token tallying to `token-count`.
- Added `.github/workflows/library-token-diff.yml` to comment library token diffs on PRs.
- Moved `artifact-quality` and `token-efficiency` into root `AGENTS.md` as always-on guidance.
- Added `explain-codebase` and `review-code` skills with eval coverage.
- Consolidated skill catalog entries through multi-variant routers.

## 2026-05-17

- Replaced unsupported skill `trigger` metadata with context-invoked metadata guidance.
- Added KISS, STAR, and SOLID guidance through `artifact-quality` rule.
- Extracted `write-prd` and `write-user-story` templates into references.
- Added tag-triggered release workflow with git-cliff release notes.

## 2026-05-16

- Split backend and frontend code-generation into language and framework routing layers.
- Built `codegen-frontend` as a router skill with language, framework, styling, and frontend capability references.

## 2026-05-15

- Moved small task notes into `src/memory/YYYY-MM-DD.md`.
- Added `design-api` router skill with OpenAPI, AsyncAPI, and GraphQL references.
- Added `codegen-test` and `codegen-backend` skills.
- Added skill length budgets: metadata ≤ 100 tokens, instructions ≤ 5000 tokens.

## 2026-05-14

- Added `create-skill`, `create-rule`, `operator-git`, and token-efficiency guidance.
- Moved GitHub Pages files into `pages/`; added path-filtered Pages workflow.
- Added Markdown formatting CI for changed Markdown files.

## 2026-05-13

- Added `writer-tech-docs`, `writer-user-story`, and `writer-sql` skills.
- Restructured `writer-sql` as a router skill.
- Folded `design-css` into `codegen-frontend`; renamed `design-schema` to `design-database`.

## 2026-05-12

- Promoted root `AGENTS.md` as the primary entry point.
- Moved `.agents` content to `examples`; flattened rules, commands, and agents layout.
- Consolidated multi-variant skills into a router pattern.
- Added `git-branch` and `git-message` commands.

## 2026-05-11

- Added Agent Playbook PRD and technical specification.
- Added `writer-prd` and `writer-spec` skills.
- Added root `AGENTS.md` guidance.
- Updated docs folder naming to include date prefixes.

## 2026-05-09

- Added `.gitignore`.
- Added automated repository label management.
- Added commit-message and branch-naming guidance skills.

## 2026-05-04

- Reorganized docs into kebab-case, directory-based layouts.
- Standardized document filenames; documented UTC as timezone for daily notes.
- Reorganized `.agent` content from flat files into directories.

## 2026-05-03

- Downgraded project version to `0.0.1` (draft stage).
- Renamed project from Constitution → Agent Context Constitution → Playbook.

## 2026-05-02

- Initialized repository with Jekyll configuration.
- Added first generated agent playbook documentation and software team skill set documents.
