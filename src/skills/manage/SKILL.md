---
name: manage
description: Manage active work across people, agents, tasks, dependencies, blockers, and handoffs. Use for coordination requests like "manage this work", "lead this", "assign", "delegate", "track blockers", "status", "handoff", and multi-workstream execution.
license: MIT
tags:
  - manage
  - execution
  - handoff
metadata:
  author: Oleg Shulyakov
  version: "1.0.3"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: project-management
---

# manage

Keep active work understandable across owners, dependencies, blockers, and handoffs.

---

## Workflow

1. Identify the goal, active workstreams, stakeholders, and ownership.
2. Capture status for each workstream: not started, in progress, blocked, review, done, or unknown.
3. Map dependencies and blockers.
4. Define next actions with owner or assumed owner.
5. Update the view as new information arrives.
6. Produce handoff notes when work pauses or transfers.

---

## Output

- **Lead with current state**: summarize whether work is on track, blocked, or needs a decision.
- **Use an execution table when useful**: include workstream, owner, status, blocker, dependency, and next action.
- **Separate assumptions**: mark assumed owners, priorities, deadlines, or statuses.
- **Preserve handoff state**: include enough context for continuation without rereading the whole thread.
- **Avoid over-documenting**: keep the view proportional to the number of workstreams.

---

## Boundaries

- **Track execution**: maintain goals, owners, dependencies, current status, blockers, decisions, and next actions.
- **Separate from planning**: planning sequences future work; coordination keeps active work moving and handoff-ready.
- **Do not invent authority**: do not silently assign real people without user-provided ownership or clearly stated assumptions.

---

## Error Paths

- **Unknown owners**: use "unassigned" or "assumed owner" instead of inventing responsibility.
- **Blocked work**: name the blocker, impact, and unblock action.
- **Conflicting updates**: keep the latest known state and identify the conflict.

---

## Verification

- **Every active stream has a next action**: done or blocked streams should say why.
- **Dependencies are visible**: downstream work should show what it waits on.
- **Handoff is concrete**: include open decisions, files, commands, artifacts, and validation status when relevant.
