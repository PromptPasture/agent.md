# US-002: Generate Skill Evals

Source documents:

- [PRD.md](../PRD.md)
- [SPEC.md](../SPEC.md)

## 🛠️ Task Specification: Generate Skill Evals (US-002)

**SYSTEM:** You are an autonomous software engineer agent. Execute the following specification.

## 📖 1. User-Story Context

- **Persona:** As a skill library maintainer,
- **Action:** I want representative evals generated for each general skill,
- **Outcome:** so that trigger behavior and near-miss boundaries can be reviewed before release.
- **Epic Context:** Implements FR-012 from the approved SPEC. Evals are generated through `.agents/skills/create-skill/` and stored inside each skill folder.

---

## 🔍 2. Strict Constraints & Scope Boundaries

- **In-Scope:**
  - Generate `.agents/skills/<skill-name>/evals/evals.json` for each new skill.
  - Include 8-10 realistic prompts where possible, never fewer than 7.
  - Include at least 3 true-positive prompts, 2 false-positive prompts, and 2 non-trigger prompts per skill.
  - Include expected trigger behavior and expected output behavior for each eval.
  - Include boundary prompts for common overlaps from the SPEC.
- **Out-of-Scope (Do NOT implement):**
  - Do not hand-roll a different eval location or filename.
  - Do not store evals in a shared docs folder.
  - Do not create eval iteration output folders unless eval runs are actually executed.
- **Data Models & Schemas:**
  - Use the eval schema expected by `.agents/skills/create-skill/`.
  - Store eval cases at `.agents/skills/<skill-name>/evals/evals.json`.
  - Store run outputs only under `.agents/skills/<skill-name>/evals/iterations/iteration-N/` if runs are performed.

---

## ✅ 3. Executable Acceptance Criteria (Gherkin Format)

*Note to Agent: Use these exact scenarios to build and validate your logic.*

```gherkin
Scenario: Generate evals for each skill
  Given the nine new general skills exist
  When the agent generates evals through create-skill conventions
  Then each new skill has evals/evals.json
  And each eval file contains 8-10 realistic prompts where possible
  And no eval file contains fewer than 7 prompts

Scenario: Cover trigger and non-trigger behavior
  Given an eval file is inspected
  When the prompt categories are counted
  Then it includes at least 3 true-positive prompts
  And it includes at least 2 false-positive prompts
  And it includes at least 2 non-trigger prompts

Scenario: Preserve eval folder discipline
  Given no eval execution run has been performed
  When the skill folder is inspected
  Then evals/iterations/ does not exist only as a placeholder
```

---

## 🛠️ 4. Targeted Workspace & Codebase Context

*Note to Agent: You are restricted to modifying or analyzing the following components.*

- **Primary Target Files:**
  1. `.agents/skills/ask/evals/evals.json` -> Trigger and output evals.
  2. `.agents/skills/brainstorm/evals/evals.json` -> Trigger and output evals.
  3. `.agents/skills/classify/evals/evals.json` -> Trigger and output evals.
  4. `.agents/skills/plan/evals/evals.json` -> Trigger and output evals.
  5. `.agents/skills/explore/evals/evals.json` -> Trigger and output evals.
  6. `.agents/skills/choose/evals/evals.json` -> Trigger and output evals.
  7. `.agents/skills/manage/evals/evals.json` -> Trigger and output evals.
  8. `.agents/skills/remember/evals/evals.json` -> Trigger and output evals.
  9. `.agents/skills/adapt/evals/evals.json` -> Trigger and output evals.
- **Shared Dependencies/Imports:**
  - Follow `.agents/skills/create-skill/references/evaluation.md`.
  - Use boundary distinctions from [SPEC.md](../SPEC.md).

---

## 💻 5. Step-by-Step Implementation Protocol

*Note to Agent: Execute these steps sequentially. Verify state after each step.*

1. **Analyze & Validate:** Read [SPEC.md](../SPEC.md) Section 8 and `.agents/skills/create-skill/references/evaluation.md`.
2. **Generate Eval Cases:** Create prompt-level evals for each new skill.
3. **Check Counts:** Verify each eval file meets the 8-10 target where possible and never drops below 7.
4. **Check Boundary Coverage:** Confirm likely overlaps are represented across the relevant eval files.
5. **Validate JSON:** Ensure every `evals.json` file is valid JSON and follows the local create-skill expectations.

---

## 🏁 6. AI Agent Definition of Done (Validation Checklist)

*Note to Agent: You must run validation scripts to check these boxes before marked as complete.*

- [ ] **Compilation:** All new `evals/evals.json` files parse as valid JSON.
- [ ] **Test Coverage:** Every new skill has enough prompt coverage for trigger review.
- [ ] **No Regression:** No existing eval files are removed or moved.
- [ ] **Idempotency:** Re-running eval generation updates intended files without duplicating cases or creating empty iteration folders.
