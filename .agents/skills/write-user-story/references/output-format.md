# User Story Output Format

Use this reference when drafting user stories and developer tasks.

## Template

**Use the exact structure below for planning-oriented user stories.**

Use this exact structure. Repeat for each story.

```md
## 📖 User-Story [N]: [Short title]

### 👤 Story Definition
**As a** [user type],
**I want** [action or capability],
**so that** [benefit or outcome].

---

### 📊 Metadata
* **Story Points:** [1 / 2 / 3 / 5 / 8]
* **Priority:** [High / Medium / Low]
* **Epic/Feature Link:** [Link to parent epic or initiative]
* **Design/Figma Link:** [Link to UI/UX prototypes if applicable]

---

### 🎯 Context & Business Value
* [Briefly explain *why* this feature matters to the business or customer]
* [Mention any data analytics, customer feedback, or metrics this aims to improve]

---

### ✅ Acceptance Criteria (AC)

- [ ] **Scenario 1: [Happy Path Title]**
  - **Given** [initial context or state]
  - **When** [the user takes an action]
  - **Then** [the expected outcome occurs]

- [ ] **Scenario 2: [Alternative Path Title]**
  - **Given** [initial context or state]
  - **When** [the user takes an action]
  - **Then** [the expected outcome occurs]

- [ ] **Edge Case / Error Handling:** [e.g., Network timeout, invalid input formats, empty states]
- [ ] **Non-Functional / Security:** [e.g., Response time under 200ms, data masking, access control]

---

### 🛠️ Implementation Plan & Dev Tasks

*Target Components / Services:* [e.g., Frontend UI, Auth Service API, DB Schema]*

| # | Task Description | Effort | Notes / Technical Approach |
|---|------------------|--------|----------------------------|
| 1 | [e.g., Create database migration script for new fields] | [S/M/L] | See module `src/db/models` |
| 2 | [e.g., Implement X endpoint in Y service controller] | [S/M/L] | Secure with JWT middleware |
| 3 | [e.g., Build frontend UI component with loading states] | [S/M/L] | Match Figma spacing tokens |
| 4 | [e.g., Write unit and integration tests] | [S/M/L] | Target >80% code coverage |

---

### 🧪 QA & Verification Notes
- [ ] [Story-specific testing constraint, e.g., "Must test cross-browser on Safari Mobile"]
- [ ] [Feature flag or environment variables required to test: `FEATURE_ENABLE_X=true`]
- [ ] [Specific test data required: e.g., "Needs an account with expired subscription status"]
```
