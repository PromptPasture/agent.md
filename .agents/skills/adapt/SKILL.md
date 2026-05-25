---
name: adapt
description: Diagnose when skills, rules, workflows, docs, evals, or memory conventions are mismatched to current conditions — triggered by failures, friction, user feedback, outdated assumptions, or changed constraints — then name the smallest change needed and route to the skill or workflow that should update it. Use when the user says "adapt based on this", "what should change after this?", "this keeps happening", "this failed, what should change?", "the workflow no longer fits", "the constraints changed", or asks what skill, rule, doc, eval, memory, or process should change.
license: MIT
tags:
  - adaptation
  - feedback
  - process
metadata:
  author: Oleg Shulyakov
  version: "1.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
  references:
    - create-skill
    - create-rule
    - remember
---

# adapt

Diagnose when skills, rules, workflows, docs, evals, or memory conventions are mismatched to current conditions — from failures, friction, feedback, outdated assumptions, or changed constraints — then name the smallest change needed and route to the skill or workflow that should update it.

---

## Workflow

1. **Classify the signal.** Identify which type of mismatch was presented:
   - *Failure* — an action produced a wrong or broken result
   - *Friction* — a step is consistently slow, ambiguous, or skipped
   - *Feedback* — the user explicitly named something that didn't work
   - *Outdated assumption* — a prior decision no longer holds given current context
   - *Changed constraint* — external requirements shifted (scope, platform, team, policy)

2. **Test durability.** Skip adaptation if all three are true:
   - The signal occurred exactly once
   - No structural cause is identifiable
   - The user hasn't signaled recurrence ("this keeps happening", "again", "always")

   Otherwise, proceed.

3. **Identify the target artifact.** Match signal type to likely target:

   | Signal | Likely target |
   | --- | --- |
   | Failure | skill, eval, test |
   | Friction | rule, workflow, process |
   | Feedback | skill, doc, memory |
   | Outdated assumption | memory, doc, spec |
   | Changed constraint | rule, PRD, skill |

4. **Prefer the source of truth.** If the artifact inherits from a template, convention, or governing doc, route the change there — not only to the downstream artifact.

5. **Name the smallest change.** One behavioral delta. Not a rewrite.

6. **Route it.** Name the follow-up skill or owner. Do not apply the update unless separately asked.

7. **Define verification.** State what must be true after the adaptation succeeds.

---

## Output

- **Signal:** What happened or changed, and which type it is.
- **Interpretation:** Why it indicates a mismatch, not a one-off.
- **Target:** The artifact or behavior that should change.
- **Change:** The smallest useful adaptation — one behavioral delta.
- **Route:** The follow-up skill or workflow that should apply the update.
- **Verification:** What must be true after the change succeeds.

### Example

**Signal:** The `create-skill` output omits a Verification section on 3 consecutive runs. *(Friction)*
**Interpretation:** A recurring omission across runs points to a missing template step, not operator error.
**Target:** `create-skill` SKILL.md — the output template is missing a required `## Verification` heading.
**Change:** Add a `## Verification` heading with a placeholder to the skill output template.
**Route:** `skill-creator` to apply the update.
**Verification:** The next 3 `create-skill` runs each include a non-empty Verification section without prompting.

---

## Boundaries

- **Diagnose, don't rewrite.** Produce a diagnosis and routing recommendation only. Apply the update only when separately asked.
- **Don't self-target by invocation.** Invoking `adapt` does not make `adapt` the target. Only route changes to `adapt` when the adaptation workflow itself failed.
- **Keep uncertainty visible.** If the target artifact or routing is unclear, name the candidates and the evidence needed to choose.

---

## Verification

- [ ] The signal maps to a concrete observed event, not a vague quality concern
- [ ] The change would apply to future occurrences, not only this exact incident
- [ ] No smaller artifact change would address the same signal
- [ ] A follow-up skill or owner is named for the actual update
