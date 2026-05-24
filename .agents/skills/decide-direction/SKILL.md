---
name: decide-direction
description: Compare options and recommend a direction. Use for decision requests like "choose", "which option", "tradeoffs", "recommend", "should we", and option selection with criteria, risks, and reversibility.
license: MIT
tags:
  - decision
  - recommendation
  - tradeoffs
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
---

# decide-direction

Choose a direction by comparing viable options against explicit criteria.

## Scope

**Use this skill when the user wants a recommendation or choice among options.**

- **Trigger on selection**: use for decision requests like "choose", "which option", "tradeoffs", "recommend", "should we", and similar decision requests.
- **State criteria**: compare options against goals, constraints, risk, cost, speed, reversibility, maintenance, user impact, or user-provided criteria.
- **Recommend when supported**: choose one option when evidence is sufficient, and say when it is not.
- **Do not just classify**: grouping options is useful only as support for a decision.

---

## Workflow

**Make the decision criteria visible before the recommendation.**

1. Identify the decision, options, and constraints.
2. Define criteria, prioritizing user-provided criteria over inferred ones.
3. Remove non-viable options with brief reasons.
4. Compare viable options against the criteria.
5. Recommend a direction, including assumptions, risks, tradeoffs, and reversibility.
6. Name what evidence would change the decision.

---

## Output

**Give the user a clear recommendation they can accept, reject, or revise.**

- **Lead with the recommendation**: state the choice when the evidence supports one.
- **Show the basis**: include criteria and concise option comparison.
- **Name tradeoffs**: explain what the recommendation gives up.
- **State reversibility**: note whether the choice is easy to change later.
- **Handle ties honestly**: recommend a tie-breaker or next evidence step when options remain balanced.

---

## Error Paths

**When criteria or evidence are missing, make the uncertainty part of the decision.**

- **No criteria**: infer practical criteria and label them as assumptions.
- **No options**: define plausible options before comparing them.
- **Insufficient evidence**: provide a conditional recommendation and the smallest information needed to firm it up.

---

## Verification

**Check that the recommendation follows from the comparison.**

- **Criteria alignment**: the selected option should win on the criteria that matter most.
- **No hidden values**: surface subjective preferences and uncertain assumptions.
- **Risk visibility**: include meaningful risks, mitigations, and reversibility.
