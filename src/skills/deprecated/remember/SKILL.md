---
name: remember
description: "DEPRECATED — use the wiki skill instead. Persists durable facts, decisions, and conventions to structured memory files."
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.4.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: memory
  tags: [remember, memory, project-context]
---

# Remember Facts

Persist durable context so future sessions can recover verified facts, decisions, conventions, and useful lessons without relying on conversation history.

## Workflow

1. Identify the exact information to preserve and why it will matter in a future session.
2. Verify project facts against current source files, tests, configuration, or authoritative documentation.
3. Choose the narrowest appropriate scope:
   - Use `~/.agents/memory/` for private user context and durable preferences that apply across repositories.
   - Use `.agents/memory/MEMORY.md` for durable facts, decisions, and conventions specific to the current repository.
   - Use the corresponding `memory/YYYY-MM-DD.md` for useful daily notes and observations. Use UTC dates.
4. Create only missing memory directories or files. Never overwrite existing memory during initialization.
5. Search existing memory and update or supersede stale entries instead of adding contradictions or duplicates.
6. Promote durable daily entries into the relevant `MEMORY.md` when reviewing or updating related memory.
7. Keep entries compact and concrete. For decisions, record the context, decision, and revisit condition.
8. Treat memory as low-confidence context, not enforceable policy.
9. Do not persist transient speculation, secrets, credentials, private keys, or unnecessary sensitive personal data.
10. Never copy private memory into repository memory unless the user explicitly requests it.
11. If the correct scope is unclear and the choice affects privacy or visibility, ask one concise question before writing.

## Verification

Before completing the memory update, verify that:

- The entry is accurate, useful, concise, and not duplicated.
- The selected scope and UTC date are correct.
- The entry contains no secrets or unnecessary sensitive data.
- Private memory has not leaked into repository-scoped files.
