---
status: IN_REVIEW
documentType: PRD
phase: delivery
createdAt: "2026-05-02"
updatedAt: "2026-05-22"
author: Oleg Shulyakov
owner: Oleg Shulyakov
stakeholders: Developers, maintainers, AI coding agent users, agent runtime implementors
demoLink: https://olegshulyakov.github.io/agent.md
tags:
  - agents
  - playbook
related:
  - SPEC.md
---

# PRD: Agent Playbook

## Objective

Developers increasingly rely on coding agents, but project-specific instructions are still scattered across READMEs, IDE settings, chat prompts, local memory, and vendor-specific files. This makes agent behavior hard to review, hard to version, and easy to lose when switching tools.

The Agent Playbook should provide a lightweight, repository-native structure for agent guidance that builds on the public `AGENTS.md` convention and the Agent Skills specification. `AGENTS.md` remains the predictable project entry point: a README for agents that captures setup commands, tests, code style, security considerations, and other recurring instructions. Skills add reusable, progressively loaded task procedures under `.agents/skills/<name>/SKILL.md`.

The product goal is not to replace existing standards. It is to package them into a practical project playbook: start with `AGENTS.md`, add `.agents/skills/` when repeatable workflows need focused instructions, and introduce supporting folders only when they reduce repetition or improve maintainability.

---

## Goals

|Goal ID|Target Outcome|Success Metric|
|---|---|---|
|G-1|Make project instructions easy for agents and humans to find|A new repository can be bootstrapped with a valid root `AGENTS.md` in under 10 minutes [assumed]|
|G-2|Improve portability across compatible coding agents|Core guidance uses Markdown, `AGENTS.md`, and `SKILL.md` conventions without vendor-only required fields|
|G-3|Support reusable task procedures without overloading base context|Skills can be discovered from metadata and loaded only when relevant|
|G-4|Keep agent behavior reviewable with normal code review workflows|Agent guidance lives in version-controlled files with clear ownership and concise scopes|

---

## Target Audience Focus

- **Persona ID: P-1 Developer / Maintainer:** Works in one or more repositories and wants agents to follow local setup, testing, style, and workflow rules without repeating the same chat instructions.
- **Persona ID: P-2 Team Lead / Reviewer:** Needs agent behavior to be auditable, diffable, and consistent enough to trust across contributors and tools.
- **Persona ID: P-3 Agent Runtime Implementor:** Needs predictable file locations and metadata conventions to discover project instructions and load task-specific capabilities efficiently.
- **Persona ID: P-4 Skill Creator:** Wants to package repeatable procedures, such as release checks or test scaffolding, into small skills that activate on the right prompts.

---

## Scope

### In Scope

