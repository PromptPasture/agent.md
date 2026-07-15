---
name: ticket-triage
description: >
  Scores open Jira tickets by urgency, staleness, and priority to produce a
  ranked "work these first" list with context, drafts status-update comments,
  and flags unassigned or overdue issues. Use when the user asks what to work
  on next, wants a triage pass on the backlog, or asks "what's most urgent"
  or "what's overdue."
---

# Ticket Triage

## Quick start

Pull open tickets from Jira, score them, and surface a ranked list with enough context to act on. Drafts comments and flags reassignment candidates — never edits or reassigns without approval.

```
User: "what should the team focus on today"
→ Pull issues: status in (To Do, In Progress), not Done
→ Score each across priority, staleness, due date, blocking relationships
→ Return ranked list (size adapts to volume) with one-line context per issue
→ Offer to draft status comments and flag unassigned/overdue items
```

## Workflow

1. **Pull open issues from Jira.** Fetch issues with status `To Do` or `In Progress` for the team's project(s). Include priority, assignee, due date, labels, linked/blocking issues, and days since last update. If Jira is unavailable, stop: "Jira isn't connected — connect it and try again."

2. **Clarify if the trigger is ambiguous.** If the user said only "backlog" without a qualifier, ask: "Quick backlog overview (counts by status) or a ranked list of what to work on first?" Don't score everything on a bare "backlog."

3. **Score each issue** across four dimensions:
   - **Priority** — Jira priority field (Highest/High/Medium/Low)
   - **Staleness** — days since last update; issues untouched 3+ business days get flagged
   - **Due date urgency** — overdue > due within 2 days > due within the sprint > no due date
   - **Blocking impact** — issues that block other open issues score higher (unblocking them unblocks the team)

4. **Build the ranked list.** Sort descending by composite score. Adapt list size to volume:
   - ≤10 issues → show all
   - 11–30 issues → show top 8
   - >30 issues → show top 10 and note the total count

   For each issue: key, title, assignee (or "unassigned"), priority, one-line context (why it's ranked here), and staleness/due-date flag if relevant.

5. **Flag unassigned and overdue issues separately**, even if they didn't make the top of the ranked list — these need a decision regardless of score.

6. **Offer status-comment drafts.** Ask: "Draft a status-check comment for any of these?" If yes, write a brief comment for each selected issue (e.g., asking the assignee for an update, or noting the blocker). Show the draft; do not post it.

7. **Offer reassignment flags.** For unassigned high-priority issues, suggest candidates based on team members with related recent activity — but never assign automatically. Present as a suggestion only.

## Approval gates

- **Never post comments to Jira.** Draft only; the user posts or asks Claude to post after explicit confirmation.
- **Never reassign or change issue status.** Suggest only.
- **Never change priority or due dates.**
- **If zero issues match the filter**, explain why and offer to check what statuses are in use — don't fabricate a list.

## Output

Present the ranked list, then the unassigned/overdue flags, then ask if the user wants comment drafts or reassignment suggestions.
