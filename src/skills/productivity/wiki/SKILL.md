---
name: wiki
description: Creates, updates, queries, and lints a structured wiki knowledge base. Use when the user says "add to wiki", "update wiki", "search wiki", "ingest this", "remember this", "save context", or asks to preserve a fact.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.0.1"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: knowledge
  tags: [wiki, knowledge-base, okf, notes]
---

# Wiki

Maintain a shared, structured knowledge base — typed concept documents, cross-linked like Obsidian, diffable in git, readable by humans and agents without tooling.

## Location

Read the wiki path in this priority order:

1. Explicit path provided in the current session or conversation context
2. `~/.agents/wiki/` if set in global agent configuration
3. Default: `docs/` in the current repo

## Entry format

Every wiki entry is a UTF-8 Markdown file with a YAML frontmatter block:

```yaml
---
type: <kebab-case-type> # REQUIRED — e.g. concept, decision, person, tool, term, playbook
title: <Wikipedia-style title>  # Recommended — natural name
description: <One-line summary> # Recommended
tags: [<tag>, …] # Recommended
created: <ISO 8601 datetime> # Recommended — set on creation, never updated thereafter
updated: <ISO 8601 datetime> # Recommended — updated on every substantive edit
---
```

**`type`** is a short kebab-case string. Pick values that are descriptive and self-explanatory. Common values: `concept`, `decision`, `person`, `tool`, `term`, `playbook`, `source`, `question`. Unknown types are valid — consumers treat them as generic concepts.

**`title`** follows Wikipedia naming convention: use the natural, most recognizable name for the concept. Examples: `Customer orders`, `BigQuery`, `HTTP request`, `Incident response`.

The body is standard Markdown. Use headings, lists, tables, and fenced code blocks over freeform prose — structure aids both human reading and agent retrieval.

Cross-link to other entries using bundle-relative paths:

```markdown
See [orders](/tables/orders.md) for the join key.
```

## Reserved files

Two filenames have defined meaning at every directory level and MUST NOT be used as concept documents:

### `index.md`

Advisory catalog of the directory's contents. Updated on every create or update operation. Format:

```markdown
# <Directory name>

- [Title](relative-path.md) — one-line description
- [Subdirectory](subdir/) — one-line description
```

`index.md` is advisory: consumers MUST fall back to filesystem scanning when it is absent or stale. A missing entry does not mean the concept does not exist.

### `changelog.md`

Append-only change history for the directory. Date-grouped, newest first. Updated on every create, update, or ingest operation. Format:

```markdown
# Changelog

## YYYY-MM-DD

- **Create**: Added [Title](path.md) — one-line reason.
- **Update**: Revised [Title](path.md) — what changed.
- **Ingest**: Processed [Source title](path.md) — N entries created/updated.
```

Date headings MUST use ISO 8601 `YYYY-MM-DD`. The leading bold word is a convention, not a requirement.

## Workflows

### Create

When the user asks to add a new concept to the wiki:

1. Determine the target directory from the entry's topic.
2. Choose a filename: kebab-case of the title, e.g. `customer-orders.md`.
3. Write the entry with full frontmatter (`type`, `title`, `description`, `tags`, `created`, `updated`).
4. Add the entry to the directory's `index.md` (create `index.md` if absent).
5. Append a `**Create**` entry to the directory's `changelog.md`.

### Update

When the user asks to revise an existing entry:

1. Find the entry by title or path — scan `index.md` first, then the filesystem.
2. Edit the body and/or frontmatter as needed.
3. Update the `updated` timestamp. Never change `created`.
4. Append an `**Update**` entry to the directory's `changelog.md`.

### Ingest

When the user provides a source document to process:

1. Read the source and discuss key takeaways with the user.
2. Write a summary entry for the source itself (`type: source`).
3. For each key concept, person, term, or decision in the source: create a new entry or update an existing one.
4. Update `index.md` for every affected directory.
5. Append an `**Ingest**` entry to the directory's `changelog.md` listing how many entries were created or updated.

A single source may touch many entries. Prefer updating existing entries over creating near-duplicates.

### Query

When the user asks a question against the wiki:

1. Read the root `index.md` to find relevant directories.
2. Read relevant `index.md` files to identify candidate entries.
3. Read the candidate entries.
4. Synthesize an answer with citations to the entries read.
5. If the answer is a valuable synthesis (comparison, analysis, discovered connection), offer to file it as a new entry.

### Lint

When the user asks for a wiki health check:

Scan for and report:

- **Orphan pages** — entries with no inbound links from other entries
- **Broken links** — links whose target file does not exist
- **Missing cross-references** — concepts mentioned by name in entries that lack a link to their own page
- **Stale claims** — entries whose `updated` date is significantly older than related entries that may have superseded them
- **Concepts without a page** — important terms or entities referenced repeatedly but never given their own entry

Report findings grouped by category. Do not modify entries during lint unless the user asks.
