---
name: to-prd
description: Writes and revises product requirements documents with structured sections covering goals, scope, requirements, and success criteria.
disable-model-invocation: true
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "2.0.2"
  source: github.com/olegshulyakov/agent.md
  catalog: product
  category: requirements
  tags: [writer, product, requirements]
---

# To Product Requirements Document

Produce a complete, structured **Product Requirements Document (PRD)** for the described product, feature, or initiative.

## Workflow

1. **Frame the decision** — identify the product decision the PRD must support, its audience, and the expected delivery stage.
2. **Gather before asking** — inspect the prompt, attached artifacts, repository context, existing requirements, research, analytics, designs, and constraints. Done when every fact already available has been collected, not re-requested.
3. **Sort what you know** — separate confirmed facts, reasonable assumptions, material unknowns, and unresolved decisions.
4. **Resolve open questions** — when the problem, target users, goals, or scope boundaries remain materially undecided, invoke `brainstorm` to work through them with the user before drafting. For a low-risk gap, mark it `[assumed]` and proceed instead.
5. **Frame the problem** — establish the customer problem, affected users, current behavior, desired outcome, business value, and cost of inaction before describing a solution.
6. **Set boundaries** — establish measurable goals, scope, non-goals, constraints, dependencies, risks, and any assumptions or open questions still worth flagging.
7. **Write outcome-focused requirements** — pair each with an acceptance signal, and cover relevant failure, empty, permission, recovery, and edge conditions. Keep implementation detail out unless it is a fixed product constraint; route detailed architecture, interfaces, or data contracts to `write-spec`.
8. **Scale the document** — lean for a narrow feature, fuller for a cross-functional product or launch.
9. **Self-review** — check the draft against the Verification checklist before finalizing. If review surfaces a new material unknown, return to step 4 before finalizing.

## Output

Produce the PRD in Markdown. When writing to disk, use the requested path or `PRD.md` by default.

Use this as the default template. Remove optional sections that add no decision or delivery value, and preserve a user-provided template when it is stricter.

```markdown
---
status: "[DRAFT | IN_REVIEW | APPROVED]"
documentType: PRD
phase: "[discovery | delivery | maintenance]"
createdAt: "[YYYY-MM-DD]"
updatedAt: "[YYYY-MM-DD]"
author: "[Name]"
owner: "[Name or TBD]"
stakeholders:
  - "[Name, team, or TBD]"
tags:
  - "[tag]"
related:
  - "[Related document or URL]"
---

# PRD: [Product or Feature Name]

## Problem

[Describe the current user problem, evidence, affected users, intended outcome, business impact, and cost of inaction. Keep implementation details out.]

## Goals and Success Metrics

|Goal ID|Target Outcome|Baseline|Target|Measurement Method|
|---|---|---|---|---|
|G-1|[Outcome]|[Known value or TBD]|[Measurable target or TBD]|[Analytics, research, operational data, or proxy]|

## Target Users

|User / Persona|Context|Need or Job to Be Done|
|---|---|---|
|[Role or segment]|[Relevant situation and constraints]|[Desired progress or outcome]|

## Scope

### In Scope

- [Concrete capability or deliverable]

### Out of Scope

- [Explicit non-goal]

### Later [optional]

- [Deliberately deferred capability]

## Requirements

|Requirement ID|Product Behavior|Priority|Acceptance Signal|Related Goal|
|---|---|---|---|---|
|FR-1|[Observable, outcome-focused behavior]|[MUST / SHOULD / COULD]|[Testable pass/fail condition]|[G-1]|

## Non-Functional Requirements [optional]

|Requirement ID|Category|Target or Constraint|
|---|---|---|
|NFR-1|[Performance, security, accessibility, privacy, reliability, compliance, or operations]|[Quantifiable requirement]|

## Dependencies and Constraints [optional]

|Item|Type|Impact|Validation or Owner|
|---|---|---|---|
|[Dependency or constraint]|[Dependency / Constraint]|[Affected scope or requirement]|[Validation method, owner, or TBD]|

## Risks and Mitigations [optional]

|Risk ID|Risk|Impact|Mitigation|Status|
|---|---|---|---|---|
|R-1|[Potential adverse outcome]|[HIGH / MEDIUM / LOW]|[Prevention, contingency, or acceptance]|[OPEN / CLOSED]|

## Rollout and Measurement [optional]

|Stage|Audience or Scope|Entry / Exit Criteria|Measurement or Monitoring|
|---|---|---|---|
|[Pilot, beta, phased rollout, or general availability]|[Users, percentage, platform, or region]|[Observable gate]|[Metric, alert, feedback, or review]|

## Open Questions and Assumptions

|Item ID|Type|Question or Assumption|Evidence or Rationale|Resolution or Validation|Owner|
|---|---|---|---|---|---|
|Q-1|Question|[Unresolved decision that affects delivery or success]|[Why it matters]|[Evidence or decision needed]|[Name, team, or TBD]|
|A-1|Assumption|[Belief marked `[assumed]`]|[Current evidence or reason]|[How and when it will be tested]|[Name, team, or TBD]|
```

