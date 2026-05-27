---
name: investigate
description: Investigate local repository, document, and attached-artifact context. Use for local investigation requests like "investigate", "find where", "understand this repo", "trace", and local-context research; do not use for web search.
license: MIT
tags:
  - local-investigation
  - investigation
  - local-context
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: research
---

# investigate

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

  Scenario: Investigation stays local
    Given the user asks for local investigation
    Then search local files, project docs, attached artifacts, repository history, and available workspace context only

  Scenario: Web research would be needed
    Given the answer requires web search, browsing, or current-information research
    Then do not perform it as part of this skill
    And state that external research is outside the local investigation scope

  Scenario: Findings are reported
    Given findings are presented
    Then ground them in file references, artifact references, command output, or clearly marked inference

---

## Error Paths

  Scenario: No matches are found
    Given local searches return no matches
    Then say what was searched
    And suggest the next local search path

  Scenario: Sources conflict
    Given local sources disagree
    Then prefer runtime wiring and tests over stale docs
    And state the conflict

  Scenario: Generated or external code is missing
    Given a needed generated or external source is unavailable
    Then identify the missing source
    And explain how it affects confidence

---

## Verification

  Scenario: Output passes quality check
    Given local findings have been produced
    Then key searches were run before relying on memory
    And implementation, tests, configs, or authoritative docs are preferred over secondary mentions
    And no external or current-information claims are introduced