- Define `AGENTS.md` as the required repository entry point for agent instructions.
- Recommend practical `AGENTS.md` sections, including project overview, setup commands, build and test commands, code style, testing instructions, security considerations, and PR or commit guidance.
- Define how nested `AGENTS.md` files work for subprojects, including the rule that the closest file to the edited path has precedence and explicit user prompts override file instructions.
- Define `.agents/skills/<skill-name>/SKILL.md` as the standard location for reusable Agent Skills.
- Specify skill authoring expectations based on the Agent Skills specification: YAML front matter with required `name` and `description`, optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`, followed by Markdown instructions.
- Document progressive disclosure: runtimes may initially scan skill metadata, then load the full skill body only when the request matches the description.
- Document optional skill-local directories: `scripts/` for executable code, `references/` for focused documentation, and `assets/` for templates and static resources.
- Provide examples for a minimal repository, a monorepo with nested `AGENTS.md`, and a repository with one or more skills.
- Document optional supporting folders, such as `.agents/rules/`, `.agents/commands/`, `.agents/agents/`, and `.agents/memory/`, as extensions rather than required baseline structure.

### Out of Scope

- Building a specific coding agent runtime.
- Requiring proprietary IDE, model, or vendor configuration.
- Defining a centralized public registry for skills or rules in the initial release.
- Guaranteeing that every model or tool will consistently execute skill instructions.
- Storing credentials, secrets, access tokens, or private user data in agent guidance files.

### Later

- Shared local or global skill libraries, such as `~/.agents/skills/`.
- Validation tooling for `AGENTS.md`; `SKILL.md` validation can reference the Agent Skills reference validator.
- A starter template generator.
- Compatibility guidance for specific clients once implementation details stabilize.

---

## Functional Requirements

|Requirement ID|Capability / Feature|Priority|Acceptance Criteria|Tracker|
|---|---|---|---|---|
|FR-1|Define root `AGENTS.md` as the baseline entry point|MUST|A repository can include only `AGENTS.md` and still be considered valid; the PRD and spec describe its purpose as agent-facing project guidance|TBD|
|FR-2|Provide recommended `AGENTS.md` content sections|MUST|Documentation includes setup, build, test, style, security, and workflow guidance examples; no section is required unless the project needs it|TBD|
|FR-3|Document nested `AGENTS.md` precedence|MUST|Guidance states that the closest `AGENTS.md` applies to the current path and that explicit user prompts override file instructions|TBD|
|FR-4|Define Agent Skills folder layout|MUST|Skills use `.agents/skills/<skill-name>/SKILL.md`; each skill directory contains at minimum `SKILL.md`; `name` metadata matches the parent directory|TBD|
|FR-5|Define required skill front matter|MUST|A valid skill includes YAML front matter with `name` and `description`; `name` is 1-64 characters, lowercase alphanumeric plus hyphens, no leading/trailing/consecutive hyphens; `description` is 1-1024 characters and states what the skill does and when to use it|TBD|
|FR-6|Define optional skill metadata|MUST|Documentation covers optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`; optional fields are described as Agent Skills compatibility, not Playbook-only invention|TBD|
|FR-7|Explain progressive disclosure for skills|MUST|Runtime guidance describes loading startup metadata first, loading full `SKILL.md` instructions on activation, and loading `scripts/`, `references/`, or `assets/` only when needed|TBD|
|FR-8|Define optional skill resource directories|SHOULD|Documentation explains `scripts/`, `references/`, and `assets/`, including expected use cases and guidance to keep references focused|TBD|
|FR-9|Provide example playbook structures|SHOULD|Examples cover minimal, monorepo, and skill-enabled repositories|TBD|
|FR-10|Position optional `.agents/` folders as extensions|SHOULD|Rules, commands, agents, and memory are documented as optional patterns with clear use cases and no baseline compliance requirement|TBD|
|FR-11|Include safety guidance for executable skills|MUST|Documentation states that tools may ask permission before running commands and that scripts must document dependencies, produce useful errors, handle edge cases, and avoid unsafe side effects|TBD|
|FR-12|Reference skill validation|SHOULD|Documentation points implementors and authors to the Agent Skills reference validator for `SKILL.md` naming and front matter checks|TBD|

---

## Non-Functional Requirements

|NFR ID|Category|Target Specification|
|---|---|---|
|NFR-1|Portability|Core files use plain Markdown and avoid required vendor-specific syntax|
|NFR-2|Simplicity|A minimal valid playbook requires only one root `AGENTS.md`|
|NFR-3|Maintainability|Files are concise, scoped, version-controlled, and reviewable in normal pull requests|
|NFR-4|Security|Documentation explicitly prohibits committing secrets and warns that command-running skills require runtime permission controls|
|NFR-5|Context Efficiency|Skills support metadata-first discovery; full `SKILL.md` instructions should stay under 5000 tokens and under 500 lines where practical|

---

## Milestones

|Milestone|Target Date|Exit Criteria|Owner|
|---|---|---|---|
|M-1 PRD rewrite|2026-05-22|Complete: PRD reflects `AGENTS.md`, Agent Skills quickstart, and Agent Skills specification guidance|Oleg Shulyakov|
|M-2 Spec alignment|TBD|`SPEC.md` no longer treats optional `.agents/` folders as mandatory baseline compliance|TBD|
|M-3 Examples|TBD|Minimal, monorepo, and skill-enabled examples are documented and internally consistent|TBD|
|M-4 Skill validation guidance|TBD|Skill examples pass Agent Skills reference validation or clearly document intentional deviations|TBD|

---

## User Interaction

Developers should be able to start with a root `AGENTS.md` that reads like direct onboarding guidance for an agent. The file should answer practical questions: how to set up the project, how to run checks, what style to follow, what security concerns matter, and where deeper instructions live.

When a repeatable workflow needs more than a few lines, the developer should move it into a skill. The skill should have valid YAML front matter with a short `name`, a specific `description` that tells the runtime when to activate it, and a body that gives the agent concrete steps to follow. If the workflow needs supporting material, the skill can keep executable code in `scripts/`, focused documentation in `references/`, and templates or static resources in `assets/`. A runtime may ask for permission before executing commands from a skill, because letting Markdown casually operate a terminal would be a bold life choice.

