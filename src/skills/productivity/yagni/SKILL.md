---
name: yagni
description: Catches speculative additions before they are built. Use when the user asks to "flag YAGNI", "is this needed?", "trim scope", or requests an explicit scope audit of code, plans, or specs.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.0.1"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: quality
  tags: [yagni, simplicity, scope, refactor]
---

# YAGNI

Build only what is needed **now** to satisfy a concrete, stated requirement.
Speculative additions accumulate cost across every artifact: code that must be maintained, designs that must be explained, specs that must be refined, and plans that never ship.

## Principle

Flag anything whose sole justification is "we might need this later" or "just in case."
When producing new work, challenge every addition against a current, concrete requirement before including it.

## Mode

**Producing** — apply before or during creation to keep scope minimal.
**Auditing** — apply to an existing artifact to find and remove speculative additions.

Determine the mode from context. If unclear, ask.

## Workflow

### When Producing

1. Clarify the concrete requirements in scope right now.
2. For each proposed addition, ask: does a current stated requirement justify this?
3. If yes — include it. If no — exclude it and note it as a future candidate only if the user asks.
4. Flag any assumptions being made about future needs and surface them explicitly.

### When Auditing

1. **Identify the target** — any artifact: code, API design, data model, architecture doc, PRD, task list, roadmap, or process definition.
2. **Map stated requirements** — list only what is explicitly required right now by the user, ticket, or spec.
3. **Scan for speculative additions** — apply the relevant checklist sections below to the artifact type.
4. **Assess each finding** — confirm it has no current stated requirement, consumer, or trigger. Avoid false positives on items that are indirectly required or mandated by an external contract.
5. **Recommend remove or defer** — prefer removal; suggest deferral only when the item would be expensive to reconstruct later and cheap to carry now.

## Checklist

Apply the sections relevant to the artifact being reviewed.

### Product & Planning

- [ ] **Unvalidated features** — feature or story with no user signal, metric, or confirmed need
- [ ] **Speculative roadmap items** — work planned beyond the current cycle with no committed driver
- [ ] **Pre-emptive edge case handling** — requirements for scenarios not yet observed or reported
- [ ] **Premature internationalisation or accessibility scope** — full i18n or a11y work before any user in that segment exists
- [ ] **Future-user personas** — design decisions made for a user type not yet served

### Architecture & Design

- [ ] **Premature scalability** — queues, caches, sharding, or CDN layers before load requires them
- [ ] **Speculative service boundaries** — microservice or module split before the seam is proven necessary
- [ ] **Unused integration points** — webhook endpoints, plugin systems, or extension hooks with no current consumer
- [ ] **Over-specified protocols** — versioned APIs, negotiation headers, or capability flags for a single current client
- [ ] **Generic frameworks for one use case** — abstraction that supports N variants but only one exists

### Code

- [ ] **Unused parameters or options** — function accepts arguments no caller passes
- [ ] **Dead branches** — `if`/`switch` paths with no current trigger
- [ ] **Abstraction layers with one implementation** — interface, base class, or factory wrapping a single concrete type
- [ ] **Speculative fields or columns** — data model attributes no code reads or writes
- [ ] **Future-proofing comments** — `// for later`, `// might need`, `// extensible for X`
- [ ] **Unused exports** — public API surface with no known consumer
- [ ] **Version scaffolding with no migration** — versioned routes or schema slots added "for future versions"
- [ ] **Feature flags always on or always off** — flags with no active toggle path
- [ ] **Over-engineered error handling** — retry logic or circuit breakers for paths that cannot currently fail that way

### Process & Tooling

- [ ] **Environments with no current use** — staging, canary, or DR setups not yet exercised
- [ ] **Monitoring for non-existent behaviour** — alerts or dashboards tracking metrics no code emits
- [ ] **Premature documentation** — docs for features not yet built or APIs not yet published
- [ ] **Speculative CI/CD stages** — pipeline steps for deployment targets not yet live

## Output

**When producing**, inline guidance is sufficient — note what was excluded and why before finalising the artifact.

**When auditing**, use this structure:

```text
Findings:
- [High/Medium/Low] Short title — artifact location or section
  What it is, why it has no current requirement, and recommended action (remove / defer).

Summary:
[One sentence: how many findings, overall scope impact, and the highest-priority action.]
```

Omit `Findings` if none. In that case, say "No YAGNI violations found." and note any borderline cases reviewed and kept.

## Rules

- Only flag items with no current stated requirement, consumer, or trigger. Do not flag items that are indirectly used or mandated by an external contract or standard.
- Do not conflate YAGNI with DRY or KISS. Do not flag duplication or complexity unless the root cause is a speculative addition.
- Do not modify the artifact unless the user explicitly asks for changes after the audit.
- If context is insufficient to confirm a finding, mark it as an open question rather than a violation.
- Prefer fewer high-confidence findings over speculative commentary.
