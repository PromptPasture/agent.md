---
topic: Wiki skill
method: comparative analysis
date: "2026-06-25"
related:
  - src/skills/productivity/remember/SKILL.md
  - docs/2026-06-25-wiki-skill/okf-spec.md
---

# Brainstorm — Wiki skill

## Goal

Build a `/wiki` skill that lets humans and agents maintain a shared, structured knowledge base — Wikipedia's concept model, Obsidian's cross-linking, and memory's persistence — backed by Open Knowledge Format (OKF).

## Context

The existing `remember` skill writes flat private agent memory to `~/.agents/memory/` or `.agents/memory/MEMORY.md`. It handles personal facts, decisions, and preferences scoped to a single agent session or repo. It is not designed for human browsing, typed concepts, or cross-linked knowledge.

The user described the target as "Wikipedia + Memory + Obsidian Notes": structured, shareable, navigable by both humans and agents, and living in version control.

OKF (explored in a prior session, see `okf-spec.md`) is the natural fit: a directory of Markdown files with YAML frontmatter, no schema registry, no required tooling, diffable in git.

## Agenda

1. Determine primary audience (human-only, agent-only, or collaborative)
2. Determine write trigger (explicit, proactive, autonomous)
3. Choose format and location conventions
4. Clarify relationship to `remember` skill

## Ideas Considered

### Option A — OKF-based wiki (chosen)

- **Description:** The skill teaches the agent to write OKF concept documents. Each entry has YAML frontmatter (`type`, `title`, `description`, `tags`, `created`, `updated`), a markdown body, and cross-links. The skill maintains `index.md` per directory and `log.md` per OKF §6–7.
- **Benefits:** Self-describing entries, typed for agent routing, cross-linked like Obsidian, exportable, diffable. Reuses a format the user already evaluated.
- **Trade-offs:** More structured than plain notes; producers must follow frontmatter conventions.

### Option B — Obsidian-style flat wiki

- **Description:** A `wiki/` folder of Markdown files with minimal frontmatter and `[[wikilink]]` syntax. Shallow structure, no formal type system.
- **Benefits:** Easy to edit by hand, familiar to Obsidian users.
- **Trade-offs:** Less machine-navigable. Loses the `type` field, which is OKF's main agent-routing win.

### Option C — Layered wiki (repo + global)

- **Description:** Two fixed scopes: `.agents/wiki/` for project facts, `~/.agents/wiki/` for reusable domain knowledge, with cross-links across scopes.
- **Benefits:** Separates project-specific and general knowledge cleanly.
- **Trade-offs:** Adds complexity the skill must manage. Not justified until multiple repos need the same wiki.

## Outcomes

### Summary

A `/wiki` skill backed by OKF format. Default location is `docs/` (standard git convention, human-visible). Location can be overridden via `AGENTS.md`/`CLAUDE.md` to `.agents/wiki/` (repo-scoped) or `~/.agents/wiki/` (global). The skill is triggered explicitly by default; the user can configure autonomous writes in `CLAUDE.md`.

### Decisions

| Decision | Choice | Reason |
| --- | --- | --- |
| Audience | Collaborative (human + agent) | Both write and read entries |
| Format | OKF | Typed, cross-linked, self-describing, already evaluated |
| Default location | `docs/` | Standard git convention, human-visible |
| Location override | Via `AGENTS.md`/`CLAUDE.md` | Keeps the skill simple; behavior driven by config |
| Trigger | Explicit (`/wiki`) by default | Autonomous mode opt-in via `CLAUDE.md` |
| Reserved files | `index.md` + `log.md` per OKF §6–7 | Navigation catalog and change history |
| Update flow | Supported — find and edit an existing entry | Entries evolve as knowledge grows |
| `log.md` scope | Per-directory | Keeps change history local to the affected scope |
| Replaces `remember` | Move `remember` to `src/skills/deprecated/` | `wiki` covers the same need with structure, typing, and human visibility |
| Setup doc | `SETUP.md` alongside `SKILL.md` | Explains how to configure the skill in `AGENTS.md`/`CLAUDE.md`: wiki location, autonomous mode instructions, example snippets |

### Open Questions

None.

## Next Steps

1. Write implementation plan for the `/wiki` skill
2. Define the skill's workflow: create entry, update entry, maintain `index.md`, append to `log.md`
3. Define the frontmatter template and required vs. recommended fields
4. Specify how location is read from `AGENTS.md`/`CLAUDE.md`
5. Write `SETUP.md` — explains how to add the skill to `AGENTS.md`/`CLAUDE.md`: wiki location override, autonomous mode opt-in, example config snippets
6. Define the three core operations:
   - **Ingest** — process a source, extract key information, write/update concept entries, update `index.md`, append to `log.md`
   - **Query** — search relevant pages, synthesize an answer with citations; valuable answers MAY be filed back as new entries
   - **Lint** — health-check the wiki: contradictions, stale claims, orphan pages, missing cross-references, concepts without their own page
