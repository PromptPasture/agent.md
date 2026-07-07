---
name: dry
description: Catches duplicated knowledge, logic, or structure that should have a single authoritative source. Use when the user asks to "find duplication", "deduplicate", "DRY this up", or requests an explicit quality review of code, docs, or data models.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.0.2"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: quality
  tags: [dry, duplication, refactor, simplicity]
---

# DRY

Every piece of knowledge must have a **single source of truth** in the system.
Duplication forces every future change to be made in multiple places, and guarantees they will eventually diverge.

## Principle

Flag anything that repeats a fact, rule, structure, or decision already expressed elsewhere.
When producing new work, always check whether the knowledge already exists before expressing it again.

## Mode

**Producing** — apply before or during creation to avoid introducing duplication.
**Auditing** — apply to an existing artifact to find and consolidate duplicated knowledge.

Determine the mode from context. If unclear, ask.

## Workflow

### When Producing

1. Before adding a fact, rule, constant, or structure — check if it already exists in the system.
2. If it exists — reference or import it; do not restate it.
3. If it does not exist — establish it as the single source of truth and reference it everywhere else.
4. Flag any cases where a shared source does not yet exist and one should be created.

### When Auditing

1. **Identify the target** — any artifact: code, schema, config, spec, doc, or process definition.
2. **Map the knowledge units** — identify distinct facts, rules, structures, and decisions expressed in the artifact.
3. **Scan for repetition** — apply the relevant checklist sections below.
4. **Assess each finding** — confirm the copies are truly the same knowledge, not coincidentally similar values. Avoid false positives on separate concerns that happen to look alike.
5. **Recommend consolidation** — identify where the single source of truth should live and how the copies should reference it.

## Checklist

Apply the sections relevant to the artifact being reviewed.

### Code

- [ ] **Duplicated logic** — same computation, condition, or algorithm in multiple places
- [ ] **Copy-pasted blocks** — identical or near-identical code segments across functions or modules
- [ ] **Repeated constants** — the same magic value or string literal in multiple locations without a named source
- [ ] **Parallel data structures** — two collections that must always stay in sync (e.g., an enum and a matching array)
- [ ] **Reimplemented utilities** — logic already provided by a shared library or existing helper

### Configuration & Schema

- [ ] **Duplicated config values** — the same setting defined in multiple config files or environments
- [ ] **Repeated schema definitions** — the same field shape defined independently in multiple schemas or types
- [ ] **Redundant validation rules** — the same constraint enforced separately at multiple layers without a shared source

### Documentation & Specs

- [ ] **Copy-pasted requirements** — the same rule or acceptance criterion stated in multiple tickets, docs, or specs
- [ ] **Duplicated data dictionaries** — field definitions maintained in both a schema and a separate doc
- [ ] **Repeated decision rationale** — the same architectural or product decision recorded in multiple places without a single authoritative ADR or doc

### Process & Tooling

- [ ] **Duplicate pipeline steps** — the same build, test, or deploy step defined in multiple CI/CD configs
- [ ] **Redundant scripts** — multiple scripts performing the same operation with minor variation
- [ ] **Overlapping runbooks** — the same incident or operational procedure documented in more than one place

## Output

**When producing**, inline guidance is sufficient — note what was reused or centralised before finalising the artifact.

**When auditing**, use this structure:

```text
Findings:
- [High/Medium/Low] Short title — locations of all copies
  What knowledge is duplicated, where each copy lives, and recommended consolidation approach.

Summary:
[One sentence: how many findings, the highest-risk divergence risk, and the highest-priority consolidation.]
```

Omit `Findings` if none. In that case, say "No DRY violations found." and note any near-duplicates reviewed and kept as intentionally separate concerns.

## Rules

- Confirm copies represent the same knowledge, not merely similar-looking values with independent meanings. Two unrelated constants that happen to share a value are not a DRY violation.
- Do not conflate DRY with YAGNI or KISS. Do not flag unused code or complexity unless the root cause is unintended duplication.
- Prefer consolidation that makes the single source of truth obvious and easy to find. A shared module, named constant, or referenced doc beats an inline comment.
- Do not modify the artifact unless the user explicitly asks for changes after the audit.
- If context is insufficient to confirm two copies share the same knowledge, mark it as an open question rather than a violation.
- Prefer fewer high-confidence findings over speculative commentary.
