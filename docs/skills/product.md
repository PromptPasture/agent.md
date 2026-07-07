---
type: concept
title: Product skills
description: Skills for writing product artifacts — PRDs, specs, and user stories.
tags: [skills, product, prd, spec, user-story]
created: "2026-06-25T00:00:00Z"
updated: "2026-07-06T00:00:00Z"
---

# Product skills

Skills for producing and revising product and delivery artifacts. All use YAML frontmatter for document metadata.

## Skills

### `to-prd`

Writes or revises a PRD, product requirements document, product brief, feature requirements, or product scope. Produces a structured document with goals, personas, scope, functional and non-functional requirements, milestones, risks, and open questions. Marks inferences with `[assumed]`. User-invoked only (`disable-model-invocation: true`); routes unresolved product decisions to `brainstorm` before drafting.

### `write-spec`

Writes or revises a technical specification. Cross-references the related PRD to stay consistent in terminology and requirements. Companion to `to-prd`.

### `write-user-story`

Writes or revises user stories, acceptance criteria, and sprint-ready increments. Uses `As a / I want / so that` framing, Card-Conversation-Confirmation, and INVEST principles. Produces observable acceptance criteria.

Does **not** handle generic tracker tickets — those go to `write-ticket` (in-progress).

## Routing: user story vs. ticket (decided 2026-06-10)

|Request|Skill|
|---|---|
|User story|`write-user-story`|
|Jira/GitHub/Linear bug, feature, task, chore, spike|`write-ticket`|
|Both explicitly requested|Both skills, each producing only its own artifact|
|Converting story → ticket or ticket → story|Requires explicit user request|

Neither skill invokes or converts through the other.

## Source documents

- `wiki/sources/2026-05-02-team-roles-as-skills/PRD.md`
- `wiki/sources/2026-06-10-split-user-story-and-ticket-writing/BRAINSTORM.md`
