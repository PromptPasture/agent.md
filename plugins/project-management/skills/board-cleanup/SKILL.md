---
name: board-cleanup
description: >
  Scans Jira for stale issues, duplicates, and missing fields, then fixes what
  the user approves. Use when the user says the board is a mess, asks for a
  backlog grooming pass, wants to clean up Jira, or asks about stale/duplicate
  tickets before sprint planning.
allowed-tools: Read, WebFetch, Bash
---

# Board Cleanup

Run a Jira hygiene pass. Act immediately — the user asked for cleanup, so skip the intent-detection step.

Parse arguments:

- `--scope` (default: `all`) — `stale` for stale-issue audit only, `duplicates` for dedup only, `fields` for missing-field audit only, `all` for everything

## Step 1 — Scan for stale issues

If scope includes stale:

1. Pull all open issues (not `Done`, not `Won't Do`) across the team's project(s).
2. Flag issues with no update (comment, status change, field edit) in the last 10 business days.
3. For each stale issue: show key, title, status, assignee, last update date, and any linked issues.
4. Propose actions per issue: ping assignee for a status check, move to backlog, close as won't-do, or update due date.

Present the full stale-issue list before making any changes.

## Step 2 — Scan for likely duplicates

If scope includes duplicates:

1. Search open issues for likely duplicates: similar titles, same component/label, opened within a few days of each other, or explicitly cross-referenced.
2. For each duplicate set: show both issues side-by-side — key, title, status, assignee, description summary.
3. Propose which issue to keep and which to close as a duplicate (linking to the kept issue).

Present all duplicate sets before closing anything.

## Step 3 — Scan for missing required fields

1. Check all open issues for missing fields: story points/estimate, priority, assignee, sprint assignment (for issues that should be in the current sprint).
2. Present a table of issues with missing fields and what's missing.

## Step 4 — Apply approved fixes

1. Walk through each finding from Steps 1–3.
2. Apply only the changes the user explicitly approves.
3. Report each change as it's made with a Jira link.

## Connector failures

If Jira/Atlassian is unreachable, stop — this workflow requires Jira as the data source. Tell the user: "Jira isn't connected. Connect it, then rerun board cleanup."

## Approval gates

- **Never delete issues.** Jira doesn't make this easy to undo, and neither does this skill. If the user asks, say the skill can't and point them to Jira directly.
- **Never close an issue (Done or Won't Do) without explicit approval**, even when staleness or duplication looks obvious. Flag and defer.
- **Never auto-link or auto-close duplicates.** Show side-by-side and wait for approval per pair.
- **Side-by-side diffs for all changes.** Show current value and proposed value; wait for approval per item.

## Output

End with a summary: X issues updated, Y duplicates closed/linked, Z fields filled. Include Jira links to the affected issues.
