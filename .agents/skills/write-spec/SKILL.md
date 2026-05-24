---
name: write-spec
description: >
  Write product specifications and requirements documents. Use for tech specs, design docs,
  TDDs, functional or non-functional requirements, data contracts, UI specs, release specs,
  handoff docs, and system behavior.
license: MIT
tags:
  - writer
  - specification
  - requirements
metadata:
  author: Oleg Shulyakov
  version: "1.3.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-team-roles
  category: documentation
---

# write-spec

A **router** skill to generate specific product specification document types. Identify user intent, select the matching spec type, and produce the document using its reference format. For ambiguous or multi-type requests, combine sections and note the merged types.

## Product Specification Model

**A product specification is the development blueprint, not just a requirements list.**

A strong product specification aligns the team on what is being built, why it matters, how the customer will use it, and how success will be measured. It should reduce ambiguity, feature creep, delays, and cross-functional disagreement by making responsibilities, scope, design, test plans, release work, and ongoing management explicit.

When product intent is missing, ask for or infer it before writing technical detail. If the user needs product purpose, personas, market context, or success metrics more than delivery detail, route them to `write-prd` first or state the assumptions clearly.

## Routing Table

**Choose the most specific spec reference for the requested document type.**

| Request Type | Reference |
| :------------------------------------------------- | :----------------------------- |
| Tech spec, design doc, TDD, end-to-end spec | `references/technical.md` |
| Functional requirements, use cases, business rules | `references/functional.md` |
| Non-functional requirements, SLAs, performance | `references/non-functional.md` |
| Data contract, event schema, data SLA | `references/data-contract.md` |
| UI/UX spec, design handoff, component states | `references/design-ui.md` |
| Release plan, rollout activities, training, documentation, support readiness | `references/technical.md` plus release sections |

## Writing Rules (All Specs)

**Every spec should produce behavior that can be reviewed and tested.**

- **Be specific & testable**: Requirements must translate directly to test cases (e.g., "Token expires after 15m").
- **Keep it simple**: Choose the smallest complete specification shape that resolves the user's decision or handoff need.
- **Behavioral, not implementational**: Describe what it does, not how it's built.
- **Define roles and decisions**: Name owners, reviewers, stakeholders, and decision areas when known.
- **Tie scope to success**: Include purpose, scope, non-goals, success measures, risks, assumptions, and excluded features where relevant.
- **Connect design and behavior**: Link or summarize workflows, UI states, high-level architecture, and user interactions when they affect requirements.
- **Plan verification and release**: Include test plans, privacy/data handling, rollout, training, documentation, support readiness, and feedback collection when the spec affects launch.
- **Use STAR for scenarios**: When examples, use cases, or incident-style context are needed, include situation, task, action, and expected result.
- **Mandatory Error Paths**: Requirements lacking error conditions are incomplete.
- **Document Omissions**: Explicitly state what is out of scope.
- **Mark Inferences**: Flag assumed details with `[assumed]`.

## Product Spec Workflow

**Research, define, specify, review, then distribute.**

Before drafting, gather customer problems, service tickets, feature requests, complaints, analytics, existing PRDs, designs, and implementation constraints when available. Define the purpose in customer and business terms, then document functional and technical requirements from user stories and project scope. Include review feedback or open questions when information is incomplete. The final spec should be ready for cross-functional review and development handoff.
