# PRD: General Agent Skills

---

## Product Overview

| Field | Value |
| --- | --- |
| Document Status | APPROVED |
| Target Date | TBD |
| Owner | Oleg Shulyakov |
| Team Members | TBD |
| Stakeholders | Users of this agent.md skill library |
| Designs Link | TBD |
| Demo Link | TBD |
| Work Tracker Link | TBD |
| Last Updated | 2026-05-21 |

---

## Objective

Create a small set of general-purpose agent skills that cover recurring thinking modes across all projects: asking, explaining, reasoning, classifying, planning, exploring local context, deciding, coordinating, and remembering. Each skill must be useful as a standalone installable unit at runtime, without assuming any other skill is present.

The remaining gap is a set of project-agnostic skills for common collaboration modes: when the user wants to ask better questions, understand something, reason through an ambiguous problem, organize messy material, frame work, inspect local project context, choose a direction, coordinate execution, or persist useful project memory.

Without these skills, the agent has to infer these broad behaviors from generic instructions each time. That increases trigger ambiguity and makes common collaboration modes less consistent.

---

## Goals

| Goal ID | Target Outcome | Success Metric |
| --- | --- | --- |
| G-1 | Provide a minimal general skill set for common agent collaboration modes. | Nine skills exist: `ask-questions`, `explain-topic`, `reason-problem`, `classify-content`, `plan-work`, `explore-context`, `decide-direction`, `coordinate-work`, and `remember-context`. |
| G-2 | Keep every skill independently installable. | Each skill works at runtime without requiring, naming, or delegating to another skill. |
| G-3 | Make trigger behavior predictable. | Each skill has explicit trigger phrases, exclusions, and at least 7 representative eval prompts: 3 true-positive, 2 false-positive, and 2 non-trigger prompts. |
| G-4 | Keep each skill lightweight and reusable across repositories. | Each `SKILL.md` stays under 500 lines and uses references only when needed. |

---

## Target Audience Focus

- **Persona ID: P-1** Individual developer or maintainer: Wants a consistent agent collaborator for asking, understanding, reasoning, classification, planning, investigation, decisions, coordination, and memory.
- **Persona ID: P-2** Skill library maintainer: Needs a small, durable general layer with clear standalone skill boundaries.
- **Persona ID: P-3** Project lead [assumed]: Wants project decisions and useful context captured without turning every conversation into a formal document.

---

## Scope

### In Scope

- `ask-questions`: Identify useful questions, missing context, hidden assumptions, and the smallest clarifications needed to move forward.
- `explain-topic`: Explain concepts, code, architecture, behavior, tradeoffs, and decisions in clear terms matched to the user's question.
- `reason-problem`: Work through ambiguous problems by clarifying terms, surfacing assumptions, generating hypotheses, testing arguments, and shaping a clearer framing.
- `classify-content`: Organize items, ideas, observations, requirements, examples, files, risks, or options into meaningful categories by similarity, difference, type, abstraction level, priority, dependency, or other explicit criteria.
- `plan-work`: Turn a goal into a scoped plan, milestones, risks, sequencing, and next actions.
- `explore-context`: Investigate local code, project docs, attached artifacts, and repository context when local research is needed.
- `decide-direction`: Compare options and recommend a course of action with tradeoffs, assumptions, and decision criteria.
- `coordinate-work`: Manage multi-step or multi-agent work by tracking goals, owners, dependencies, status, blockers, handoffs, and next actions.
- `remember-context`: Capture durable project facts, decisions, and useful observations in `.agents/memory/`.
- Trigger and exclusion guidance for each skill.
- Acceptance criteria and eval prompts for skill behavior.
- Standalone installation guidance for each skill.

### Out of Scope

- Live integrations with Jira, Linear, Confluence, GitHub Issues, or external memory stores.
- Web search, web browsing, or external/current-information research inside `explore-context`.
- Automatic memory writes without user intent or clearly durable project value.
- Replacing project instructions in `AGENTS.md`.

