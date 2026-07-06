---
name: to-skill
description: Draft, revise, and prune skills authoring rules and the Trigger, Structure, Steering, and Pruning checklist.
disable-model-invocation: true
license: MIT
metadata:
  author: Matt Pocock
  version: 1.1.0
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: authoring
  tags: [skills, authoring, meta]
---

# Write Skill

A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same _process_ every run, not producing the same output — is the root virtue every step below serves.
Use this checklist to draft a new skill under `src/skills/`, or to revise, prune, or split an existing one — the same four steps apply either way.

## Workflow

1. **Trigger** — decide how the skill is invoked and write its frontmatter accordingly.
   Done when `description` and `disable-model-invocation` match that decision, `name` matches the folder, and a quick trigger test confirms it fires (or stays silent) as intended.
2. **Structure** — sort the content: what is a step, what is in-file reference, and what belongs behind a pointer in `references/`, `scripts/`, or `assets/`.
   Done when `SKILL.md` holds only what every branch needs and every pushed-out file has a working pointer.
3. **Steering** — draft the steps, each ending on a checkable completion criterion, and reach for a leading word instead of restating a quality across several sentences.
   Done when every step has a clear done/not-done condition.
4. **Pruning** — hunt duplication, sediment, no-ops, and sprawl; if pruning reveals the skill is carrying more than one branch's worth of material, split it instead of trimming further.
   Done when every remaining line earns its place and no meaning is stated twice.
5. **Finalize** — fix any relative links the change affects, and bump `metadata.version` (semver) for a material edit to an existing skill.
   Done when the README table and every relative link match the current file layout.

## Trigger — Deciding and Writing Invocation

Two ways a skill is reached — pick one:

- **Model-invoked** — keep a `description` field. Fires autonomously and is reachable by other skills. Cost: **context load** (always in the agent's context). Use when the agent must reach it on its own, or another skill needs to invoke it.
- **User-invoked** — set `disable-model-invocation: true`. Reachable only by a human typing its name. Cost: **cognitive load** (the human must remember it exists). Use when the skill only ever fires by hand.

Splitting a skill always spends one of these loads (**granularity**) — only split when the independent reach is worth it. If user-invoked skills multiply past what's memorable, add a **router skill** that names the others.

### Writing the description

- **Model-invoked:** include both **what the skill does** and **when to use it** — concrete trigger phrases the user would actually say.
Front-load the leading word the skill should be invoked by. One trigger phrase per distinct branch; a synonym that just renames the same branch is duplication —
collapse it. Under 1024 characters. No `<` or `>`.
- **User-invoked:** strip triggers; the description becomes a one-line human-facing summary — what the skill is for, not when the agent should reach for it (it can't).

### Frontmatter mechanics

- `name`: kebab-case, matches the folder name exactly, verb-first (`<verb>[-<subject>]`).
- `description`: required; see above.
- `license`, `metadata` (`author`, `version`, `source`, `catalog`, `category`, `tags`): optional but, when present, use this repository's compact single-block format.
- No XML angle brackets (`<` `>`) anywhere in frontmatter. No platform-reserved names or prefixes.

### Verify it fires correctly

- **Should trigger:** run the phrases from the description's trigger list; confirm a model-invoked skill loads, or that a user-invoked one is easy to recall by name.
- **Should not trigger:** run adjacent but unrelated requests; confirm a model-invoked skill stays silent.
- **Under-triggering:** add concrete trigger phrases before adding more prose. Over-triggering: narrow the description or add an explicit negative trigger ("do NOT use for...").

## Structure — Information Hierarchy and File Layout

### File layout

A skill folder is a directory of:

|File/Folder|Required|Purpose|
|---|---|---|
|`SKILL.md`|Yes|Instructions and YAML frontmatter — the primary tier.|
|`references/`|No|Reference material loaded only when needed.|
|`scripts/`|No|Deterministic helpers, validators, converters.|
|`assets/`|No|Templates, examples, or other reusable output resources.|

`SKILL.md` must be named exactly that (no `SKILL.MD`, `skill.md`).

`README.md` inside a skill folder is optional. It may contain some guidence or other usefull information for a user.

### The information hierarchy

Content ranked by how immediately the agent needs it:

1. **In-skill step** — an ordered action in `SKILL.md`. Ends on a **completion criterion**.
2. **In-skill reference** — a definition, rule, or fact kept in `SKILL.md`, consulted on demand. A flat peer-set of rules is a fine arrangement at this rung, not a smell.
3. **Disclosed reference** — pushed out of `SKILL.md` into a bundled file (`references/`, `scripts/`, `assets/`) reached by a pointer, loaded only when that pointer fires.

### Branching and progressive disclosure

A **branch** is a distinct path through the skill — drafting a new skill vs revising an existing one, for instance. Push down what only some branches need; keep inline what every branch needs — that move is **progressive disclosure**.

A pointer's _wording_, not its target, decides how reliably the agent reaches the material.
If a must-have reference keeps getting missed, sharpen the pointer's wording first, and only pull the material back inline if that fails.

**Co-location:** keep a concept's definition, rules, and caveats under one heading rather than scattered, so reading one part brings its neighbors with it.

## Steering — Completion Criteria and Leading Words

### Completion criteria

Every step ends on a condition that tells the agent the work is done. Make it:

- **Checkable** — can the agent tell done from not-done? ("every modified model accounted for", not "produce a change list").
- **Exhaustive**, where it matters — a demanding criterion forces more **legwork** (the digging the agent does within the step).

A vague criterion invites **premature completion** — attention slips to _being done_, pulled forward by steps it can already see waiting next. Defend in order:

1. Sharpen the completion criterion first — cheap and local.
2. Only if it's irreducibly fuzzy _and_ the rush is actually observed, hide the later steps by splitting the sequence into two skills (or a user-invoked hand-off; an inline call leaves them in context and clears nothing).

### Leading words

A **leading word** is a compact concept already in the model's pretraining (_tracer bullet_, _fog of war_) that the agent thinks with while running the skill. Reach for one instead of restating a quality across several sentences ("fast, deterministic, low-overhead" → _tight_).

Watch the agent's reasoning traces for the word appearing back — that confirms it anchored. If it isn't changing behavior, it's too weak; use a stronger word (_thorough_ → _relentless_), not a different technique.

## Pruning — Keeping a Skill Lean

Check every remaining line against these failure modes; delete or fix what fails.

- **Duplication** — the same meaning in more than one place. Costs maintenance (change one place, must change the others) and inflates that meaning's prominence past its real rank. Keep each meaning in exactly one **single source of truth**.
- **Sediment** — stale layers that settle because adding feels safe and removing feels risky. Check every line for **relevance**: does it still bear on what the skill does, or has it drifted stale?
- **No-op** — an instruction the model already follows by default, so it costs load to say nothing. Test each sentence in isolation: delete it — does behavior change? If not, delete the sentence rather than trim it. Most prose that fails this test should go, not be reworded.
- **Sprawl** — the skill is simply too long, even with everything live and unique. The cure is the information hierarchy: push reference behind pointers, and split by branch or by sequence so each path carries only what it needs.

If pruning surfaces more than one branch's worth of material, or a sequence whose later steps keep tempting premature completion, that is the signal to split the skill rather than keep pruning it in place.

Bump `metadata.version` (semantic versioning) for any material change to an existing skill's behavior.
