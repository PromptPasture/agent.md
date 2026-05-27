---
name: remember
description: Preserve durable project facts, decisions, and useful observations in memory files. Use for memory requests like "remember this", "save context", "record a decision", "update memory", or preserving a project fact.
license: MIT
tags:
  - remember
  - memory
  - project-context
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
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

- **Auto-approve explicit memory**: when the user clearly asks to remember something, write the memory without asking for separate confirmation.
- **Store durable value**: record project facts, decisions, conventions, recurring constraints, implementation observations, and useful handoff facts.
- **Reject low-value memory**: do not store transient chatter, todo noise, sensitive information, unverifiable assumptions as fact, or details already captured better in durable docs.

---

## Error Paths

- **Sensitive content**: refuse to store secrets and suggest storing the location or policy instead.
- **Transient detail**: explain that it is not worth durable memory unless the user insists and it has future value.
- **Unverifiable claim**: record as "user stated" or ask one clarifying question if writing it as fact would mislead future work.

---

## Verification

- **Read before writing**: check relevant existing memory when practical.
- **Keep provenance clear**: distinguish observed repository facts from user-provided decisions.
- **Report the write**: tell the user the file updated and summarize the note.