### Later

- Shared eval harness for trigger overlap across all skills.
- Memory summarization or pruning workflows.

---

## Functional Requirements

| Requirement ID | Capability / Feature | Priority | Acceptance Criteria | Tracker |
| --- | --- | --- | --- | --- |
| FR-1 | Define `ask-questions` as the skill for question generation and clarification. | MUST | Triggers on “ask-questions”, “what should I ask”, “what are the right questions”, “what are we missing”, “clarify this”, and ambiguous requests where progress depends on missing context. Produces a minimal, prioritized set of useful questions, assumptions, and context gaps. | TBD |
| FR-2 | Define `explain-topic` as the skill for clarification and teaching. | MUST | Triggers on “explain-topic”, “what is”, “why”, “how does”, “walk me through”, and code/concept explanation requests. Produces clear explanations matched to the user's context and desired depth. | TBD |
| FR-3 | Define `reason-problem` as the skill for working through ambiguous problems. | MUST | Triggers on “reason through”, “think through”, “brainstorm”, “tackle this problem”, “help me frame this”, “let’s work through this”, and messy problem statements where the desired output is not yet clear. Clarifies terms, assumptions, constraints, possible explanations, and candidate directions without forcing a premature decision or plan. | TBD |
| FR-4 | Define `classify-content` as the skill for organizing material into meaningful groups. | MUST | Triggers on “classify-content”, “categorize”, “group”, “cluster”, “sort”, “taxonomy”, “organize these”, and requests to group items by similarity, difference, category, priority, dependency, abstraction level, or other explicit criteria. Produces labeled groups, grouping criteria, notable edge cases, and items that do not clearly fit. | TBD |
| FR-5 | Define `plan-work` as the skill for sequencing work before execution. | MUST | Triggers on “plan-work”, “break this down”, “roadmap”, “approach”, “milestones”, and “how should we proceed”. Produces scoped steps, risks, assumptions, and verification strategy when relevant. | TBD |
| FR-6 | Define `explore-context` as the skill for local investigation and repository research. | MUST | Triggers on “explore-context”, “investigate”, “find where”, “understand this repo”, “trace”, and local-context research requests. Covers local code, project docs, attached artifacts, and repository context only. Produces findings with file references, artifact references, or uncertainty clearly marked. | TBD |
| FR-7 | Define `decide-direction` as the skill for choosing among options. | MUST | Triggers on “decide-direction”, “choose”, “which option”, “tradeoffs”, “recommend”, and “should we”. States decision criteria, compares viable options, recommends one, and identifies reversibility or risk. | TBD |
| FR-8 | Define `coordinate-work` as the skill for managing active work across people, agents, tasks, and dependencies. | MUST | Triggers on “coordinate-work”, “manage this work”, “team lead”, “lead this”, “assign”, “delegate”, “track blockers”, “status”, “handoff”, and multi-agent or multi-workstream requests. Maintains an execution view with goals, owners, dependencies, current status, blockers, and next actions. | TBD |
| FR-9 | Define `remember-context` as the skill for durable project memory. | MUST | Triggers when the user asks to remember, save context, record a decision, update memory, or preserve a project fact. When the user explicitly asks to remember something, the memory write is auto-approved and should proceed without asking again. Writes only durable facts, decisions, and observations to `.agents/memory/` according to project conventions. Avoids storing transient task chatter or unverifiable assumptions as fact. | TBD |
| FR-10 | Document standalone runtime boundaries. | MUST | Each skill defines its own purpose, trigger phrases, non-trigger cases, expected behavior, and output shape without requiring, naming, or delegating to another skill at runtime. | TBD |
| FR-11 | Add behavior evals. | SHOULD | Each skill has at least 7 representative prompts: 3 true-positive prompts, 2 false-positive prompts, and 2 non-trigger prompts. | TBD |

