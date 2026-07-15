---
name: write-ticket
description: >
  Write a feature spec or PRD from a problem statement or feature idea. Use
  when turning a vague idea or ticket request into a structured document,
  scoping a feature with goals and non-goals, defining success metrics and
  acceptance criteria, or breaking a big ask into a phased spec ready to
  become Jira epics and stories.
allowed-tools: Read, WebFetch, Bash
---

# Write Spec

Write a feature specification or PRD, then optionally turn it into Jira epics/stories.

## Step 1 — Understand the feature

Accept any starting point: a feature name, a problem statement, a user request, or a vague idea. Ask what the user wants to spec if it isn't clear yet.

## Step 2 — Gather context

Ask conversationally, not as a dumped list — most important first, fill gaps as you go:

- **User problem** — what problem does this solve, who experiences it?
- **Target users** — which segment(s)?
- **Success metrics** — how will you know it worked?
- **Constraints** — technical, timeline, regulatory, dependencies
- **Prior art** — has this been attempted before?

## Step 3 — Pull context from Jira

If Jira/Atlassian is connected: search for related epics, stories, or tickets; pull in any existing requirements or acceptance criteria; identify dependencies on other in-flight work. If nothing relevant is connected or found, proceed entirely from what the user provides — don't block on it.

## Step 4 — Generate the PRD

```
## Problem Statement
{2-3 sentences: the problem, who's affected, cost of not solving it}

## Goals
- {3-5 specific, measurable outcomes}

## Non-Goals
- {3-5 things explicitly out of scope, with why}

## User Stories
As a {user type}, I want {capability} so that {benefit}.
(grouped by persona, ordered by priority, including edge cases)

## Requirements
Must-Have (P0): {with acceptance criteria}
Nice-to-Have (P1): {...}
Future Considerations (P2): {...}

## Success Metrics
Leading indicators: {adoption, activation, task completion, error rate}
Lagging indicators: {retention, revenue, satisfaction, support load}
Targets: {specific numbers, measurement method, evaluation timing}

## Open Questions
- {question} — needs answer from {engineering/design/legal/stakeholder}, {blocking/non-blocking}

## Timeline Considerations
{hard deadlines, dependencies, suggested phasing}
```

### Writing good user stories

Specific user type (not just "user"), capability described as what not how, clear benefit. Cover error states and edge cases. Common mistakes to avoid: too vague ("faster"), solution-prescriptive ("a dropdown"), no benefit, too large (break it up), or internally focused ("as the eng team...").

### Categorizing requirements (MoSCoW)

Be ruthless about P0 — if everything is P0, nothing is. Challenge every must-have: "would we really not ship without this?" P1s should be things you're confident you'll build soon, not a wishlist. P2s are architectural insurance that guide design decisions now even though you're not building them yet.

### Acceptance criteria

Given/When/Then or a checklist. Cover happy path, error cases, and edge cases. Be specific about behavior, not implementation. Avoid ambiguous words like "fast" or "intuitive" without defining what they mean concretely.

## Step 5 — Review, iterate, and (optionally) create Jira epics

After generating the PRD: ask if any section needs adjustment, offer to expand specific sections. If the user wants it broken into work, offer to draft the corresponding epic(s) and top-level stories — show what would be created and wait for approval before writing anything to Jira.

## Approval gates

- **Never create Jira epics/stories without the user reviewing and approving the breakdown first.**
- **Non-goals matter as much as goals.** Always include them — they prevent scope creep during implementation.

## Tips

- Be opinionated about scope. A tight, well-defined spec beats an expansive vague one.
- If the idea is too big for one spec, suggest phasing and spec the first phase only.
- Success metrics should be specific and measurable — "improve UX" is not a metric.
- Open questions should be genuinely open — don't include ones you can already answer from context.
