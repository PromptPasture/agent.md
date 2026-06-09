---
name: write-changelog
description: Write or revise developer-facing changelogs. Use for CHANGELOG.md files, unreleased sections, version entries, commit or pull-request categorization, breaking changes, deprecations, removals, fixes, and security changes.
license: Apache-2.0
tags:
  - writer
  - docs
  - changelog
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
---

# write-changelog

Create a concise developer-facing record of notable changes and their upgrade impact.

## Workflow

1. Determine whether the task is an unreleased update, one release entry, or a complete changelog.
2. Establish the version, release date, versioning convention, previous release, and available issue or pull-request links.
3. Inspect the actual change set: commits, pull requests, issues, diffs, migration notes, and security advisories.
4. Exclude changes that are not meaningful to consumers unless the repository treats them as product changes.
5. Group entries using Keep a Changelog categories: Added, Changed, Deprecated, Removed, Fixed, and Security.
6. Highlight breaking changes and required migration work.
7. Verify entries and comparison links against repository history.

## Entry Rules

- Describe the observable change and affected interface or behavior.
- State required developer action for breaking, deprecated, or removed behavior.
- Keep one meaningful change per bullet.
- Link the relevant issue, pull request, advisory, or migration guide when available.
- Put security changes in `Security`, even when implemented as dependency updates.
- Put performance changes in `Changed` only when they are meaningful to consumers.
- Omit internal refactors, formatting, test-only changes, and routine CI maintenance unless externally relevant.

Use Conventional Commit types only as initial evidence:

| Commit signal | Likely category |
| --- | --- |
| `feat` | Added |
| `fix` | Fixed |
| `perf` | Changed when externally meaningful |
| `BREAKING CHANGE` | Changed or Removed, prominently marked |
| `chore`, `refactor`, `test` | Usually omit |

Inspect the actual change rather than categorizing by prefix alone.

## Writing Rules

- Follow the repository's existing changelog format; otherwise use Keep a Changelog.
- Use ISO dates and the repository's exact version syntax.
- Be specific enough that developers can determine whether their code or deployment must change.
- Separate deprecation from removal and state replacement guidance when known.
- Do not turn changelog entries into marketing copy.
- Do not claim compatibility, security impact, or migration requirements without evidence.
- Mark unresolved categorization or impact with `[assumed]` only in drafts.

## Error Paths

- If version or release date is unknown, update `Unreleased` rather than inventing release metadata.
- If commit messages are vague, inspect diffs or related pull requests before writing an entry.
- If a breaking change lacks migration guidance, identify that gap prominently.
- If security details are embargoed, use the approved disclosure language and avoid exposing exploit details.

## Verification

- Every entry is notable, accurate, categorized correctly, and traceable to a change.
- Breaking changes, deprecations, removals, security fixes, and required actions are prominent.
- Versions, dates, links, and compare references are valid and ordered consistently.
- Internal-only noise, duplicate entries, placeholders, and unsupported claims are absent.
