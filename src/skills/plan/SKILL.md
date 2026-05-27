---
name: plan
description: Sequence work before execution. Use for planning requests like "break this down", "roadmap", "approach", "milestones", "how should we proceed", migration planning, rollout planning, and scoped next steps.
license: MIT
tags:
  - plan
  - roadmap
  - sequencing
metadata:
  author: Oleg Shulyakov
  version: "1.0.3"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: project-management
---

# plan

Turn a goal into a practical sequence of work.

---

## Workflow

1. Define the goal, scope, and success condition.
2. Identify constraints, assumptions, dependencies, and unknowns.
3. Break work into ordered phases or steps.
4. Add risks and mitigation where failure would be costly.
5. Define verification for each meaningful phase.
6. End with the next concrete action.

---

## Output

- **Lead with the approach**: state the overall strategy in one short paragraph.
- **Use phases for larger work**: include purpose, key tasks, dependencies, and validation.
- **Keep steps scoped**: each step should have a visible outcome.
- **Flag blockers**: name missing context that prevents a reliable plan.
- **Avoid fake precision**: do not invent owners, dates, or estimates without evidence.

---

## Boundaries

- **Sequence work**: identify phases, dependencies, assumptions, risks, verification, and immediate next actions.
- **Stay pre-execution**: do not manage live owners, blockers, or handoffs as the primary behavior.
- **Default conversationally**: create durable files only when the user asks or the work clearly needs durable task documentation.

---

## Error Paths

- **Unclear goal**: ask the one question that most affects scope, then provide a provisional outline if useful.
- **Many unknowns**: split discovery from execution and identify what must be learned first.
- **Execution already active**: switch the output toward status, blockers, and handoff only when the user asks to manage ongoing work.

---

## Verification

- **Trace dependencies**: verify that later steps do not require missing earlier outputs.
- **Define done**: include validation or acceptance checks for non-trivial work.
- **Keep it current**: revise the plan when new facts change scope, risk, or sequence.
