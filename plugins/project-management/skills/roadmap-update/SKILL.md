---
name: roadmap-update
description: >
  Update, create, or reprioritize the team's roadmap. Use when adding a new
  initiative and deciding what moves to make room, shifting priorities after
  new information comes in, moving timelines due to a dependency slip, or
  building a Now/Next/Later view from Jira epics.
allowed-tools: Read, WebFetch, Bash
---

# Roadmap Update

Update, create, or reprioritize a roadmap built from Jira epics/initiatives — one level above individual sprints.

## Step 1 — Understand current state

If Jira/Atlassian is connected: pull current epics/initiatives with status, assignee (or owning sub-team), and target timeframe. Identify items overdue, at risk, or recently completed, and flag any without a clear owner or date.

If Jira isn't connected or the roadmap isn't tracked as epics: ask the user to describe or paste the current roadmap.

## Step 2 — Determine the operation

Ask what the user wants to do:

- **Add item** — gather name, description, priority, rough effort, target timeframe, owner, dependencies. Suggest where it fits given current priorities and capacity.
- **Update status** — not started / in progress / at risk / blocked / completed / cut. For at-risk or blocked, ask for the blocker and mitigation.
- **Reprioritize** — ask what changed (new info, strategy shift, resourcing, customer feedback). Apply a framework from below if useful. Show before/after.
- **Move timeline** — ask why, identify downstream impact on dependent items, flag anything moving past a hard deadline.
- **Create from scratch** — ask timeframe (quarter/half/year) and format (Now/Next/Later is the default and usually the right call for a 5–10 person team).

## Step 3 — Generate the roadmap view

**Now / Next / Later** (default format):

- **Now** — current sprint's committed epics. High confidence in scope and timeline.
- **Next** — next 1–3 months. Scoped and prioritized, not yet started.
- **Later** — 3–6+ months out. Directional; scope and timing still flexible.

For each item: name, one-line description, status (on track / at risk / blocked / completed / not started), target timeframe, owner, key dependencies.

Follow with:

- **Risks and dependencies** — blocked/at-risk items with detail; cross-team dependencies; items approaching hard deadlines
- **Changes this update** — items added/removed/reprioritized, timeline shifts, status changes (if this is an update to an existing roadmap)

## Step 4 — Follow up

Offer to: draft communication about a change, or update the corresponding Jira epics' status/dates if the user approves specific changes.

## Prioritization frameworks (use when reprioritizing)

- **RICE** — (Reach × Impact × Confidence) / Effort. Good for a quantitative pass over a large backlog.
- **MoSCoW** — Must / Should / Could / Won't have. Good for scoping a quarter and forcing tradeoff conversations.
- **ICE** — Impact × Confidence × Ease (1–10 each). Faster than RICE, good when data is thin.
- **Value vs. effort matrix** — quick wins (high value, low effort) first; avoid low-value/high-effort "money pits."

## Capacity guidance for a 5–10 person team

A reasonable default allocation: 70% planned feature work, 20% technical health (debt, reliability, DX), 10% unplanned buffer. If roadmap commitments exceed capacity, something has to move — don't solve it by assuming people can do more.

## Approval gates

- **Never update Jira epic status, dates, or priority without the user approving the specific change.** Show current → proposed and wait.
- **When adding something to Now or Next, ask what comes off.** Roadmaps are zero-sum against capacity — say so if the user doesn't raise it themselves.

## Tips

- A roadmap is a communication tool, not a task list — keep it at the level of themes and outcomes.
- Dependencies are the biggest risk to any roadmap. Surface them explicitly, don't bury them.
- Batch roadmap changes at a natural cadence (e.g. monthly) rather than reshuffling for every new data point — frequent churn often signals unclear strategy more than good responsiveness.
