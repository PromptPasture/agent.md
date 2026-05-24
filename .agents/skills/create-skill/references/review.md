# Skill Review Checklist

Use this reference when reviewing a created or revised skill folder. Treat the skill as executable guidance for another agent: review whether it will trigger at the right time, load the right amount of context, and produce reliable behavior.

## Trigger Description

**The description should make the skill trigger for the right work and stay quiet for near misses.**

Check whether the frontmatter `description` is a useful trigger signal.

- **Intent phrasing**: use imperative, intent-focused language such as "Use when..." or "Use for..." rather than only describing internal mechanics.
- **Trigger contexts**: name the core user intents and strongest trigger contexts. Be proactive when the skill applies even if the user does not name the domain directly, such as when they omit an obvious domain keyword.
- **Near misses**: avoid broad keyword stuffing that would trigger on adjacent tasks the skill does not actually handle.
- **Hard limit**: stay under the **1024-character hard limit** enforced by the spec. Check the character count directly; detailed routing, exclusions, and examples belong in the body or references.
- **Skill value**: remember that agents tend to reach for skills only when a task requires knowledge or capabilities beyond what they can handle alone. Weight eval queries toward specialized knowledge, unfamiliar APIs, or domain-specific workflows.
- **Trigger evals**: check for realistic should-trigger and should-not-trigger prompts. Strong should-trigger cases are ones where the skill would help but the connection is not obvious; strong should-not-trigger cases are near misses. Vary phrasing, explicitness, detail level, and complexity.

## Coherence And Boundaries

**One skill should cover one coherent unit of work.**

Check whether the skill covers a coherent unit of work and adds genuine value.

- **Added value**: ask whether the skill adds what the agent *lacks*, such as project-specific conventions, domain procedures, non-obvious edge cases, or particular tools and APIs.
- **Mixed jobs**: flag skills that combine unrelated work, because they become hard to trigger precisely and can load conflicting instructions.
- **Over-narrow boundaries**: flag skills that are so narrow they force several skills to activate for one normal user task.
- **Body scope sections**: flag `## Scope` sections that describe activation criteria. Skill-call scope belongs in the frontmatter `description`; body sections should cover workflow, boundaries, routing, and output rules.
- **Defaults first**: prefer defaults over menus when the skill names tools, formats, or procedures. Alternatives should be escape hatches, not equal-choice catalogs.

## Instruction Quality

**The body should teach reusable judgment, not a one-off answer.**

Check whether the body teaches a reusable procedure rather than a one-off answer.

- **Generalizable method**: describe how to approach a *class* of problems, not what to produce for a specific instance.
- **Purpose over procedure**: where multiple approaches are valid, explain *why* over prescribing *how*. Be prescriptive when operations are fragile, consistency matters, or a specific sequence must be followed.
- **Right-sized detail**: watch for overcomprehensiveness. When in doubt, cut and let the agent use its own judgment.
- **Ordered workflow**: make workflows stepwise, ordered, and validation-aware when the task has dependencies or failure modes.
- **Templates**: provide output templates when format consistency matters. Short templates can live inline; longer or conditional ones belong in `assets/`.
- **Section boundaries**: require standalone `---` delimiters between `##` sections in `SKILL.md`, without changing YAML frontmatter delimiters or adding an extra delimiter before the `#` title.
- **Execution-first order**: the first body section should usually be `## Workflow`, `## Source Handling`, or `## Route the Work`, not `## Boundaries`. Boundary-first order needs a concrete safety or destructive-action reason.
- **Scan anchors**: require a bold principle sentence after each `##` section heading and bold labels for distinct rule bullets in prose skill docs, unless the section is a schema, command example, or literal output template.
- **Gotchas**: capture non-obvious mistakes an agent is likely to make, not generic advice like "handle errors appropriately."
- **Sensitive behavior**: make security-sensitive or destructive behavior explicit, expected by the user, and bounded by the skill description.

## Progressive Disclosure

**Spend context deliberately and only when it changes the run.**

Check whether context is spent deliberately.

- **Top-level focus**: `SKILL.md` should contain the routing logic and shared rules needed on every run. The spec recommends keeping it under **500 lines and 5,000 tokens**.
- **Resource purpose**: deep details should live in `references/`, `assets/`, or `scripts/` only when they are actually used.
- **Load conditions**: references must be loaded by clear conditions, not vague "read everything" guidance.
- **Metadata references**: verify `metadata.references` lists only local skills or rules used inside the workflow. Remove route-away, adjacent-skill, near-miss, exclusion, and boundary mentions.
- **Unused folders**: placeholder folders or unused resources are review issues when they make the skill harder to understand or maintain.

## Validation And Evals

**A good skill can be tested without pretending every judgment is objective.**

Check whether the skill can be tested and improved systematically.

- **Trigger sets**: split trigger-sensitive eval queries into **should-trigger** and **should-not-trigger** sets. Aim for roughly 20 queries total, with 8-10 per side.
- **Repeated runs**: run each query multiple times and compute a **trigger rate**. A should-trigger query passes at a rate >= 0.5; a should-not-trigger query passes at a rate < 0.5.
- **Train and validation**: use about 60% as a **train set** and hold out about 40% as a **validation set**. Both sets should have a proportional mix of positive and negative cases. Keep the split fixed across iterations.
- **Avoid overfitting**: fix the *category* a failing query represents; do not copy keywords from the failing prompt into the description.
- **Objective checks**: include validators, scripts, schemas, or acceptance checks where practical.
- **Nondeterminism**: prefer repeated runs or trigger-rate style evaluation over a single pass.
- **Stalled results**: if performance is not improving, consider whether the queries are too easy, too hard, or poorly labeled.
