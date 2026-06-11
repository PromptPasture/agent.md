---
name: write-ticket
description: You MUST use this when the user asks to write or revise Jira/GitHub tickets, issues, or work items, including bug, feature, task, chore, documentation, and spike requests.
license: Apache-2.0
tags:
  - writer
  - tickets
  - issue-tracking
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: product
  category: requirements
---

# Writing Tickets

Write implementation-ready Jira, GitHub, or standalone Markdown tickets using language and structure appropriate to the work item.

## Workflow

1. Identify the requested tracker, audience, desired result, and available source material.
2. Inspect the prompt, repository, requirements, designs, logs, existing issues, and constraints before asking for information already available.
3. Infer the ticket type from the work:
   - **Bug:** incorrect or unexpected existing behavior.
   - **Feature:** a new or changed capability with a defined outcome.
   - **Task:** implementation, maintenance, chore, or documentation work.
   - **Spike:** a bounded investigation that must answer a question.
4. Default genuine ambiguity to `task`. State the assumption only when another type would materially change the ticket.
5. Separate confirmed facts, reasonable assumptions, material unknowns, and unresolved decisions.
6. Ask one concise question only when the missing answer would materially change the objective, scope, completion criteria, or investigation boundary. Otherwise, mark low-risk assumptions and proceed.
7. Select the matching writing model and include only sections that make the ticket actionable.
8. Adapt metadata and field placement to the requested tracker without changing the ticket's writing model.
9. Split multiple independently deliverable outcomes into separate tickets.
10. Self-review each ticket for clear purpose, bounded scope, observable completion, unsupported claims, and unnecessary user-story framing.

## Ticket Models

### Bug

Include:

- problem context
- reproduction steps
- actual result
- expected result
- impact
- completion criteria

Do not invent reproduction details, environment information, severity, or root cause.
Mark unavailable evidence and ask only when it blocks an actionable ticket.

### Feature

Include:

- problem
- desired outcome
- scope
- requirements
- acceptance criteria
- non-goals when needed to prevent material ambiguity

Describe the capability directly.

### Task

Include:

- objective
- required work
- relevant constraints
- completion criteria
- verification

Map chores and documentation tickets to this model.
Keep the required work outcome-focused and avoid prescribing unsupported implementation details.

### Spike

Include:

- question to answer
- investigation scope
- expected deliverable
- stopping condition or timebox when known

Define completion as producing evidence or a decision, not implementing the solution being investigated.

## Output

Produce concise Markdown suitable for the requested destination. Preserve a user-provided template when it is stricter.

Use an outcome-focused title and the selected ticket model. Add assumptions, dependencies, risks, or open questions only when they affect delivery.

- **Jira:** map known issue type, priority, labels, epic, ownership, and relationships to native fields instead of duplicating them in the body.
- **GitHub:** use known labels, linked issues, issue-form conventions, and task lists when they match the repository's issue style.
- **Standalone Markdown:** put known status, type, priority, owner, labels, and related work in YAML frontmatter.

When drafting text without direct tracker access, return known tracker fields in a compact `Metadata` section before the ticket body. Omit unknown optional fields instead of inventing values.

Do not invent tracker fields or values. Omit unknown optional metadata unless the user expects the field and it must be marked `TBD`.

### Feature Ticket Example

```markdown
# Allow administrators to revoke active sessions

## Problem

Compromised or obsolete sessions remain active until they expire.

## Desired Outcome

Administrators can revoke a selected active session and prevent its further use.

## Acceptance Criteria

- The selected session becomes invalid immediately after revocation.
- Other sessions remain active.
- Unauthorized users cannot revoke sessions.
```

## Writing Rules

- **Write the work item, not a disguised story:** use the selected ticket model rather than persona-based story language.
- **Keep one objective:** each ticket should produce one coherent, independently verifiable result.
- **Make completion observable:** state what must be true and how it can be checked.
- **Separate facts from assumptions:** label inferred details with `[assumed]` when the distinction matters.
- **Use repository evidence:** cite verified paths, modules, commands, logs, or interfaces. Use logical names marked `[assumed]` when the repository is unavailable.
- **Cover relevant failure behavior:** include validation, authorization, privacy, security, recovery, and boundary conditions only when applicable.
- **Avoid hidden scope:** distinguish required work, non-goals, dependencies, and later work.
- **Estimate only when requested:** use the team's known scale and state uncertainty; do not convert points to time.
- **Keep skills independent:** do not invoke or automatically convert through `write-user-story`. When the user explicitly requests both artifacts, write only the ticket portion of this skill's output.
- **Route mismatched requests:** use `write-user-story` when the requested artifact is a user story rather than a ticket.

## Verification

Before finalizing, verify that:

- The inferred ticket type matches the work or a material assumption is stated.
- The ticket uses the corresponding bug, feature, task, or spike model.
- The objective, scope, and completion conditions are clear and consistent.
- Tracker adaptation changes metadata placement without changing the writing model.
- Chore and documentation requests use the task model.
- The output contains no forced user-story framing, unsupported claims, duplicated requirements, unresolved instructional placeholders, or unnecessary sections.
