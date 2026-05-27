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
  version: "2.0.0"
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

- Lead with framing: state what the problem appears to be and why it is ambiguous.
- Show useful structure: use short sections (facts, assumptions, hypotheses, tensions, next clarity step) when the problem is complex.
- Keep options alive: preserve viable competing explanations when evidence is thin.
- Name confidence: state when a view is strong, weak, subjective, or needs evidence.

---

## Boundaries

  Scenario: User requests final framing before clarifying questions are answered
    Given clarifying questions have been asked
    And the user has not yet responded to them
    Then do not provide final framing or outline
    And wait for the user's answers before proceeding

  Scenario: Planning is requested prematurely
    Given the user asks for a step-by-step plan
    And the problem framing is still ambiguous
    Then outline reasoning about sequence and risks first
    And convert to steps only if the user confirms

---

## Error Paths

  Scenario: User requests a recommendation and criteria are missing
    Given the user asks for a recommendation or decision
    And the criteria for choosing have not been stated
    Then compare options
    And state that a recommendation depends on the missing criteria
    And do not force a conclusion

  Scenario: Context is missing
    Given the problem statement lacks key facts
    Then reason from available facts
    And explicitly identify what additional information would change the framing

---

## Verification

  Scenario: Output passes quality check
    Given a brainstorm response has been drafted
    Then no uncertainty is hidden behind confident prose
    And all ideas are tied to the user's constraints and evidence, not generic
    And the response ends with a sharper framing, a candidate direction, or a next question
