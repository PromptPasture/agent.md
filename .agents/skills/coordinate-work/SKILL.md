---
name: coordinate-work
description: Manage active work across people, agents, tasks, dependencies, blockers, and handoffs. Use for "coordinate-work", "manage this work", "lead this", "assign", "delegate", "track blockers", "status", "handoff", and multi-workstream execution.
license: MIT
version: 1.0.0
tags:
  - coordinate-work
  - execution
  - handoff
author: Oleg Shulyakov
metadata:
  catalog: utility
---

# coordinate-work

Keep active work understandable across owners, dependencies, blockers, and handoffs.

## Scope

**Use this skill when execution is active or split across workstreams.**

- **Trigger on coordination**: use for "coordinate-work", "manage this work", "team lead", "lead this", "assign", "delegate", "track blockers", "status", "handoff", and multi-agent or multi-workstream requests.
- **Track execution**: maintain goals, owners, dependencies, current status, blockers, decisions, and next actions.
- **Separate from planning**: planning sequences future work; coordination keeps active work moving and handoff-ready.
- **Do not invent authority**: do not silently assign real people without user-provided ownership or clearly stated assumptions.

---

## Workflow

**Maintain a compact execution view that another person or agent can resume from.**

1. Identify the goal, active workstreams, stakeholders, and ownership.
2. Capture status for each workstream: not started, in progress, blocked, review, done, or unknown.
3. Map dependencies and blockers.
4. Define next actions with owner or assumed owner.
5. Update the view as new information arrives.
6. Produce handoff notes when work pauses or transfers.

---

## Output

**Make status, ownership, blockers, and next actions explicit.**

- **Lead with current state**: summarize whether work is on track, blocked, or needs a decision.
- **Use an execution table when useful**: include workstream, owner, status, blocker, dependency, and next action.
- **Separate assumptions**: mark assumed owners, priorities, deadlines, or statuses.
- **Preserve handoff state**: include enough context for continuation without rereading the whole thread.
- **Avoid over-documenting**: keep the view proportional to the number of workstreams.

---

## Error Paths

**When ownership or status is unclear, expose the gap and keep work moving where possible.**

- **Unknown owners**: use "unassigned" or "assumed owner" instead of inventing responsibility.
- **Blocked work**: name the blocker, impact, and unblock action.
- **Conflicting updates**: keep the latest known state and identify the conflict.

---

## Verification

**Check that another capable person could continue from the coordination view.**

- **Every active stream has a next action**: done or blocked streams should say why.
- **Dependencies are visible**: downstream work should show what it waits on.
- **Handoff is concrete**: include open decisions, files, commands, artifacts, and validation status when relevant.
