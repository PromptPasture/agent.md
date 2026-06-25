---
status: DRAFT
documentType: PRD
phase: discovery
createdAt: "2026-05-24"
updatedAt: "2026-05-24"
author: Oleg Shulyakov
owner: Oleg Shulyakov
stakeholders: Users and maintainers of this agent.md skill library
tags:
  - agents
  - rules
  - skills
  - engineering-principles
related:
  - SPEC.md
  - Most Popular Principles.md
---

# PRD: Engineering Principles for Agent Instructions

## Objective

Integrate common engineering principles into `.agents` so coding, review, and skill-authoring behavior becomes more consistent without turning every skill into a principles textbook.

The collected principles in `Most Popular Principles.md` are useful, but they are currently source material rather than executable agent guidance. The product goal is to translate them into concise runtime instructions, targeted skill behavior, and review lenses that help agents choose simpler, better-scoped implementations.

Without this integration, agents may apply principles inconsistently: overusing SOLID as ceremony, treating DRY as a ban on repeated syntax, skipping YAGNI during implementation, or doing unrelated cleanup under the Boy Scout Rule.

---

## Goals

|Goal ID|Target Outcome|Success Metric|
|---|---|---|
|G-1|Establish a shared engineering-principles rule for `.agents`.|One concise global rule exists under `src/rules/` and is referenced by implementation-facing skills where useful.|
|G-2|Make principles operational in code-writing and code-review workflows.|`code-backend`, `code-frontend`, `code-database`, `code-tests`, `review-code`, and `create-skill` apply relevant principle lenses without duplicating the full source document.|
|G-3|Keep runtime instructions token-efficient.|New or edited runtime guidance is concise and avoids copying the entire collected principles list into every skill.|
|G-4|Preserve pragmatic judgment.|Guidance explicitly treats KISS and YAGNI as default brakes, DRY as knowledge deduplication, and SOLID as useful only when it reduces real coupling or change risk.|

---

## Target Audience Focus

- **Persona ID: P-1** Agent user: Wants implementation changes that are simple, scoped, maintainable, and verifiable.
- **Persona ID: P-2** Skill maintainer: Needs reusable quality guidance that can be applied across skills without bloating each `SKILL.md`.
- **Persona ID: P-3** Code reviewer [assumed]: Wants principle-based findings grounded in concrete failure modes, not style preferences.

---

## Scope

### In Scope

- Create a compact `src/rules/engineering-principles.md` rule.
- Translate SOLID, DRY, KISS, YAGNI, Law of Demeter, Composition Over Inheritance, Boy Scout Rule, CQS, and Separation of Concerns into practical agent behavior.
- Update selected implementation and review skills only where the principle changes expected behavior.
- Add or update focused eval prompts where needed to check that agents avoid over-engineering, speculative abstraction, and vague principle-name dropping.
- Keep `Most Popular Principles.md` as source material, not a runtime instruction file.

### Out of Scope

- Rewriting every skill to mention every principle.
- Enforcing principles mechanically as absolute rules.
- Adding a new standalone `engineering-principles` skill unless later evidence shows rule-level guidance is insufficient.
- Broad refactors of existing skills unrelated to principle integration.
- Changing project `AGENTS.md` behavior unless a later implementation decision requires it.

### Later

- Add a quality-gate script that checks changed skills for excessive principle duplication or vague principle wording.
- Add examples showing good and bad applications of each principle in agent-generated code.

---

## Functional Requirements

|Requirement ID|Capability / Feature|Priority|Acceptance Criteria|Tracker|
|---|---|---|---|---|
|FR-1|Define a global engineering-principles rule.|MUST|A new `src/rules/engineering-principles.md` exists with metadata, scope, and concise guidance for applying the collected principles pragmatically.|TBD|
|FR-2|Prioritize simplicity before abstraction.|MUST|The rule states that KISS and YAGNI are default constraints for implementation and that new abstractions require evidence of reduced complexity, duplication of knowledge, coupling, or test risk.|TBD|
|FR-3|Clarify DRY behavior.|MUST|Guidance distinguishes duplicated knowledge or business logic from harmless repeated syntax, markup, or test setup.|TBD|
|FR-4|Clarify SOLID behavior.|MUST|Guidance applies SRP, ISP, DIP, and related principles through clear responsibilities, small interfaces, and explicit dependencies without adding ceremonial layers.|TBD|
|FR-5|Scope Boy Scout cleanup.|MUST|Guidance allows cleanup only in touched code or code required for the requested change, and forbids unrelated opportunistic refactors.|TBD|
|FR-6|Add principle lenses to implementation skills.|SHOULD|`code-backend`, `code-frontend`, `code-database`, and `code-tests` contain targeted principle guidance only where it changes implementation behavior.|TBD|
|FR-7|Add principle lenses to review and skill-authoring workflows.|SHOULD|`review-code` and `create-skill` can identify over-abstraction, duplicated knowledge, unclear responsibilities, leaky dependencies, and untestable side effects as concrete issues.|TBD|
|FR-8|Add focused eval coverage.|COULD|At least one eval or test prompt verifies the agent rejects speculative abstraction and one verifies it flags duplicated business rules over duplicated text.|TBD|

