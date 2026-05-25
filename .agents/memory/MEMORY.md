# Memory

## Facts

- **Root `AGENTS.md` is the primary entry point** — Playbook docs were updated on 2026-05-12 to make root `AGENTS.md` the concrete entry point for agent guidance.
- **Memory stores small completed task notes** — Use `.agents/memory/YYYY-MM-DD.md` for small task observations that do not need a PRD, SPEC, architecture, or design document.
- **Dated memory uses UTC** — Daily notes use `YYYY-MM-DD` filenames and UTC dating.
- **GitHub Pages source lives in `pages/`** — Repository Pages files were moved from the root into `pages/` on 2026-05-14.
- **JavaScript tooling lives in `.devops/js-tools`** — Markdown linting and token counting were consolidated there; `token-count` is the current token script name.
- **Library content lives under `.agents`** — The maintained library was moved under `.agents` on 2026-05-19.
- **Library skills have a table-of-contents README** — `.agents/skills/README.md` indexes the maintained skills.
- **Router skills are the preferred pattern for multi-variant skills** — Multi-variant skill families such as Git, API design, database/code generation, and frontend/backend generation route to focused references.
- **Creator skills support multiple agent runtimes** — `.agents/skills/create-skill` guidance and scripts avoid assuming a single coding-agent runtime.
- **Skill audit tasks are grouped by skill** — When auditing skill format or authoring compliance, write remediation checklists as one top-level task per skill folder; put style, structure, reference, and validation fixes under that skill.
- **Agent artifact metadata is compact** — Skills, rules, and commands store `author`, `version`, `source`, and `category` under `metadata`; use compact source references such as `github.com/olegshulyakov/agent.md`.
- **Generated docs use YAML frontmatter for document metadata** — PRDs, specs, stories, runbooks, and similar generated Markdown artifacts put document-level metadata in frontmatter instead of body metadata tables or `Document Info` blocks.
- **Skills use verb-first naming** — All skills are named using the `<verb>-<subject>[-<variant>]` or concise `<verb>` convention (e.g., `code-tests`, `ask`, `choose`).

## Preferences

- **Token-efficient agent output** — Keep agent responses concise while preserving logic and useful implementation detail.
- **Compact memory entries** — Record reusable observations, decisions, and conventions; avoid raw Git-log summaries and transient task noise.

## Decisions

### [2026-05-14] Use memory for small completed task notes

**Context:** Several `docs/2026-05-14-*` folders contained only completed `TASKS.md` files.
**Decision:** Preserve those notes in `.agents/memory/2026-05-14.md` and reserve docs task folders for work that needs task-scoped PRD, SPEC, architecture, or design documentation.
**Revisit if:** Small tasks start needing richer traceability than dated memory notes provide.

### [2026-05-24] Use YAML frontmatter for generated document metadata

**Context:** Generated PRDs, specs, stories, and technical docs previously mixed metadata tables and `Document Info` blocks into document bodies.
**Decision:** Put document-level metadata in YAML frontmatter. Quote date-like values, keep placeholder examples in square brackets, use no-space status tokens such as `IN_REVIEW`, `IN_PROGRESS`, and `READY_FOR_DEV`, and add optional fields only when they have real value.
**Revisit if:** A target renderer or downstream tooling cannot consume YAML frontmatter.

### [2026-05-25] Group skill audit remediation by skill

**Context:** A skill-format audit checklist was initially grouped by issue type, which made execution awkward because fixes are applied skill folder by skill folder.
**Decision:** For skill authoring or format audits, group remediation checklists by affected skill folder first. Put style, structure, reference, and validation fixes as subitems under each skill.
**Revisit if:** A future audit is only a single mechanical issue across many files and bulk editing by issue type is clearly faster.

### [2026-05-25] Use verb-first naming and mandate semantic version bumps for skills

**Context:** Skill naming was previously inconsistent, and version bumping was frequently forgotten during edits.
**Decision:** All skills must be named using the `<verb>-<subject>[-<variant>]` convention or a concise `<verb>` format (e.g., `code-tests`, `ask`, `choose`). Whenever a skill is materially updated, its `metadata.version` must be incremented using semantic versioning.
**Revisit if:** The verb-first convention causes collisions or if version tracking is moved to automated tooling.
