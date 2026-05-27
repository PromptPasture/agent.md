---
name: choose
description: Compare options and recommend a direction. Use for decision requests like "choose", "which option", "tradeoffs", "recommend", "should we", and option selection with criteria, risks, and reversibility.
license: MIT
tags:
  - decision
  - recommendation
  - tradeoffs
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: project-management
---

# choose

Choose a direction by comparing viable options against explicit criteria.

---

## Workflow

1. Identify the decision, options, and constraints.
2. Define criteria, prioritizing user-provided criteria over inferred ones.
3. Remove non-viable options with brief reasons.
4. Compare viable options against the criteria.
5. Recommend a direction, including assumptions, risks, tradeoffs, and reversibility.
6. Name what evidence would change the decision.

---

## Output

- **Lead with the recommendation**: state the choice when the evidence supports one.
- **Show the basis**: include criteria and concise option comparison.
- **Name tradeoffs**: explain what the recommendation gives up.
- **State reversibility**: note whether the choice is easy to change later.
- **Handle ties honestly**: recommend a tie-breaker or next evidence step when options remain balanced.

---

## Boundaries

  Scenario: Criteria are needed for comparison
    Given options are being compared
    Then compare them against goals, constraints, risk, cost, speed, reversibility, maintenance, user impact, or user-provided criteria

  Scenario: Evidence supports a recommendation
    Given evidence is sufficient to prefer one option
    Then choose one option
    And state when the evidence is not sufficient

  Scenario: Output drifts into classification
    Given grouping options is useful
    Then use grouping only as support for a decision
    And keep the primary output focused on choosing

---

## Error Paths

  Scenario: No criteria are provided
    Given the user has not provided decision criteria
    Then infer practical criteria
    And label them as assumptions

  Scenario: No options are provided
    Given the user has not provided options
    Then define plausible options before comparing them

  Scenario: Evidence is insufficient
    Given the available evidence cannot support a firm recommendation
    Then provide a conditional recommendation
    And name the smallest information needed to firm it up

---

## Verification

  Scenario: Output passes quality check
    Given a recommendation has been produced
    Then the selected option wins on the criteria that matter most
    And subjective preferences and uncertain assumptions are surfaced
    And meaningful risks, mitigations, and reversibility are included
