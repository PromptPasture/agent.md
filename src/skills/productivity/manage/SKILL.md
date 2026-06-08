---
name: manage
description: Manage active work across people, agents, tasks, dependencies, blockers, and handoffs. Use for coordination requests like "manage this work", "lead this", "assign", "delegate", "track blockers", "status", "handoff", and multi-workstream execution.
license: Apache-2.0
tags:
  - manage
  - execution
  - handoff
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: management
---

# Managing Work

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

  Scenario: Active execution is being managed
    Given work is underway
    Then maintain goals, owners, dependencies, current status, blockers, decisions, and next actions

  Scenario: Output drifts into planning
    Given the main need is future sequencing
    Then distinguish planning from coordination
    And keep this skill focused on active work and handoff readiness

  Scenario: Ownership is unclear
    Given real people have not been assigned by the user
    Then do not silently assign them
    And mark ownership as user-provided, unassigned, or assumed

---

## Error Paths

  Scenario: Owners are unknown
    Given ownership is not known
    Then use "unassigned" or "assumed owner"
    And do not invent responsibility

  Scenario: Work is blocked
    Given a workstream is blocked
    Then name the blocker, impact, and unblock action

  Scenario: Updates conflict
    Given status updates conflict
    Then keep the latest known state
    And identify the conflict

---

## Verification

  Scenario: Output passes quality check
    Given an execution view has been produced
    Then every active stream has a next action or a reason it is done or blocked
    And dependencies are visible
    And handoff context includes open decisions, files, commands, artifacts, and validation status when relevant
