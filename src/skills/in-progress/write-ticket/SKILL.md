---
name: write-ticket
description: You MUST use this when the user asks to write or revise Jira/GitHub tickets, issues, or work items, including bug, feature, task, chore, documentation, and spike requests.
license: Apache-2.0
tags:
  - writer
  - tickets
  - issue-tracking
metadata:
  author: Oleg Shulyakov
  version: "1.1.1"
  source: github.com/olegshulyakov/agent.md
  catalog: product
  category: requirements
---

# Writing Tickets

Produces clear, complete, and actionable tickets for Jira, GitHub Issues, or any work-item tracker. Covers bugs, features, tasks, chores, documentation, and spikes.

---

## Instructions

### Step 1: Identify the ticket type

Determine which type applies before writing anything:

| Type | Use when |
| --- | --- |
| **Bug** | Something is broken or behaves unexpectedly |
| **Feature** | New capability or user-visible behaviour is requested |
| **Task / Chore** | Internal work with no direct user impact (refactor, upgrade, CI fix) |
| **Documentation** | Docs need to be created, updated, or removed |
| **Spike** | Research or investigation needed before committing to an approach |

If the type is ambiguous, ask one concise question before writing.

### Step 2: Gather missing context

Only ask when information is genuinely absent and cannot be inferred. Ask all missing questions in a single message.

**Always needed (all types):**

- One-sentence summary of the problem or goal
- Affected area or component (if not obvious)

**Type-specific:**

- _Bug_ — Steps to reproduce, actual behaviour, expected behaviour, environment/version
- _Feature_ — Who benefits, what they need, why it matters, any constraints
- _Spike_ — Questions to answer, time-box (e.g. 2 days), deliverable (doc, PR, ADR)
- _Docs_ — Target audience, scope (new page vs. update), where it lives

### Step 3: Write the ticket

Use the template for the identified type (see Templates below). Follow all formatting rules.

### Step 4: Self-review before presenting

Check every field:

- [ ] Title: ≤ 72 characters, action-oriented, no jargon acronyms without expansion
- [ ] No placeholder text (`TBD`, `TODO`, `...`) unless the user explicitly asked for a draft
- [ ] Acceptance criteria are testable — each starts with "Given / When / Then" or a clear pass/fail statement (Feature only)
- [ ] Reproducing steps are numbered and deterministic (bug only)
- [ ] Scope section states what is explicitly out of scope (feature/spike)
- [ ] Spike has a time-box and a named deliverable

Fix any issue found before presenting.

---

## Templates

### Bug

```markdown
# [Component] Short description of the broken behaviour

**Type:** Bug
**Priority:** P0 | P1 | P2 | P3

## Summary

One or two sentences describing what is broken and its user impact.

## Environment

- Version / Release:
- Platform / OS:
- Browser (if applicable):

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Actual Behaviour

What happens today.

## Expected Behaviour

What should happen instead.

## Additional Context

Screenshots, logs, related tickets, workarounds.
```

---

### Feature

```markdown
# [Verb] [object] so that [benefit]

**Type:** Feature
**Priority:** P0 | P1 | P2 | P3

## User Story

As a [role], I want [capability] so that [benefit].

## Problem Statement

Why this matters and what gap it closes.

## Proposed Solution [optional]

High-level description of the approach (avoid implementation detail).

## Acceptance Criteria

- Given [context], when [action], then [outcome].
- ...

## Out of Scope

- What this ticket explicitly does NOT cover.

## Dependencies

List any blocking tickets, services, or decisions.

## Additional Context

Mockups, references, related tickets.
```

---

### Task / Chore

```markdown
# [Verb] [object] (chore)

**Type:** Task | Chore
**Priority:** P0 | P1 | P2 | P3

## Summary

What needs to be done and why, in two to three sentences.

## Motivation

Technical or operational reason (e.g. dependency is EOL, test suite is slow).

## Definition of Done

- [ ] Concrete, verifiable outcome 1
- [ ] Concrete, verifiable outcome 2

## Out of Scope

What this ticket does NOT change.

## Dependencies

Blocking tickets or decisions.
```

