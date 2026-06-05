---
name: write-user-story
description: >
  Write user stories with acceptance criteria and developer tasks. Use for story writing,
  Jira/Linear/GitHub tickets, task breakdowns, story points, and story-level sprint planning.
license: MIT
tags:
  - writer
  - agile
  - user-stories
metadata:
  author: Oleg Shulyakov
  version: "1.2.1"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: project-management
---

# write-user-story

Produce one or more **user stories** with acceptance criteria, then decompose each into **developer tasks** with file/module hints and effort estimates.

---

## Workflow

Stories capture user intent and define done. Tasks translate that intent into work a developer can pick up without a meeting. Linking them hierarchically prevents the classic gap where stories are approved but engineers still don't know what to build.

Follow the **3 C's** framework: **Card** (the written story), **Conversation** (the ongoing dialogue that refines scope and details — stories are conversation starters, not specs), **Confirmation** (acceptance criteria that define done).

Use **STAR** as a lightweight quality check when context is available: the situation explains the user's current problem, the task defines the goal, the action appears in the behavior or developer work, and the result is captured in the "so that" clause and acceptance criteria.

---

## Information gathering

Extract from the user's input:

- **Feature or capability** being described
- **User type(s)** / persona(s)
- **Technical context**: codebase language, framework, relevant modules (if mentioned or inferable)
- **Scope**: single story, or multiple stories for a feature/epic?

Ask for missing information only when the answer would materially change the story, acceptance criteria, or implementation tasks.

- **Delivery audience:** If missing, ask who the story is for before drafting: a product/planning workflow or an AI coding agent that will implement it.
- **Critical context:** Ask for any additional missing context that blocks a useful output, such as persona, business outcome, feature scope, target platform, codebase stack, or target modules.
- **Question budget:** Ask the smallest useful set of questions in one pass. Do not force a fixed number; ask more than one when several answers are genuinely needed, and proceed with marked assumptions when the missing details are low-risk.
- **Sparse context:** If the user cannot provide more detail, write one exemplary story with clear assumptions and a note that more context would improve the task breakdown.

---

## Output

- **Product or planning audience:** Read `references/output-format.md` for the default Jira/Linear/GitHub story format.
- **AI implementation audience:** Read `references/ai-output-format.md` when the user asks for an AI-agent-ready story, autonomous implementation prompt, task specification, executable agent handoff, or code-agent work item.
- **Ambiguous audience:** Use the delivery-audience answer from information gathering before choosing a template.
- **Story metadata:** Put status, story type, phase, story ID, points, priority, owner, epic, design link, tags, and related docs in YAML frontmatter. Add optional fields only when they have real value.

---

## Writing guidance

- **Single value:** One user value per story — resist the urge to bundle two different user goals.
- **Outcome first:** The "so that" is the most important part — it defines the WHY and prevents gold-plating.
- **Small cards:** Keep stories simple. Split whenever the card needs multiple personas, unrelated outcomes, or more than one sprint-sized goal.
- **INVEST check:** Validate each story against **INVEST**:
  - **I**ndependent (self-contained, orderable),
  - **N**egotiable (details emerge through conversation),
  - **V**aluable (delivers user value),
  - **E**stimable (team can size it),
  - **S**mall (fits one sprint),
  - **T**estable (clear pass/fail via AC)
- **Acceptance criteria:** Write AC in Given/When/Then; each criterion should be independently testable.
- **Edge coverage:** Include at least one error/edge-case AC.
- **Points:** Points reflect uncertainty + effort. Anything >5 should be split.
- **Keep the story statement implementation-free** — describe the user goal, not the UI or technology. "I want to invite my friends" not "I want to click an invite button in the settings menu".

**Tasks:**

- **Task size:** Each task is a single coherent unit of developer work (ideally <1 day).
- **Phrasing:** Use imperative phrasing: "Add", "Create", "Update", "Wire", "Write".
- **File hints:** File hints should be concrete if context allows: `src/api/users.ts`, `UserService.java`.
- **Unknown codebase:** If you don't know the codebase, use logical module names and note them as `[assumed path]`.
- **Effort scale:** Use XS (<1h), S (1–2h), M (half-day), L (full day).

**Estimation:**

- **Uncertainty:** Be honest about uncertainty. If the task involves unknown third-party APIs, say so.
- **Risk:** Flag high-risk tasks with ⚠️.

---

## Splitting stories

If the feature described maps to multiple user goals, split into separate stories. Common split patterns:

- **Happy path + error handling** (different complexity, can ship incrementally)
- **Core feature + admin/configuration** (different user types)
- **Read + write operations** (can be developed in parallel)

When examples would help calibrate story granularity, acceptance criteria, or developer-task detail, read `references/examples.md`.

---

## Verification

Confirm each story has a persona, user value, acceptance criteria, and developer tasks sized for handoff. Check that assumptions are marked, points reflect uncertainty, and any story above 5 points is split or called out as needing decomposition.
