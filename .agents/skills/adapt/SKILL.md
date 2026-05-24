---
name: adapt
description: Detect evidence-driven change needs. Use when the user says "adapt based on this", "what should change after this?", "this keeps happening", "this failed, what should change?", "the workflow no longer fits", "the constraints changed", or asks what skill, rule, doc, eval, memory, or process should change.
license: MIT
tags:
  - adaptation
  - feedback
  - process
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
  references:
    - create-skill
    - create-rule
    - remember-context
    - write-prd
    - write-spec
    - write-tech-docs
    - build-tests
    - write-user-story
---

# adapt

## Workflow

**Detect what should change going forward because reality contradicted the current setup.**

1. Identify the adaptation signal: observed outcome, user feedback, failure, repeated friction, outdated assumption, or changed constraint.
2. Decide whether the signal is durable enough to justify adaptation, or only a one-off exception.
3. Identify the affected behavior or artifact: skill, rule, workflow, document, eval, memory convention, test, or process.
4. Check whether the symptom comes from a governing convention, template, or source-of-truth artifact; route the change there instead of patching only the local artifact.
5. State the smallest useful change that would prevent recurrence or fit the new constraint.
6. Route the actual update to the appropriate follow-up skill, workflow, or owner.
7. Define how the adaptation should be verified.

---

## Output

**Make the diagnosis actionable without doing the update by default.**

- **Signal:** State what happened or changed.
- **Interpretation:** Explain why it indicates a future behavior or artifact may need to change.
- **Target:** Name the affected artifact, behavior, or process when identifiable.
- **Change:** Describe the smallest useful adaptation.
- **Route:** Identify the appropriate follow-up skill, workflow, or owner for the actual update.
- **Verification:** State what should be true after the adaptation.

---

## Boundaries

**Adaptation is diagnosis and routing, not a generic rewrite workflow.**

- **Do not overfit:** Avoid changing durable behavior for a single ambiguous incident unless the user explicitly wants a one-off correction.
- **Do not rewrite by default:** Do not edit skills, rules, docs, evals, tests, or memory unless the user separately asks to proceed with that update.
- **Use evidence:** Base adaptation on observed outcomes, feedback, failures, repeated friction, outdated assumptions, or changed constraints.
- **Route precisely:** Skills belong with skill-authoring workflows, rules with rule-authoring workflows, docs with writing workflows, tests with testing workflows, and durable facts with memory workflows.
- **Prefer source of truth:** When the mismatch comes from a convention, template, or authoring guidance, adapt that governing artifact instead of only patching the artifact that exposed the problem.
- **Keep uncertainty visible:** If the target artifact or change is unclear, name the likely candidates and the evidence needed to choose.

---

## Non-Triggers

**Nearby requests often need another mode unless they ask what should change going forward.**

- **Direct editing:** "Update this doc" or "rewrite this skill" should perform the requested artifact update, not stop at adaptation diagnosis.
- **Memory only:** "Remember this decision" should preserve durable context rather than diagnose process change.
- **Root-cause only:** "Why did this fail?" should explain or investigate unless the user asks what should change afterward.
- **Decision only:** "Which option should we choose?" should compare options and recommend a direction.
- **Planning only:** "Break this down" should produce a plan when the desired change is already known.

---

## Verification

**A good adaptation recommendation changes future behavior without broadening the system unnecessarily.**

- **Evidence test:** The recommendation ties back to a concrete signal, not a vague desire to improve.
- **Durability test:** The change handles a repeated or likely future condition, not only the exact current wording.
- **Scope test:** The proposed change is the smallest artifact or behavior update that addresses the signal.
- **Routing test:** The actual update path is clear and does not create a hidden runtime dependency on another skill.
