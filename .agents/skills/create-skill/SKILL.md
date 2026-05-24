---
name: create-skill
description: Use when creating, editing, reviewing, evaluating, packaging, optimizing or improving skills.
license: Apache-2.0
version: 1.1.3
tags:
  - creator
  - skills
  - authoring
author: Anthropic
metadata:
  catalog: utility
---

# create-skill

Create new skills, review and improve existing skills, evaluate outputs, optimize trigger descriptions, and package final skill folders.

---

## Route the Work

**Read only the reference that matches the user's current task.**

| User intent | Read |
| --- | --- |
| Create a new skill or revise skill instructions | `references/authoring.md` |
| Review a created or revised skill | `references/review.md` |
| Build eval cases, run iterations, benchmark outputs, or collect human feedback | `references/evaluation.md` |
| Optimize a skill description for trigger accuracy | `references/description-optimization.md` |
| Adapt the workflow for agents without subagents, Claude Code, generic CLIs, or Cowork | `references/agent-compatibility.md` |
| Validate eval, grading, benchmark, or feedback JSON structures | `references/schemas.md` |

If the request spans multiple phases, read the references in workflow order: authoring, review, evaluation, description optimization, then agent compatibility only when platform details matter.

---

## Core Workflow

**Clarify, write, test, show, iterate, and package — in that order.**

1. **Clarify scope**: identify what the skill should do, which user phrases or contexts should trigger it, what output it should produce, and whether objective evals are useful.
2. **Write the skill**: revise `SKILL.md` with concise metadata, focused instructions, bold scan anchors, and references for details that would bloat the main file.
3. **Test behavior**: run this skill's `scripts/quick_validate.py` against the target skill; for router skills, confirm every `references/*.md` file has 8-10 evals mapped by `reference`; for objectively testable skills, run skill-enabled outputs against a meaningful baseline.
4. **Show evidence**: share outputs and benchmark results with the user before making another revision.
5. **Iterate deliberately**: continue until feedback is resolved or further changes stop improving results.
6. **Package last**: package the final skill only after the user is satisfied with behavior and trigger accuracy.

---

## Skill Authoring Rules

**One skill, one workflow, one clear trigger — no more.**

- **Section delimiters**: place a standalone `---` between `##` sections in authored `SKILL.md` files so models see strong structural boundaries.
- **Section principles**: open each `##` section with a single bold sentence that states the section's core principle.
- **Scan anchors**: use bold labels for distinct rule bullets in prose skill docs unless the section is a schema, command example, or literal output template.
- **Size discipline**: keep metadata under 100 tokens and the main instruction body under 500 lines; use references for anything that would push past that.
- **Metadata fields**: use only `name`, `description`, `license`, `version`, `tags`, `author`, and `metadata`; only `name` and `description` are required.
- **Reference metadata**: use `metadata.references` only for local skills or rules the skill uses as part of its workflow; do not list route-away, adjacent-skill, near-miss, or boundary mentions.
- **Pushy descriptions**: explicitly name the user phrases and contexts that should trigger the skill, not just what it does. Claude tends to undertrigger, so err toward specificity.
- **Trigger placement**: put all "when to use" information in the frontmatter `description`; put routing, exclusions, examples, and detailed procedures in the body or references.
- **No placeholders**: add `scripts/`, `references/`, `assets/`, or `evals/` only when the skill actually uses them.
- **Deterministic helpers**: prefer scripts for repetitive validation, grading, packaging, and report generation.
- **STAR examples**: write examples and eval prompts so reviewers can see the situation, task, expected action, and result criteria.
- **SOLID code**: keep responsibilities clear, interfaces small, and dependencies explicit without adding unnecessary layers in code-generation skills and bundled helper scripts.
- **Portability**: keep skills portable across agents unless the user asks for one specific runtime. Isolate platform-specific behavior in a compatibility section or reference.

---

## Bundled Resources

**Scripts and agents cover the full eval, grading, and packaging loop.**

- **Trigger optimization**: `scripts/run_eval.py`, `scripts/run_loop.py`, and `scripts/improve_description.py`
- **Validation**: `scripts/quick_validate.py`
- **Benchmark summaries**: `scripts/aggregate_benchmark.py`
- **Packaging**: `scripts/package_skill.py`
- **Human review UI**: `eval-viewer/generate_review.py`
- **Review agents**: `agents/grader.md`, `agents/comparator.md`, `agents/analyzer.md`, and `agents/benchmark-analyzer.md`
