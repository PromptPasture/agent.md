---
name: git-branch
description: You MUST use this for branch name requests and branch actions. Create, switch, or rename Git branches using repository-aware branch naming conventions.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: version-control
  tags: [git, branch]
---

# Git Branching

Generate, switch, and apply clear Git branch names that follow repository and team conventions.

---

## Workflow

1. Classify the request as an output or action workflow.
2. Inspect repository context when it can affect the branch name or action.
3. Apply the naming rules below.
4. Return only the requested branch name for pure generation requests.
5. For actions, inspect the current branch and worktree before running Git.

### Output Workflow

Use when the user asks to generate, suggest, improve, or review a branch name.

For pure generation requests, return only the branch name unless the user asks
for options or rationale. Reviews may include concise, actionable feedback.

### Action Workflow

Use when the user asks to create, start, switch, check out, or rename a branch.

- Preserve user work. Never reset, discard, or overwrite changes.
- If the requested branch already exists, switch to it only when that clearly
  matches the request; otherwise report the conflict.
- Report the command outcome or any blocker that prevents completion.

---

## Branch Name Structure

```text
<type>/<ticket-id>-<short-description>
```

| Part | Required | Notes |
| --- | --- | --- |
| `type` | Yes | Category prefix (see below) |
| `ticket-id` | If available | Lowercase issue/ticket ID, e.g. `proj-123` or `42` |
| `short-description` | Yes | kebab-case summary of the work |

**Examples:**

- **Feature:** `feature/proj-42-user-authentication`
- **Bugfix:** `bugfix/proj-101-fix-login-redirect`
- **Hotfix:** `hotfix/payment-null-pointer-crash`
- **Chore:** `chore/upgrade-node-18`
- **Release:** `release/v2.4.0`

---

## Type Prefixes

| Prefix | When to Use |
| --- | --- |
| `feature/` | New functionality or user-facing capability |
| `bugfix/` | Non-urgent bug fixes going through normal workflow |
| `hotfix/` | Urgent fixes that go directly to production/main |
| `release/` | Release preparation branches (`release/v1.2.0`) |
| `chore/` | Maintenance, dependency updates, config changes, refactors |
| `docs/` | Documentation-only changes |
| `test/` | Adding or fixing tests with no production code change |
| `experiment/` | Exploratory work, spikes, or proof-of-concepts |

---

## Action Words

Treat these user words as branch action intent:

| User wording | Git behavior |
| --- | --- |
| `create a branch` | Create a new branch from the current `HEAD` |
| `start a branch` | Create and switch to a new branch |
| `checkout a branch` | Create/switch if clearly requested by the user |
| `switch to a branch` | Switch to an existing branch, or create if asked |
| `rename this branch` | Rename the current branch after checking context |

Prefer `git switch -c <branch>` for creating and switching to a new branch. Prefer `git switch <branch>` for switching to an existing branch.

---

## Formatting Rules

1. **kebab-case only** — Use hyphens, never underscores or spaces.
   - ✅ `feature/user-profile-settings`
   - ❌ `feature/user_profile_settings`
   - ❌ `feature/User Profile Settings`

2. **Lowercase** — All characters should be lowercase.
   - ✅ `bugfix/proj-99-fix-api-timeout`
   - ❌ `BugFix/Proj-99-Fix-API-Timeout`

3. **Keep it short but descriptive** — Aim for 3–6 words in the description segment. Max ~60 characters total.
   - ✅ `feature/add-dark-mode-toggle`
   - ❌ `feature/add-a-new-dark-mode-toggle-setting-to-the-user-preferences-page`

4. **No special characters** — Use one `/` between the type prefix and branch
   description. Otherwise, avoid `/`, `\`, `@`, `#`, `~`, `^`, `:`, `?`, `*`,
   and spaces; hyphens are the only other allowed non-alphanumeric characters.

5. **Include ticket ID when available** — Makes branches traceable to issues.
   - ✅ `bugfix/gh-204-session-expiry-error`
   - ✅ `feature/123-export-to-csv` _(if project uses numeric IDs only)_

6. **No trailing slashes or dots.**
   - ❌ `feature/add-search.`
   - ❌ `feature/`

---

## When the User Provides a Branch Name for Review

Check it against:

- [ ] Correct type prefix used?
- [ ] Ticket ID included (if relevant)?
- [ ] kebab-case, all lowercase?
- [ ] Under ~60 characters?
- [ ] No special characters or spaces?
- [ ] Description is meaningful (not vague like `fix` or `stuff`)?

Give specific, actionable feedback. If the name is mostly fine, say so and suggest a small tweak. If it's unclear what the branch is for, ask what the task is before suggesting a name.

---

## Verification

- Generated and reviewed names satisfy the formatting rules.
- Action workflows leave the repository on the requested branch.
- Existing user changes remain intact.
