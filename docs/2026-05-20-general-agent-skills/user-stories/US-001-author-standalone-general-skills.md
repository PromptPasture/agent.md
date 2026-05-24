# US-001: Author Standalone General Skills

Source documents:

- [PRD.md](../PRD.md)
- [SPEC.md](../SPEC.md)

## 🛠️ Task Specification: Author Standalone General Skills (US-001)

**SYSTEM:** You are an autonomous software engineer agent. Execute the following specification.

## 📖 1. User-Story Context

- **Persona:** As a skill library maintainer,
- **Action:** I want the missing general-purpose agent skills authored as standalone installable skill folders,
- **Outcome:** so that users can invoke consistent collaboration modes without hidden runtime dependencies.
- **Epic Context:** Implements the approved General Agent Skills PRD/SPEC by creating `ask-questions`, `reason-problem`, `classify-content`, `plan-work`, `explore-context`, `decide-direction`, `coordinate-work`, `remember-context`, and `adapt`. Existing `explain-topic` is already complete and must not be rewritten unless validation reveals a spec violation.

---

## 🔍 2. Strict Constraints & Scope Boundaries

- **In-Scope:**
  - Create `.agents/skills/<skill-name>/SKILL.md` for `ask-questions`, `reason-problem`, `classify-content`, `plan-work`, `explore-context`, `decide-direction`, `coordinate-work`, `remember-context`, and `adapt`.
  - Use initial skill version `1.0.0`.
  - Include frontmatter fields required by local skill conventions.
  - Define each skill's purpose, trigger cases, non-trigger cases, workflow, output expectations, error paths, and verification guidance where relevant.
  - Keep every skill independently installable and runtime-standalone.
- **Out-of-Scope (Do NOT implement):**
  - Do not modify `explain-topic` unless a direct mismatch with the approved SPEC is found and documented.
  - Do not add live Jira, Linear, Confluence, GitHub Issues, web browsing, web search, or external memory integrations.
  - Do not create placeholder `references/`, `scripts/`, or `assets/` folders.
  - Do not make one skill delegate to another skill at runtime.
- **Data Models & Schemas:**
  - Skill folder shape:

```text
.agents/skills/<skill-name>/
├── SKILL.md
└── evals/
    └── evals.json
```

---

## ✅ 3. Executable Acceptance Criteria (Gherkin Format)

*Note to Agent: Use these exact scenarios to build and validate your logic.*

```gherkin
Scenario: Create standalone skill instructions
  Given the approved SPEC defines nine new general skills
  When the agent creates the new skill folders and SKILL.md files
  Then each new skill folder exists under .agents/skills/
  And each SKILL.md includes name, description, license, version, tags, author, and metadata frontmatter
  And each new skill uses version 1.0.0

Scenario: Preserve standalone runtime boundaries
  Given each new SKILL.md is inspected
  When the agent reviews the runtime instructions
  Then no skill requires, calls, imports, names, or delegates to another skill at runtime
  And development-time validation references are clearly not runtime dependencies

Scenario: Avoid placeholder support folders
  Given a new skill does not need supporting files beyond SKILL.md and evals
  When the agent creates the skill folder
  Then no empty references, scripts, or assets folder is created
```

---

## 🛠️ 4. Targeted Workspace & Codebase Context

*Note to Agent: You are restricted to modifying or analyzing the following components.*

- **Primary Target Files:**
  1. `.agents/skills/ask-questions/SKILL.md` -> New question-generation skill.
  2. `.agents/skills/reason-problem/SKILL.md` -> New ambiguous-problem reasoning skill.
  3. `.agents/skills/classify-content/SKILL.md` -> New classification and grouping skill.
  4. `.agents/skills/plan-work/SKILL.md` -> New planning skill.
  5. `.agents/skills/explore-context/SKILL.md` -> New local investigation skill.
  6. `.agents/skills/decide-direction/SKILL.md` -> New decision support skill.
  7. `.agents/skills/coordinate-work/SKILL.md` -> New coordination skill.
  8. `.agents/skills/remember-context/SKILL.md` -> New durable memory skill.
  9. `.agents/skills/adapt/SKILL.md` -> New evidence-driven adaptation diagnosis and routing skill.
- **Shared Dependencies/Imports:**
  - Follow `.agents/skills/create-skill/references/authoring.md`.
  - Use [SPEC.md](../SPEC.md) as the implementation contract.
  - Treat `.agents/skills/explain-topic/SKILL.md` as complete.

---

## 💻 5. Step-by-Step Implementation Protocol

*Note to Agent: Execute these steps sequentially. Verify state after each step.*

1. **Analyze & Validate:** Read [SPEC.md](../SPEC.md), `.agents/skills/create-skill/SKILL.md`, and `.agents/skills/create-skill/references/authoring.md`.
2. **Create Skill Folders:** Create only the nine missing skill directories and required files.
3. **Author Skill Instructions:** Write focused `SKILL.md` files with explicit trigger and non-trigger behavior.
4. **Check Runtime Boundaries:** Search new skill files for runtime dependency language that points to another skill.
5. **Check Folder Hygiene:** Confirm no placeholder support folders were created.

---

## 🏁 6. AI Agent Definition of Done (Validation Checklist)

*Note to Agent: You must run validation scripts to check these boxes before marked as complete.*

- [ ] **Compilation:** Not applicable; Markdown authoring only.
- [ ] **Test Coverage:** New skill files are ready for eval generation in US-002.
- [ ] **No Regression:** Existing `.agents/skills/explain-topic/SKILL.md` remains unchanged unless a documented spec mismatch required a fix.
- [ ] **Idempotency:** Re-running the work does not duplicate folders, sections, or placeholder resources.
