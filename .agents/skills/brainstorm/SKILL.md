---
name: brainstorm
description: Work through ambiguous problems before a firm output shape is warranted. Use for reasoning requests like "reason through", "think through", "brainstorm", "help me frame this", "let's work through this", and messy problem statements.
license: MIT
tags:
  - reason
  - framing
  - thinking
metadata:
  author: Oleg Shulyakov
  version: "1.0.6"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
---

# brainstorm

Clarify messy problems without forcing a premature answer.

---

## Workflow

1. **Identify the tension.** Map the central tension, ambiguity, or decision pressure.
2. **Ask clarifying questions.** Ask any necessary questions to resolve ambiguity. Wait for the user's response before moving to the next step.
3. **List facts and assumptions.** Explicitly mark what is known and what is assumed.
4. **Name hypotheses.** List plausible interpretations or competing views.
5. **Test each direction.** Evaluate against constraints, evidence, tradeoffs, and failure modes.
6. **End with framing.** Provide the clearest current framing and the next useful clarity step.

---

## Output

- **Lead with framing**: state what the problem appears to be and why it is ambiguous.
- **Show useful structure**: use short sections such as facts, assumptions, hypotheses, tensions, and next clarity step when the problem is complex.
- **Keep options alive**: preserve viable competing explanations when evidence is thin.
- **Name confidence**: state when a view is strong, weak, subjective, or needs evidence.

---

## Boundaries

- **Frame the problem**: clarify terms, goals, constraints, assumptions, competing interpretations, hypotheses, and possible directions.
- **Enforce the loop**: Do not provide the final framing or outline until the user has answered the clarifying questions. You may ask multiple questions in a single message if needed.
- **Keep uncertainty visible**: separate facts, assumptions, opinions, and open questions.
- **Avoid premature closure**: do not force a recommendation, step-by-step plan, or implementation unless the user asks for that next.

---

## Error Paths

- **Missing context**: reason from available facts and identify what would change the framing.
- **Decision requested**: compare options and state that a recommendation depends on criteria when criteria are missing.
- **Planning requested**: outline reasoning about sequence and risks before turning it into steps only if asked.

---

## Verification

- **No false certainty**: do not hide uncertainty behind confident prose.
- **No generic brainstorming**: tie ideas to the user's constraints and evidence.
- **Clear exit**: end with a sharper framing, candidate direction, or next question.
