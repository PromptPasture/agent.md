---
name: investigate
description: You MUST use this before drawing conclusions about local repository, document, or artifact context — do not assume. Investigates and reports evidence-backed findings from local sources only. Use for local investigation requests like "investigate", "find where", "understand this repo", "trace", and local-context research; do not use for web search.
license: Apache-2.0
tags:
  - local-investigation
  - investigation
  - local-context
metadata:
  author: Oleg Shulyakov
  version: "1.3.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: research
---

# Investigation

Investigate local context and report evidence-backed conclusions.

## Workflow

1. Define the question and local scope.
2. Inspect the named targets and repository guidance before searching related files, symbols, references, history, configuration, and tests.
3. Follow relevant connections far enough to understand the behavior and test plausible alternative explanations.
4. Prefer current source code, tests, and configuration over memory, names, comments, generated summaries, or stale documentation.
5. Separate confirmed facts, supported inferences, conflicting evidence, and unknowns.
6. Stop when local evidence answers the question or cannot resolve the remaining uncertainty.

## Output

- **Lead with the answer**: state the conclusion or that local evidence is insufficient.
- **Cite local evidence**: identify precise sources for each material conclusion.
- **State uncertainty**: label inferences, conflicts, unknowns, and confidence limits.
- **Report missing context**: identify missing targets and what was searched.
- **Keep scope tight**: omit search transcripts and findings unrelated to the question.
- **Respect boundaries**: do not modify files or perform external research unless the user explicitly requests it.

## Verification

- Every material conclusion is traceable to inspected local evidence.
- Facts and inferences are distinct.
- Conflicts and unresolved gaps are visible.
- Confidence matches the available evidence.
- No external claims or unrelated recommendations were introduced.
