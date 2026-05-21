# PRD: General Agent Skills

---

## Product Overview

| Field | Value |
| --- | --- |
| Document Status | DRAFT |
| Target Date | TBD |
| Owner | Oleg Shulyakov |
| Team Members | TBD |
| Stakeholders | Users of this agent.md skill library |
| Designs Link | TBD |
| Demo Link | TBD |
| Work Tracker Link | TBD |
| Last Updated | 2026-05-20 |

---

## Objective

Create a small set of general-purpose agent skills that cover recurring thinking modes across all projects: explaining, planning, exploring or researching, deciding, and remembering. These skills should complement the role-oriented skill catalog in [Software Team Roles as Skills](../2026-05-02-team-roles-as-skills/PRD.md), not duplicate its implementation, documentation, review, testing, or delivery roles.

The current skill library already covers many artifact-producing team responsibilities. The remaining gap is a set of project-agnostic skills for the moments before or around artifact production: when the user wants to understand something, frame work, inspect local or external context, choose a direction, or persist useful project memory.

Without these skills, the agent has to infer these broad behaviors from generic instructions each time. That increases trigger ambiguity and makes common collaboration modes less consistent.

---

## Goals

| Goal ID | Target Outcome | Success Metric |
| --- | --- | --- |
| G-1 | Provide a minimal general skill set for common agent collaboration modes. | Five skills exist: `explain`, `plan`, `explore`, `decide`, and `remember`. |
| G-2 | Avoid overlap with role-specific skills from the May 2 catalog. | Each skill documents when to hand off to existing writer, codegen, review, design, test, or GitHub skills. |
| G-3 | Make trigger behavior predictable. | Each skill has explicit trigger phrases, exclusions, and at least 5 representative eval prompts [assumed]. |
| G-4 | Keep each skill lightweight and reusable across repositories. | Each `SKILL.md` stays under 500 lines and uses references only when needed. |

---

## Target Audience Focus

- **Persona ID: P-1** Individual developer or maintainer: Wants a consistent agent collaborator for understanding, planning, investigation, decisions, and memory without invoking a heavier role workflow.
- **Persona ID: P-2** Skill library maintainer: Needs a small, durable general layer that routes cleanly around specialized skills.
- **Persona ID: P-3** Project lead [assumed]: Wants project decisions and useful context captured without turning every conversation into a formal document.

---

## Scope

### In Scope

- `explain`: Explain concepts, code, architecture, behavior, tradeoffs, and decisions in clear terms matched to the user's question.
- `plan`: Turn a goal into a scoped plan, milestones, risks, sequencing, and next actions.
- `explore`: Investigate local code, project docs, attached artifacts, or external/current information when research is needed.
- `decide`: Compare options and recommend a course of action with tradeoffs, assumptions, and decision criteria.
- `remember`: Capture durable project facts, decisions, and useful observations in `.agents/memory/`.
- Trigger and exclusion guidance for each skill.
- Acceptance criteria and eval prompts for skill behavior.
- Cross-reference to role-specific skills that should remain responsible for implementation, docs, review, tests, and delivery artifacts.

### Out of Scope

- New implementation, refactoring, debugging, testing, review, documentation, GitHub, or release skills already covered by the role-skill catalog.
- Live integrations with Jira, Linear, Confluence, GitHub Issues, or external memory stores.
- Automatic memory writes without user intent or clearly durable project value.
- Replacing project instructions in `AGENTS.md`.

### Later

- A lightweight router skill that chooses among general and role-specific skills [assumed].
- Shared eval harness for trigger overlap across all skills.
- Memory summarization or pruning workflows.

---

## Functional Requirements

| Requirement ID | Capability / Feature | Priority | Acceptance Criteria | Tracker |
| --- | --- | --- | --- | --- |
| FR-1 | Define `explain` as the skill for clarification and teaching. | MUST | Triggers on “explain”, “what is”, “why”, “how does”, “walk me through”, and code/concept explanation requests.<br>Does not trigger when the user asks to write a PRD, spec, code, tests, or review. | TBD |
| FR-2 | Define `plan` as the skill for sequencing work before execution. | MUST | Triggers on “plan”, “break this down”, “roadmap”, “approach”, “milestones”, and “how should we proceed”.<br>Produces scoped steps, risks, assumptions, and verification strategy when relevant. | TBD |
| FR-3 | Define `explore` as the skill for investigation and research. | MUST | Triggers on “explore”, “investigate”, “find where”, “research”, “look up”, “understand this repo”, and “trace”.<br>Covers both local context gathering and external/current research when needed.<br>Produces findings with sources, file references, or uncertainty clearly marked. | TBD |
| FR-4 | Define `decide` as the skill for choosing among options. | MUST | Triggers on “decide”, “choose”, “which option”, “tradeoffs”, “recommend”, and “should we”.<br>States decision criteria, compares viable options, recommends one, and identifies reversibility or risk. | TBD |
| FR-5 | Define `remember` as the skill for durable project memory. | MUST | Triggers when the user asks to remember, save context, record a decision, update memory, or preserve a project fact.<br>Writes only durable facts, decisions, and observations to `.agents/memory/` according to project conventions.<br>Avoids storing transient task chatter or unverifiable assumptions as fact. | TBD |
| FR-6 | Document cross-skill boundaries. | MUST | Each skill names adjacent skills it should defer to, including `writer-prd`, `writer-spec`, `codegen-*`, `review-code`, `codegen-test`, and GitHub-specific skills where applicable. | TBD |
| FR-7 | Add behavior evals. | SHOULD | Each skill has representative prompts for true positives, false positives, and handoff cases [assumed]. | TBD |

