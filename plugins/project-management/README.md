# Project Management Plugin

Pre-built Jira workflows for [Cowork](https://claude.com/product/cowork), Anthropic's agentic desktop application — also works in Claude Code, Codex, and OpenCode. Built for a Scrum team of 5–10 people running 2-week sprints. Fully self-contained — no dependency on any other plugin.

You don't need to memorize anything. Just tell Claude what you need — "what's the team working on," "the board is a mess," "plan the next sprint," "write this up as a ticket" — and it routes you to the right workflow. Every workflow pauses before changing anything in Jira, so nothing happens without your say-so.

> **Important**: This plugin assists with project-management workflows but does not make product, staffing, or performance decisions. All outputs should be reviewed by you before use.

## Installation

### Cowork

Install the packaged `project-management.plugin` file directly.

### Claude Code

```bash
claude plugin install https://github.com/PromptPasture/agent.md/tree/main/plugins/project-management
```

### Codex

```bash
codex plugin install https://github.com/PromptPasture/agent.md/tree/main/plugins/project-management
```

Or manually: clone the skills into your project's `.agents/skills/` directory:

```bash
git clone --depth 1 https://github.com/PromptPasture/agent.md /tmp/promptpasture
cp -r /tmp/promptpasture/plugins/project-management/skills/* .agents/skills/
rm -rf /tmp/promptpasture
```

The Atlassian MCP server is configured via `.mcp.json` at the plugin root — Codex picks it up automatically.

### OpenCode

Clone the repo and point `skills.paths` at the local skills directory:

```bash
git clone --depth 1 https://github.com/PromptPasture/agent.md ~/.agents/promptpasture
```

Then add to your existing `opencode.json`:

```json
{
  "skills": {
    "paths": ["~/.agents/promptpasture/plugins/project-management/skills"]
  },
  "mcp": {
    "atlassian": {
      "type": "remote",
      "url": "https://mcp.atlassian.com/v1/mcp",
      "enabled": true
    }
  }
}
```

Restart OpenCode after adding the config.

## What you'll need to connect

**Jira (via the Atlassian MCP connector)** — powers the Jira-dependent workflows below. A few skills work standalone (from what you tell the agent) even without it — see the table.

- **Cowork / Claude Code**: uses the built-in Atlassian MCP server
- **Codex**: configure the Atlassian MCP server in `config.toml` or via `.mcp.json`
- **OpenCode**: configured via `opencode.json` (included in this plugin)

## Skills

|Skill|What it does|Needs Jira?|
|---|---|---|
|`pm-router`|The front door — routes open-ended requests to the right skill|—|
|`status-brief`|One-page sprint status: burndown, shipped, blocked, week ahead|Yes|
|`ticket-triage`|Ranks open tickets by urgency/staleness/priority; flags unassigned & overdue|Yes|
|`board-cleanup`|Finds stale tickets, likely duplicates, and missing fields; fixes what you approve|Yes|
|`sprint-close`|Reconciles planned vs. completed scope, flags spillover, writes a retro-ready summary|Yes|
|`sprint-planning`|Plans the next sprint: capacity, scope, sprint goal, risks|No (Jira only needed to create the sprint)|
|`roadmap-update`|Builds or updates a Now/Next/Later roadmap from epics; prioritization frameworks|No (Jira only needed to pull/update epics)|
|`write-ticket`|Writes a feature spec/PRD with goals, non-goals, requirements, acceptance criteria|No|

## How it works

Say what you need in plain English. `pm-router` figures out which skill applies, tells you what it's about to do, and waits for your go-ahead. Every skill that would change something in Jira — closing a ticket, merging a duplicate, updating a field, creating a sprint — shows you the change and waits for approval before writing anything.

## Platform compatibility

|Platform|Skill format|MCP config|Plugin manifest|
|---|---|---|---|
|Cowork / Claude Code|`skills/<name>/SKILL.md`|`.mcp.json`|`.claude-plugin/plugin.json`|
|Codex|`skills/<name>/SKILL.md`|`.mcp.json`|`.codex-plugin/plugin.json`|
|OpenCode|`skills/<name>/SKILL.md`|`opencode.json`|`opencode.json`|
