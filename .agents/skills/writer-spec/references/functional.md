# Functional Requirements Specification: [System / Module Name]

**Version:** [1.0 Draft]
**Date:** [YYYY-MM-DD]
**Status:** [DRAFT | IN REVIEW | APPROVED]

## 1. Overview

**Summarize the system purpose and business context.**

[2–4 sentences: what system, its purpose, business context.]

## 2. Purpose & Success Measures

**Connect the functional scope to measurable outcomes.**

| Purpose / Outcome | Success Measure | Target |
| ----------------- | --------------- | ------ |

## 3. Roles & Responsibilities

**Name who owns decisions and delivery responsibilities.**

| Role / Team | Responsibility | Decision Area |
| ----------- | -------------- | ------------- |

## 4. Actors

**Identify every human, system, or scheduled actor in scope.**

| Actor | Type | Description |
| ------ | ---------------------------- | --------------------------- |
| [Name] | [Human / System / Scheduled] | [Role and key interactions] |

## 5. System Boundary

**Separate the specified system from external dependencies.**

[What is inside this spec vs. what interacts from outside. Bulleted list of external systems suffices.]

## 6. Scope

**State included and excluded behavior explicitly.**

### In Scope

- **Included:** [Feature, function, or workflow]

### Out of Scope

- **Excluded:** [Excluded feature or future consideration]

## 7. Data Entities (Conceptual)

**List the business entities needed to understand behavior.**

| Entity | Key Attributes | Notes |
| ------ | -------------- | ----- |

## 8. Functional Requirements

**Describe testable behavior by capability area or workflow.**

### 8.1 [Capability Area / Actor Workflow]

**FR-[N]-[M]: [Requirement name]**

- **Description:** The system shall…
- **Trigger:** [What initiates this behavior]
- **Preconditions:** [What must be true before]
- **Postconditions:** [What is true after successful completion]
- **Business Rules:** [Reference by BR-N]
- **Error Conditions:** [What happens when preconditions aren't met or processing fails]

## 9. Business Rules

**Capture constraints that govern functional behavior.**

| Rule ID | Rule | Applies To |
| ------- | ---- | ---------- |

## 10. Data Validation Rules

**Define field-level rules and user-facing error messages.**

| Field | Validation | Error Message |
| ----- | ---------- | ------------- |

## 11. State Transitions (if applicable)

**Document valid lifecycle movement and guards.**

| From State | Event | To State | Guards |
| ---------- | ----- | -------- | ------ |

## 12. Test Plan

**Map required behavior to verification scenarios.**

| Scenario | Expected Result | Test Level |
| -------- | --------------- | ---------- |

## 13. Release & Support Readiness

**List launch activities needed for operational handoff.**

| Activity | Owner | Notes |
| -------- | ----- | ----- |
| Documentation | | |
| Support training | | |
| Rollout / communication | | |
| Feedback collection | | |

## 14. Non-Functional Requirements (brief)

**Call out the most important quality constraints.**

[Most critical NFRs only. For a full NFR spec, use the NFR spec type.]

## 15. Assumptions & Constraints

**Separate inferred details from known constraints.**

| # | Type | Detail |
| --- | ---------- | --------- |
| A-1 | Assumption | [assumed] |

## 16. Open Issues

**Track unresolved decisions and questions.**

- [ ] **Open question:** [Question or decision needed]

## Appendix: Glossary

**Define terms that reviewers must interpret consistently.**

| Term | Definition |
| ---- | ---------- |
