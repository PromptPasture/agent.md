---
title: How to Write Great Skills
author: Matt Pocock
source: https://www.youtube.com/watch?v=UNzCG3lw6O0
---

# How to Write Great Skills

> Lecture notes distilled from a recorded talk originally intended for the AI Engineer World's Fair. The speaker maintains a popular engineering skills repo (referred to in the transcript as "Matt PCO skills") and the `writing-great-skills` skill that operationalizes this checklist.

## The Problem: "Skill Hell"

Developers have moved through several eras of "hell":

- **Tutorial hell** — endless tutorials that never combine into real understanding.
- **Framework hell** — constant churn chasing the newest JavaScript framework.
- **Skill hell** — the current era. Skills are freely available, forkable, and shareable, but there's no shared rubric for telling a good skill from a bad one. Individuals and organizations alike end up piling on skills without knowing which parts are pulling their weight.

The missing piece isn't more skills — it's a **framework for evaluating and improving the skills you already have.**

## The Skill Checklist

Four areas to evaluate any skill against, roughly in the order you'd design a new one:

1. **Trigger** — how the skill gets invoked.
2. **Structure** — how the skill is internally composed.
3. **Steering** — how you get the agent to actually follow the skill.
4. **Pruning** — how you cut a working skill down to its smallest useful form.

---

## 1. Trigger — User-Invoked vs. Model-Invoked

Every skill can be **user invoked**: it sits on the file system, and the human tells the agent to use it (not always literally `/slash-command` — depends on the harness).

Some skills are also **model invoked**: the skill's `description` lives permanently in the agent's context as a *context pointer*. The agent reads the description, decides the skill is relevant, and pulls the full `SKILL.md` into context on its own.

- A model-invocable skill has a description the agent can see and act on unprompted.
- Setting `disable model invocation: true` makes a skill **user-invoked only** — its description is hidden from the agent and shown only to the user.

**Tip 1: Decide, deliberately, whether each skill is user-invoked or model-invoked.**

This isn't a free win either way — both options carry a real cost:

|Approach|Cost|
|---|---|
|Model-invoked|Adds **context load**: every model-invoked skill adds a description to every request, and one more thing for the agent to weigh. 100 model-invoked skills = 100 descriptions sitting in context.|
|User-invoked|Adds **cognitive load**: the user has to remember which skill to invoke and when. More user-invoked skills = more the "pilot" has to keep in their head.|

There's also an **unpredictability cost** specific to model invocation: a context pointer can simply be ignored by the model, even when it's the perfect skill for the task. That unpredictability is what pushes people toward building evals just to confirm skills fire when expected.

This is the core philosophical difference between the speaker's skills repo (mostly user-invoked — full control, more cognitive load on the user) and "superpowers" (mostly model-invoked — more flexible, more context load, less predictable).

---

## 2. Structure — Composing the Skill Internally

Think of a skill as built from two units:

- **Steps** — the step-by-step procedure the skill walks through.
- **Reference** — supporting material the steps need to execute correctly.

A skill can be all steps, all reference, or (usually) a mix. Example: a "write a PRD" skill with three steps (find relevant context → confirm test seams with the user → write the PRD) paired with two reference docs (what a test seam is, and a PRD template).

**Tip 3: Keep the main `SKILL.md` as small as possible.**

Smaller skills are easier to maintain, easier to audit, and cheaper — every word removed is a token removed, multiplied across every future invocation.

**Technique: hide branch-specific reference behind context pointers.**

If a skill has only one path through it (like the PRD example above), all its reference material belongs directly in `SKILL.md` — it's needed every time.

If a skill has multiple branches — e.g., a "domain modeling" skill that can either update a glossary (`context.md`) *or* create an architectural decision record, or do neither — then each branch's reference material (the ADR template, the glossary template) should live in **separate files**, referenced from `SKILL.md` via a pointer ("if you need the template, go to this file"). This is an **external reference**: bundled with the skill, but only pulled into context when that branch is actually taken.

Summary for structure:

- Split skills into **steps** + **reference**.
- Keep `SKILL.md` minimal.
- Push branch-specific reference material out behind context pointers.

---

## 3. Steering — Getting the Agent to Actually Do What You Want

The central failure mode: *"I specified this in the skill, I was clear, and the agent still didn't do it."*

### Leading words

The main technique here is **leading words** — words or short phrases that pack a large amount of meaning into a small footprint. Put a leading word in the skill's text; the agent will echo that word back in its own reasoning and output, and that repetition drives its behavior.

**Example:** agents tend to code layer-by-layer (all of the DB layer, then all the schema, then all the API, then all the frontend) rather than seeking feedback early. Simply saying "don't code layer by layer, start small" is weak. Instead, introduce the leading word/phrase **"vertical slice"** — an already well-understood term in software development — and repeat it through the skill. It triggers the model's prior knowledge far more effectively than a generic instruction.

You can verify a leading word is working by watching for it in the reasoning traces (e.g., "we're going to do this as a thin vertical slice"). If the agent still isn't behaving, the fix is usually to make leading words **more consistent and more precise**, or find better candidates — English gives you a very wide surface area to experiment with.

### Leg work

Sometimes the agent under-invests effort on a given step because it can already see the *next* step and rushes toward it.

**Classic case: "plan mode."** When "ask clarifying questions" and "create a plan" are both visible as part of the same flow, the agent does the bare minimum of clarifying questions before eagerly jumping to the plan.

**Fix:** split the flow into genuinely separate skills, so the agent can only see the step it's currently on. E.g., a "grill with docs" skill (clarifying questions only) runs to completion as its own skill, with no visibility into the follow-on "write PRD" skill. Hiding future steps from the agent increases the leg work it puts into the current one. Not needed for every skill — but there's no substitute for it when you specifically need more depth on a given step.

---

## 4. Pruning — Cutting the Skill Down

Oversized skills are usually a **symptom**, not a root cause. Three concrete failure modes to check for:

1. **Duplication (violating DRY).** Every piece of reference material (a template, a definition) should have a **single source of truth**. Don't repeat the same guidance across multiple steps or reference docs.

2. **Sediment.** Happens naturally when multiple people contribute to a shared skill file: everyone adds their own bit, nobody feels safe deleting or editing someone else's. The result is accumulated, often-irrelevant material. Fix by revisiting **structure** first — move branch-specific content into the right branch, or delete it if it's irrelevant or stale.

3. **No-ops.** Instructions that look like they influence behavior but don't. Test with the **deletion test**: remove a paragraph (e.g., "write a long, detailed commit message") and check whether the agent's behavior actually changes. If it wouldn't have written a good commit message anyway, the paragraph is a no-op — delete it.

The speaker's approach to keeping skills small in practice: run the deletion test, compress instructions into leading words, and continuously check for sediment and no-ops.

---

## Full Checklist Recap

1. **Trigger** — Is this skill user-invoked, model-invoked, or both? Weigh context load (model-invoked) against cognitive load (user-invoked).
2. **Structure** — Split into steps + reference. Keep `SKILL.md` small. Push branch-specific reference behind context pointers.
3. **Steering** — Use leading words consistently and verify them in reasoning traces. Hide future steps to force more leg work on the current one.
4. **Pruning** — Check for duplication, sediment, and no-ops. Run the deletion test on anything you suspect isn't earning its keep.

## Resources Mentioned

- `writing-great-skills` skill — encodes this entire checklist; can be run over your own skills or community-authored ones to audit quality.
- aihero.dev — speaker's newsletter; an "AI coding crash course" was announced as an upcoming resource.
