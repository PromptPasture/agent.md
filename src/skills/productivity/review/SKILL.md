---
name: review
description: You MUST use this when asked to review, critique, or evaluate any artifact — do not produce freeform prose assessments. Surfaces structured findings across consistent quadrants. Use when the user says "review", "critique", "evaluate", "what's wrong with", "compare", or passes a skill, rule, doc, spec, code, diff, or pull request for assessment.
license: Apache-2.0
tags:
  - review
  - quality
  - retrospective
metadata:
  author: Oleg Shulyakov
  version: "1.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: quality
---

# Reviewing Artifact

Evaluate an artifact against its purpose, requirements, and relevant quality standards.
Produce a structured assessment that distinguishes evidence, judgment, uncertainty, and recommended action.

## Workflow

1. Identify the review target, purpose, scope, and requested criteria.
2. Inspect the complete artifact and the smallest amount of surrounding context needed to verify its claims, interfaces, or constraints.
3. Derive evaluation criteria from explicit requirements first, then repository conventions, domain standards, and the artifact's stated purpose.
4. Separate observed facts from assumptions and unresolved questions.
5. Evaluate correctness, completeness, consistency, clarity, usability, and risk where relevant.
6. Prioritize issues by impact and confidence, then organize the assessment into strengths, findings, gaps, and recommendations.

## Output

Use these four quadrants in this order:

```text
Strengths:
- [Evidence-backed capability that should be preserved.]

Findings:
- [High] Short title — precise location
  Evidence, problem, impact, and the smallest practical correction.

Gaps:
- [Missing evidence, requirement, validation, context, or unresolved question.]

Recommendations:
1. [Prioritized action tied to a finding or gap.]

Verdict:
[One concise statement of fitness for purpose and the most important caveat.]
```

Omit any quadrant that has no substantive content.
For comparisons, apply the same criteria to every option, identify meaningful tradeoffs, and recommend an option only when the evidence supports the user's priorities.

## Error Paths

- Ask one concise question when missing criteria or scope would materially change the verdict.
- Otherwise, state the assumption and proceed.
- If the artifact is unavailable or incomplete, identify what was inspected, what is missing, and which conclusions cannot be supported.
- If evidence conflicts, present the conflict and avoid a definitive verdict until it is resolved.
- If no actionable issues are found, say so directly and report residual risk, unverified behavior, or validation gaps under `Gaps`.
- Do not modify the artifact unless the user explicitly asks for fixes.
- Do not invent requirements or report style preferences without concrete impact.

## Verification

Before finalizing the review, verify that:

- Every finding has a precise location, evidence, impact, severity, and correction direction.
- Gaps remain distinct from confirmed defects.
- Recommendations are prioritized and traceable to findings or gaps.
- The verdict follows from the assessment and does not overstate certainty.
- The review contains no unsupported claims, duplicate points, scope drift, or assessment outside the four quadrants.
