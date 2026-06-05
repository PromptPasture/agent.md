# User Story AI Output Format

Use this reference when drafting user stories and developer tasks for an AI coding agent.

---

## Template

Use this exact structure. Repeat for each story.

```md
---
status: "[DRAFT | READY | IN_PROGRESS | DONE]"
documentType: AI_IMPLEMENTATION_STORY
phase: "[delivery | maintenance]"
storyId: "[US-N]"
storyPoints: "[1 | 2 | 3 | 5 | 8]"
priority: "[High | Medium | Low]"
owner: "[agent, team, or assignee]"
epic: "[Link to parent epic or initiative]"
tags:
  - "[tag]"
related:
  - "[PRD.md, SPEC.md, issue, or related doc]"
---

## 🛠️ Task Specification: [Short Title] ([Story ID])
# SYSTEM: You are an autonomous software engineer agent. Execute the following specification.

## 📖 1. User-Story Context
*   **Persona:** As a [user type],
*   **Action:** I want [action or capability],
*   **Outcome:** so that [benefit or outcome].
*   **Epic Context:** [Provide high-level architecture goal or epic link]

---

## 🔍 2. Strict Constraints & Scope Boundaries
*   **In-Scope:**
    *   [Explicitly state what the AI MUST implement, e.g., "Only the API endpoint, no UI changes"]
*   **Out-of-Scope (Do NOT implement):**
    *   [Explicitly state boundaries to prevent AI scope creep, e.g., "Do not touch billing logic"]
*   **Data Models & Schemas:**
    *   [Provide expected input/output JSON schemas or database fields here]

---

## ✅ 3. Executable Acceptance Criteria (Gherkin Format)
*Note to Agent: Use these exact scenarios to build and validate your logic.*

```gherkin
Scenario: [Happy Path Title]
  Given [initial state or system configuration]
  And [additional prerequisite]
  When [the agent/user executes action]
  Then [precise, verifiable system state change occurs]
  And [response status code or exact payload match]

Scenario: [Error/Edge Case Path Title]
  Given [initial state]
  When [invalid action or bad payload is sent]
  Then [system handles safely without crashing]
  And [returns specific error code: e.g., 400 Bad Request]
```

---

## 🛠️ 4. Targeted Workspace & Codebase Context

*Note to Agent: You are restricted to modifying or analyzing the following components.*

* **Primary Target Files:**
    1. `[path/to/exact/file.ts]` -> [Responsibility: e.g., Controller layer]
    2. `[path/to/another/file.spec.ts]` -> [Responsibility: e.g., Unit tests]
* **Shared Dependencies/Imports:**
  * Use existing utilities in `[path/to/shared/utils]`. Do NOT create duplicate helper functions.

---

## 💻 5. Step-by-Step Implementation Protocol

*Note to Agent: Execute these steps sequentially. Verify state after each step.*

1. **Analyze & Validate:** Inspect `[Target Files]` and verify that no breaking changes will occur to existing exports.
2. **Scaffold Interface:** Define types/interfaces matching the schema provided in Section 2.
3. **Implement Core Logic:** Write the business logic fulfilling the Gherkin scenarios.
4. **Write Tests:** Create automated tests inside `[Test File Path]` covering all happy and edge paths.

---

## 🏁 6. AI Agent Definition of Done (Validation Checklist)

*Note to Agent: You must run validation scripts to check these boxes before marked as complete.*

* [ ] **Compilation:** Code compiles successfully with zero linter errors (`npm run lint` / `cargo check`).
* [ ] **Test Coverage:** Execution of `[your test command]` passes successfully with 100% success rate on new code.
* [ ] **No Regression:** Existing test suites pass without modifications to unrelated tests.
* [ ] **Idempotency:** Code can run multiple times without corrupting state or database tables.

```
