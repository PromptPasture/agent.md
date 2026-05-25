---
name: create-skill
description: Create, edit, review, evaluate, package, and optimize skills. Use when users ask to create a skill, revise skill instructions, review a skill, run skill evals, benchmark skill performance, package a skill, or optimize a skill description for trigger accuracy.
license: Apache-2.0
tags:
  - creator
  - skills
  - authoring
metadata:
  author: Anthropic
  version: "1.9.0"
  source: github.com/anthropics/skills
  catalog: utility
  category: meta
---

# create-skill

Create new skills, review and improve existing skills, evaluate outputs, optimize trigger descriptions, and package final skill folders.

---

## Workflow

1. **Route the request.** Read only the reference that matches the user's current task:

   | User intent | Read |
   | --- | --- |
   | Create a new skill or revise skill instructions | `references/authoring.md` |
   | Review a created or revised skill | `references/review.md` |
   | Build eval cases, run iterations, benchmark outputs, or collect human feedback | `references/evaluation.md` |
   | Optimize a skill description for trigger accuracy | `references/description-optimization.md` |
   | Adapt the workflow for agents without subagents, Claude Code, generic CLIs, or Cowork | `references/agent-compatibility.md` |
   | Validate eval YAML or grading, benchmark, and feedback JSON structures | `references/schemas.md` |

   If the request spans multiple phases, read the references in workflow order: authoring, review, evaluation, description optimization, then agent compatibility only when platform details matter.

2. **Clarify activation and behavior.** Identify what the skill should do, which user phrases or contexts should trigger it, what output it should produce, and whether objective evals are useful.
3. **Write or revise the skill.** Name new skills using the `<verb>-<subject>[-<variant>]` convention or a concise `<verb>` format (e.g., `code-tests`, `ask`). Follow `references/authoring.md` for metadata, trigger descriptions, `SKILL.md` body format, reference file format, section delimiters, scan anchors, examples, helper scripts, portability, and validation. Always bump `metadata.version` using semantic versioning upon any material change to a skill's files.
4. **Test behavior.** Run this skill's `scripts/quick_validate.py` against the target skill when available. For router skills, confirm every `references/*.md` file has 8-10 evals mapped by `reference`; for objectively testable skills, run skill-enabled outputs against a meaningful baseline.
5. **Show evidence.** Share validation output, eval results, benchmark summaries, and relevant diffs before making another revision.
6. **Iterate deliberately.** Continue until feedback is resolved or further changes stop improving behavior.
7. **Package last.** Package the final skill only after the user is satisfied with behavior and trigger accuracy.

---

## Output

- **For skill edits:** summarize changed files, behavior changes, and validation results.
- **For reviews:** lead with correctness, trigger, structure, safety, and test coverage findings.
- **For evals or benchmarks:** report the command, dataset or eval set, pass/fail counts, variance notes, and recommended next change.
- **For packaging:** report the generated artifact path and any remaining manual checks.

---

## Boundaries

- **Use the reference as source of truth.** Do not duplicate detailed authoring, review, evaluation, schema, or compatibility rules in this file.
- **Keep skills focused.** Center each skill on one trigger and one workflow; route broad domains through references instead of expanding the main body.
- **Avoid placeholders.** Add `scripts/`, `references/`, `assets/`, or `evals/` only when the skill actually uses them.
- **Package after behavior.** Do not package a skill before the user is satisfied with behavior and trigger accuracy.

---

## Bundled Resources

- **Trigger optimization**: `scripts/run_eval.py`, `scripts/run_loop.py`, and `scripts/improve_description.py`
- **Validation**: `scripts/quick_validate.py`
- **Benchmark summaries**: `scripts/aggregate_benchmark.py`
- **Packaging**: `scripts/package_skill.py`
- **Human review UI**: `eval-viewer/generate_review.py`
- **Review agents**: `agents/grader.md`, `agents/comparator.md`, `agents/analyzer.md`, and `agents/benchmark-analyzer.md`

---

## Verification

- [ ] The selected reference matches the user's current task
- [ ] `SKILL.md` and reference edits follow `references/authoring.md`
- [ ] Validation, eval, benchmark, or packaging commands were run when applicable
- [ ] Results and remaining risks are reported to the user
