# PRD Output Format

Use this reference when drafting the final PRD.

## Template

Always produce a Markdown file. Use this structure exactly unless the user provides a stricter template:

```md
# PRD: [Product / Feature Name]

## Product Overview

| Field | Value |
| --- | --- |
| Document status | Draft / In Review / Approved |
| Target date | [date or TBD] |
| Owner | [if known, else TBD] |
| Team members | [names or teams, else TBD] |
| Stakeholders | [list if mentioned, else TBD] |
| Designs | [links or TBD] |
| Demo | [links or TBD] |
| Work tracker | [Jira/GitHub/Linear links or TBD] |
| Last updated | [date] |

## Objective

[1–3 paragraphs. What pain exists? Who feels it? Why now? What's the cost of inaction?]

## Goals

| Goal | Success Metric |
| --- | --- |
| [Outcome] | [Measurable indicator, target, or proxy] |

## Target Users / Personas

[For each persona: role, context, key jobs-to-be-done, frustrations]

## User Stories

| User Story | Priority | Success / Acceptance Signal |
| --- | --- | --- |
| As a [persona], I want [capability], so that [outcome]. | High / Medium / Low | [metric, behavior, or validation] |

## Scope

### In Scope

- [Concrete capability or deliverable]

### Out of Scope [optional]

- [Explicit exclusions to prevent scope creep]
- [Items that may be considered later should be marked as Later, not silently implied]

## Requirements

| Requirement | User Story / Need | Importance | Tracker | Notes |
| --- | --- | --- | --- | --- |
| [Outcome-focused requirement] | [Related story or need] | High / Medium / Low | [issue/link or TBD] | [constraints, acceptance notes, or evidence] |

## Non-Functional Requirements

[Performance, availability, security, compliance, accessibility, data, operational, or localization requirements. Keep this summary-level unless the user asks for a technical spec.]

## Milestones [optional]

| Milestone | Target Date | Exit Criteria | Owner |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

## User Interaction & Design [optional]

[Links to wireframes, prototypes, design explorations, screenshots, demos, or UX notes. Summarize only the decisions that affect requirements.]

## User Journeys / Key Flows [optional]

[1–3 critical flows described as numbered steps. Diagrams optional but welcome.]

## Assumptions & Dependencies

| Item | Type | Detail | Validation / Owner |
| --- | --- | --- | --- |
| ... | Assumption / Dependency | ... | ... |

## Open Questions

| Question | Answer / Decision | Owner | Date Answered |
| --- | --- | --- | --- |
| [Question that must be resolved before or during implementation] | TBD | ... | ... |

## Reference Links [optional]

[Customer interviews, research, analytics, related docs, prior discussions, technical docs, demos, or glossary entries.]
```

## Section Rules

Keep the main PRD short enough to function as the initiative landing page. Link to deeper source material rather than copying long research notes, technical designs, or implementation plans into the PRD.

Use `TBD` for genuinely unknown fields when the missing value is expected, and `[assumed]` for inferred content the user should verify.
