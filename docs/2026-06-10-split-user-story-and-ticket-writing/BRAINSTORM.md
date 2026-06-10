# Split User Story and Ticket Writing

## Outcome

Separate user-story writing from generic Jira, GitHub, and Linear ticket
writing so each artifact uses language appropriate to its purpose.

`write-user-story` remains focused on independently valuable user outcomes.
A new `write-ticket` skill produces tracker work items without forcing them
into persona-based user-story language.

## Skill Boundaries

### `write-user-story`

Produces user stories centered on one persona, capability, and meaningful
outcome. It uses story-specific practices such as:

- `As a / I want / so that` framing
- Card, Conversation, Confirmation
- INVEST
- acceptance criteria describing observable user or system behavior

It does not handle generic tracker tickets or task breakdowns unless the user
explicitly requests a user story as one of multiple artifacts.

### `write-ticket`

Produces Jira, GitHub, Linear, or standalone Markdown work items. It infers the
ticket type from the request and writes the content according to that type.
It does not force persona language, user-value framing, or INVEST onto work
that is not a user story.

The initial ticket types are:

- bug
- feature
- task
- spike

Chore and documentation requests map to `task`. When the type is genuinely
ambiguous, the skill defaults to `task` and states the assumption when it
matters to the result.

## Ticket Writing Models

### Bug

A bug ticket includes:

- concise problem context
- reproduction steps
- actual result
- expected result
- impact
- completion criteria

### Feature

A feature ticket includes:

- problem
- desired outcome
- scope
- non-goals when they prevent material ambiguity
- requirements
- acceptance criteria

Feature tickets describe the requested capability without requiring
persona-based story syntax.

### Task

A task ticket includes:

- objective
- required work
- relevant constraints
- completion criteria
- verification

### Spike

A spike ticket includes:

- question to answer
- investigation scope
- expected deliverable
- stopping condition or timebox when known

## Tracker Adaptation

All tracker outputs use the same type-specific writing models. Tracker
adaptation changes field placement and metadata, not the meaning or style of
the prose.

- Jira output may map issue type, priority, labels, epic, and ownership to
  native fields.
- GitHub output may use labels, linked issues, issue-form conventions, and task
  lists where appropriate.
- Linear output may map team, project, priority, labels, and relationships to
  native fields.
- Standalone Markdown keeps relevant metadata in YAML frontmatter.

A user-provided template takes precedence when it is stricter than the
skill's default output.

## Routing

- A request for a user story triggers `write-user-story`.
- A request for a Jira, GitHub, Linear, bug, feature, task, chore,
  documentation, or spike ticket triggers `write-ticket`.
- A request that explicitly asks for both artifacts may trigger both skills.
  Each skill produces only its own artifact.
- Neither skill invokes, derives, converts, or delegates to the other.
- Converting an existing user story into tickets, or tickets into a user
  story, requires an explicit user request.

When both skills are triggered, output order follows the user's request.
Otherwise, present the user story before the tickets.

## Implementation Scope

The implementation should:

- narrow the `write-user-story` description, workflow, output, writing rules,
  and verification to user stories
- add a focused `write-ticket` skill with the four agreed writing models
- update the skill catalog so generic tracker tickets route to `write-ticket`
- increment `write-user-story`'s semantic version because its trigger and
  responsibilities change
- add or update validation cases for routing and artifact behavior

The implementation should not add live tracker integrations, automatic
cross-skill conversion, additional ticket types, or a shared work-item router.

## Verification

Validate the skill behavior with prompts for:

- a standalone user story
- a Jira or GitHub bug ticket
- a feature ticket without persona language
- a task, chore, and documentation ticket using the task model
- a spike with a defined investigation deliverable
- an ambiguous generic ticket that reasonably defaults to task
- one prompt explicitly requesting both a user story and tickets
- an explicit conversion request

Verification passes when:

- generic ticket requests do not produce `As a / I want / so that` framing
- user-story requests retain persona, outcome, INVEST, and story acceptance
  criteria guidance
- each ticket type uses its agreed content model
- tracker adaptation affects fields and metadata without rewriting the item as
  a user story
- neither skill claims to invoke or automatically convert through the other
