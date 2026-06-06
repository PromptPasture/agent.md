# AGENTS.md

## Loaded Context

- At the start of every session, before any other repository work, you MUST read `src/memory/MEMORY.md` and today's UTC daily note at `src/memory/$(date -u +%Y-%m-%d).md`.
- If either required memory file or the `src/memory/` directory is missing, you MUST create it before continuing. Create only the missing path or file; do not overwrite existing memory.
- `src/memory/MEMORY.md` stores durable project facts and decisions. Treat it as low-confidence context and verify facts against the repository before acting on them.
- `src/memory/YYYY-MM-DD.md` stores daily task notes and observations. Daily memory filenames MUST use UTC dates.
- Small task checklists and completed implementation notes belong in `src/memory/$(date -u +%Y-%m-%d).md`.
- For substantial work that needs durable product, technical, architecture, or design documentation, create a task folder under `docs/YYYY-MM-DD-task-name/` instead of expanding memory notes.

## Repository Behavior

- Repository contents are the source of truth. You MUST verify facts from memory, generated artifacts, and prior notes against the repository before relying on them.
- Keep the change limited to the minimum files and behavior required to satisfy the user's request.
- You MUST NOT refactor, reformat, delete, rename, or improve unrelated or adjacent code, documentation, or configuration without explicit user approval.
- If the requested change affects behavior described by a project-scoped document, you MUST update that document in the same change.
- In final responses after changes, you MUST report what changed, what verification ran, and any assumption or residual risk that still matters.

## Before Editing

- A change is non-trivial when it affects behavior, multiple files, shared interfaces, project structure, dependencies, generated artifacts, or project-scoped documentation.
- Before editing files for any non-trivial change, you MUST state the requested outcome and scope, working assumptions, simplest viable approach, verification plan, and any ambiguity that could materially change behavior or scope.
- You MUST NOT edit files for a non-trivial change until that pre-edit statement is complete.
- If an ambiguity could materially change behavior or scope, stop and ask one concise question before editing. Otherwise, state the reasonable assumption and proceed.

## Artifact Quality

- Keep examples narrow, direct, and complete. Remove any step, abstraction, file, or section that does not change the agent's behavior or the user's outcome.
- Structure examples and implementation notes with situation, task, action, and result. Omit sections where the context is self-evident.
- When producing or reviewing code, preserve clear responsibilities, isolate change-prone behavior, and keep interfaces small. Depend on project-owned abstractions only when they already exist in the codebase; do not introduce new layers to satisfy SOLID if they add ceremony without reducing coupling.
- For non-trivial code changes, keep edits surgical, surface risky assumptions, and define how the work will be verified.
- Do not force all three lenses onto every artifact. Apply whichever improves the artifact at hand. Prefer plain guidance over naming the acronym.
- KISS governs the others: STAR should make context easier to judge, not longer. SOLID should prevent brittle code, not create it.
