---
name: sprint-close
description: >
  Closes out a 2-week sprint — reconciles planned vs. completed scope, flags
  spillover and scope creep, writes a retro-ready summary, and gives a
  heads-up on the next sprint's readiness. Use when the user says the sprint
  is ending, asks for a sprint report, wants retro prep, or asks what's
  carrying over to next sprint.
allowed-tools: Read, WebFetch, Bash
---

# Sprint Close

Run the sprint-close workflow. Reconcile scope, flag issues worth discussing at retro, and get the team ready for sprint planning.

Parse arguments:

- `--sprint` (default: the most recently completed or currently active sprint) — sprint name or ID
- `--save-to` (default: show in chat only) — offer to save the summary as a file if the user wants a record

## Step 1 — Reconcile scope

1. Pull all issues that were in the sprint at any point (via sprint history/changelog if available, otherwise current sprint membership).
2. Categorize:
   - **Completed** — issues moved to `Done` within the sprint window
   - **Spillover** — issues still open, carrying into the next sprint
   - **Scope added mid-sprint** — issues added after the sprint started
   - **Scope removed mid-sprint** — issues pulled out before completion
3. Compute: planned points vs. completed points vs. committed-vs-delivered ratio.

## Step 2 — Flag things worth a look

Surface in the same report:

- **Spillover issues with no comment/update explaining why** — these are the ones worth asking about
- **Issues that bounced status** (e.g., went back from `In Progress` to `To Do`, or reopened after `Done`)
- **Issues with no story-point estimate** that were still worked on

For each, note it plainly — this isn't a workflow that fixes anything, it's a workflow that gets the facts straight before retro.

## Step 3 — Sprint summary

Generate a plain-English summary:

```
Sprint {name} closed at {X of Y committed points} ({Z}% completion).

Completed: {N} issues / {points} points
Spillover: {N} issues / {points} points — carrying to next sprint
Scope changes: {+N added / -M removed} mid-sprint

Notable:
1. {spillover pattern, bounced ticket, or estimate gap worth discussing at retro}
2. ...

Team breakdown:
- {assignee}: {completed} done, {in-progress/spillover} carrying over
```

## Step 4 — Next-sprint readiness

1. Check the backlog for the next sprint's candidate issues: are they estimated, prioritized, and have acceptance criteria?
2. Flag any top-priority backlog issue missing an estimate — these will slow down sprint planning if not groomed first.
3. Note spillover issues that should auto-carry into the next sprint (already flagged in Step 1) versus ones that might need re-scoping.

## Approval gates

- **Never move issues, close the sprint, or start the next sprint in Jira.** This skill reports and recommends; the sprint transition itself is the Scrum Master's call, done in Jira directly (or with explicit confirmation if the user asks Claude to do it).
- **Never editorialize about individual performance.** Report completion by assignee factually — no commentary on why someone's number is lower.

## Connector failures

If Jira/Atlassian is unreachable, stop — this workflow requires Jira as the source of truth.

## Output

End with the sprint summary and next-sprint readiness check. Offer to save it as a file for the retro doc, and ask if the user wants the spillover list turned into a ticket-triage pass.
