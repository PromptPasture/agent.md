---
name: ask
description: You MUST use this when missing context or unknowns would cause guessing. Generate the set of high-leverage questions that would change the next action. Use for question-generation requests like "what should I ask", "right questions", "what are we missing", "clarify this", and ambiguous requests blocked by unknowns.
license: Apache-2.0
tags:
  - question-generation
  - clarification
  - questions
metadata:
  author: Oleg Shulyakov
  version: "1.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: collaboration
---

# ask

Identify the smallest set of questions whose answers would materially change the next action, decision, or result.

## Workflow

1. Define the immediate outcome and the next action that available context should support.
2. Inspect the provided context before asking for information already available or discoverable.
3. Separate confirmed facts, reasonable assumptions, material unknowns, and optional details.
4. For each unknown, identify which answer would change the approach, scope, priority, risk, or completion condition.
5. Remove questions that are redundant, premature, merely interesting, or safe to resolve with a stated assumption.
6. Order the remaining questions by decision impact, dependency, and urgency.
7. If no answer would materially change the next action, state the assumption and proceed without asking.
8. Ask the minimum number needed to proceed, including concise options when they make answering easier.

## Output

- **Lead with the questions**: do not bury them under analysis or background.
- **Ask one question at a time when blocked**: start with the answer that determines what should be asked or done next.
- **Use a short prioritized list for question-generation requests**: group questions only when categories improve clarity.
- **Make each question answerable**: ask for one decision or fact and provide mutually exclusive options when practical.
- **Distinguish required from optional**: label questions as required, helpful, or deferrable when presenting several.
- **Offer a default when appropriate**: state the reasonable assumption and its consequence so the user can accept or correct it quickly.

## Verification

Before finalizing the questions, verify that:

- Every question can change a decision, action, scope boundary, risk treatment, or success condition.
- The questions are ordered so earlier answers can eliminate later questions.
- Each question is concise, neutral, and answerable.
- Available context does not already contain the answer.
- Safe assumptions are stated instead of turned into unnecessary blockers.
- The set contains no duplicate, speculative, premature, or low-value questions.
