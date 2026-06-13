---
name: write-spec
description: >
  Write product specifications and requirements documents. Use for tech specs, design docs,
  TDDs, functional or non-functional requirements, data contracts, UI specs, release specs,
  handoff docs, and system behavior.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.4.2"
  source: github.com/olegshulyakov/agent.md
  catalog: product
  category: requirements
  tags: [writer, specification, requirements]
---

# write-spec

A **router** skill to generate specific product specification document types. Identify user intent, select the matching spec type, and produce the document using its reference format. For ambiguous or multi-type requests, combine sections and note the merged types.

---

## Product Specification Model

A strong product specification aligns the team on what is being built, why it matters, how the customer will use it, and how success will be measured. It should reduce ambiguity, feature creep, delays, and cross-functional disagreement by making responsibilities, scope, design, test plans, release work, and ongoing management explicit.

When product intent is missing, ask for or infer it before writing technical detail. If the user needs product purpose, personas, market context, or success metrics more than delivery detail, route them to `write-prd` first or state the assumptions clearly.

---

## Routing Table

| Request Type | Reference |
| :------------------------------------------------- | :----------------------------- |
| Tech spec, design doc, TDD, end-to-end spec | `references/technical.md` |
| Functional requirements, use cases, business rules | `references/functional.md` |
| Non-functional requirements, SLAs, performance | `references/non-functional.md` |
| Data contract, event schema, data SLA | `references/data-contract.md` |
| UI/UX spec, design handoff, component states | `references/design-ui.md` |
| Release plan, rollout activities, training, documentation, support readiness | `references/technical.md` plus release sections |

---

## Writing Rules (All Specs)

- **Be specific & testable**: Requirements must translate directly to test cases (e.g., "Token expires after 15m").
- **Keep it simple**: Choose the smallest complete specification shape that resolves the user's decision or handoff need.
- **Behavioral, not implementational**: Describe what it does, not how it's built.
- **Define roles and decisions**: Name owners, reviewers, stakeholders, and decision areas when known.
- **Use frontmatter for metadata**: Put document status, type, phase, version, dates, author/owner, tags, and related docs in YAML frontmatter instead of a body "Document Info" block. Add optional fields such as `reviewers`, `targetDate`, or `tracker` only when they have real value.
- **Use real Markdown structure**: Use `###`/`####` headings for named flows, decisions, examples, and subsections. Do not use bold-only lines as pseudo-headings, because they fail Markdown lint rules such as `MD036`.
- **Tie scope to success**: Include purpose, scope, non-goals, success measures, risks, assumptions, and excluded features where relevant.
- **Connect design and behavior**: Link or summarize workflows, UI states, high-level architecture, and user interactions when they affect requirements.
- **Plan verification and release**: Include test plans, privacy/data handling, rollout, training, documentation, support readiness, and feedback collection when the spec affects launch.
- **Use STAR for scenarios**: When examples, use cases, or incident-style context are needed, include situation, task, action, and expected result.
- **Mandatory Error Paths**: Requirements lacking error conditions are incomplete.
- **Document Omissions**: Explicitly state what is out of scope.
- **Mark Inferences**: Flag assumed details with `[assumed]`.

---

## Product Spec Workflow

Before drafting, gather customer problems, service tickets, feature requests, complaints, analytics, existing PRDs, designs, and implementation constraints when available. Define the purpose in customer and business terms, then document functional and technical requirements from user stories and project scope. Include review feedback or open questions when information is incomplete. The final spec should be ready for cross-functional review and development handoff.

---

## Verification

Confirm the selected reference matches the requested spec type, the document includes measurable acceptance or verification criteria, and assumptions are marked with `[assumed]`. Check that scope, non-goals, error paths, owners, and release or support readiness are explicit when relevant.
