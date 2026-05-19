<!-- markdownlint-disable-next-line MD041 -->
![A small home where an AI agent lives](./pages/assets/landing.jpeg)

# Agent Playbook

> A portable, tool-agnostic file structure playbook for LLM agents in software projects.

Agent behavior is code. It should be versioned, reviewed, modular, and readable by both humans and machines. The `.agents/` folder is the single source of truth for everything an LLM agent needs to operate within a project — permissions, instructions, skills, memory, commands, and documentation artifacts.

## Overview

Every team using LLM agents invents their own folder structure. Instructions live in random `.md` files, prompts are buried in config, and memory is nowhere. When the runtime changes or someone new joins the project, nothing is discoverable.

This playbook gives agents — and the humans working alongside them — a consistent, predictable home. It defines where agent instructions, rules, skills, memory, commands, and documentation live, consistently across any project and any runtime.

## Features

- **`AGENTS.md`** — Primary instruction file and manifest. Every runtime loads this first.
- **`.agents/rules/`** — Modular, composable instruction files.
- **`.agents/skills/`** — Auto-invoking workflows triggered by events or file patterns.
- **`.agents/commands/`** — Explicit slash commands.
- **`.agents/agents/`** — Subagent personas invoked by `@mention`.
- **`.agents/memory/`** — Persistent, append-only memory across sessions.
- **`docs/`** — Task-scoped documentation with standardized layout (PRD, SPEC, ARCHITECTURE, TASKS).

## Core Principles

- **Co-location** — Agent files live alongside the code they govern.
- **Modularity** — Each concern lives in its own folder, adopted incrementally.
- **Composability** — Rules, skills, and agents mix and match across projects.
- **Portability** — Works with any LLM runtime: Claude, Cursor, Copilot, custom.
- **Progressive disclosure** — Start with one `AGENTS.md`. Add folders as needed.

## Folder Structure

```text
agent.md/              # ← this repository
├── .agents/           # Maintained agent asset library
├── docs/              # Task-scoped documentation
├── pages/             # GitHub Pages source
│   ├── _config.yml    # GitHub Pages configuration
│   ├── index.md       # GitHub Pages entry point
│   └── PLAYBOOK.md    # Full playbook specification
└── LICENSE
```

## Quick Start

The minimum viable setup is a single file:

```text
AGENTS.md
```

Write your agent instructions. Add folders only when you have a reason to.

### Playbook setup

```text
AGENTS.md
.agents/
├── rules/
│   └── general.md
└── memory/
    └── MEMORY.md
```

### Full setup

Add `skills/`, `commands/`, `agents/`, and `docs/` as the project matures.

## Usage

### Library

This repository maintains its primary reusable agent assets in [`.agents/`](./.agents):

- **Rules** — `.agents/rules/formatting-markdown.md`
- **Skills** — `.agents/skills/on-new-example/SKILL.md`
- **Commands** — `.agents/commands/validate.md`
- **Agents** — `.agents/agents/spec-reviewer.md`
- **Memory** — `.agents/memory/MEMORY.md`

### Real project layout

```text
project-root/
├── AGENTS.md                  # Primary instruction file + table of contents
├── .agents/
│   ├── rules/                 # Modular instruction files
│   │   ├── code-style.md      # TypeScript conventions
│   │   ├── testing.md         # Test coverage requirements
│   │   └── security.md        # OWASP top-10 awareness
│   ├── skills/                # Auto-invoking workflows (trigger → action)
│   │   ├── on-new-file/       # Auto-scaffold test files
│   │   │   └── SKILL.md
│   │   └── on-test-fail/      # Diagnose CI failures
│   │       └── SKILL.md
│   ├── commands/              # Custom slash commands
│   │   ├── review.md          # /review — structured code review
│   │   └── scaffold.md        # /scaffold — generate boilerplate
│   ├── agents/                # Subagent personas
│   │   ├── architect.md       # @architect — system design advisor
│   │   └── security-auditor.md # @security — OWASP-focused review
│   └── memory/                # Persistent agent memory
│       ├── MEMORY.md          # Long-term memory
│       └── YYYY-MM-DD.md      # Daily notes
├── docs/                      # Project-scoped documentation
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   └── YYYY-MM-DD-task-name/
│       ├── PRD.md
│       ├── SPEC.md
│       ├── ARCHITECTURE.md
│       ├── DESIGN.md
│       └── TASKS.md
├── src/
├── package.json
└── README.md
```

## Development

This repo uses itself to govern its own development — the `.agents/` folder is the maintained set of playbook-conformant assets used for that work.

```bash
# No build step required. All content is plain Markdown.
# Fork, edit, and open a pull request.
```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Commit your changes following [Conventional Commits](https://www.conventionalcommits.org).
4. Open a pull request.

Before writing code, create a task folder: `mkdir docs/$(date +%Y-%m-%d)-my-feature` and use `TASKS.md` as your checklist.

## References

- **[Docs site](https://olegshulyakov.github.io/agent.md)** — GitHub Pages documentation
- **[PLAYBOOK.md](./pages/PLAYBOOK.md)** — Full playbook specification
- **[Agent PDLC](./pages/AGENT_PDLC.md)** — Lifecycle diagram for working with an agent
- **[Library](./.agents)** — Maintained playbook-conformant assets

## License

MIT — see [LICENSE](./LICENSE) for details.

---

_This playbook is intentionally tool-agnostic. Runtimes may extend it provided they do not break compatibility with the core specification._
