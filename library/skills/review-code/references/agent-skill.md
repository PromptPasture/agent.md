# Skill Review Checklist

Use this reference when reviewing a created or revised skill folder. Treat the skill as executable guidance for another agent: review whether it will trigger at the right time, load the right amount of context, and produce reliable behavior.

## Trigger Description

Check whether the frontmatter `description` is a useful trigger signal.

- It should use imperative, intent-focused phrasing such as "Use when..." or "Use for..." rather than only describing internal mechanics.
- It should name the core user intents and strongest trigger contexts, including less explicit prompts where the skill should still apply.
- It should avoid broad keyword stuffing that would trigger on adjacent tasks the skill does not actually handle.
- It should stay concise and under the runtime limit, with detailed routing, exclusions, and examples in the body or references.
- If trigger evals exist, check for realistic should-trigger and should-not-trigger prompts, including near misses, varied phrasing, concrete paths or artifacts, and enough coverage to expose false positives and false negatives.

## Scope And Coherence

Check whether the skill is one coherent workflow.

- Flag skills that combine unrelated jobs, because they become hard to trigger precisely and can load conflicting instructions.
- Flag skills that are so narrow they force several skills to activate for one normal user task.
- Confirm the skill adds domain-specific or project-specific value the base agent would not reliably infer.
- Prefer defaults over menus when the skill names tools, formats, or procedures. Alternatives should be escape hatches, not equal-choice catalogs.

## Instruction Quality

Check whether the body teaches a reusable procedure rather than a one-off answer.

- Instructions should be concrete enough for fragile steps and flexible enough where multiple approaches are valid.
- Workflows should be stepwise, ordered, and validation-aware when the task has dependencies or failure modes.
- Output templates should be provided when format consistency matters.
- Gotchas should capture non-obvious mistakes an agent is likely to make, not generic advice like "handle errors appropriately."
- Security-sensitive or destructive behavior must be explicit, expected by the user, and bounded by the skill description.

## Progressive Disclosure

Check whether context is spent deliberately.

- `SKILL.md` should contain the routing logic and shared rules needed on every run.
- Deep details should live in `references/`, `assets/`, or `scripts/` only when they are actually used.
- References should be loaded by clear conditions, not by vague "read everything" guidance.
- Placeholder folders or unused resources are review issues when they make the skill harder to understand or maintain.

## Validation And Evals

Check whether the skill can be tested or improved.

- Trigger-sensitive skills should have eval prompts or clear instructions for creating them, split between positive cases and near-miss negative cases.
- Objective workflows should include validators, scripts, schemas, or acceptance checks where practical.
- For nondeterministic agent behavior, prefer repeated runs or trigger-rate style evaluation over a single pass.
- Watch for overfitting: description changes should generalize from failure categories, not copy exact words from failed eval prompts.
