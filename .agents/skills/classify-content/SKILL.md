---
name: classify-content
description: Organize material into meaningful groups. Use for "classify", "categorize", "group", "cluster", "sort", "taxonomy", "organize these", and grouping by criteria, priority, dependency, similarity, or abstraction level.
license: MIT
version: 1.0.0
tags:
  - classify
  - taxonomy
  - organization
author: Oleg Shulyakov
metadata:
  catalog: utility
---

# classify-content

Group material by explicit criteria while preserving edge cases.

## Scope

**Use this skill when the primary task is assigning items to meaningful groups.**

- **Trigger on grouping**: use for "classify", "categorize", "group", "cluster", "sort", "taxonomy", "organize these", and requests to group items by explicit criteria.
- **Support many criteria**: group by similarity, difference, category, priority, dependency, abstraction level, user need, risk, ownership, or another stated lens.
- **Respect ambiguity**: keep multi-fit, unclear, or unclassified items visible instead of forcing false precision.
- **Do not decide by default**: classification may inform a decision, but the primary output is labeled organization.

---

## Workflow

**State the grouping lens before assigning items.**

1. Identify the items to classify and any user-provided criteria.
2. Define or infer the grouping criteria, marking inferred criteria as assumptions.
3. Create clear group labels with short definitions.
4. Place each item into one or more groups as appropriate.
5. Call out ambiguous, duplicate, out-of-scope, or unclassified items.

---

## Output

**Make the taxonomy easy to inspect and revise.**

- **Lead with criteria**: state the grouping rule before or alongside the groups.
- **Use stable labels**: choose labels that describe the underlying reason items belong together.
- **Preserve source text**: keep item names recognizable unless normalization is requested.
- **Explain edge cases**: briefly note why ambiguous items are multi-fit or unresolved.
- **Offer refinements**: suggest a better lens only when the requested criteria produce weak groups.

---

## Error Paths

**When the items or criteria are unclear, classify what can be classified and isolate the rest.**

- **No criteria provided**: infer a practical lens and state it as an assumption.
- **Too little item detail**: group by observable wording and list what context would improve accuracy.
- **Conflicting criteria**: choose the primary criterion first, then note secondary tags if useful.

---

## Verification

**Check for useful categories, not tidy-looking fiction.**

- **Every group has a reason**: remove or merge groups whose distinction does not matter.
- **Every item is accounted for**: placed, multi-labeled, or explicitly unclassified.
- **Ambiguity remains visible**: do not hide uncertainty to make the table look clean.
