# Skill Review Checklist

Use this reference when reviewing a created or revised skill folder. Treat the skill as executable guidance for another agent: it should trigger at the right time, load the right amount of context, and produce reliable behavior.

## Start With The Contract

Before listing findings, identify what the skill is promising.

A good review starts from four questions:

1. **When should this skill activate?** Read the frontmatter `description` as the trigger contract.
2. **What work does it perform?** Read the workflow, output, and boundaries as the behavior contract.
3. **What extra context does it load?** Check references, scripts, assets, and evals.
4. **How would we know it worked?** Check validation, evals, and expected output shape.

If those four answers do not line up, that is usually the core review finding.

---

## Trigger Description

The `description` is the main activation signal. It should describe the user intent, not the skill's internal mechanics.

Good trigger descriptions usually say "Use when..." or "Use for..." and name the strongest contexts where the skill should help. They include representative user phrases only when those phrases improve routing. They avoid keyword stuffing because broad keywords create false positives on adjacent work.

### What to check

- **Intent phrasing:** Does the description name the task the agent should perform?
- **Trigger contexts:** Does it cover the real situations where the skill should activate, including cases where the user may not name the domain directly?
- **Near misses:** Does it avoid claiming adjacent tasks the skill cannot actually handle?
- **Length:** Is it under the 1024-character hard limit?
- **Skill value:** Would this skill help on tasks that require domain knowledge, project conventions, non-obvious APIs, or special workflows?

### Weak vs strong

Weak:

```text
Use for documents.
```

Strong:

```text
Use when creating, editing, rendering, or visually verifying .docx files, Word-style documents, or Google Docs-targeted document artifacts.
```

The strong version names actions, artifacts, and activation cues. The weak version is a fog machine with a YAML header.

---

## Coherence And Boundaries

A skill should cover one coherent unit of work. If it combines unrelated jobs, it becomes hard to trigger precisely and easy to misuse.

Flag a skill when it:

- **Mixed capabilities:** it combines unrelated work that needs different triggers or workflows.
- **Over-narrow scope:** it forces several skills to activate for one normal user task.
- **Generic value:** it adds advice the base agent already knows instead of project-specific or domain-specific value.
- **Misplaced scope:** it puts activation criteria in a body `## Scope` section instead of the frontmatter `description`.
- **Menu defaults:** it presents equal-choice menus where the skill should provide a default and name alternatives as escape hatches.

### Useful test

Ask: "Could I explain this skill's purpose in one sentence without using `and then also`?"

If not, the skill probably needs a router shape, a narrower trigger, or a split.

---

## Instruction Quality

The body should teach a reusable procedure, not answer one past request.

Good instructions describe how to approach a class of tasks. They explain why constraints matter when the agent needs judgment, and they prescribe exact steps when order, safety, or consistency matters.

Look for:

- **Generalizable method:** The workflow applies beyond one example.
- **Right-sized detail:** The skill gives enough guidance to prevent common mistakes without becoming a manual for every possible case.
- **Ordered workflow:** Dependent steps appear in execution order and include validation points.
- **Templates:** Output templates appear when format consistency matters.
- **Gotchas:** Non-obvious mistakes are named directly.
- **Sensitive behavior:** Destructive or security-sensitive actions are explicit, bounded, and expected from the description.

### Formatting checks

For `SKILL.md`, require standalone `---` delimiters between `##` sections. Do not add an extra delimiter between YAML frontmatter and the `#` title.

The first body section should usually be `## Workflow`, `## Source Handling`, or `## Route the Work`. Put boundaries first only when safety or destructive behavior must be checked before any action.

Use bold scan anchors when they help a reader skim distinct actions or fields. Do not require a bold principle sentence after every heading.

---

## Progressive Disclosure

A skill spends context in three layers: metadata, the main body, and bundled resources.

`SKILL.md` should contain the routing logic and shared rules needed on every run. Deep details belong in `references/`, `assets/`, or `scripts/` only when a workflow actually uses them.

Check that:

- **Load conditions:** references are loaded by clear conditions, not vague "read everything" instructions.
- **Metadata references:** `metadata.references` lists only local skills or rules used in the workflow.
- **Metadata exclusions:** route-away, adjacent-skill, near-miss, exclusion, and boundary mentions are not listed as metadata references.
- **Resource hygiene:** placeholder folders and unused resources are removed.

---

## Validation And Evals

Review whether the skill can be tested and improved systematically.

- **Trigger coverage:** For trigger-sensitive skills, evals should include should-trigger and should-not-trigger cases. Good positive cases are not just obvious keyword matches; they are realistic requests where the skill would help. Good negative cases are near misses. Case count should be driven by coverage, not a fixed target.
- **Trigger rate:** Run each trigger query multiple times when the runtime is nondeterministic, then review the trigger rate instead of a single pass. A should-trigger query should pass at a rate >= 0.5; a should-not-trigger query should pass at a rate < 0.5. Keep train and validation splits fixed across iterations so changes are comparable.
- **Objective checks:** For behavior-sensitive skills, evals should include objective checks when practical: validators, schemas, deterministic scripts, known fixture outputs, or acceptance checks.

### What good eval coverage catches

- **False positives:** the skill triggers on adjacent work.
- **False negatives:** the skill does not activate when it should.
- **Skipped steps:** the workflow collapses under pressure.
- **Format drift:** outputs stop matching the promised shape.
- **Overfitting:** revisions copy one prompt instead of fixing the category.
- **Brittleness:** edge or invalid inputs break the workflow.

If results stall, inspect the eval set before rewriting the skill. The queries may be too easy, too hard, mislabeled, or too repetitive to reveal useful signal.

---

## Review Output

Lead with findings. Put summaries after the issues, not before them.

Each finding should include:

- **Severity:** how much it affects triggering, correctness, safety, or maintainability
- **Evidence:** specific file and line reference when possible
- **Impact:** what can go wrong in agent behavior
- **Fix direction:** the smallest useful change

If there are no findings, say that clearly and name any remaining test gaps or residual risk.
