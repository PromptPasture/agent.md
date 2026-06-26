---
name: review
description: Surfaces structured findings across consistent quadrants, not freeform prose assessments. Use when the user says "review", "critique", "evaluate", "what's wrong with", "compare", or passes a skill, rule, doc, spec, code, diff, or pull request for assessment.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.3.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: quality
  tags: [review, quality, retrospective]
---

# Reviewing Artifact

Evaluate an artifact against its purpose, requirements, and relevant quality standards.
Produce a structured assessment that distinguishes evidence, judgment, uncertainty, and recommended action.

## Workflow

### Goal

A four-quadrant assessment.

### Setup

1. Identify the target, purpose, scope, and criteria.
2. Inspect the artifact and minimum surrounding context. Derive criteria from explicit requirements first, then conventions and the artifact's stated purpose. Separate facts from assumptions.

### Loop

1. Evaluate against criteria: correctness, completeness, consistency, clarity, usability, and risk. Produce candidate findings.
2. Validate each finding against evidence:
   - Supported → keep, assign severity.
   - Unsupported → dismiss.
   - Impact overstated → downgrade.
   - Dismissal uncovers a new gap → add it and re-evaluate.

### Exit

When all remaining findings are evidence-backed and no new surface was identified.

### Report

Prioritize by impact and confidence. Organize into strengths, findings, gaps, and recommendations. State a verdict.

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
- If no issues are found, say so directly and report residual risk, unverified behavior, or validation gaps under `Gaps`.
- Do not modify the artifact unless the user explicitly asks for fixes.
- Do not invent requirements or report style preferences without concrete impact.

## Verification

Before finalizing the review, verify that:

- Every finding has a precise location, evidence, impact, severity, and correction direction.
- Gaps remain distinct from confirmed defects.
- Recommendations are prioritized and traceable to findings or gaps.
- The verdict follows from the assessment and does not overstate certainty.
- The review contains no unsupported claims, duplicate points, scope drift, or assessment outside the four quadrants.
