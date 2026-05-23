# US-004: Prepare Release Handoff

Source documents:

- [PRD.md](../PRD.md)
- [SPEC.md](../SPEC.md)

## 🛠️ Task Specification: Prepare Release Handoff (US-004)

**SYSTEM:** You are an autonomous software engineer agent. Execute the following specification.

## 📖 1. User-Story Context

- **Persona:** As the project owner,
- **Action:** I want a concise release handoff for the general skills work,
- **Outcome:** so that a reviewer or future agent can understand what changed, what was validated, and what remains.
- **Epic Context:** Completes release readiness for the approved General Agent Skills effort without adding external integrations or unnecessary documentation.

---

## 🔍 2. Strict Constraints & Scope Boundaries

- **In-Scope:**
  - Summarize created or updated skill files.
  - Summarize validation commands and results.
  - Note any deviations from the approved SPEC.
  - Record durable implementation observations in `.agents/memory/` only if they are useful beyond the task.
- **Out-of-Scope (Do NOT implement):**
  - Do not create a new PRD, SPEC, architecture doc, or design doc.
  - Do not record transient task chatter in memory.
  - Do not mark unresolved validation failures as complete.
- **Data Models & Schemas:**
  - No data model changes.
  - Use existing `.agents/memory/` conventions if memory is updated.

---

## ✅ 3. Executable Acceptance Criteria (Gherkin Format)

*Note to Agent: Use these exact scenarios to build and validate your logic.*

```gherkin
Scenario: Produce implementation handoff
  Given the skill authoring, eval generation, and validation work is complete
  When the agent prepares the handoff
  Then it lists the created or updated files
  And it lists validation commands and outcomes
  And it calls out any unresolved issues or says none remain

Scenario: Record only durable memory
  Given the implementation produces a reusable project fact or decision
  When the agent considers memory updates
  Then it writes only durable project value to .agents/memory/
  And it avoids duplicating the PRD, SPEC, or story contents

Scenario: Avoid false completion
  Given one or more validation checks could not run or failed
  When the handoff is prepared
  Then the limitation is stated plainly
  And the work is not described as fully validated
```

---

## 🛠️ 4. Targeted Workspace & Codebase Context

*Note to Agent: You are restricted to modifying or analyzing the following components.*

- **Primary Target Files:**
  1. `.agents/skills/<skill-name>/` -> Created skill artifacts.
  2. `.agents/skills/README.md` -> Index updates, if any.
  3. `.agents/memory/YYYY-MM-DD.md` -> Optional durable implementation notes.
- **Shared Dependencies/Imports:**
  - Use [SPEC.md](../SPEC.md) as the completion contract.
  - Use existing `.agents/memory/MEMORY.md` and dated memory conventions.

---

## 💻 5. Step-by-Step Implementation Protocol

*Note to Agent: Execute these steps sequentially. Verify state after each step.*

1. **Analyze & Validate:** Inspect git diff and validation output from prior stories.
2. **Summarize Scope:** List new skills, eval files, and index changes.
3. **Capture Validation:** Record commands run and outcomes.
4. **Check Deviations:** Compare final state to [SPEC.md](../SPEC.md).
5. **Write Durable Notes:** Update memory only for facts worth keeping after the task ends.

---

## 🏁 6. AI Agent Definition of Done (Validation Checklist)

*Note to Agent: You must run validation scripts to check these boxes before marked as complete.*

- [ ] **Compilation:** Not applicable; handoff documentation only.
- [ ] **Test Coverage:** Handoff includes validation evidence or explicitly states what could not be validated.
- [ ] **No Regression:** No approved PRD/SPEC scope is silently changed during handoff.
- [ ] **Idempotency:** Re-running handoff generation updates notes without duplicating memory entries.
