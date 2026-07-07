---
name: adapt
description: Diagnoses mismatches in skills, rules, or workflows and applies the smallest necessary change. Use when the user says "adapt based on this", "what should change after this?", "this keeps happening", "this failed, what should change?", "the workflow no longer fits", "the constraints changed", or asks what skill, rule, doc, eval, memory, or process should change.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.6.1"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: adaptation
  tags: [adaptation, feedback, process]
---

# Adapting to Changes

Turn failures, friction, feedback, stale assumptions, and changed constraints into a surgical, verified change that prevents the mismatch from recurring.

## Workflow

### Goal

Resolve the mismatch with a surgical, verified change.

### Setup

1. Identify the signal, expected vs. observed behavior, impact, and evidence. Treat feedback as evidence to investigate, not proof of cause or remedy.
2. Inspect the artifact involved. Verify facts before relying on feedback.

### Loop

1. Determine the cause and narrowest target:
   - Artifact instruction wrong or incomplete → correct the artifact.
   - Artifact adequate but not followed → correct execution.
   - New durable context → update memory.
   - Recurrence needs a reproducible check → add or update an evaluation.
2. Apply the change, or diagnose without editing if the user asked what should change.
3. Verify: run a surgical check that confirms the fix. Review for contradictions, regressions, and scope creep. Preserve behavior unrelated to the mismatch.

### Exit

When the mismatch is resolved or no further change is justified by evidence.

### Report

Cause, changed artifacts, verification outcome, and any unresolved risk.

## Output

After applying the adaptation, report:

```text
Cause:
[Evidence-backed explanation of the mismatch.]

Changed:
- [Artifact and the surgical correction made.]

Verified:
- [Check performed and result.]

Residual risk:
- [Unresolved uncertainty or "None identified."]
```

Keep diagnosis proportional to the evidence. When no change is justified, state why and identify the additional evidence needed.

## Error Paths

- Ask one concise question when competing interpretations would change scope; otherwise state the assumption and proceed.
- If required evidence is unavailable, report what was inspected, make no unsupported change, and stop.
- If the needed change is outside available authority, escalate rather than applying it.

## Verification

Before completing the adaptation, verify that:

- The change addresses the observed cause rather than only its symptom.
- Every modified artifact is supported by evidence and necessary for consistency.
- The original mismatch is reproduced or represented by a meaningful check when practical.
- Existing valid behavior remains intact.
- Documentation, tests, evaluations, and metadata affected by the change are synchronized.
- The result contains no speculative policy, duplicate guidance, placeholders, contradictions, or unrelated improvements.
