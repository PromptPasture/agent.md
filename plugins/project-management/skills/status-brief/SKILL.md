---
name: status-brief
description: >
  Generates a one-page weekly status brief from Jira — sprint burndown, what
  shipped, what's blocked, and the week ahead. Built for a Scrum team running
  2-week sprints. Use when the user asks for a status update, standup summary,
  sprint check-in, or "what's the team working on."
allowed-tools: Read, WebFetch, Bash
---

# Weekly Status Brief

Pull current sprint data from Jira and deliver a one-page brief the team lead can read in under two minutes and forward to stakeholders as-is.

## Step 1 — Pull sprint data

1. Identify the active sprint on the team's board (Jira sprint with status `active`).
2. Pull all issues in the sprint: status, assignee, story points, last updated.
3. Compute:
   - **Burndown** — points completed vs. points remaining vs. days left in the sprint
   - **Shipped this week** — issues moved to `Done` in the last 7 days
   - **In progress** — issues currently `In Progress`, grouped by assignee
   - **Blocked** — issues flagged `Blocked` or with no update in 3+ business days
   - **Scope changes** — issues added to or removed from the sprint after it started

4. If no active sprint exists, say so and offer to pull the backlog's top priority issues instead.

## Step 2 — Format the brief

```
# Weekly Status — {Mon DD, YYYY}
Sprint: {sprint name} ({day X of 10})

## Burndown
{X of Y points done} · {on track / behind by Z points} · {N days left}

## Shipped this week
- {issue key} — {title}
- ...

## In progress
- {assignee}: {issue key} — {title}
- ...

## Blocked
- {issue key} — {title} — blocked {N} days — {reason if known}
- ...

## Week ahead
- {notable deadline or ceremony, e.g. sprint review Thu 2pm}

## Needs attention
1. {highest-leverage thing for the lead to act on, one line}
2. {...}
```

## Step 3 — Deliver

1. Show the full brief in chat.
2. Offer to save the brief as a file if the user wants a record.

## Approval gates

- **Never edit or comment on Jira issues from this skill.** This is a read-only reporting workflow — route the user to `ticket-triage` or `board-cleanup` if they want to act on findings.
- **Flag blocked and stalled issues plainly** rather than softening the language — the point of the brief is to surface what needs the lead's attention.

## Connector failures

If Jira/Atlassian is unreachable, stop and tell the user: "Jira isn't connected — connect it and try again." This skill has no other data source to fall back on.

## Output

End with the formatted brief and ask if the user wants it saved as a file.
