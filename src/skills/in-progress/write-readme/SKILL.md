---
name: write-readme
description: Write or revise project README files. Use for repository, library, CLI, service, internal-tool, and open-source project introductions, installation, quick starts, usage, configuration, development, contribution, support, and license guidance.
license: Apache-2.0
tags:
  - writer
  - docs
  - readme
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
---

# write-readme

Write a README that lets its intended audience understand, install, and use the project.

## Workflow

1. Determine whether the project is a library, CLI, service, application, internal tool, or open-source project.
2. Inspect repository truth before writing: manifests, entry points, existing docs, configuration, scripts, examples, license, and contribution guidance.
3. Identify the primary audience and the shortest successful path from discovery to working usage.
4. Preserve accurate useful content in an existing README; replace only content that is stale, misleading, duplicated, or poorly organized.
5. Write only sections supported by the project and audience.
6. Verify commands, examples, links, requirements, and configuration against the repository.

## Content

A complete README usually includes:

- Project name and a one-sentence explanation of what it does and why it is useful
- A short overview and the most important capabilities
- Requirements and installation instructions
- A working quick start near the beginning
- Common usage and configuration
- Development and test commands when relevant
- Links to detailed API or operational documentation instead of duplicating it
- Contribution, support, maintenance ownership, status, roadmap, or license information when relevant

Adapt the emphasis:

- **Library:** lead with a minimal import and working code example.
- **CLI:** show installation, common commands, and useful `--help` output early.
- **Service or API:** explain how to run it, authenticate, and find detailed API docs.
- **Internal tool:** state who owns it and how teammates get access; omit community material.
- **Open source:** include contribution, support, status, and license information.

## Writing Rules

- Explain the project before describing its implementation.
- Keep the first successful example short, complete, and consistent with the current interface.
- Use exact repository commands and minimum supported versions.
- Document configuration names, defaults, purpose, and whether values are sensitive.
- Link to authoritative detailed docs rather than reproducing large references.
- Do not add badges unless their targets are real and useful.
- Mark unsupported inferences with `[assumed]`; do not invent project facts.
- Remove placeholders and sections that do not apply.

## Error Paths

- If installation or usage cannot be established from repository evidence, state the missing fact instead of inventing a command.
- If existing docs conflict with code or configuration, follow repository behavior and identify the discrepancy.
- If the repository contains multiple products, document the shared entry point and link to product-specific docs rather than forcing all details into one file.

## Verification

- The opening explains what the project does, why it matters, and who it serves.
- A reader can reach a working first result without guessing.
- Commands, paths, interfaces, requirements, links, and configuration match repository evidence.
- The structure is proportional to the project and contains no empty, speculative, or duplicate sections.
- No placeholders or unmarked assumptions remain.
