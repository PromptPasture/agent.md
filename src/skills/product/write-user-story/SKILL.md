---
name: write-user-story
description: You MUST use this when the user asks to write or revise user stories, acceptance criteria, story points, or sprint-ready user-value increments.
license: Apache-2.0
tags:
  - writer
  - agile
  - user-stories
metadata:
  author: Oleg Shulyakov
  version: "1.4.0"
  source: github.com/olegshulyakov/agent.md
  catalog: product
  category: requirements
---

# Writing User Story

Produce one or more **user stories** centered on a specific user, capability, and meaningful outcome.

## Workflow

1. Identify the capability, target user, desired outcome, delivery audience, and requested story format.
2. Inspect the prompt, repository, PRD, specification, designs, existing stories, and constraints before asking for information already available.
3. Separate confirmed facts, reasonable assumptions, material unknowns, and unresolved product or technical decisions.
4. Ask only questions whose answers would materially change the user value, scope, acceptance criteria, dependencies, or estimate. If missing details are low-risk, mark assumptions and proceed.
5. Split the request into independently valuable stories when it contains multiple personas, outcomes, workflows, or sprint-sized goals.
6. Write each story from the user's perspective using the Card, Conversation, Confirmation model:
   - **Card:** a concise statement of user value.
   - **Conversation:** context, scope, assumptions, and open decisions needed for shared understanding.
   - **Confirmation:** observable acceptance criteria that define done.
7. Derive acceptance criteria from the story and relevant requirements. Cover the primary path and applicable validation, permission, empty, error, recovery, and boundary conditions.
8. Estimate story points only when the user requests them or the team scale is known. State uncertainty and avoid false precision.
9. Self-review every story for user value, scope, independence, testability, implementation leakage, unsupported assumptions, and missing failure behavior.

## Output

Produce Markdown suitable for a standalone story file or a user-provided story template.

Use this default structure and remove optional sections that add no delivery value:

```markdown
---
status: "[DRAFT | READY | IN_PROGRESS | DONE]"
phase: "[discovery | delivery | maintenance]"
storyId: "[US-N]"
storyPoints: "[1 | 2 | 3 | 5 | 8]"
priority: "[HIGH | MEDIUM | LOW]"
owner: "[Name, team, or TBD]"
epic: "[Parent epic, initiative, or URL]"
tags:
  - "[tag]"
related:
  - "[PRD, specification, design, issue, or URL]"
---

# [US-N]: [Outcome-focused title]

## Story

**As a** [specific user or role],\
**I want** [capability or action],\
**so that** [measurable or observable benefit].

## Acceptance Criteria

### Scenario: [Primary path]

**Given** [initial state or prerequisite]\
**When** [user or system action]\
**Then** [observable result]

### Scenario: [Relevant failure or edge path]

**Given** [initial state or prerequisite]\
**When** [invalid, unavailable, unauthorized, empty, or boundary condition]\
**Then** [observable handling and recovery behavior]

## Verification

- [Test, command, review, or observable check that proves the story is done]

## Dependencies and Open Questions [optional]

- [Dependency, unresolved decision, owner, or resolution condition]
```

- Put status, identifiers, estimates, ownership, epic, tags, and related documents in YAML frontmatter when writing a standalone story file.
- Repeat the structure for each story and keep IDs, dependencies, and ordering consistent.
- Add context or scope boundaries only when they are necessary for shared understanding.
- Omit Dependencies and Open Questions when the story has no meaningful dependency or unresolved decision.
- Do not emit instructional placeholders in a completed story. Populate them, mark a genuinely unresolved value as `TBD`, or remove the optional field or section.

## Writing Rules

- **Center one user value:** each story serves one persona pursuing one coherent outcome.
- **Keep the card implementation-free:** describe the needed capability and benefit, not a prescribed UI control, framework, endpoint, or database design unless it is a fixed constraint.
- **Make value explicit:** the `so that` clause must explain why the capability matters and must not merely restate the action.
- **Apply INVEST:** stories should be independent, negotiable, valuable, estimable, small, and testable. Surface dependencies when full independence is impossible.
- **Make criteria atomic:** each scenario covers one behavior and has observable preconditions, action, and result.
- **Cover unhappy paths:** include only relevant errors and edge cases, but never omit material validation, authorization, privacy, security, recovery, or empty-state behavior.
- **Avoid hidden scope:** distinguish required behavior, non-goals, dependencies, and later work.
- **Mark uncertainty:** label inferred details with `[assumed]`; use `TBD` only when a value is expected but cannot yet be resolved.
- **Use evidence for technical constraints:** cite verified repository paths, interfaces, and existing modules when they materially constrain the story.
- **Use the team's estimation scale:** do not assume story-point meaning or convert points to time. If no scale exists, omit estimates or provide qualitative sizing with the uncertainty stated.
- **Split oversized stories:** split by workflow step, business rule, persona, operation, platform, or risk when a story cannot be completed and verified as one coherent increment.
- **Handle incomplete input:** ask one concise blocking question when the user or desired outcome is unknown; otherwise mark low-risk assumptions and proceed.
- **Surface conflicts:** identify contradictory requirements and the decision needed instead of silently choosing.

## Verification

Before finalizing, verify that:

- Every story identifies a specific user, capability, and meaningful outcome.
- Each story represents one coherent, independently valuable increment or explicitly states unavoidable dependencies.
- Acceptance criteria are unambiguous, observable, independently testable, and cover relevant failure behavior.
- Scope, non-goals, assumptions, dependencies, and open decisions are visible and do not contradict one another.
- Estimates, file paths, metrics, and technical constraints are evidence-based or clearly marked as uncertain.
- The output contains no unsupported claims, duplicated requirements, unresolved instructional placeholders, or unnecessary implementation detail.
