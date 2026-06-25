---
type: concept
title: Agent Playbook
description: Lightweight repository-native structure for agent guidance built on AGENTS.md and Agent Skills.
tags: [agents, playbook, agents-md, skills]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Agent Playbook

The Agent Playbook packages the public `AGENTS.md` convention and the Agent Skills specification into a practical project structure. It provides a repository-native way for developers to give agents consistent, reviewable, version-controlled guidance.

## Core idea

Developers increasingly rely on coding agents, but project instructions are scattered across READMEs, IDE settings, chat prompts, and vendor-specific files. The Playbook defines a predictable layout that any compatible agent runtime can discover.

## Entry point: `AGENTS.md`

`AGENTS.md` at the repository root is the **required baseline**. It reads like onboarding guidance for an agent — not for a human. Practical sections:

- Project overview
- Setup and build commands
- Test commands
- Code style
- Security considerations
- PR and commit guidance

### Nested `AGENTS.md`

Each subdirectory or subproject can carry its own `AGENTS.md`. The **closest file to the edited path takes precedence**. Explicit user prompts override file instructions.

## Skills: `.agents/skills/<name>/SKILL.md`

When a workflow needs more than a few lines, move it into a [skill](/docs/skills/skill-system.md). Skills are reusable, progressively loaded task procedures.

Minimum valid skill: YAML frontmatter with `name` and `description` followed by Markdown instructions.

Optional per-skill directories:

- `scripts/` — executable code (runtimes may ask permission before executing)
- `references/` — focused reference docs loaded on demand
- `assets/` — templates and static resources

## Optional extensions

All other `.agents/` folders are **optional** project extensions, not baseline requirements:

|Folder|Purpose|
|---|---|
|`.agents/rules/`|Short always-loaded behavioral rules|
|`.agents/commands/`|Slash commands|
|`.agents/agents/`|Named sub-agent personas|
|`.agents/memory/`|Durable project memory|

## Design constraints

- Core files use plain Markdown — no required vendor-specific syntax.
- A minimal valid playbook is one root `AGENTS.md`.
- Skills should stay under 5 000 tokens / 500 lines; overflow moves to `references/`.
- Never store secrets, credentials, or access tokens in agent guidance files.

## Source documents

- PRD: `wiki/sources/2026-05-02-agent-playbook/PRD.md`
- Public AGENTS.md convention: <https://agents.md>
- Agent Skills spec: <https://agentskills.io/specification>
