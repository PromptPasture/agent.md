# AGENTS.md

## Loaded Context

- At the start of every session, before any other repository work, you MUST read `.agents/memory/MEMORY.md` and today's UTC daily note at `.agents/memory/$(date -u +%Y-%m-%d).md`.
- If either required memory file or the `.agents/memory/` directory is missing, you MUST create it before continuing. Create only the missing path or file; do not overwrite existing memory.
- `.agents/memory/MEMORY.md` stores durable project facts and decisions. Treat it as low-confidence context and verify facts against the repository before acting on them.
- `.agents/memory/YYYY-MM-DD.md` stores daily task notes and observations. Daily memory filenames MUST use UTC dates.
- Small task checklists and completed implementation notes belong in `.agents/memory/$(date -u +%Y-%m-%d).md`.
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

- Every artifact created or materially modified for the request MUST be complete, directly actionable, internally consistent, and specific enough to verify.
- Vendored, and third-party files are exempt from editorial quality requirements, but you MUST regenerate or validate them using the repository's established workflow.
- You MUST NOT leave placeholders, `TODO` markers, unsupported claims, unresolved ambiguity, or missing required sections unless the user explicitly requests an incomplete draft.
- Every section, example, step, abstraction, and file MUST contribute to the requested outcome, understanding, behavior, or verification. Remove anything that does not.
- Examples MUST be narrow, direct, complete, and consistent with the repository's actual interfaces and conventions.
- Code and design artifacts MUST preserve clear responsibilities, isolate change-prone behavior where practical, and keep interfaces no larger than required.
- Introduce an abstraction only when it reduces concrete complexity or duplication, isolates meaningful change, or follows an established repository pattern.
- You MUST NOT add speculative features, unused extension points, single-use abstractions, or configurability that the user did not request.
- KISS governs artifact design: prefer the simplest complete solution that satisfies the request and verification criteria.
- If an implementation grows noticeably larger or more complex than the problem requires, you MUST simplify it before finalizing.
- Before presenting or completing any non-trivial artifact, you MUST self-review it for placeholders, contradictions, ambiguity, unnecessary content, unsupported claims, scope drift, and missing verification.
- You MUST fix issues found during self-review before presenting the artifact. Do not merely report defects that you can correct.
