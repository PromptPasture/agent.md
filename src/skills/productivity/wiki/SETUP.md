# Wiki skill — setup

The wiki skill works out of the box with no configuration. This file covers how to change the wiki location and enable autonomous maintenance.

## Add to your agent configuration

Add this line to your `AGENTS.md` or `CLAUDE.md`:

```
Wiki knowledge base → read `~/.agents/skills/wiki/SKILL.md`
```

## Default behavior

- Wiki lives in `docs/` of the current repo.
- The skill is triggered explicitly: invoke `/wiki` or say "add to wiki", "update wiki", "ingest this", etc.
- The agent never writes wiki entries unless you ask.

## Change the wiki location

Add one line to your `AGENTS.md` or `CLAUDE.md`:

```
Wiki location: .agents/wiki/
```

For a global wiki shared across all repos, add it to `~/.agents/AGENTS.md`:

```
Wiki location: ~/.agents/wiki/
```

The skill checks `AGENTS.md`/`CLAUDE.md` first, then falls back to `docs/`.

## Enable autonomous mode

Add instructions to `AGENTS.md` or `CLAUDE.md` to have the agent maintain the wiki without being asked each time.

**Ingest sources automatically:**

```
When I drop a new file into docs/inbox/, use the wiki skill to ingest it:
extract key concepts, write or update entries, and update index.md and changelog.md.
```

**File valuable query answers:**

```
When a wiki query produces a useful synthesis or comparison, offer to file
it as a new wiki entry before ending the response.
```

**Write during conversations:**

```
During any conversation, if you learn a fact, decision, or concept that
belongs in the wiki, write it without being asked.
```

Mix and match. The more specific the instruction, the more predictable the behavior.

## First use

1. Invoke the skill: type `/wiki` or say "add to wiki".
2. Describe the concept: "Add an entry for our database naming convention."
3. The agent writes the entry, creates `index.md` if absent, and appends to `changelog.md`.
4. Verify: open the wiki directory and check that the entry file, `index.md`, and `changelog.md` are all present and correct.

## Relationship to the `remember` skill

The `remember` skill is deprecated. Use `wiki` instead. The wiki covers the same need — persisting durable facts and decisions — with structure, typing, and human visibility added.
