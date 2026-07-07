---
name: to-ticket
description: Writes and revises Jira, GitHub, and Linear tickets — bugs, features, tasks, chores, documentation, and spikes — using type-specific templates.
disable-model-invocation: true
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "2.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: product
  category: requirements
  tags: [writer, tickets, issue-tracking, agile, user-stories]
---

# To Ticket

Produce a clear, complete, and actionable ticket for Jira, GitHub Issues, Linear, or any work-item tracker.

## Workflow

1. **Identify the ticket type** — Bug, Feature, Task/Chore, Documentation, or Spike (see table below). Ask one concise question when the type is ambiguous.
2. **Gather missing context** — inspect the prompt and available context first; ask only for genuinely absent, type-specific details, all in a single message.
3. **Size the Feature** — decide whether the request needs sprint-ready rigor (story points, epic linkage, independent scenarios) or stays a lightweight capability ask. Split a request spanning multiple personas, outcomes, or workflows into independent tickets.
4. **Write the ticket** — fill the matching template below and apply the Writing Rules.
5. **Self-review** — check the draft against the Verification checklist before presenting.

|Type|Use when|
|---|---|
|**Bug**|Something is broken or behaves unexpectedly|
|**Feature**|New capability or user-visible behavior is requested|
|**Task / Chore**|Internal work with no direct user impact (refactor, upgrade, CI fix)|
|**Documentation**|Docs need to be created, updated, or removed|
|**Spike**|Research or investigation needed before committing to an approach|

### Type-specific context to gather

- _Bug_ — steps to reproduce, actual behavior, expected behavior, environment/version
- _Feature_ — who benefits, what they need, why it matters, any constraints; for sprint-ready detail, also the target persona, parent epic, and the team's estimation scale
- _Spike_ — questions to answer, time-box (e.g. 2 days), deliverable (doc, PR, ADR)
- _Documentation_ — target audience, scope (new page vs. update), where it lives

## Output

Produce the ticket in Markdown. Present it directly in the conversation, formatted for pasting into the tracker; write it to a file only if the user names a path.

Use the template for the identified type below, and remove optional fields or sections that add no value.

### Bug

```markdown
# [Component] Short description of the broken behaviour

**Type:** Bug
**Severity:** Critical | Major | Minor | Trivial
**Priority:** P0 | P1 | P2 | P3
**Regression:** Yes (from [version]) | No | Unknown

## Summary

One or two sentences describing what is broken and its user impact.

## Environment

- Version / Release:
- Platform / OS:
- Browser (if applicable):

## Preconditions [optional]

State or setup required before reproducing (e.g. account type, feature flag, data state).

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Actual Behaviour

What happens today.

## Expected Behaviour

What should happen instead.

## Workaround [optional]

Known mitigation, if any, and its limitations.

## Additional Context [optional]

Screenshots, logs, related tickets.
```

### Feature

```markdown
# [Verb] [object] so that [benefit]

**Type:** Feature
**Priority:** P0 | P1 | P2 | P3
**Story Points:** [1 | 2 | 3 | 5 | 8 | TBD] [optional — sprint-ready only]
**Epic:** [Parent epic, initiative, or URL] [optional]

## User Story

**As a** [specific user or role],
**I want** [capability or action],
**so that** [measurable or observable benefit].

## Problem Statement

Why this matters and what gap it closes.

## Proposed Solution [optional]

High-level description of the approach (avoid implementation detail).

## Acceptance Criteria

### Scenario: [Primary path]

**Given** [initial state or prerequisite]
**When** [user or system action]
**Then** [observable result]

### Scenario: [Relevant failure or edge path] [optional]

**Given** [initial state or prerequisite]
**When** [invalid, unavailable, unauthorized, empty, or boundary condition]
**Then** [observable handling and recovery behavior]

## Definition of Done [optional]

- [ ] Code reviewed and merged
- [ ] Automated tests added or updated and passing
- [ ] Documentation updated (if user-facing)

## Out of Scope [optional]

- What this ticket explicitly does NOT cover.

## Dependencies [optional]

List any blocking tickets, services, or decisions.

## Additional Context [optional]

Mockups, references, related tickets.
```

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

## Out of Scope [optional]

What this ticket does NOT change.

## Dependencies [optional]

Blocking tickets or decisions.
```

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

## Out of Scope [optional]

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

## Writing Rules

- **Title:** imperative verb, sentence case, ≤ 72 characters, rendered as an `#` H1. Do not start with "We need to" or "I want".
- **Priority:** choose exactly one: P0 (critical/blocking), P1 (high), P2 (medium), P3 (low). If unsure, default to P2 and note the assumption.
- **Separate Severity from Priority (Bug):** Severity states impact (Critical/Major/Minor/Trivial); Priority states urgency to fix. A high-severity bug can be low priority and vice versa — never conflate them.
- **Flag regressions (Bug):** state whether the bug is a regression and, if known, the version it regressed from; use `Unknown` rather than guessing.
- **Center one user value (Feature):** each feature ticket serves one persona pursuing one coherent outcome.
- **Apply INVEST (Feature):** independent, negotiable, valuable, estimable, small, and testable; state dependencies when full independence isn't possible.
- **Make acceptance criteria atomic:** each Feature scenario has an observable Given/When/Then precondition, action, and result; other types use a clear pass/fail statement. Never use vague terms like "works correctly" or "looks good".
- **Distinguish Acceptance Criteria from Definition of Done (Feature):** Acceptance Criteria define what makes this increment done; Definition of Done is the team's standing bar (review, tests, docs) — do not merge them into one list.
- **Estimate story points only when asked or the team's scale is known (Feature):** state uncertainty instead of inventing precision.
- **Mark uncertainty:** label inferred details `[assumed]`; use `TBD` only for a genuinely expected but unresolved value.
- **Bound the scope:** state what a Feature or Spike ticket explicitly does NOT cover; omit only when the boundary is self-evident.
- **Use plain Markdown:** `#` for the title, `##` for each section; keep formatting compatible with both GitHub and Jira (avoid HTML tags).

## Verification

Before presenting the ticket, verify that:

- The title is ≤ 72 characters, action-oriented, and free of unexpanded jargon acronyms.
- No placeholder text (`TBD`, `TODO`, `...`) remains unless the user explicitly asked for a draft.
- Acceptance criteria are testable: Given/When/Then for Feature scenarios, a clear pass/fail statement otherwise.
- A Bug has both Severity and Priority set, and they are not conflated; Regression is stated rather than left blank.
- Reproduction steps are numbered and deterministic (Bug only).
- Out of Scope is stated (Feature/Spike).
- A Feature ticket represents one independently valuable increment (INVEST) or explicitly states its dependencies.
- A Feature's Definition of Done, if present, is distinct from its Acceptance Criteria.
- Story points, if present, reflect the team's scale rather than invented precision.
- A Spike has a time-box and a named deliverable.
