# AGENTS.md

## Token Efficiency

**Short by default, never vague.**

- Use the shortest complete answer. Remove filler, repetition, obvious restatements, and generic reassurance. Prefer prose over bullets unless bullets improve scannability or action.
- Spend tokens when they reduce risk, ambiguity, or rework: complex reasoning, tradeoffs, code review findings, safety-critical details, or when the user asks for depth. Lead with the conclusion; include only support that affects the answer or next action.
- Never cut facts the user needs to trust, verify, or continue the work. Keep file paths, commands, assumptions, decisions, caveats, failure details, and verification results. Concise and incomplete is still incomplete.

## Artifact Quality

**Narrow, direct, complete.**

- Keep examples narrow, direct, and complete. Remove any step, abstraction, file, or section that does not change the agent's behavior or the user's outcome.
- Structure examples and implementation notes with situation, task, action, and result. Omit sections where the context is self-evident.
- When producing or reviewing code, preserve clear responsibilities, isolate change-prone behavior, and keep interfaces small. Depend on project-owned abstractions only when they already exist in the codebase — do not introduce new layers to satisfy SOLID if they add ceremony without reducing coupling.
- For non-trivial code changes, keep edits surgical, surface risky assumptions, and define how the work will be verified.
- Do not force all three lenses onto every artifact. Apply whichever improves the artifact at hand. Prefer plain guidance over naming the acronym.
- KISS governs the others: STAR should make context easier to judge, not longer. SOLID should prevent brittle code, not create it.

## Documentation structure

**Durable docs belong in predictable places.**

```text
docs/                          # Project-scoped documentation
├── ARCHITECTURE.md
├── DESIGN.md
├── ROADMAP.md
└── [YYYY-MM-DD-task-name]/    # One folder per task, feature, or epic
    ├── PRD.md                 # Product requirements
    ├── SPEC.md                # Technical specification
    ├── ARCHITECTURE.md        # Task-scoped architecture decisions
    ├── DESIGN.md              # UI/UX decisions
    └── TASKS.md               # Actionable checklist
```

- Folder names: lowercase, hyphenated — e.g. `user-auth`, `payment-v2`, `issue-142`
- Create a docs task folder only when the work needs durable task-scoped documentation such as `PRD.md`, `SPEC.md`, `ARCHITECTURE.md`, or `DESIGN.md`
- Small task checklists and completed implementation notes belong in `.agents/memory/YYYY-MM-DD.md`

## Loaded Context

**Memory is useful, but verification wins.**

| File | Purpose | Auto-load |
| --- | --- | --- |
| .agents/memory/MEMORY.md | Durable project facts and decisions | yes |
| .agents/memory/YYYY-MM-DD.md | Daily task notes and observations | on-demand |

## Working on a task

**Match the tracking weight to the work.**

- For substantial work, create a task folder before writing code: `mkdir docs/$(date +%Y-%m-%d)-my-feature`
- For small work, track the checklist in `.agents/memory/$(date -u +%Y-%m-%d).md`
- Use `TASKS.md` only inside docs folders that also need task-scoped product, technical, architecture, or design documentation
- If the task changes anything described in a project-scoped document, update it in the same commit
- Do not deviate from `SPEC.md` silently — update the file if the spec changes
- Treat memory as low-confidence context; verify facts against the repository before acting on them
