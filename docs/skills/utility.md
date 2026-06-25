---
type: concept
title: Utility skills
description: Cross-cutting utility skills for git workflow, content quality, and skill security.
tags: [skills, utility, git, security, writing]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Utility skills

Thin, focused skills for recurring mechanical tasks that apply across all projects and catalogs.

## Skills

### `audit-skill-security`

Must be used before installing, updating, or trusting **any** skill from any source. Audits `SKILL.md`, permissions, dependencies, prompt-injection patterns, network behavior, exfiltration risk, bundled resources, and suspicious patterns.

### `avoid-ai-writing`

Audits and rewrites content to remove AI writing patterns ("AI-isms"). Supports detect-only mode, edit-in-place mode for files, and an optional voice profile (casual / professional / technical / warm / blunt). Runs an iterate-to-convergence pass.

### `git-branch`

Creates, switches, or renames Git branches using repository-aware naming conventions. Must be used for all branch name requests and branch actions.

### `git-commit`

Generates, improves, or applies Conventional Commit messages using staged changes and repository history. Must be used for all commit-message requests and when committing staged changes.
