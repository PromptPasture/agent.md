---
name: write-tech-docs
description: >
  Write technical docs. Use for READMEs, API docs, endpoint references, routine or on-call
  runbooks, operational procedures, changelogs, and release notes. Use for operational,
  reference, and release communication docs rather than product or specification docs.
license: MIT
tags:
  - writer
  - docs
  - technical-writing
metadata:
  author: Oleg Shulyakov
  version: "1.1.1"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: documentation
---

# write-tech-docs

Router skill that dispatches to the correct technical documentation variant.

---

## Variant Detection

Check in this order:

1. **Explicit user mention**: "write a README", "API docs for this endpoint", "on-call runbook for alert X", "changelog entry", "release notes for version Y"
2. **File references in context**: `README.md`, `CHANGELOG.md`, `docs/api/`, `runbooks/`
3. **Keywords in the request**:
   - `readme` — README variant
   - `api doc` / `endpoint` / `route` / `reference doc` — api-docs variant
   - `runbook` / `operational` / `procedure` / `how-to` (ops) — runbook-routine variant
   - `on-call` / `alert` / `pagerduty` / `incident response` — runbook-oncall variant
   - `changelog` / `keep a changelog` / `CHANGELOG` — changelog variant
   - `release notes` / `what's new` / `version announcement` — release-notes variant
4. **If still ambiguous**: ask the user once with the list of variants

---

## Variants

| Variant | Output | When to use |
| ----------------- | ----------------------------------------------------- | ------------------------------------------- |
| `readme` | Full README.md: install, usage, API, contributing | Project/repo documentation, library docs |
| `api-docs` | Endpoint reference: params, schemas, errors, examples | Documenting existing endpoints |
| `runbook-routine` | Step-by-step operational procedures | Routine maintenance, deploy, rotate secrets |
| `runbook-oncall` | Alert response runbook with diagnosis/mitigation | On-call alerts, incident response |
| `changelog` | Developer changelog (Keep a Changelog format) | Changes between versions, developer-facing |
| `release-notes` | User-facing release notes | Product updates, version announcements |

---

## Loading References

After detecting the variant, load the corresponding reference:

- **README:** `references/readme.md`
- **API docs:** `references/api-docs.md`
- **Routine runbook:** `references/runbook-routine.md`
- **On-call runbook:** `references/runbook-oncall.md`
- **Changelog:** `references/changelog.md`
- **Release notes:** `references/release-notes.md`

Never load multiple reference files simultaneously. If the user switches context to a different variant, unload and reload.

---

## Common Principles Across All Variants

- **Know your audience**: internal devs, external partners, end users, or on-call engineers
- **Link rather than repeat**: reference existing docs rather than duplicating them
- **Default to Markdown** unless the context specifies another format
- **Use frontmatter for document metadata** when the doc has ownership, status, version, dates, tags, or related-doc fields. Keep task-specific operational facts in the body where operators can scan them.
- **Flag assumptions**: mark anything you inferred with `[assumed]` if you're not certain
- **Remove placeholder text before outputting**: no `[YOUR_VALUE]` or `[TODO]` left behind

---

## Verification

Confirm the selected variant matches the user request, the loaded reference was applied, and the output is audience-appropriate. Check that assumptions are marked, placeholders are removed, and operational or release docs include the concrete commands, owners, dates, versions, or escalation paths needed by their audience.
