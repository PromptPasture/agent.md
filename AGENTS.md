# AGENTS.md

## Loaded Context

- At the start of every session, before any other repository work, you MUST read `src/memory/MEMORY.md` and today's UTC daily note at `src/memory/$(date -u +%Y-%m-%d).md`.
- If either required memory file or the `src/memory/` directory is missing, you MUST create it before continuing. Create only the missing path or file; do not overwrite existing memory.
- `src/memory/MEMORY.md` stores durable project facts and decisions. Treat it as low-confidence context and verify facts against the repository before acting on them.
- `src/memory/YYYY-MM-DD.md` stores daily task notes and observations. Daily memory filenames MUST use UTC dates.
- Small task checklists and completed implementation notes belong in `src/memory/$(date -u +%Y-%m-%d).md`.
- For substantial work that needs durable product, technical, architecture, or design documentation, create a task folder under `docs/YYYY-MM-DD-task-name/` instead of expanding memory notes.

## Repository Behavior

- Treat memory, generated artifacts, and prior notes as low-confidence context; verify facts against the repository before relying on them.
- Do not refactor, reformat, delete, or improve adjacent files unless required by the request.
- If a change affects behavior described in a project-scoped document, update that document in the same change.
- Do not deviate from an active `SPEC.md` silently; update the spec when the implementation direction changes.
- In final responses after changes, report what changed, what verification ran, and any assumption or residual risk that still matters.

## Before Editing

- For non-trivial changes, briefly state the working assumptions, simplest viable approach, verification plan, and any ambiguity that would change the implementation.
- Ask one concise question when ambiguity blocks a correct result.

## Artifact Quality

- Keep examples narrow, direct, and complete. Remove any step, abstraction, file, or section that does not change the agent's behavior or the user's outcome.
- Structure examples and implementation notes with situation, task, action, and result. Omit sections where the context is self-evident.
- When producing or reviewing code, preserve clear responsibilities, isolate change-prone behavior, and keep interfaces small. Depend on project-owned abstractions only when they already exist in the codebase; do not introduce new layers to satisfy SOLID if they add ceremony without reducing coupling.
- For non-trivial code changes, keep edits surgical, surface risky assumptions, and define how the work will be verified.
- Do not force all three lenses onto every artifact. Apply whichever improves the artifact at hand. Prefer plain guidance over naming the acronym.
- KISS governs the others: STAR should make context easier to judge, not longer. SOLID should prevent brittle code, not create it.
