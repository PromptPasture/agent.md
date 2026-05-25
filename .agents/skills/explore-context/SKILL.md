---
name: explore-context
description: Investigate local repository, document, and attached-artifact context. Use for local investigation requests like "investigate", "find where", "understand this repo", "trace", and local-context research; do not use for web search.
license: MIT
tags:
  - local-investigation
  - investigation
  - local-context
metadata:
  author: Oleg Shulyakov
  version: "1.0.2"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: research
---

# explore-context

Investigate local context and report evidence-backed findings.

---

## Workflow

1. Identify the target concept, behavior, file, command, error, or workflow.
2. Search names, strings, docs, tests, configuration, and related symbols.
3. Follow call paths, imports, references, generated sources, and tests only as needed.
4. Distinguish live behavior from dead code, examples, fixtures, or stale docs.
5. Summarize findings, gaps, and confidence with references.

---

## Output

- **Lead with the answer**: state what was found or not found.
- **Cite local evidence**: include file paths, line references when available, and relevant commands.
- **Separate inference**: label deductions that are not directly stated in files.
- **Name gaps**: call out missing files, inaccessible artifacts, ambiguous ownership, or unverified runtime behavior.
- **Keep scope tight**: do not explain unrelated systems discovered during the search.

---

## Boundaries

- **Stay local**: search local files, project docs, attached artifacts, repository history, and available workspace context only.
- **Exclude web research**: do not perform web search, browsing, or current-information research as part of this skill.
- **Report evidence**: ground findings in file references, artifact references, command output, or clearly marked inference.

---

## Error Paths

- **No matches**: say what was searched and suggest the next local search path.
- **Conflicting sources**: prefer runtime wiring and tests over stale docs, and state the conflict.
- **Generated or external code missing**: identify the missing source and how it affects confidence.

---

## Verification

- **Reproduce key searches**: use fast local search before relying on memory.
- **Prefer primary files**: cite implementation, tests, configs, or authoritative docs over secondary mentions.
- **No external claims**: leave web or current-information research to an explicit user request outside this skill.
