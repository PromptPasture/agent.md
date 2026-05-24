---
name: reason-problem
description: Work through ambiguous problems before a firm output shape is warranted. Use for reasoning requests like "reason through", "think through", "brainstorm", "help me frame this", "let's work through this", and messy problem statements.
license: MIT
tags:
  - reason
  - framing
  - thinking
metadata:
  author: Oleg Shulyakov
  version: "1.0.1"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
---

# reason-problem

Clarify messy problems without forcing a premature answer.

## Workflow

**Move from confusion to a sharper framing.**

1. Identify the central tension, ambiguity, or decision pressure.
2. List known facts and explicitly mark assumptions.
3. Name plausible interpretations or hypotheses.
4. Test each direction against constraints, evidence, tradeoffs, and failure modes.
5. End with the clearest current framing and the next useful clarity step.

---

## Output

**Make the thinking trace useful without dumping private scratchwork.**

- **Lead with framing**: state what the problem appears to be and why it is ambiguous.
- **Show useful structure**: use short sections such as facts, assumptions, hypotheses, tensions, and next clarity step when the problem is complex.
- **Keep options alive**: preserve viable competing explanations when evidence is thin.
- **Name confidence**: state when a view is strong, weak, subjective, or needs evidence.

---

## Boundaries

**Use structured thinking without forcing a premature artifact.**

- **Frame the problem**: clarify terms, goals, constraints, assumptions, competing interpretations, hypotheses, and possible directions.
- **Keep uncertainty visible**: separate facts, assumptions, opinions, and open questions.
- **Avoid premature closure**: do not force a recommendation, step-by-step plan, or implementation unless the user asks for that next.

---

## Error Paths

**When the user needs a different artifact, say so and produce the closest useful reasoning.**

- **Missing context**: reason from available facts and identify what would change the framing.
- **Decision requested**: compare options and state that a recommendation depends on criteria when criteria are missing.
- **Planning requested**: outline reasoning about sequence and risks before turning it into steps only if asked.

---

## Verification

**Check that the answer improves clarity instead of sounding clever.**

- **No false certainty**: do not hide uncertainty behind confident prose.
- **No generic brainstorming**: tie ideas to the user's constraints and evidence.
- **Clear exit**: end with a sharper framing, candidate direction, or next question.
