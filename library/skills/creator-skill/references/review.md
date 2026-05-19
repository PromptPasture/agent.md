# Skill Review Checklist

Use this reference when reviewing a created or revised skill folder. Treat the skill as executable guidance for another agent: review whether it will trigger at the right time, load the right amount of context, and produce reliable behavior.

## Trigger Description

Check whether the frontmatter `description` is a useful trigger signal.

- It should use imperative, intent-focused phrasing such as "Use when..." or "Use for..." rather than only describing internal mechanics.
- It should name the core user intents and strongest trigger contexts. Be proactive: explicitly list contexts where the skill applies even when the user doesn't name the domain directly (e.g. "even if they don't explicitly mention 'CSV' or 'analysis'").
- It should avoid broad keyword stuffing that would trigger on adjacent tasks the skill does not actually handle.
- It must stay under the **1024-character hard limit** enforced by the spec. Check the character count directly - don't rely on a subjective sense of conciseness. Detailed routing, exclusions, and examples belong in the body or references.
- Note that agents tend to reach for skills only when a task requires knowledge or capabilities beyond what they can handle alone. Simple one-step requests may not trigger a skill even with a well-matched description. Eval queries should reflect this: weight them toward tasks with specialized knowledge, unfamiliar APIs, or domain-specific workflows.
- If trigger evals exist, check for realistic should-trigger and should-not-trigger prompts. The most useful should-trigger cases are ones where the skill would help but the connection isn't obvious from the query alone. The most useful should-not-trigger cases are near-misses: prompts sharing keywords or concepts with the skill but actually needing something different. Vary phrasing, explicitness, detail level, and complexity.

## Scope And Coherence

Check whether the skill covers a coherent unit of work and adds genuine value.

- The core question: does this skill add what the agent *lacks* - project-specific conventions, domain-specific procedures, non-obvious edge cases, or particular tools and APIs? If the agent would reliably handle the task without it, the skill may not be adding value.
- Flag skills that combine unrelated jobs, because they become hard to trigger precisely and can load conflicting instructions.
- Flag skills that are so narrow they force several skills to activate for one normal user task.
- Prefer defaults over menus when the skill names tools, formats, or procedures. Alternatives should be escape hatches, not equal-choice catalogs.

## Instruction Quality

Check whether the body teaches a reusable procedure rather than a one-off answer.

- Instructions should describe how to approach a *class* of problems, not what to produce for a specific instance. A reusable method (e.g. "read the schema, join on the `_id` convention, aggregate as needed") generalizes; a specific answer (e.g. "join `orders` to `customers` on `customer_id`") does not.
- For steps where multiple approaches are valid, prefer explaining *why* over prescribing *how* - an agent that understands the purpose behind an instruction makes better context-dependent decisions. Be prescriptive only when operations are fragile, consistency matters, or a specific sequence must be followed.
- Watch for overcomprehensiveness: skills that try to cover every edge case can hurt more than they help. The agent may struggle to extract what's relevant and pursue unproductive paths triggered by instructions that don't apply to the current task. When in doubt, cut and let the agent use its own judgment.
- Workflows should be stepwise, ordered, and validation-aware when the task has dependencies or failure modes.
- Output templates should be provided when format consistency matters; agents pattern-match well against concrete structures. Short templates can live inline; longer or conditional ones belong in `assets/`.
- Gotchas should capture non-obvious mistakes an agent is likely to make: environment-specific facts that defy reasonable assumptions, naming inconsistencies, soft-delete conventions, misleading status endpoints. Not generic advice like "handle errors appropriately."
- Security-sensitive or destructive behavior must be explicit, expected by the user, and bounded by the skill description.

## Progressive Disclosure

Check whether context is spent deliberately.

- `SKILL.md` should contain the routing logic and shared rules needed on every run. The spec recommends keeping it under **500 lines and 5,000 tokens**.
- Deep details should live in `references/`, `assets/`, or `scripts/` only when they are actually used.
- References must be loaded by clear conditions, not vague "read everything" guidance. "Read `references/api-errors.md` if the API returns a non-200 status code" is useful; "see references/ for details" is not.
- Placeholder folders or unused resources are review issues when they make the skill harder to understand or maintain.

## Validation And Evals

Check whether the skill can be tested and improved systematically.

- Trigger-sensitive skills should have eval queries split into **should-trigger** and **should-not-trigger** sets. Aim for roughly 20 queries total (8-10 per side). See the Trigger Description section for what makes a strong query in each category.
- Because model behavior is nondeterministic, run each query multiple times (3 is a reasonable minimum) and compute a **trigger rate**. A should-trigger query passes at a rate >= 0.5; a should-not-trigger query passes at a rate < 0.5.
- To avoid overfitting, split the query set: use about 60% as a **train set** to identify failures and guide description changes, and hold out about 40% as a **validation set** to check whether changes generalize. Both sets should have a proportional mix of positive and negative cases. Keep the split fixed across iterations.
- When iterating on a description, fix the *category* a failing query represents; don't copy keywords from the failing prompt into the description. That's overfitting.
- Objective workflows should include validators, scripts, schemas, or acceptance checks where practical.
- For nondeterministic agent behavior, prefer repeated runs or trigger-rate style evaluation over a single pass.
- If performance isn't improving after several iterations, consider whether the queries are the problem: too easy, too hard, or poorly labeled.
