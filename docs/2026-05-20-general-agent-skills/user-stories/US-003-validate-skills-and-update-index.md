# US-003: Validate Skills and Update Index

Source documents:

- [PRD.md](../PRD.md)
- [SPEC.md](../SPEC.md)

## 🛠️ Task Specification: Validate Skills and Update Index (US-003)

**SYSTEM:** You are an autonomous software engineer agent. Execute the following specification.

## 📖 1. User-Story Context

- **Persona:** As a skill library maintainer,
- **Action:** I want the general skills validated and indexed,
- **Outcome:** so that the skill library can expose the new skills consistently and catch authoring issues before release.
- **Epic Context:** Implements the validation and release-readiness portions of the approved SPEC.

---

## 🔍 2. Strict Constraints & Scope Boundaries

- **In-Scope:**
  - Run available create-skill validation checks on each new skill.
  - Review line counts, metadata, section style, and runtime standalone behavior.
  - Update `.agents/skills/README.md` if it indexes maintained skills.
  - Fix validation failures that are directly related to the new skills.
- **Out-of-Scope (Do NOT implement):**
  - Do not refactor unrelated existing skills.
  - Do not change project-level `AGENTS.md`.
  - Do not introduce a shared trigger-overlap harness.
  - Do not package or publish skills unless explicitly requested.
- **Data Models & Schemas:**
  - No runtime data model changes.
  - README entries shall follow existing `.agents/skills/README.md` conventions.

---

## ✅ 3. Executable Acceptance Criteria (Gherkin Format)

*Note to Agent: Use these exact scenarios to build and validate your logic.*

```gherkin
Scenario: Validate each new skill
  Given a new skill folder exists with SKILL.md and evals/evals.yaml
  When create-skill validation is run against the skill folder
  Then validation passes
  And any failures are fixed or documented with a clear reason

Scenario: Update skill index when present
  Given .agents/skills/README.md indexes maintained skills
  When the new general skills are ready
  Then the README includes the new skills using the existing index format
  And unrelated README sections remain unchanged

Scenario: Prevent runtime coupling
  Given the new SKILL.md files are searched
  When runtime dependency language is found
  Then it is removed or rewritten as development-time guidance
  And the skill remains independently installable
```

---

## 🛠️ 4. Targeted Workspace & Codebase Context

*Note to Agent: You are restricted to modifying or analyzing the following components.*

- **Primary Target Files:**
  1. `.agents/skills/<skill-name>/SKILL.md` -> Validation target.
  2. `.agents/skills/<skill-name>/evals/evals.yaml` -> Validation target.
  3. `.agents/skills/README.md` -> Skill index, if present.
- **Shared Dependencies/Imports:**
  - Use `.agents/skills/create-skill/scripts/validate.py` when available.
  - Follow `.agents/skills/create-skill/references/authoring.md`.

---

## 💻 5. Step-by-Step Implementation Protocol

*Note to Agent: Execute these steps sequentially. Verify state after each step.*

1. **Analyze & Validate:** Inspect `.agents/skills/README.md` and create-skill validation scripts.
2. **Run Validation:** Run quick validation for each new skill directory.
3. **Fix Failures:** Apply focused fixes to new skill files and evals.
4. **Update Index:** Add new skills to the README only if the README indexes maintained skills.
5. **Run Final Checks:** Re-run validation or targeted checks after fixes.

---

## 🏁 6. AI Agent Definition of Done (Validation Checklist)

*Note to Agent: You must run validation scripts to check these boxes before marked as complete.*

- [ ] **Compilation:** Markdown and JSON files pass local validation/parsing checks.
- [ ] **Test Coverage:** Creator-skill validation passes for each new skill or any exception is documented.
- [ ] **No Regression:** Existing skills and README entries are not rewritten outside the required index additions.
- [ ] **Idempotency:** Re-running validation and README update does not duplicate entries.
