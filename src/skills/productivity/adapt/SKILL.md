---
name: adapt
description: You MUST use this when a mismatch signal appears — triggered by failures, friction, user feedback, outdated assumptions, or changed constraints. Diagnose mismatches in skills, rules or workflows and route to the right skill or workflow to apply the smallest necessary change. Use when the user says "adapt based on this", "what should change after this?", "this keeps happening", "this failed, what should change?", "the workflow no longer fits", "the constraints changed", or asks what skill, rule, doc, eval, memory, or process should change.
license: Apache-2.0
tags:
  - adaptation
  - feedback
  - process
metadata:
  author: Oleg Shulyakov
  version: "1.5.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: adaptation
  references:
    - create-skill
    - create-rule
    - remember
---

# adapt

Turn failures, friction, feedback, stale assumptions, and changed constraints into the smallest verified change that prevents the mismatch from recurring.

## Workflow

1. Identify the mismatch signal, expected behavior, observed behavior, impact, and available evidence. Treat feedback as evidence to investigate, not proof of the cause or requested remedy.
2. Inspect the current skill, rule, workflow, documentation, evaluation, memory, or implementation involved. Verify repository facts before relying on feedback or prior context. When required evidence or a target artifact is unavailable, report what was inspected, make no unsupported change, and identify what is needed to continue.
3. Determine the cause:
   - Correct an artifact when its instruction, behavior, or assumption is wrong or incomplete.
   - Correct execution when the artifact is adequate but was not followed.
   - Update memory when the new information is durable context rather than enforceable behavior.
   - Add or update an evaluation when recurrence needs a reproducible check.
   - Escalate to the responsible owner when the required change is outside the available authority or evidence.
4. Choose the narrowest durable target. Prefer correcting an existing artifact over adding a new one. Touch multiple artifacts only when evidence shows each contributes to the mismatch or consistency requires the change.
5. Define the intended change and how it will resolve the mismatch without weakening valid behavior.
6. Apply the change automatically when the user explicitly asks to adapt, fix, update, or implement it. When the user asks only what should change, diagnose and recommend without editing. Ask one concise question before editing when competing interpretations would materially change behavior, privacy, authority, or scope; otherwise, state the assumption and proceed. Do not modify external systems, public artifacts, or protected policy without the required confirmation or authority.
7. Run the smallest meaningful verification that reproduces the original signal or checks the corrected behavior.
8. Review the result for contradictions, regressions, unnecessary scope, and unsupported changes. Preserve intentional behavior unrelated to the mismatch, and do not encode a one-off preference as durable policy unless the user makes it a lasting requirement. Iterate only when verification shows the mismatch remains.
9. Report the cause, changed artifacts, verification, and any unresolved risk.

## Output

After applying the adaptation, report:

```text
Cause:
[Evidence-backed explanation of the mismatch.]

Changed:
- [Artifact and smallest necessary correction.]

Verified:
- [Check performed and result.]

Residual risk:
- [Unresolved uncertainty or "None identified."]
```

Keep diagnosis proportional to the evidence. When no change is justified, state why and identify the additional evidence needed.

## Verification

Before completing the adaptation, verify that:

- The change addresses the observed cause rather than only its symptom.
- Every modified artifact is supported by evidence and necessary for consistency.
- The original mismatch is reproduced or represented by a meaningful check when practical.
- Existing valid behavior remains intact.
- Documentation, tests, evaluations, and metadata affected by the change are synchronized.
- The result contains no speculative policy, duplicate guidance, placeholders, contradictions, or unrelated improvements.
