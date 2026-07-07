---
name: plan
description: Sequences work into ordered phases with dependencies and success conditions. Use for planning requests like "break this down", "roadmap", "approach", "milestones", "how should we proceed", migration planning, rollout planning, and scoped next steps.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.4.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: planning
  tags: [plan, roadmap, sequencing]
---

# Planning Steps

Turn a defined outcome into an ordered, executable path with dependencies, decision points, and success conditions.

## Workflow

### Goal

An ordered, executable plan that the user has explicitly approved and, once approved, saved to `docs/YYYY-MM-DD-[topic]/PLAN.md`.

### Setup

1. Define the desired outcome, scope, constraints, and completion condition.
2. Inspect the available context before proposing work. Separate confirmed facts from assumptions and unresolved questions.

### Loop

1. Break simple work into an ordered checklist and complex work into phases or milestones. Order work by dependency, risk, and feedback value.
2. Specify the action, expected result, dependencies, and verification for each meaningful step.
3. Identify blockers, decision points, rollback needs, and work that can proceed in parallel.
4. Remove unnecessary work and separate optional follow-ups from the required scope.
5. Present and revise the plan conversationally. Do not save discussion drafts.

### Exit

When the user explicitly approves the final plan. Do not infer approval from silence or a request to begin implementation.

### Report

Save the approved plan to `docs/YYYY-MM-DD-[topic]/PLAN.md` (earlier only if the user explicitly asks to save it). Produce the plan without executing it unless the user also asks for implementation.

## Output

Lead with the approach, then the plan:

```text
Approach:
[One or two sentence summary of the intended path.]

Assumptions:
- [Assumption affecting sequencing, cost, or behavior — only where evidence is incomplete.]

Plan:
1. [Phase or step] — action, expected result, dependencies, verification.

Risks & Decisions:
- [Risk, mitigation, decision owner, or evidence needed to decide.]

Completion:
[Condition that marks the overall outcome finished.]
```

Use ordered phases or steps with dependencies and success conditions for each. Avoid false precision: state dates, owners, and estimates only when evidence supports them. Keep planning distinct from coordination — focus on future sequencing, not active status or handoffs.

## Error Paths

- Ask one concise clarifying question when different interpretations would materially change the plan.
- Otherwise, state a reasonable assumption and proceed.
- Do not invent repository structure, interfaces, owners, or deadlines.
- Mark work as blocked when an unresolved dependency prevents it from starting safely.
- Identify the prerequisite and condition required to unblock it.
- Avoid false precision: use relative sizing, ranges, or no estimate when evidence can't support an exact figure, and name the source of the uncertainty.
- Divide an overly broad plan into milestones.
- Make the first milestone concrete enough to begin.

## Verification

Before finalizing the plan, verify that:

- Every step contributes to the requested outcome.
- Dependencies are ordered correctly.
- Material assumptions, risks, and decisions are visible.
- Each phase or meaningful step has an observable success condition.
- Completion criteria match the user's requested result.
- Optional work is separated from required scope.
- The plan contains no unnecessary steps or false precision.
- Discussion drafts were not saved unless the user explicitly requested it.
- An approved plan is saved to `docs/YYYY-MM-DD-[topic]/PLAN.md` or the user-specified location.