---

## Non-Functional Requirements

| NFR ID | Category | Target Specification |
| --- | --- | --- |
| NFR-1 | Maintainability | Each skill has one clear workflow and avoids becoming a dumping ground for generic agent behavior. |
| NFR-2 | Portability | Skills work across repositories and do not assume this repository layout except where `remember-context` explicitly uses `.agents/memory/`. Runtime behavior must not depend on any other skill being installed. |
| NFR-3 | Token Efficiency | Main `SKILL.md` files stay concise; long examples or eval details move to references only when they reduce ambiguity. |
| NFR-4 | Question Quality | `ask-questions` must prefer the fewest high-leverage questions over exhaustive questionnaires. |
| NFR-5 | Reasoning Quality | `reason-problem` must expose assumptions, uncertainty, and competing interpretations instead of presenting guesses as settled conclusions. |
| NFR-6 | Classification Quality | `classify-content` must state the grouping criteria and preserve ambiguous or multi-fit items instead of forcing every item into a clean bucket. |
| NFR-7 | Source Discipline | `explore-context` must cite local files, project docs, or attached artifacts and distinguish verified repository facts from inference. It must not perform web search or browsing. |
| NFR-8 | Memory Hygiene | `remember-context` must preserve useful context without duplicating docs or storing sensitive/transient information. |
| NFR-9 | Coordination Clarity | `coordinate-work` must keep status, owners, blockers, and next actions explicit enough that another agent or human can continue the work. |

---

## Milestones

| Milestone | Target Date | Exit Criteria | Owner |
| --- | --- | --- | --- |
| M-1 | TBD | Draft PRD approved. | Oleg Shulyakov |
| M-2 | TBD | Skill descriptions and trigger boundaries drafted for all nine skills. | TBD |
| M-3 | TBD | `SKILL.md` files created or updated. | TBD |
| M-4 | TBD | Eval prompts added and trigger overlap checked. | TBD |

---

## User Journeys / Key Flows

1. A user asks, “What should we ask before committing to this approach?” The agent uses `ask-questions` to produce a short set of high-leverage questions, assumptions, and missing context.
2. A user asks, “Explain how this auth flow works.” The agent uses `explain-topic`, reads the relevant code only if needed, and returns a clear explanation with file references when applicable.
3. A user asks, “Let’s think through why this workflow feels fragile.” The agent uses `reason-problem` to clarify the problem, surface assumptions, generate hypotheses, and identify what would make the situation clearer.
4. A user asks, “Classify these feature requests by underlying user need.” The agent uses `classify-content` to define grouping criteria, label groups, place items, and flag ambiguous cases.
5. A user asks, “Let’s plan the migration.” The agent uses `plan-work` to identify phases, risks, verification, assumptions, and next actions.
6. A user asks, “Explore whether we already support this.” The agent uses `explore-context`, searches local files, project docs, and attached artifacts, then reports findings and gaps.
7. A user asks, “Should we build this as a plugin or a skill?” The agent uses `decide-direction`, compares options against explicit criteria, and recommends one.
8. A user asks, “Lead this migration across frontend, backend, and tests.” The agent uses `coordinate-work` to track workstreams, owners, dependencies, blockers, status, and handoffs.
9. A user asks, “Remember that we chose skills over plugins for this.” The agent uses `remember-context`, records the durable decision in the appropriate memory file, and keeps the note concise.

---

## Risks, Assumptions, & Mitigations

