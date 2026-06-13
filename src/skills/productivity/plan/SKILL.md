---
name: plan
description: You MUST use this before starting any multi-step execution. Sequence work into ordered phases with dependencies and success conditions. Use for planning requests like "break this down", "roadmap", "approach", "milestones", "how should we proceed", migration planning, rollout planning, and scoped next steps.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.3.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: planning
  tags: [plan, roadmap, sequencing]
---

# Planning Steps

Turn a defined outcome into an ordered, executable path with dependencies, decision points, and success conditions.

## Workflow

1. Define the desired outcome, scope, constraints, and completion condition.
2. Inspect the available context before proposing work.
3. Separate confirmed facts from assumptions and unresolved questions.
4. Break simple work into an ordered checklist and complex work into phases or milestones.
5. Order work by dependency, risk, and feedback value.
6. Specify the action, expected result, dependencies, and verification for each meaningful step.
7. Identify blockers, decision points, rollback needs, and work that can proceed in parallel.
8. Remove unnecessary work and separate optional follow-ups from the required scope.
9. Present and revise the plan conversationally without saving discussion drafts.
10. Ask the user to explicitly approve the final plan.
11. After approval, save the plan to `docs/YYYY-MM-DD-[topic]/PLAN.md`. Save it earlier only when the user explicitly asks to save the plan.
12. Produce the plan without executing it unless the user also asks for implementation.

## Output

- **Lead with the approach**: summarize the intended path in one or two sentences.
- **Keep drafts conversational**: do not create or update a plan file while the user is discussing or revising the plan.
- **Require explicit approval**: do not infer approval from silence or a request to begin implementation.
- **Write the approved plan**: after explicit approval, save it to `docs/YYYY-MM-DD-[topic]/PLAN.md` unless the user specifies another location.
- **Honor direct save requests**: save before approval only when the user explicitly says "save plan" or makes an equivalent request.
- **State assumptions and scope**: include only assumptions that affect sequencing, cost, or behavior.
- **Use ordered phases or steps**: include dependencies and success conditions for each.
- **Name verification**: define how each meaningful result and the overall outcome will be checked.
- **Surface risks and decisions**: include mitigations, decision owners, or the evidence needed to decide.
- **End with completion criteria**: make it clear when the plan is finished.
- **Avoid false precision**: use dates, owners, and estimates only when evidence supports them.
- **Keep planning distinct from coordination**: focus on future sequencing rather than active status and handoffs.

## Error Paths

- Ask one concise clarifying question when different interpretations would materially change the plan.
- Otherwise, state a reasonable assumption and proceed.
- Do not invent repository structure, interfaces, owners, or deadlines.
- Mark work as blocked when an unresolved dependency prevents it from starting safely.
- Identify the prerequisite and condition required to unblock it.
- Use relative sizing, ranges, or no estimate when evidence cannot support precise effort or dates.
- State the source of estimation uncertainty.
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
- The plan contains no unnecessary steps or unsupported precision.
- Discussion drafts were not saved unless the user explicitly requested it.
- An approved plan is saved to `docs/YYYY-MM-DD-[topic]/PLAN.md` or the user-specified location.
