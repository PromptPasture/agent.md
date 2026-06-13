---
name: write-changelog
description: You MUST use this to write or revise developer-facing changelogs. Use for CHANGELOG.md files, unreleased sections, version entries, commit or pull-request categorization, breaking changes, deprecations, removals, fixes, and security changes.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
  tags: [writer, docs, changelog]
---

# Writing Changelogs

Write an accurate developer-facing record of notable changes for a project or release.

## Workflow

1. **Define the task:** Identify whether to create a changelog, update an unreleased section, or add or revise a version entry.
2. **Inspect evidence:** Use authoritative sources such as the existing changelog, repository conventions, commits, pull requests, issues, release tags, migrations, and security advisories.
3. **Set release scope:** Determine the version, date, comparison range, and intended audience. If version or date is unknown, update `Unreleased` when the repository uses it; otherwise identify the missing metadata instead of inventing it.
4. **Preserve conventions:** Follow the established format, headings, ordering, link style, and versioning convention. For a new changelog, choose the simplest consistent structure suited to the project.
5. **Select and classify changes:** Use the project's existing categories. Otherwise use only applicable categories such as Added, Changed, Deprecated, Removed, Fixed, and Security.
6. **Consolidate and order entries:** Merge duplicate or closely related changes, then order entries by developer impact within each category.
7. **Surface critical impact:** Make migration requirements, compatibility limits, deprecations, removals, breaking changes, and security implications explicit.
8. **Revise safely:** Verify every entry against the selected release range and update the changelog without rewriting unrelated history.

## Writing Rules

- **Focus on outcomes:** Describe the observable change and its developer impact, not the implementation process.
- **Keep entries independent:** Write concise entries that stand alone without requiring the reader to inspect a commit, issue, or pull request.
- **Match changelog voice:** Use imperative-free completed-change language consistent with the existing changelog.
- **Link selectively:** Include issue, pull-request, commit, migration, or advisory links only when useful and consistent with the project's style.
- **Mark incompatibility:** Distinguish incompatible behavior from ordinary changes. State what breaks, who is affected, and the required migration or action when evidence supports it.
- **Preserve lifecycle order:** Record deprecations before removals when the release history supports that sequence.
- **Handle security carefully:** Describe security changes precisely without exposing exploit details or unverified severity claims.
- **Exclude internal noise:** Omit routine refactors, test-only changes, formatting, dependency churn, and internal maintenance unless they affect consumers, compatibility, operations, or security.
- **Avoid duplication:** Do not reproduce release notes, marketing language, raw commit messages, or exhaustive repository history.
- **Stop on uncertainty:** If evidence conflicts or release scope is unclear, stop the disputed entry and identify what must be confirmed. Do not invent versions, dates, impact, links, or migration guidance.

## Verification

- **Conventions:** The version, date, release range, headings, ordering, and links follow the project's conventions.
- **Traceability:** Every entry belongs to the named release, is supported by repository evidence, and appears once in the most appropriate category.
- **Critical impact:** Breaking changes, deprecations, removals, migrations, compatibility limits, and security changes are visible and actionable where applicable.
- **Content quality:** Entries describe developer-relevant outcomes accurately and contain no raw commit noise, unsupported claims, placeholders, or unmarked assumptions.
- **Change isolation:** Existing historical entries and unrelated changelog content remain unchanged.
