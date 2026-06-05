---
name: ask
description: Generate high-leverage questions and clarify missing context. Use for question-generation requests like "what should I ask", "right questions", "what are we missing", "clarify this", and ambiguous requests blocked by unknowns.
license: Apache-2.0
tags:
  - question-generation
  - clarification
  - questions
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: collaboration
---

# ask

Generate the smallest useful set of questions that would change the next action.

---

## Workflow

1. Restate the blocked decision or task in one sentence when helpful.
2. Separate known facts from assumptions and missing context.
3. Select the fewest questions that would materially change the next action.
4. Order questions by leverage, dependency, or urgency.
5. Add default assumptions only when they let work proceed despite unanswered questions.

---

## Output

- **Lead with the core gap**: name the uncertainty that makes the questions necessary.
- **Group only when needed**: group questions into categories such as goal, scope, risk, data, owner, acceptance criteria only if they improve scannability.
- **Use short lists when useful**: prefer three to seven prioritized questions for normal work across all categories.
- **Mark blockers**: distinguish must-answer questions from nice-to-have questions.
- **Include assumptions sparingly**: list assumptions only when they affect the question set or proposed next step.

---

## Boundaries

  Scenario: Resolving unknowns
    Given there are missing facts, constraints, stakeholders, acceptance criteria, data, ownership, risks, or decision criteria
    Then explicitly surface these gaps as questions

  Scenario: Output crosses into action or planning
    Given the generated output is mainly a recommendation, plan, explanation, or classification
    Then flag that ask is no longer the right mode
    And adjust the output to remain question-first
    And avoid making decisions or producing implementation plans

  Scenario: Full questionnaire was not requested
    Given the user has not explicitly requested a full discovery list
    Then ask only the few questions likely to affect the next move
    And do not generate a long, exhaustive questionnaire

---

## Error Paths

  Scenario: Domain is entirely unclear
    Given there is no clear domain or context for the task
    Then ask exactly one question about the intended context
    And do not generate a detailed set of questions until answered

  Scenario: Too many unknowns exist to prioritize
    Given the problem has too many unknowns to ask a concise list
    Then provide a first-pass discovery set
    And name what constraints would help refine it

  Scenario: User asks for action alongside questions
    Given the user requests both questions and an action
    Then answer the question-generation part first
    And state what action can proceed after the answers are provided

---

## Verification

  Scenario: Output passes quality check
    Given the question set is generated
    Then no decorative questions remain (questions whose answer would not change scope, approach, risk, or acceptance)
    And assumptions are not presented as facts
    And boundaries are respected (no implicit planning or decision making)
