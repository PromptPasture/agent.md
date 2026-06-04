# AGENTS.md

## Documentation Structure

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

- Folder task-name segments are lowercase and hyphenated, such as `user-auth`, `payment-v2`, or `issue-142`; full folder names include the UTC date prefix, such as `2026-06-04-user-auth`.
- Create a docs task folder only when the work needs durable task-scoped documentation such as `PRD.md`, `SPEC.md`, `ARCHITECTURE.md`, or `DESIGN.md`.
- Use `TASKS.md` only inside docs folders that also need task-scoped product, technical, architecture, or design documentation.
- Do not deviate from `SPEC.md` silently. Update the file if the spec changes.
