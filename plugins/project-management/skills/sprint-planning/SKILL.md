---
name: sprint-planning
description: >
  Plan the next 2-week sprint — scope work from the Jira backlog, estimate
  team capacity (accounting for PTO), set a sprint goal, and draft a sprint
  plan. Use when kicking off a new sprint, sizing the backlog against team
  availability, deciding what's P0 vs. stretch, or handling carryover
  flagged by `sprint-close`.
allowed-tools: Read, WebFetch, Bash
---

# Sprint Planning

Plan a sprint by scoping work from Jira, estimating capacity for a 5–10 person team, and setting one clear sprint goal.

## Step 1 — Gather inputs

1. **Carryover** — if `sprint-close` was just run, use its spillover list as the starting point for this sprint's backlog. Otherwise pull open issues still assigned to the just-completed sprint.
2. **Backlog** — pull the top-priority unestimated and estimated issues from the product backlog (not yet in a sprint).
3. **Team availability** — ask the user for each person's availability this sprint (PTO, on-call, partial allocation to other projects). This skill doesn't have calendar access, so capacity input comes from the user.
4. **Sprint goal** — ask what success looks like for this sprint in one sentence, if not already stated.

## Step 2 — Estimate capacity

For each team member: available days this sprint (out of 10 for a standard 2-week sprint) minus PTO/other commitments, converted to a rough point capacity using the team's typical points-per-day. Sum for team capacity. Plan to **70–80% of raw capacity** — leave buffer for interrupts, code review, and support rotation.

## Step 3 — Scope the sprint

1. Sort backlog + carryover by priority.
2. Assign items to the sprint until planned load reaches ~75% of capacity, marking the boundary between committed (P0/P1) and stretch (P2).
3. Flag any item without an estimate — these need sizing before they can be committed, not just added on faith.
4. Flag dependencies (cross-team, external, or on another in-flight issue).

## Step 4 — Produce the sprint plan

```
## Sprint Plan: {Sprint Name}
Dates: {start} — {end} | Team: {N} people
Sprint Goal: {one clear sentence}

### Capacity
| Person | Available days | Allocation | Notes |
|---|---|---|---|
| {name} | {X of 10} | {points} | {PTO/on-call/etc.} |
| **Total** | | **{X} points** | |

### Sprint Backlog
| Priority | Issue | Estimate | Owner | Dependencies |
|---|---|---|---|---|
| P0 | {key — title} | {pts} | {name} | {none / blocked by X} |
| P1 | ... | | | |
| P2 (stretch) | ... | | | |

Planned load: {X} points ({Y}% of capacity)

### Risks
| Risk | Impact | Mitigation |
|---|---|---|
| {risk} | {what happens} | {plan} |

### Key dates
| Date | Event |
|---|---|
| {date} | Sprint start |
| {date} | Mid-sprint check-in |
| {date} | Sprint review / demo |
| {date} | Retro |
```

## Step 5 — Create the sprint in Jira

Once the user approves the plan, offer to:

1. Create the sprint (if it doesn't already exist) with the agreed start/end dates.
2. Add the committed (P0/P1) issues to it. Ask before adding stretch (P2) items — some teams prefer to pull those in mid-sprint only if capacity allows.

## Approval gates

- **Never create the sprint or move issues into it without the user reviewing the plan first.** Show the full plan, then ask "create this in Jira?"
- **Never commit stretch items as part of the base plan.** They're explicitly optional.
- **If backlog items lack estimates, don't guess.** Flag them and ask the user or suggest a quick estimation pass before finalizing.

## Connector failures

If Jira/Atlassian is unreachable, the skill can still run using backlog details and carryover the user pastes in manually — but note that nothing can be created in Jira until it's connected.

## Tips

- One clear sprint goal. If it can't be stated in one sentence, the sprint is unfocused.
- Carry over honestly — if something didn't ship last sprint, understand why before re-committing it at the same size.
- Plan to 70–80% capacity, not 100%. Interrupts happen.
