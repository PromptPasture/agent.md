# AGENTS.md

## Session Start

Before any work, read `docs/index.md` for the current wiki state.

- Wiki location: `docs/`
- For wiki operations use the `src/skills/productivity/wiki` skill.
- For substantial work needing durable documentation, create `docs/decisions/YYYY-MM-DD-task-name/`.

## Repository Behavior

- Repo is source of truth. Verify memory and prior notes against it before acting.
- Limit changes to the minimum required. Do not refactor, reformat, or improve unrelated code without explicit approval.
- Update project-scoped documents in the same change if behavior they describe is affected.
- Final response must state: what changed, what verification ran, and any residual risk.

## Artifact Quality

- Self-review every non-trivial artifact for placeholders, contradictions, scope drift, and missing verification. Fix issues before presenting.
- No speculative features, unused extension points, or unrequested configurability.