- Put document status, phase, dates, owner, stakeholders, tags, and related documents in YAML frontmatter when known.
- Always include Problem, Goals and Success Metrics, Target Users, Scope, Requirements, and Open Questions and Assumptions.
- Include optional sections only when they contain information that affects a product decision, delivery, verification, or launch.
- Use tables when they improve comparison or traceability, especially for metrics, requirements, risks, dependencies, and open questions.
- Use stable IDs such as `G-1`, `FR-1`, `NFR-1`, and `R-1` only when the document needs cross-references.
- Do not emit instructional placeholders or empty tables in a completed PRD. Populate them, mark genuinely expected unknown values as `TBD`, or remove the optional section.
- When revising an existing PRD, preserve valid content and decisions; restructure or rewrite only what is needed to resolve gaps.

## Writing Rules

- **Lead with the problem:** explain who is affected, what they cannot do today, why it matters, and why the work is timely.
- **Separate outcomes from solutions:** goals describe results; requirements describe observable product behavior; implementation belongs in a specification.
- **Make success measurable:** define a baseline, target, measurement method, and evaluation window when evidence supports them. Do not invent precision.
- **Bound the scope:** state concrete in-scope capabilities, explicit non-goals, and deliberately deferred work.
- **Make requirements testable:** use unambiguous language and observable pass/fail conditions. Avoid terms such as "fast," "easy," or "intuitive" without a measure.
- **Trace user value:** connect requirements to a user need, journey, goal, or risk when the relationship is not obvious.
- **Cover unhappy paths:** include errors, empty states, permissions, limits, recovery, and degraded behavior when relevant.
- **Mark uncertainty:** label inferred content with `[assumed]`; use `TBD` only for a genuinely expected value that is not yet known.
- **Keep evidence distinct:** do not present hypotheses, stakeholder opinions, or inferred metrics as validated research.
- **Keep the PRD concise:** link to research, designs, technical specs, trackers, and launch plans instead of duplicating their full contents.
- **Use plain Markdown:** use real headings rather than bold pseudo-headings, and avoid decorative formatting that does not improve comprehension.
- **Decompose broad requests:** when one PRD cannot represent a coherent product decision, split independent product areas or produce an umbrella PRD with clearly separated child initiatives.
- **Avoid fabricated metrics:** when a baseline, target, or measurement source is unknown, define the intended outcome and measurement method and leave the unresolved value as `TBD`.
- **Surface conflicts:** identify contradictory requirements and the decision needed instead of silently choosing.

## Verification

Before finalizing the PRD, verify that:

- The problem, target users, desired outcome, and business value are explicit.
- Goals have measurable success signals or clearly marked measurement gaps.
- In-scope work, non-goals, constraints, and dependencies are distinct.
- Every requirement is necessary, outcome-focused, unambiguous, and verifiable.
- Relevant edge cases and failure conditions are covered.
- Questions and assumptions are labeled distinctly, and evidence, risks, mitigations, and open decisions are not conflated.
- The document contains no placeholders beyond intentional `TBD` fields, unsupported claims, contradictory requirements, duplicated sections, or implementation detail without product significance.
- The PRD is concise enough to guide alignment and specific enough to support design, specification, planning, and acceptance.
