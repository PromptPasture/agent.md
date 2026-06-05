---
name: remember
description: Preserve durable project facts, decisions, and useful observations in memory files. Use for memory requests like "remember this", "save context", "record a decision", "update memory", or preserving a project fact.
license: Apache-2.0
tags:
  - remember
  - memory
  - project-context
metadata:
  author: Oleg Shulyakov
  version: "1.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: productivity
---

# remember

Write durable project memory only when it will help future work.

---

## Workflow

1. Identify the fact, decision, convention, or observation to preserve.
2. Check whether it is durable, project-relevant, and safe to store.
3. Inspect existing `.agents/memory/MEMORY.md` and the current dated memory file when needed to avoid duplication.
4. Write concise notes under the existing memory convention.
5. Report what was recorded and where.

---

## Output

- **Use dated notes for task observations**: prefer `.agents/memory/YYYY-MM-DD.md` for day-specific implementation facts.
- **Use durable memory for stable facts**: use `.agents/memory/MEMORY.md` for ongoing project conventions or long-lived decisions when that file's structure supports it.
- **Mark uncertainty**: record assumptions as assumptions, not facts.
- **Avoid secrets**: do not store credentials, private tokens, personal sensitive data, or material the user did not intend to persist.
- **Avoid duplication**: link or summarize existing docs rather than copying large content.

---

## Boundaries

  Scenario: User explicitly asks to remember something
    Given the memory request is clear
    Then write the memory without asking for separate confirmation

  Scenario: Information has durable value
    Given the information is a project fact, decision, convention, recurring constraint, implementation observation, or useful handoff fact
    Then record it in the appropriate memory file

  Scenario: Information has low durable value
    Given the information is transient chatter, todo noise, sensitive information, an unverifiable assumption, or already captured better in durable docs
    Then do not store it as durable memory

---

## Error Paths

  Scenario: Content is sensitive
    Given the user asks to store secrets or sensitive information
    Then refuse to store the sensitive content
    And suggest storing the location or policy instead

  Scenario: Detail is transient
    Given the information is not worth durable memory
    Then explain that it should not be stored unless the user insists and it has future value

  Scenario: Claim is unverifiable
    Given writing the claim as fact would mislead future work
    Then record it as "user stated"
    And ask one clarifying question before storing it as fact when needed

---

## Verification

  Scenario: Output passes quality check
    Given memory has been written
    Then relevant existing memory was checked when practical
    And observed repository facts are distinguished from user-provided decisions
    And the updated file and note summary are reported