---

## Non-Functional Requirements

| NFR ID | Category | Target Specification |
| --- | --- | --- |
| NFR-1 | Maintainability | Each skill has one clear workflow and avoids becoming a dumping ground for generic agent behavior. |
| NFR-2 | Portability | Skills work across repositories and do not assume this repository layout except where `remember` explicitly uses `.agents/memory/`. |
| NFR-3 | Token Efficiency | Main `SKILL.md` files stay concise; long examples or eval details move to references only when they reduce ambiguity. |
| NFR-4 | Safety | `explore` must cite current external sources when browsing is required and distinguish verified facts from inference. |
| NFR-5 | Memory Hygiene | `remember` must preserve useful context without duplicating docs or storing sensitive/transient information. |

---

## Milestones

| Milestone | Target Date | Exit Criteria | Owner |
| --- | --- | --- | --- |
| M-1 | TBD | Draft PRD approved. | Oleg Shulyakov |
| M-2 | TBD | Skill descriptions and trigger boundaries drafted for all five skills. | TBD |
| M-3 | TBD | `SKILL.md` files created or updated. | TBD |
| M-4 | TBD | Eval prompts added and trigger overlap checked. | TBD |

---

## User Journeys / Key Flows

1. A user asks, “Explain how this auth flow works.” The agent uses `explain`, reads the relevant code only if needed, and returns a clear explanation with file references when applicable.
2. A user asks, “Let’s plan the migration.” The agent uses `plan`, identifies phases, risks, verification, and when a dedicated spec or implementation skill should take over.
3. A user asks, “Explore whether we already support this.” The agent uses `explore`, searches local files and docs, optionally researches current external context, then reports findings and gaps.
4. A user asks, “Should we build this as a plugin or a skill?” The agent uses `decide`, compares options against explicit criteria, and recommends one.
5. A user asks, “Remember that we chose skills over plugins for this.” The agent uses `remember`, records the durable decision in the appropriate memory file, and keeps the note concise.

---

## Risks, Assumptions, & Mitigations

| Risk ID | Assumption / Risk Description | Impact | Mitigation Strategy | Status |
| --- | --- | --- | --- | --- |
| R-1 | General skills could become too broad and overlap with specialized role skills. | HIGH | Define hard exclusions and handoff rules in every skill. | OPEN |
| R-2 | `explore` could blur local investigation and web research. | MEDIUM | Require source discipline: file references for local findings, links for external/current research, and explicit uncertainty. | OPEN |
| R-3 | `remember` could accumulate low-value notes. | MEDIUM | Require durability criteria before writing memory. | OPEN |
| R-4 | `decide` recommendations may hide subjective criteria. | MEDIUM | Require explicit criteria, assumptions, and reversibility notes. | OPEN |
| R-5 | Eval coverage may be too small to catch trigger conflicts. | MEDIUM | Include false-positive and handoff prompts, not only happy-path prompts. | OPEN |

---

## External Dependencies

| Dependency ID | Item | Impacted Requirements | Validation Owner |
| --- | --- | --- | --- |
| D-1 | Existing role-skill catalog in `docs/2026-05-02-team-roles-as-skills/` | FR-6 | Oleg Shulyakov |
| D-2 | Existing `.agents/memory/` conventions | FR-5, NFR-5 | Oleg Shulyakov |
| D-3 | `creator-skill` validation workflow | FR-7 | TBD |

---

## Open Questions

| Question ID | Question | Answer / Decision | Owner | Resolution Date |
| --- | --- | --- | --- | --- |
| Q-1 | Should `explore` include web research by default, or only when the user asks or current information matters? | Proposed: include it, with source discipline and browsing only when needed. | Oleg Shulyakov | TBD |
| Q-2 | Should `remember` ask before writing memory, or write automatically when the user explicitly says “remember”? | TBD | Oleg Shulyakov | TBD |
| Q-3 | Should these skills use neutral names (`plan`) or prefix-first names (`planner-general`, `research-general`)? | Proposed: keep the simple names because they are cognitive modes, not artifact roles. | Oleg Shulyakov | TBD |
| Q-4 | Should `plan` create task files, or only produce conversational plans unless paired with another writing skill? | Proposed: conversational by default; durable task files require explicit user request or substantial work. | Oleg Shulyakov | TBD |

---

## Reference Links

- **Ref-1**: Role-specific skill catalog PRD - [docs/2026-05-02-team-roles-as-skills/PRD.md](../2026-05-02-team-roles-as-skills/PRD.md)
- **Ref-2**: Role-specific skill catalog SPEC - [docs/2026-05-02-team-roles-as-skills/SPEC.md](../2026-05-02-team-roles-as-skills/SPEC.md)