---

## User Journeys / Key Flows

1. **Bootstrap a small repository:** A maintainer creates `AGENTS.md` at the root, adds setup and test commands, documents code style, and commits it with the rest of the project.
2. **Support a monorepo:** A platform team keeps broad guidance in the root `AGENTS.md`; each package adds its own nested `AGENTS.md` for local commands, style exceptions, and test instructions.
3. **Create a reusable skill:** A developer creates `.agents/skills/release-check/SKILL.md` with required `name` and `description`, plus a short release verification workflow. The runtime discovers the metadata and loads the skill when the user asks for a release check.
4. **Review agent behavior:** A reviewer inspects changes to `AGENTS.md` or `SKILL.md` in a pull request before those instructions affect future agent sessions.

---

## Risks, Assumptions, & Mitigations

|Risk ID|Assumption / Risk Description|Impact|Mitigation Strategy|Status|
|---|---|---|---|---|
|R-1|Tools vary in how reliably they follow skill instructions|MEDIUM|Document expected behavior without promising universal execution; include manual verification steps|OPEN|
|R-2|A large mandatory `.agents/` schema could compete with the simpler `AGENTS.md` convention|HIGH|Make `AGENTS.md` the baseline and every `.agents/` folder optional except skills when skills are used|OPEN|
|R-3|Poor skill descriptions may activate at the wrong time|MEDIUM|Require descriptions to state both capability and trigger context, stay within the Agent Skills 1-1024 character constraint, and include task-specific keywords|OPEN|
|R-4|Skills that run commands can create security or trust issues|HIGH|Keep executable code in `scripts/`, require documented dependencies and helpful errors, use permission-aware runtime behavior, and warn against secrets|OPEN|
|R-5|Teams may duplicate README content into `AGENTS.md` and let it drift|MEDIUM|Recommend linking to existing human docs when details are already maintained elsewhere|OPEN|

---

## External Dependencies

|Dependency ID|Item|Impacted Requirements|Validation Owner|
|---|---|---|---|
|D-1|Public `AGENTS.md` convention|FR-1, FR-2, FR-3|TBD|
|D-2|Agent Skills specification and quickstart|FR-4, FR-5, FR-6, FR-7, FR-8, FR-11, FR-12|TBD|
|D-3|Compatible coding-agent clients|FR-3, FR-7, FR-11|TBD|

---

## Open Questions

|Question ID|Question|Answer / Decision|Owner|Resolution Date|
|---|---|---|---|---|
|Q-1|Should `.agents/rules/`, `.agents/commands/`, `.agents/agents/`, and `.agents/memory/` remain project-specific extensions or become formal spec sections?|Keep them as example extension patterns. The current project may use `.agents/` folders to organize local rules, memory, commands, or agent personas, but they are not required baseline Playbook sections.|Oleg Shulyakov|2026-05-22|
|Q-2|Should this project define validation rules for skill metadata beyond `name` and `description`?|No for baseline compatibility. Use Agent Skills required fields and constraints; treat `license`, `compatibility`, `metadata`, and experimental `allowed-tools` as optional spec-aligned fields.|Oleg Shulyakov|2026-05-22|
|Q-3|Should global skills under `~/.agents/` be included in v1 or deferred?|Defer. The Agent Skills specification defines skill directory structure but does not require a global `~/.agents/` registry for baseline skill validity.|Oleg Shulyakov|2026-05-22|
|Q-4|What compatibility level should be claimed for clients that support `AGENTS.md` but not skills?|Treat `AGENTS.md` and Agent Skills as independent capabilities. A client can support project instruction loading through `AGENTS.md`, skill loading through `SKILL.md`, both, or neither; Playbook documentation should describe each capability separately.|Oleg Shulyakov|2026-05-22|

---

## Reference Links

- **Ref-1:** AGENTS.md public convention - <https://agents.md>
- **Ref-2:** Agent Skills quickstart - <https://agentskills.io/skill-creation/quickstart>
- **Ref-3:** Agent Skills specification - <https://agentskills.io/specification>
- **Ref-4:** Current technical specification - [SPEC.md](./SPEC.md)
- **Ref-5:** Agent Playbook draft - [Agent Playbook v0.0.5](../../pages/PLAYBOOK.md)
