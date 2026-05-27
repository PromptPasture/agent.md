---
name: ask
description: Generate high-leverage questions and clarify missing context. Use for question-generation requests like "what should I ask", "right questions", "what are we missing", "clarify this", and ambiguous requests blocked by unknowns.
license: MIT
tags:
  - question-generation
  - clarification
  - questions
metadata:
  author: Oleg Shulyakov
  version: "1.0.3"
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
- **Use short lists when useful**: prefer three to seven prioritized questions for normal work.
- **Group only when needed**: use categories such as goal, scope, risk, data, owner, and acceptance criteria only if they improve scanability.
- **Mark blockers**: distinguish must-answer questions from nice-to-have questions.
- **Include assumptions sparingly**: list assumptions only when they affect the question set or proposed next step.

---

## Boundaries

- **Surface gaps**: identify unknown goals, constraints, stakeholders, acceptance criteria, data, ownership, risks, and decision criteria.
- **Stay question-first**: do not make decisions, produce implementation plans, or change files as the primary output.
- **Avoid questionnaires**: ask only the few questions likely to affect the next move unless the user explicitly requests a full discovery list.

---

## Error Paths

- **No clear domain**: ask one question about the intended context before generating a detailed set.
- **Too many unknowns**: provide a first-pass discovery set and name what would refine it.
- **User asks for action too**: answer the question-generation part first, then state what can proceed after the answers.

---

## Verification

- **Remove decorative questions**: delete questions whose answer would not change scope, approach, risk, or acceptance.
- **Check boundaries**: if the output is mainly a recommendation, plan, explanation, or classification, this skill is no longer the right mode.
- **Preserve uncertainty**: do not present assumptions as facts.
