---
name: classify
description: Organize material into meaningful groups. Use for classification requests like "categorize", "group", "cluster", "sort", "taxonomy", "organize these", and grouping by criteria, priority, dependency, similarity, or abstraction level.
license: Apache-2.0
tags:
  - classification
  - taxonomy
  - organization
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: data
---

# classify

Group material by explicit criteria while preserving edge cases.

---

## Workflow

1. Identify the items to classify and any user-provided criteria.
2. Define or infer the grouping criteria, marking inferred criteria as assumptions.
3. Create clear group labels with short definitions.
4. Place each item into one or more groups as appropriate.
5. Call out ambiguous, duplicate, out-of-scope, or unclassified items.

---

## Output

- **Lead with criteria**: state the grouping rule before or alongside the groups.
- **Use stable labels**: choose labels that describe the underlying reason items belong together.
- **Preserve source text**: keep item names recognizable unless normalization is requested.
- **Explain edge cases**: briefly note why ambiguous items are multi-fit or unresolved.
- **Offer refinements**: suggest a better lens only when the requested criteria produce weak groups.

---

## Boundaries

  Scenario: Classification criteria vary
    Given the user provides or implies a grouping lens
    Then group by similarity, difference, category, priority, dependency, abstraction level, user need, risk, ownership, or another stated lens

  Scenario: Items are ambiguous
    Given items are multi-fit, unclear, or unclassified
    Then keep the ambiguity visible
    And do not force false precision

  Scenario: Output drifts into decision making
    Given classification could inform a decision
    Then keep the primary output as labeled organization
    And do not decide by default

---

## Error Paths

  Scenario: No criteria are provided
    Given the user has not provided grouping criteria
    Then infer a practical lens
    And state it as an assumption

  Scenario: Item detail is insufficient
    Given the items lack enough detail for confident grouping
    Then group by observable wording
    And list what context would improve accuracy

  Scenario: Criteria conflict
    Given multiple grouping criteria conflict
    Then choose the primary criterion first
    And note secondary tags if useful

---

## Verification

  Scenario: Output passes quality check
    Given classification has been produced
    Then every group has a meaningful reason
    And every item is placed, multi-labeled, or explicitly unclassified
    And ambiguity remains visible
