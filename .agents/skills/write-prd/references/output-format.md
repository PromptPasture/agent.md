# PRD Output Format

**Use this reference when drafting the final PRD.**

---

## Template

Use this structure exactly unless the user provides a stricter template:

```md
---
status: "[DRAFT | IN_REVIEW | APPROVED]"
documentType: PRD
phase: "[discovery | delivery | maintenance]"
createdAt: "[YYYY-MM-DD]"
updatedAt: "[YYYY-MM-DD]"
author: "[Name]"
owner: "[Name or TBD]"
stakeholders: "[Names, teams, or TBD]"
tags:
  - "[tag]"
related:
  - "[SPEC.md or related doc]"
---

# PRD: [Product / Feature Name]

## 🎯 Objective

[1–3 paragraphs defining: User Pain, Target Persona, Market Timing, and Cost of Inaction. Keep technical solution details out of this section.]

---

## 📊 Goals

| Goal ID | Target Outcome | Success Metric |
| --- | --- | --- |
| G-1 | [Outcome] | [Measurable indicator, target, or proxy] |

---

## 👥 Target Audience Focus

[For each persona: role, context, key jobs-to-be-done]

- **Persona ID: P-1** [Name / Role]: Context, frustrations, and key jobs-to-be-done.
- **Persona ID: P-2** [Name / Role]: Context, frustrations, and key jobs-to-be-done.

---

## 📐 Scope

### ✅ In Scope

- [Concrete capability or deliverable]

### 🚫 Out of Scope

- [Explicit exclusions to prevent scope creep]

### ⏳ Later [optional]

- [Items deliberately deferred to a future phase]

---

## 📋 Functional Requirements

| Requirement ID | Capability / Feature | Priority | Acceptance Criteria | Tracker |
| --- | --- | --- | --- | --- |
| FR-1 | [Outcome-focused requirement] | [MUST / SHOULD / COULD] | - Criteria 1<br>- Criteria 2 | [URL or TBD] |

---

## ⚡ Non-Functional Requirements [optional]

[Performance, availability, security, compliance, accessibility, data, operational, or localization requirements. Keep this summary-level unless the user asks for a technical spec.]

| NFR ID | Category | Target Specification |
| --- | --- | --- |
| NFR-1 | [Performance / Security / Accessibility] | [Quantifiable engineering constraint] |

---

## 🌟 Milestones [optional]

| Milestone | Target Date | Exit Criteria | Owner |
| --- | --- | --- | --- |
| M-1 | [YYYY-MM-DD] | [Quantifiable milestone gate] | [Name] |

---

## 👤 User Interaction [optional]

[Key interaction patterns, input methods, feedback mechanisms, error states, or UX notes that directly affect implementation.]

---

## 🎨 Design [optional]

[Links to wireframes, prototypes, design system component references, or screenshots.]

---

## 🗺️ User Journeys / Key Flows [optional]

[Describe 1–3 critical user flows as explicit, chronological numbered steps.]

---

## 🤔 Risks, Assumptions, & Mitigations

| Risk ID | Assumption / Risk Description | Impact (H/M/L) | Mitigation Strategy | Status |
| --- | --- | --- | --- | --- |
| R-1 | [Risk description or dependency assumption] | [HIGH / MEDIUM / LOW] | [Engineering or product workaround] | [OPEN / CLOSED] |

---

## 🔗 External Dependencies [optional]

[External items or deliverables that must be true or completed before this work can proceed or be verified.]

| Dependency ID | Item | Impacted Requirements | Validation Owner |
| --- | --- | --- | --- |
| D-1 | [System, API, or team dependency] | [e.g., FR-1, FR-2] | [Name] |

---

## ❓ Open Questions [optional]

| Question ID | Question | Answer / Decision | Owner | Resolution Date |
| --- | --- | --- | --- | --- |
| Q-1 | [Question to resolve before or during implementation] | [TBD / Decision text] | [Name] | [YYYY-MM-DD or TBD] |

---

## 📚 Reference Links [optional]

[Customer interviews, research, analytics, related docs, prior discussions, technical docs, demos, or glossary entries.]

- **Ref-1**: [Description of link, e.g., Customer Interview Notes] - [URL]
- **Ref-2**: [Description of link, e.g., Technical API Documentation] - [URL]
```

---

## Section Rules

Keep the main PRD short enough to function as the initiative landing page. Link to deeper source material rather than copying long research notes, technical designs, or implementation plans into the PRD.

Use frontmatter for document-level metadata instead of a body "Product Overview" table. Keep frontmatter narrow: status, document type, phase, dates, author/owner, stakeholders, tags, and related docs. Add optional fields such as `targetDate`, `tracker`, `designsLink`, or `demoLink` only when they have real values. Quote date-like values so CLI agents and YAML parsers keep them as strings.

Use `TBD` for genuinely unknown fields when the missing value is expected, and `[assumed]` for inferred content the user should verify.