---

### Documentation

```markdown
# [Add | Update | Remove] docs for [subject]

**Type:** Documentation
**Priority:** P0 | P1 | P2 | P3

## Summary

What documentation needs to change and why.

## Audience

Who will read this (e.g. end users, developers, operators).

## Scope

- New page / section: [location or URL]
- OR: Update existing page: [link]
- OR: Remove outdated content: [link]

## Key Topics to Cover

- Topic 1
- Topic 2

## Definition of Done

- [ ] Content reviewed for accuracy
- [ ] Published to [location]
- [ ] Linked from [parent page / nav]
```

---

### Spike

```markdown
# Spike: [Question or decision to resolve]

**Type:** Spike
**Priority:** P0 | P1 | P2 | P3
**Time-box:** [e.g. 2 days]

## Background

Context that makes this investigation necessary.

## Questions to Answer

1. Question one
2. Question two

## Out of Scope

What the spike will NOT investigate.

## Deliverable

- [ ] Short written summary
- [ ] ADR (Architecture Decision Record)
- [ ] Proof-of-concept branch
- [ ] Other: ...

## Definition of Done

- [ ] All questions above have a documented answer
- [ ] Deliverable is linked or attached
- [ ] Follow-up tickets are created if needed
```

---

## Formatting Rules

- **Title** — imperative verb, sentence case, ≤ 72 characters, rendered as an `#` H1. Do not start with "We need to" or "I want".
- **Priority** — choose exactly one: P0 (critical / blocking), P1 (high), P2 (medium), P3 (low). If unsure, default to P2 and note the assumption.
- **Acceptance Criteria** — use Given/When/Then format or plain pass/fail statements. Never use vague terms like "works correctly" or "looks good".
- **Out of Scope** — required for Feature and Spike. Omit only if the boundary is genuinely self-evident and you state why.
- **Markdown** — use `#` for the title and `##` for each section header. Keep formatting compatible with both GitHub and Jira (avoid HTML tags).

---

## Examples

### Example 1: Bug from a vague report

**User says:** "The login button doesn't work on mobile."

**Ticket produced:**

```markdown
# [Auth] Login button unresponsive on iOS Safari 17

**Type:** Bug
**Priority:** P1

## Summary

Tapping the login button on iOS Safari 17 produces no response — no
navigation, no error, and no network request. Users cannot sign in on
affected devices.

## Environment

- Version: 2.4.1
- Platform: iOS 17.4 / Safari 17
- Desktop browsers: unaffected

## Steps to Reproduce

1. Open the app at app.example.com on an iPhone running iOS 17.4.
2. Enter valid credentials.
3. Tap the Login button.

## Actual Behaviour

Nothing happens. No spinner, no redirect, no console error visible to
the user.

## Expected Behaviour

The user is authenticated and redirected to the dashboard within 2 s.

## Additional Context

First reported in #support-channel. No related open tickets found.
```

---

### Example 2: Feature from a user story

**User says:** "Users should be able to export their data as CSV."

**Ticket produced:**

```markdown
# Add CSV export for user data

**Type:** Feature
**Priority:** P2

## User Story

As a data analyst, I want to export my account data as a CSV file so
that I can process it in Excel or Python without manual copy-paste.

## Problem Statement

Currently there is no bulk export. Users copy data row by row, leading
to errors and support requests.

## Proposed Solution

Add an "Export as CSV" button to the Account > Data page. On click,
generate and download a CSV containing all records visible in the
current filtered view.

## Acceptance Criteria

- Given I am on the Account > Data page, when I click "Export as CSV",
  then a download starts within 3 s.
- Given the download completes, then the file contains all columns
  shown in the current view with a header row.
- Given the filtered view has 0 rows, then the export contains only
  the header row and a user-facing message explains the result.

## Out of Scope

- Excel (.xlsx) export format
- Scheduled / automated exports
- Export of data from other sections of the app

## Dependencies

- None identified
```
