---
type: concept
title: Productivity skills
description: General-purpose thinking, quality, and workflow skills usable across all projects.
tags: [skills, productivity]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Productivity skills

Project-agnostic skills for common collaboration modes. Each works without assuming any other skill is installed.

## Skills

### `adapt`

Detects mismatches between existing behavior and observed reality — failures, friction, repeated issues, changed constraints — then identifies what should change (skill, rule, doc, eval, memory) and routes to the appropriate update skill. Does **not** perform the actual update.

Triggers: "adapt based on this", "what should change after this?", "this keeps happening", "the workflow no longer fits".

### `brainstorm`

Explores user intent, requirements, and design before any implementation begins. Clarifies terms, surfaces assumptions, generates hypotheses, and shapes a clearer framing without forcing a premature decision.

Must be used before creative work: creating features, building components, adding functionality, or modifying behavior.

### `dry`

Reviews any artifact for duplicated knowledge, logic, or structure that should have a single authoritative source. Distinguishes duplicated knowledge from harmless repeated syntax.

Must be used whenever reviewing or producing any artifact.

### `handoff`

Compacts the current conversation into a handoff document so another agent can resume with full context. Used when a session is approaching context limits or when work transfers between agents.

### `plan`

Turns a goal into ordered phases with dependencies, risks, and success conditions. Pre-execution sequencing — not active coordination (that is `manage`).

Must be used before starting any multi-step execution. Triggers: "break this down", "roadmap", "approach", "milestones", "how should we proceed".

### `review`

Surfaces structured findings across consistent quadrants when evaluating any artifact. Produces a structured assessment, not a freeform prose opinion.

Must be used when asked to review, critique, or evaluate any artifact — skill, rule, doc, spec, code, diff, or pull request.

### `wiki`

Creates and maintains a structured knowledge base in OKF format: typed Markdown entries with YAML frontmatter, `index.md` catalog, and `changelog.md` per directory. Replaces the deprecated `remember` skill.

Workflows: create · update · ingest · query · lint.

Default location: `docs/` (overridable via `AGENTS.md`/`CLAUDE.md`).

### `yagni`

Catches speculative additions — features, abstractions, extension points, configurability — before they are built. Must be used whenever reviewing or producing any artifact.

## Source documents

- `wiki/sources/2026-05-20-general-agent-skills/PRD.md` — original general skills PRD (ask, explain, brainstorm, classify, plan, investigate, choose, manage, remember, adapt)
- `wiki/sources/2026-06-25-wiki-skill/BRAINSTORM.md` — wiki skill design
- `wiki/sources/2026-05-23-design-principles/PRD.md` — engineering principles (DRY, YAGNI)
