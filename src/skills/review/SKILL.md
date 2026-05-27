---
name: review
description: Review any artifact and output results in a Retrospective board format — what is well, what is bad, what should be improved, what to change. Use when the user says "review", "critique", "evaluate", "what's wrong with", "compare", or passes a skill, rule, doc, spec, code, diff, or pull request for assessment. Works on a single artifact, an artifact against a reference, a diff or PR, or two artifacts side by side.
license: MIT
tags:
  - review
  - quality
  - retrospective
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
---

# review

Evaluate any artifact and surface findings as a Retrospective board.

---

## Input Shapes

| Shape | Description | Example |
| --- | --- | --- |
| Single artifact | Standalone review, no reference | `review this SKILL.md` |
| Artifact + reference | Artifact is judged against a ground truth | `review this against the spec` |
| Diff / PR | Before state is ground truth; changes are under review | `review this pull request` |
| A vs B | Symmetric comparison, neither is authoritative | `compare these two implementations` |

---

## Workflow

1. **Identify input shape.** Determine which of the four shapes applies from what was provided.
2. **Triage.** Decide whether a full review is warranted before proceeding.
3. **Identify artifact type.** Match against the known type registry or fall back to autonomous derivation.
4. **Derive criteria.** Apply typed criteria for known types; derive autonomously for unknown types.
5. **Populate quadrants.** Fill each quadrant according to its definition.
6. **Output the board.**

---

## Triage

Before running a full review, assess whether it is warranted:

- Is the artifact non-empty and in a reviewable state?
- For diffs: is the change substantive, or a mass rename, whitespace pass, or trivial one-liner?
- For A vs B: are both artifacts present and comparable?

If triage fails, output a short explanation and stop. Do not produce quadrants.

---

## Artifact Type Registry

| Type | Key criteria |
| --- | --- |
| `skill` | Frontmatter completeness, description triggering quality, Gherkin correctness, boundary coverage, workflow clarity |
| `rule` | Scope, one concern per file, concrete imperatives, conflict with existing rules |
| `doc / spec` | Clarity, completeness, no stale assumptions |
| `code` | Correctness, readability, edge case handling |
| `diff / PR` | Change correctness, regression risk, scope creep, missing tests |
| `unknown` | Derive criteria autonomously from artifact structure and content |

For **artifact + reference** and **A vs B** shapes, criteria are derived from the comparison axis regardless of type: conformance, gaps, regressions, and structural drift.

---

## Quadrants

Output exactly these four quadrants by default. Caller may override labels or count.

| Quadrant | Definition |
| --- | --- |
| **What is well** | What holds up and should be kept as-is |
| **What is bad** | What is wrong, missing, or harmful and should stop |
| **What should be improved** | What exists but needs tuning — same direction, better execution |
| **What to change** | What needs replacement or restructuring — different direction |

The distinction between *improve* and *change*: improve means adjust degree; change means alter kind.

For **A vs B**, quadrants shift to: what A does better, what B does better, what both get wrong, what the stronger candidate should adopt from the weaker.

---

## Boundaries

  Scenario: Artifact is empty or not yet in a reviewable state
    Given the artifact has no substantive content
    Then fail triage
    And explain what is missing before a review can proceed
    And stop

  Scenario: Diff is non-substantive
    Given the diff contains only whitespace, renames, or trivial changes
    Then fail triage
    And state that no meaningful review is possible for this change
    And stop

  Scenario: Caller overrides quadrant labels or count
    Given the caller specifies custom quadrant names or a different number of quadrants
    Then use the caller-specified quadrants
    And preserve their definitions as stated

---

## Error Paths

  Scenario: Artifact type is unrecognized
    Given the artifact does not match any entry in the type registry
    Then derive criteria autonomously from artifact structure and content
    And note in the output that autonomous derivation was used

  Scenario: Reference is missing for artifact + reference shape
    Given the caller implies a reference exists
    And no reference was provided
    Then ask for the reference before proceeding
    And do not fall back to single artifact review silently

  Scenario: A vs B artifacts are not comparable
    Given the two artifacts are of incompatible types or purposes
    Then state why comparison is not meaningful
    And offer to review each independently instead

---

## Verification

  Scenario: Output passes quality check
    Given a review has been produced
    Then every finding is tied to a specific artifact element, not a vague impression
    And improve findings are distinct from change findings — degree vs kind
    And the output is actionable: each quadrant entry implies a next step
    And triage was completed before quadrants were populated
