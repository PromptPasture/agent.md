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
  version: "1.1.0"
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

  Scenario: Work needs sequencing
    Given the user asks how to proceed
    Then identify phases, dependencies, assumptions, risks, verification, and immediate next actions

  Scenario: Execution is already active
    Given the primary need is managing live owners, blockers, or handoffs
    Then do not treat planning as the primary behavior
    And route the output toward coordination only when the user asks to manage ongoing work

  Scenario: Durable documentation is optional
    Given the user has not requested durable files
    Then default to a conversational plan
    And create durable files only when the work clearly needs durable task documentation

---

## Error Paths

  Scenario: Goal is unclear
    Given the goal is not clear enough to plan reliably
    Then ask the one question that most affects scope
    And provide a provisional outline if useful

  Scenario: Many unknowns exist
    Given too many unknowns prevent reliable sequencing
    Then split discovery from execution
    And identify what must be learned first

  Scenario: Execution is already active
    Given the user asks about ongoing work
    Then switch the output toward status, blockers, and handoff only when the user asks to manage that work

---

## Verification

  Scenario: Output passes quality check
    Given a plan has been produced
    Then later steps do not require missing earlier outputs
    And validation or acceptance checks are included for non-trivial work
    And the plan is revised when new facts change scope, risk, or sequence
