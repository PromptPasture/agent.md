# Functional Requirements Specification

Use this template for functional requirements, use cases, workflows, and business rules.

---

## Metadata Template

```yaml
status: "[DRAFT | IN_REVIEW | APPROVED]"
documentType: SPEC
phase: "[discovery | delivery | maintenance]"
version: "[1.0]"
createdAt: "[YYYY-MM-DD]"
updatedAt: "[YYYY-MM-DD]"
author: "[name or team]"
tags:
  - "[functional-requirements]"
related:
  - "[PRD.md or related doc]"
```

---

## Document Template

```markdown
# Functional Requirements Specification: [System / Module Name]

## 1. Overview

[2–4 sentences: what system, its purpose, business context.]

---

## 2. Purpose & Success Measures

|Purpose / Outcome|Success Measure|Target|
|-----------------|---------------|------|

---

## 3. Roles & Responsibilities

|Role / Team|Responsibility|Decision Area|
|-----------|--------------|-------------|

---

## 4. Actors

|Actor|Type|Description|
|------|----------------------------|---------------------------|
|[Name]|[Human / System / Scheduled]|[Role and key interactions]|

---

## 5. System Boundary

[What is inside this spec vs. what interacts from outside. Bulleted list of external systems suffices.]

---

## 6. Scope

### In Scope

- **Included:** [Feature, function, or workflow]

### Out of Scope

- **Excluded:** [Excluded feature or future consideration]

---

## 7. Data Entities (Conceptual)

|Entity|Key Attributes|Notes|
|------|--------------|-----|

---

## 8. Functional Requirements

### 8.1 [Capability Area / Actor Workflow]

**FR-[N]-[M]: [Requirement name]**

- **Description:** The system shall…
- **Trigger:** [What initiates this behavior]
- **Preconditions:** [What must be true before]
- **Postconditions:** [What is true after successful completion]
- **Business Rules:** [Reference by BR-N]
- **Error Conditions:** [What happens when preconditions aren't met or processing fails]

---

## 9. Business Rules

|Rule ID|Rule|Applies To|
|-------|----|----------|

---

## 10. Data Validation Rules

|Field|Validation|Error Message|
|-----|----------|-------------|

---

## 11. State Transitions (if applicable)

|From State|Event|To State|Guards|
|----------|-----|--------|------|

---

## 12. Test Plan

|Scenario|Expected Result|Test Level|
|--------|---------------|----------|

---

## 13. Release & Support Readiness

|Activity|Owner|Notes|
|--------|-----|-----|
|Documentation|||
|Support training|||
|Rollout / communication|||
|Feedback collection|||

---

## 14. Non-Functional Requirements (brief)

[Most critical NFRs only. For a full NFR spec, use the NFR spec type.]

---

## 15. Assumptions & Constraints

|#|Type|Detail|
|---| ---------- | --------- |
|A-1|Assumption|[assumed]|

---

## 16. Open Issues

- [ ] **Open question:** [Question or decision needed]

---

## Appendix: Glossary

|Term|Definition|
|----|----------|
```
