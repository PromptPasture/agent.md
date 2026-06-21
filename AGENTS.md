# AGENTS.md

## Session Start

Before any work, read `.agents/memory/MEMORY.md` and `.agents/memory/$(date -u +%Y-%m-%d).md`. Create missing files or the `.agents/memory/` directory if needed; never overwrite existing memory.

- `MEMORY.md` — durable project facts. Treat as low-confidence; verify against repo before acting.
- `YYYY-MM-DD.md` — daily task notes (UTC dates). Use for checklists and completed implementation notes.
- For substantial work needing durable documentation, create `docs/YYYY-MM-DD-task-name/` instead.

## Repository Behavior

- Repo is source of truth. Verify memory and prior notes against it before acting.
- Limit changes to the minimum required. Do not refactor, reformat, or improve unrelated code without explicit approval.
- Update project-scoped documents in the same change if behavior they describe is affected.
- Final response must state: what changed, what verification ran, and any residual risk.

## Before Editing (Non-Trivial Changes)

A change is non-trivial when it affects behavior, multiple files, shared interfaces, structure, dependencies, generated artifacts, or project docs.

Before editing, state: requested outcome and scope, working assumptions, simplest viable approach, verification plan, and any material ambiguity. If an ambiguity could materially change scope, ask one concise question first.

## Artifact Quality

- Every artifact must be complete, actionable, internally consistent, and specific enough to verify.
- No placeholders, TODOs, unsupported claims, or missing required sections unless the user requests a draft.
- Every section, example, and abstraction must contribute to the outcome. Remove anything that does not.
- Examples must be narrow, direct, complete, and consistent with actual repo interfaces.
- Introduce abstractions only when they reduce real complexity or follow an established pattern.
- No speculative features, unused extension points, or unrequested configurability.
- KISS: prefer the simplest complete solution. If an implementation grows beyond what the problem requires, simplify before finalizing.
- Self-review every non-trivial artifact for placeholders, contradictions, scope drift, and missing verification. Fix issues before presenting.