---

## Non-Functional Requirements

|NFR ID|Category|Target Specification|
|---|---|---|
|NFR-1|Token Efficiency|Runtime instructions should summarize principle behavior rather than repeat definitions available in the source document.|
|NFR-2|Maintainability|Principle guidance should live primarily in one rule and be referenced or locally specialized only where needed.|
|NFR-3|Practicality|Guidance must favor concrete behavior and failure modes over principle-name dropping.|
|NFR-4|Compatibility|Changes must preserve existing skill names, folder layout, metadata style, and validation workflow.|
|NFR-5|Reviewability|The implementation should be small enough to review as a focused docs/rules/skills change.|

---

## Milestones

|Milestone|Target Date|Exit Criteria|Owner|
|---|---|---|---|
|M-1|TBD|PRD and SPEC drafted.|Oleg Shulyakov|
|M-2|TBD|Global rule drafted and reviewed.|Oleg Shulyakov|
|M-3|TBD|Targeted skill updates completed.|TBD|
|M-4|TBD|Markdown lint and skill validation checks pass or known gaps are documented.|TBD|

---

## User Journeys / Key Flows

1. A user asks the agent to implement a small backend change. The agent checks local patterns, chooses the smallest complete change, avoids speculative extension points, and adds focused verification.
2. A user asks for a code review. The agent flags a duplicated business rule or unclear responsibility when it creates a concrete risk, but ignores harmless repeated markup or style preferences.
3. A maintainer edits a skill. The agent keeps `SKILL.md` concise, moves detailed examples to references only when they reduce ambiguity, and avoids introducing a new layer unless it improves runtime behavior.

---

## Risks, Assumptions, & Mitigations

|Risk ID|Assumption / Risk Description|Impact|Mitigation Strategy|Status|
|---|---|---|---|---|
|R-1|Principle guidance could become verbose and reduce runtime precision.|HIGH|Put the canonical short guidance in one rule and only specialize skills where needed.|OPEN|
|R-2|Agents could enforce principles mechanically.|HIGH|State that principles are decision lenses and must be balanced against local context, requested scope, and verification.|OPEN|
|R-3|SOLID guidance could encourage unnecessary layers.|MEDIUM|Explicitly require evidence that an abstraction reduces coupling, complexity, duplication of knowledge, or test risk.|OPEN|
|R-4|Boy Scout guidance could justify unrelated cleanup.|MEDIUM|Scope cleanup to touched code or required nearby code.|OPEN|
|R-5|Existing rules may already cover some behavior.|LOW|Patch existing guidance surgically and avoid duplicate wording.|OPEN|

---

## External Dependencies

|Dependency ID|Item|Impacted Requirements|Validation Owner|
|---|---|---|---|
|D-1|`docs/2026-05-23-design-principles/Most Popular Principles.md`|FR-1 through FR-5|Oleg Shulyakov|
|D-2|Existing `src/rules/karpathy-guidelines.md`|FR-1, FR-2, FR-5|Oleg Shulyakov|
|D-3|Existing implementation and review skills|FR-6, FR-7|TBD|

---

## Open Questions

|Question ID|Question|Answer / Decision|Owner|Resolution Date|
|---|---|---|---|---|
|Q-1|Should this be only a global rule, or also a standalone skill?|Proposed: start as a global rule; create a skill only if users ask to reason explicitly about engineering principles.|Oleg Shulyakov|TBD|
|Q-2|Which skills should receive direct updates in the first implementation pass?|Proposed: `code-backend`, `code-frontend`, `code-database`, `code-tests`, `review-code`, and `create-skill`.|Oleg Shulyakov|TBD|
|Q-3|Should eval coverage be added now or after the first rule/skill update?|TBD|Oleg Shulyakov|TBD|

---

## Reference Links

- **Ref-1**: Source principles collection - `docs/2026-05-23-design-principles/Most Popular Principles.md`
- **Ref-2**: Existing simplicity and verification guidance - `src/rules/karpathy-guidelines.md`
