---
type: concept
title: Product skills
description: Skills for writing product artifacts — PRDs, specs, and tickets.
tags: [skills, product, prd, spec, ticket]
created: "2026-06-25T00:00:00Z"
updated: "2026-07-07T00:00:00Z"
---

# Product skills

Skills for producing and revising product and delivery artifacts. All use YAML frontmatter for document metadata.

## Skills

### `to-prd`

Writes or revises a PRD, product requirements document, product brief, feature requirements, or product scope. Produces a structured document with goals, personas, scope, functional and non-functional requirements, milestones, risks, and open questions. Marks inferences with `[assumed]`. User-invoked only (`disable-model-invocation: true`); routes unresolved product decisions to `brainstorm` before drafting.

### `write-spec`

Writes or revises a technical specification. Cross-references the related PRD to stay consistent in terminology and requirements. Companion to `to-prd`.

### `to-ticket`

Writes or revises Jira, GitHub, and Linear tickets — bugs, features, tasks, chores, documentation, and spikes — using type-specific templates. The feature type carries full sprint-ready user-story rigor (Card-Conversation-Confirmation, INVEST, story points, epic linkage, Given/When/Then scenarios) when the request needs it, and stays a lightweight capability ask otherwise. User-invoked only (`disable-model-invocation: true`).

## Consolidation (decided 2026-07-07)

`write-user-story` and `write-ticket` were split into independent skills on 2026-06-10. They are now consolidated back into the single `to-ticket` skill: its feature ticket type absorbs everything `write-user-story` did. `write-user-story` is deprecated in favor of `to-ticket`.

## Source documents

- `wiki/sources/2026-05-02-team-roles-as-skills/PRD.md`
- `wiki/sources/2026-06-10-split-user-story-and-ticket-writing/BRAINSTORM.md`