| Risk ID | Assumption / Risk Description | Impact | Mitigation Strategy | Status |
| --- | --- | --- | --- | --- |
| R-1 | General skills could become too broad and behave inconsistently. | HIGH | Define clear trigger phrases, non-trigger cases, and output expectations in every skill. | OPEN |
| R-2 | `explore-context` could be mistaken for web research. | MEDIUM | Define `explore-context` as local and artifact investigation only; external/current research remains out of scope for this skill. | OPEN |
| R-3 | `remember-context` could accumulate low-value notes. | MEDIUM | Require durability criteria before writing memory. | OPEN |
| R-4 | `decide-direction` recommendations may hide subjective criteria. | MEDIUM | Require explicit criteria, assumptions, and reversibility notes. | OPEN |
| R-5 | Eval coverage may be too small to catch trigger conflicts. | MEDIUM | Include false-positive and non-trigger prompts, not only happy-path prompts. | OPEN |
| R-6 | `coordinate-work` could overlap with `plan-work`. | MEDIUM | Define `plan-work` as pre-execution sequencing and `coordinate-work` as active coordination across workstreams, owners, blockers, and handoffs. | OPEN |
| R-7 | `reason-problem` could become vague brainstorming without useful output. | MEDIUM | Require a clear problem framing, assumptions, hypotheses or options, and suggested next clarity step. | OPEN |
| R-8 | `ask-questions` could become an endless questionnaire. | MEDIUM | Require prioritized questions and a bias toward the smallest question set that changes the next action. | OPEN |
| R-9 | `classify-content` could force false precision. | MEDIUM | Require explicit grouping criteria, ambiguous cases, and optional multi-label classifications when needed. | OPEN |

---

## External Dependencies

| Dependency ID | Item | Impacted Requirements | Validation Owner |
| --- | --- | --- | --- |
| D-1 | Existing `.agents/memory/` conventions | FR-9, NFR-8 | Oleg Shulyakov |
| D-2 | `create-skill` validation workflow for development-time checks only | FR-11 | TBD |

---

## Resolved Questions

| Question ID | Question | Answer / Decision | Owner | Resolution Date |
| --- | --- | --- | --- | --- |
| Q-1 | Should `explore-context` include web research by default, or only when the user asks or current information matters? | Decided: no. `explore-context` covers local code, project docs, attached artifacts, and repository context only. Web search and browsing are out of scope. | Oleg Shulyakov | 2026-05-21 |
| Q-2 | Should `remember-context` ask before writing memory, or write automatically when the user explicitly asks to remember something? | Decided: explicit user requests to remember context are auto-approved. The skill should write without asking again, while still filtering for durable project value and avoiding sensitive, transient, or unverifiable notes. | Oleg Shulyakov | 2026-05-21 |
| Q-3 | Should these skills use neutral names (`plan-work`) or verb-first names (`plan-general`, `research-context`)? | Decided: keep simple names because they are standalone cognitive modes. | Oleg Shulyakov | 2026-05-21 |
| Q-4 | Should `plan-work` create task files, or only produce conversational plans unless paired with another writing skill? | Decided: conversational by default; durable task files require explicit user request or substantial work. | Oleg Shulyakov | 2026-05-21 |
| Q-5 | Should the coordination skill be named `coordinate-work`, `lead`, or `manage`? | Decided: `coordinate-work`, because it is plain, action-oriented, and covers team-leading, delegation, status, and multi-agent coordination without implying people-management authority. | Oleg Shulyakov | 2026-05-21 |
| Q-6 | Should the ambiguous-problem skill be named `reason-problem`, `think`, or `brainstorm`? | Decided: `reason-problem`, because it covers brainstorming, framing, assumptions, and argument-testing without being limited to idea generation. | Oleg Shulyakov | 2026-05-21 |
| Q-7 | Should question generation be its own skill or part of `reason-problem`? | Decided: keep `ask-questions` separate because identifying the right questions is a distinct output and often useful before any reasoning path is chosen. | Oleg Shulyakov | 2026-05-21 |
| Q-8 | Should grouping be named `classify-content`, `sort`, or `categorize`? | Decided: `classify-content`, because it covers category assignment, similarity/difference grouping, taxonomies, and edge cases more precisely than `sort`. | Oleg Shulyakov | 2026-05-21 |

---
