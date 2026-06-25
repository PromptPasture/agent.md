---
topic: Wiki skill
date: "2026-06-25"
related:
  - docs/2026-06-25-wiki-skill/BRAINSTORM.md
  - src/skills/productivity/remember/SKILL.md
  - okf-spec.md
---

# Plan — Wiki skill

## Approach

Build the skill in four sequential phases: scaffold the folder, write `SKILL.md`, write `SETUP.md`, deprecate `remember`. Each phase is independently verifiable before the next starts.

## Assumptions

- OKF frontmatter: `type` required (kebab-case), `title`/`description`/`tags`/`created`/`updated` recommended
- `index.md` and `log.md` follow OKF §6–7 as drafted in `okf-spec.md`
- `SETUP.md` is a new convention; no existing template to follow
- OKF rules are embedded inline in `SKILL.md`; no separate reference file needed

---

## Phase 1 — Scaffold

| Step | Action | Success condition |
| --- | --- | --- |
| 1.1 | Create `src/skills/productivity/wiki/` folder | Folder exists |

---

## Phase 2 — Write `SKILL.md`

### 2.1 Frontmatter

```yaml
name: wiki
description: <specific trigger description — see below>
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: knowledge
  tags: [wiki, knowledge-base, okf, notes]
```

Trigger description must be specific enough for the agent runtime to load on `/wiki` invocations and when autonomous mode is configured in `AGENTS.md`/`CLAUDE.md`.

### 2.2 Location resolution

The skill reads the wiki path in this priority order:

1. Explicit path in `AGENTS.md`/`CLAUDE.md` (e.g. `wiki location: .agents/wiki/`)
2. `~/.agents/wiki/` if a global instruction is set
3. Default: `docs/` in the current repo

### 2.3 Frontmatter template

OKF entry template with required vs. recommended fields:

```yaml
---
type: <kebab-case-type>        # REQUIRED
title: <Sentence case title>   # Recommended
description: <One-line summary> # Recommended
tags: [<tag>, …]               # Recommended
created: <ISO 8601>            # Recommended — set on creation, never updated
updated: <ISO 8601>            # Recommended — updated on every substantive edit
---
```

### 2.4 Workflows

| Workflow | Trigger | Steps |
| --- | --- | --- |
| **Create** | New concept | Write entry file → update directory `index.md` → append to directory `log.md` |
| **Update** | Existing concept | Find entry by title/path → edit body/frontmatter → update `updated` → append to `log.md` |
| **Ingest** | Source doc provided | Read source → extract key concepts → create/update entries → update `index.md` → append to `log.md` |
| **Query** | Question asked | Read `index.md` → drill into relevant entries → synthesize answer with citations → optionally file answer as new entry |
| **Lint** | Periodic health check | Scan for: orphan pages, broken links, missing cross-refs, stale claims, concepts mentioned but lacking own page |

### 2.5 Reserved files

- **`index.md`** — advisory catalog per directory; lists entries with title, path, and description; updated on every create/update
- **`log.md`** — append-only change history per directory; date-grouped, newest first; entry format per OKF §7

**Success condition:** `SKILL.md` covers all five workflows, location resolution, frontmatter template, and reserved file conventions.

---

## Phase 3 — Write `SETUP.md`

Three configuration scenarios with copy-paste snippets:

### Scenario 1 — Default (no config needed)

Wiki lives in `docs/`. Triggered explicitly with `/wiki` only. No `AGENTS.md` changes required.

### Scenario 2 — Custom location

Add one line to `AGENTS.md`/`CLAUDE.md`:

```
Wiki location: .agents/wiki/
```

or for global:

```
Wiki location: ~/.agents/wiki/
```

### Scenario 3 — Autonomous mode

Add to `AGENTS.md`/`CLAUDE.md`:

```
When ingesting a new source document, use the wiki skill to extract key
concepts and write or update entries automatically.
When a query produces a valuable synthesis, file it as a new wiki entry.
```

### First-use example

Minimal walkthrough: invoke `/wiki`, create one entry, verify `index.md` and `log.md` are present and correct.

**Success condition:** A user can configure the skill and write their first entry by following `SETUP.md` alone.

---

## Phase 4 — Deprecate `remember`

| Step | Action | Success condition |
| --- | --- | --- |
| 4.1 | Move `src/skills/productivity/remember/` to `src/skills/deprecated/remember/` | Skill no longer in active productivity folder |
| 4.2 | Add deprecation notice at top of `deprecated/remember/SKILL.md` pointing to `wiki` | Notice visible on open |

---

## Completion criteria

- [ ] `src/skills/productivity/wiki/SKILL.md` covers: location resolution, frontmatter template, create/update/ingest/query/lint workflows, `index.md` and `log.md` conventions
- [ ] `src/skills/productivity/wiki/SETUP.md` covers: default setup, location override, autonomous mode, first-use example
- [ ] `src/skills/deprecated/remember/` exists with deprecation notice
- [ ] No file in `src/skills/productivity/` still references `remember` as the active memory skill
