---
title: Complete Guide to Building Skills
source: "https://claude.com/blog/complete-guide-to-building-skills-for-claude"
author: Anthropic
published: 2026-01-29
---

<!-- markdownlint-disable-next-line MD025 -->
# Complete Guide to Building Skills

## Introduction

A **skill** is a set of instructions — packaged as a simple folder — that teaches an AI agent how to handle specific tasks or workflows. Skills are one of the most powerful ways to customize agents for your specific needs. Instead of re-explaining your preferences, processes, and domain expertise in every conversation, skills let you teach the workflow once and benefit every time.

Skills are powerful when you have repeatable workflows: generating frontend designs from specs, conducting research with consistent methodology, creating documents that follow your team’s style guide, or orchestrating multi-step processes. They work well with agent capabilities like code execution, document creation, browsing, and tool use. For those building MCP integrations, skills add another powerful layer helping turn raw tool access into reliable, optimized workflows.

### What You’ll Learn

- Technical requirements and best practices for skill structure
- Patterns for standalone skills and MCP-enhanced workflows
- Patterns we’ve seen work well across different use cases
- How to test, iterate, and distribute your skills

### Who This Is For

- Developers who want agents to follow specific workflows consistently
- Power users who want agents to follow specific workflows
- Teams looking to standardize how agents work across their organization

### Two Paths Through This Guide

- **Building standalone skills?** Focus on Fundamentals, Planning and Design, and categories 1–2.
- **Enhancing an MCP integration?** The “Skills + MCP” section and category 3 are for you.

Both paths share the same technical requirements, but you choose what’s relevant to your use case.

> **What you’ll get:** By the end, you’ll be able to build a functional skill in a single sitting. Expect about 15–30 minutes to build and test your first working skill using the skill-creator.

## Chapter 1 – Fundamentals

### What Is a Skill?

A skill is a folder containing:

|File/Folder|Required|Purpose|
|---|---|---|
|`SKILL.md`|✅ Required|Instructions in Markdown with YAML frontmatter|
|`scripts/`|Optional|Executable code (Python, Bash, etc.)|
|`references/`|Optional|Documentation loaded as needed|
|`assets/`|Optional|Templates, fonts, icons used in output|

### Core Design Principles

#### Progressive Disclosure

Skills use a three-level system:

1. **First level (YAML frontmatter):** Always loaded or indexed by the agent runtime. Provides just enough information for the agent to know when each skill should be used without loading all of it into context.
1. **Second level (SKILL.md body):** Loaded when the agent determines the skill is relevant to the current task. Contains the full instructions and guidance.
1. **Third level (Linked files):** Additional files bundled within the skill directory that the agent can choose to navigate and discover only as needed.

This progressive disclosure minimises token usage while maintaining specialised expertise.

#### Composability

Agents can load multiple skills simultaneously. Your skill should work well alongside others, not assume it’s the only capability available.

#### Portability

Skills are intended to be portable across compatible agent runtimes, IDE agents, chat surfaces, and APIs. Create a skill once and adapt only platform-specific packaging, installation, and dependency details.

### For MCP Builders: Skills + Connectors

> 💡 **Building standalone skills without MCP?** Skip to Planning and Design — you can always return here later.

If you already have a working MCP server, you’ve done the hard part. Skills are the knowledge layer on top — capturing the workflows and best practices you already know, so an agent can apply them consistently.

#### The Kitchen Analogy

- **MCP** provides the professional kitchen: access to tools, ingredients, and equipment.
- **Skills** provide the recipes: step-by-step instructions on how to create something valuable.

Together, they enable users to accomplish complex tasks without needing to figure out every step themselves.

#### How They Work Together

|MCP (Connectivity)|Skills (Knowledge)|
|---|---|
|Connects agents to your service (Notion, Asana, Linear, etc.)|Teaches agents how to use your service effectively|
|Provides real-time data access and tool invocation|Captures workflows and best practices|
|What the agent *can* do|How the agent *should* do it|

#### Why This Matters for Your MCP Users

**Without skills:**

- Users connect your MCP but don’t know what to do next
- Support tickets asking “how do I do X with your integration”
- Each conversation starts from scratch
- Inconsistent results because users prompt differently each time
- Users blame your connector when the real issue is workflow guidance

**With skills:**

- Pre-built workflows activate automatically when needed
- Consistent, reliable tool usage
- Best practices embedded in every interaction
- Lower learning curve for your integration

## Chapter 2 – Planning and Design

### Start with Use Cases

Before writing any code, identify 2–3 concrete use cases your skill should enable.

**Good use case definition:**

```
Use Case: Project Sprint Planning
Trigger: User says "help me plan this sprint" or "create sprint tasks"
Steps:
  1. Fetch current project status from Linear (via MCP)
  2. Analyze team velocity and capacity
  3. Suggest task prioritization
  4. Create tasks in Linear with proper labels and estimates
Result: Fully planned sprint with tasks created
```

**Ask yourself:**

- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP)?
- What domain knowledge or best practices should be embedded?

### Common Skill Use Case Categories

#### Category 1: Document & Asset Creation

**Used for:** Creating consistent, high-quality output including documents, presentations, apps, designs, code, etc.

**Real example:** `frontend-design` skill

> *“Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, artifacts, posters, or applications.”*

**Key techniques:**

- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalising
- No external tools required — uses the agent’s built-in capabilities

#### Category 2: Workflow Automation

**Used for:** Multi-step processes that benefit from consistent methodology, including coordination across multiple MCP servers.

**Real example:** `skill-creator` skill

> *“Interactive guide for creating new skills. Walks the user through use case definition, frontmatter generation, instruction writing, and validation.”*

**Key techniques:**

- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

#### Category 3: MCP Enhancement

**Used for:** Workflow guidance to enhance the tool access an MCP server provides.

**Real example:** `sentry-code-review` skill (from Sentry)

> *“Automatically analyzes and fixes detected bugs in GitHub Pull Requests using Sentry’s error monitoring data via their MCP server.”*

**Key techniques:**

- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

### Define Success Criteria

> These are aspirational targets — rough benchmarks rather than precise thresholds. Aim for rigor but accept that there will be an element of vibes-based assessment.

#### Quantitative Metrics

- **Skill triggers on 90% of relevant queries**
  - *Measure:* Run 10–20 test queries that should trigger your skill. Track how many times it loads automatically vs. requires explicit invocation.
- **Completes workflow in X tool calls**
  - *Measure:* Compare the same task with and without the skill enabled. Count tool calls and total tokens consumed.
- **0 failed API calls per workflow**
  - *Measure:* Monitor MCP server logs during test runs. Track retry rates and error codes.

#### Qualitative Metrics

- Users don’t need to prompt the agent about next steps
- Workflows complete without user correction
- Consistent results across sessions

### Technical Requirements

#### File Structure

```
your-skill-name/
├── SKILL.md              # Required - main skill file
├── scripts/              # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/           # Optional - documentation
│   ├── api-guide.md
│   └── examples/
└── assets/               # Optional - templates, etc.
    └── report-template.md
```

#### Critical Rules

**SKILL.md naming:**

- Must be exactly `SKILL.md` (case-sensitive)
- No variations accepted (`SKILL.MD`, `skill.md`, etc.)

**Skill folder naming:**

- ✅ Use kebab-case: `notion-project-setup`
- ❌ No spaces: `Notion Project Setup`
- ❌ No underscores: `notion_project_setup`
- ❌ No capitals: `NotionProjectSetup`

**No README.md inside the skill folder:**

- All documentation goes in `SKILL.md` or `references/`
- Note: when distributing via GitHub, you’ll still want a repo-level README for human users

### YAML Frontmatter: The Most Important Part

The YAML frontmatter is how an agent runtime decides whether to load your skill.

#### Minimal Required Format

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

#### Field Requirements

**`name` (required):**

- kebab-case only
- No spaces or capitals
- Should match folder name

**`description` (required):**

- MUST include BOTH: what the skill does AND when to use it (trigger conditions)
- Under 1024 characters
- No XML tags (`<` or `>`)
- Include specific tasks users might say
- Mention file types if relevant

**`license` (optional):**

- Use if making skill open source
- Common: `MIT`, `Apache-2.0`

**`compatibility` (optional):**

- 1–500 characters
- Indicates environment requirements

**`metadata` (optional):**

```yaml
metadata:
  author: ProjectHub
  version: 1.0.0
  mcp-server: projecthub
```

#### Security Restrictions

Forbidden in frontmatter:

- XML angle brackets (`< >`)
- Skills with platform-reserved names or prefixes

### Writing Effective Skills

#### The Description Field

Structure: `[What it does] + [When to use it] + [Key capabilities]`

**✅ Good descriptions:**

```yaml
# Specific and actionable
description: Analyzes Figma design files and generates developer handoff
  documentation. Use when user uploads .fig files, asks for "design specs",
  "component documentation", or "design-to-code handoff".

# Includes trigger phrases
description: Manages Linear project workflows including sprint planning, task
  creation, and status tracking. Use when user mentions "sprint", "Linear
  tasks", "project planning", or asks to "create tickets".
```

**❌ Bad descriptions:**

```yaml
# Too vague
description: Helps with projects.

# Missing triggers
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

#### Writing the Main Instructions

**Recommended structure:**

```markdown
---
name: your-skill
description: [...]
---

# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.

```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

Expected output: [describe what success looks like]

## Examples

### Example 1: [common scenario]

User says: “Set up a new marketing campaign”
Actions:

1. Fetch existing campaigns via MCP
1. Create new campaign with provided parameters
   Result: Campaign created with confirmation link

## Troubleshooting

### Error: [Common error message]

Cause: [Why it happens]
Solution: [How to fix]

```
#### Best Practices for Instructions

**Be specific and actionable:**

```markdown
✅ Good:
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)

❌ Bad:
Validate the data before proceeding.
```

**Include error handling:**

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

**Use progressive disclosure:** Keep `SKILL.md` focused on core instructions. Move detailed documentation to `references/` and link to it.

## Chapter 3 – Testing and Iteration

Skills can be tested at varying levels of rigor:

- **Manual testing in a chat or IDE agent** — Run queries directly and observe behavior. Fast iteration, no setup required.
- **Scripted testing in an agent runtime or API** — Automate test cases for repeatable validation across changes.
- **Programmatic testing via skills API** — Build evaluation suites that run systematically against defined test sets.

> 💡 **Pro Tip:** Iterate on a single task before expanding. The most effective skill creators iterate on a single challenging task until the agent succeeds, then extract the winning approach into a skill.

### Recommended Testing Approach

#### 1. Triggering Tests

**Goal:** Ensure your skill loads at the right times.

```
Should trigger:
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
- "Initialize a ProjectHub project for Q4 planning"

Should NOT trigger:
- "What's the weather in San Francisco?"
- "Help me write Python code"
- "Create a spreadsheet" (unless ProjectHub skill handles sheets)
```

#### 2. Functional Tests

**Goal:** Verify the skill produces correct outputs.

```
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When: Skill executes workflow
Then:
  - Project created in ProjectHub
  - 5 tasks created with correct properties
  - All tasks linked to project
  - No API errors
```

#### 3. Performance Comparison

**Goal:** Prove the skill improves results vs. baseline.

|Metric|Without Skill|With Skill|
|---|---|---|
|User instructions|Provided each time|Automatic|
|Back-and-forth messages|15|2|
|Failed API calls|3|0|
|Tokens consumed|12,000|6,000|

### Using the skill-creator Skill

The `skill-creator` skill can help you build and iterate on skills:

- **Creating skills:** Generate skills from natural language descriptions, produce properly formatted `SKILL.md` with frontmatter, suggest trigger phrases and structure
- **Reviewing skills:** Flag common issues, identify over/under-triggering risks, suggest test cases
- **Iterative improvement:** Bring edge cases and failures back to skill-creator for refinement

```
"Use the skill-creator skill to help me build a skill for [your use case]"
```

> **Note:** skill-creator helps you design and refine skills but does not execute automated test suites or produce quantitative evaluation results.

### Iteration Based on Feedback

|Signal|Symptom|Solution|
|---|---|---|
|**Undertriggering**|Skill doesn’t load when it should|Add more detail and keywords to description|
|**Overtriggering**|Skill loads for irrelevant queries|Add negative triggers, be more specific|
|**Execution issues**|Inconsistent results, API failures|Improve instructions, add error handling|

## Chapter 4 – Distribution and Sharing

### Current Distribution Model (January 2026)

**How individual users get skills:**

1. Download the skill folder
1. Package it in the format your target runtime expects (for example, a folder or `.zip`)
1. Install it through the runtime’s skills, capabilities, or extensions UI
1. Or place it in the runtime’s configured skills directory

**Organisation-level skills:**

- Admins may deploy skills workspace-wide when the target platform supports it
- Automatic updates
- Centralised management

### An Open Standard

Agent Skills are designed as a portable pattern across tools and platforms. Like MCP, the goal is to separate reusable workflow knowledge from a specific model or interface. Authors can note platform-specific requirements in the skill’s `compatibility` field.

### Using Skills via API

|Use Case|Best Surface|
|---|---|
|End users interacting with skills directly|Chat app or IDE agent|
|Manual testing and iteration during development|Chat app, IDE agent, or local runtime|
|Individual, ad-hoc workflows|Chat app or IDE agent|
|Applications using skills programmatically|Runtime API|
|Production deployments at scale|Runtime API|
|Automated pipelines and agent systems|Runtime API|

> **Note:** API support and required tools vary by provider. Check your target runtime’s documentation before relying on code execution, file access, browsing, or MCP tools.

**Relevant docs:**

- Skills API Quickstart
- Create Custom Skills
- Skills in the Agent SDK

### Recommended Distribution Approach

#### 1. Host on GitHub

- Public repo for open-source skills
- Clear README with installation instructions
- Example usage and screenshots

#### 2. Document in Your MCP Repo

- Link to skills from MCP documentation
- Explain the value of using both together
- Provide quick-start guide

#### 3. Create an Installation Guide

```markdown
# Installing the [Your Service] Skill

1. Download the skill:
   - Clone repo: `git clone https://github.com/yourcompany/skills`
   - Or download ZIP from Releases

2. Install in your agent runtime:
   - Open the runtime’s skills, capabilities, or extensions settings
   - Click "Upload skill" or the equivalent action
   - Select the skill folder or packaged archive

3. Enable the skill:
   - Toggle on the [Your Service] skill
   - Ensure your MCP server is connected

4. Test:
   - Ask the agent: "Set up a new project in [Your Service]"
```

### Positioning Your Skill

**Focus on outcomes, not features:**

```
✅ Good:
"The ProjectHub skill enables teams to set up complete project workspaces
in seconds — including pages, databases, and templates — instead of
spending 30 minutes on manual setup."

❌ Bad:
"The ProjectHub skill is a folder containing YAML frontmatter and Markdown
instructions that calls our MCP server tools."
```

**Highlight the MCP + skills story:**

> “Our MCP server gives agents access to your Linear projects. Our skills teach agents your team’s sprint planning workflow. Together, they enable AI-powered project management.”

## Chapter 5 – Patterns and Troubleshooting

> These patterns emerged from skills created by early adopters and internal teams. They represent common approaches, not prescriptive templates.

### Choosing Your Approach: Problem-First vs. Tool-First

- **Problem-first:** “I need to set up a project workspace” → Your skill orchestrates the right MCP calls in the right sequence.
- **Tool-first:** “I have Notion MCP connected” → Your skill teaches the agent the optimal workflows and best practices.

### Pattern 1: Sequential Workflow Orchestration

**Use when:** Your users need multi-step processes in a specific order.

```markdown
# Workflow: Onboard New Customer

## Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

## Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

## Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)

## Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**Key techniques:** Explicit step ordering, dependencies between steps, validation at each stage, rollback instructions for failures.

### Pattern 2: Multi-MCP Coordination

**Use when:** Workflows span multiple services.

```markdown
# Phase 1: Design Export (Figma MCP)
1. Export design assets from Figma
2. Generate design specifications
3. Create asset manifest

# Phase 2: Asset Storage (Drive MCP)
1. Create project folder in Drive
2. Upload all assets
3. Generate shareable links

# Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links to tasks
3. Assign to engineering team

# Phase 4: Notification (Slack MCP)
1. Post handoff summary to #engineering
2. Include asset links and task references
```

**Key techniques:** Clear phase separation, data passing between MCPs, validation before moving to next phase, centralised error handling.

### Pattern 3: Iterative Refinement

**Use when:** Output quality improves with iteration.

```markdown
# Iterative Report Creation

## Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

## Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues: missing sections, inconsistent formatting, data errors

## Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met

## Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

### Pattern 4: Context-Aware Tool Selection

**Use when:** Same outcome, different tools depending on context.

```markdown
# Smart File Storage

## Decision Tree
1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage

## Execute Storage
Based on decision, call appropriate MCP tool, apply service-specific
metadata, and generate access link.

## Provide Context to User
Explain why that storage was chosen.
```

### Pattern 5: Domain-Specific Intelligence

**Use when:** Your skill adds specialised knowledge beyond tool access.

```markdown
# Payment Processing with Compliance

## Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision

## Processing
IF compliance passed:
  - Call payment processing MCP tool
  - Apply appropriate fraud checks
  - Process transaction
ELSE:
  - Flag for review
  - Create compliance case

## Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

### Troubleshooting

#### Skill Won’t Upload

##### Error: “Could not find SKILL.md in uploaded folder”

- Rename to `SKILL.md` (case-sensitive)
- Verify with: `ls -la` — should show `SKILL.md`

##### Error: “Invalid frontmatter”

```yaml
# Wrong - missing delimiters
name: my-skill
description: Does things

# Wrong - unclosed quotes
name: my-skill
description: "Does things

# Correct
---
name: my-skill
description: Does things
---
```

##### Error: “Invalid skill name”

```yaml
# Wrong
name: My Cool Skill

# Correct
name: my-cool-skill
```

#### Skill Doesn’t Trigger

**Quick checklist:**

- Is the description too generic? (“Helps with projects” won’t work)
- Does it include trigger phrases users would actually say?
- Does it mention relevant file types if applicable?

**Debugging:** Ask the agent: *“When would you use the [skill name] skill?”* — the agent should reflect the description back. Adjust based on what’s missing.

#### Skill Triggers Too Often

**Solutions:**

```yaml
# 1. Add negative triggers
description: Advanced data analysis for CSV files. Use for statistical
  modeling, regression, clustering. Do NOT use for simple data exploration
  (use data-viz skill instead).

# 2. Be more specific
# Too broad:
description: Processes documents
# More specific:
description: Processes PDF legal documents for contract review

# 3. Clarify scope
description: PayFlow payment processing for e-commerce. Use specifically
  for online payment workflows, not for general financial queries.
```

#### MCP Connection Issues

**Checklist:**

1. Verify MCP server is connected (Settings > Extensions > should show “Connected”)
1. Check authentication (API keys valid, proper permissions, OAuth tokens refreshed)
1. Test MCP independently: *“Use [Service] MCP to fetch my projects”*
1. Verify tool names are correct and case-sensitive

#### Instructions Not Followed

**Common causes:**

1. **Instructions too verbose** — Keep concise, use bullet points, move detail to `references/`
1. **Instructions buried** — Put critical instructions at the top, use `## Important` or `## Critical` headers

```markdown
❌ Bad:
Make sure to validate things properly.

✅ Good:
CRITICAL: Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past
```

1. **Model “laziness”** — Add explicit encouragement (more effective in user prompts than in `SKILL.md`):

```markdown
## Performance Notes
- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps
```

> 💡 **Advanced technique:** For critical validations, bundle a script that performs checks programmatically. Code is deterministic; language interpretation isn’t.

#### Large Context Issues

**Solutions:**

1. Move detailed docs to `references/` and link to them
1. Keep `SKILL.md` under 5,000 words
1. Reduce the number of simultaneously enabled skills (evaluate if you have more than 20–50)
1. Consider skill “packs” for related capabilities

## Chapter 6 – Resources and References

### Official Documentation

**Anthropic Resources:**

- Best Practices Guide
- Skills Documentation
- API Reference
- MCP Documentation

**Blog Posts:**

- Introducing Agent Skills
- Engineering Blog: Equipping Agents for the Real World
- Skills Explained
- How to Create Skills for Claude
- Building Skills for Claude Code
- Improving Frontend Design through Skills

### Example Skills

- **GitHub:** `anthropics/skills` — Contains Anthropic-created skills you can customise

### Tools and Utilities

**skill-creator skill:**

- Built into Claude.ai and available for Claude Code
- Use: *“Help me build a skill using skill-creator”*
- Ask: *“Review this skill and suggest improvements”*

### Getting Support

- **General questions:** Community forums at the Claude Developers Discord
- **Bug reports:** GitHub Issues at `anthropics/skills/issues` — Include skill name, error message, steps to reproduce

## Reference A – Quick Checklist

### Before You Start

- [ ] Identified 2–3 concrete use cases
- [ ] Tools identified (built-in or MCP)
- [ ] Reviewed this guide and example skills
- [ ] Planned folder structure

### During Development

- [ ] Folder named in kebab-case
- [ ] `SKILL.md` file exists (exact spelling)
- [ ] YAML frontmatter has `---` delimiters
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] `description` includes WHAT and WHEN
- [ ] No XML tags (`< >`) anywhere
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] Examples provided
- [ ] References clearly linked

### Before Upload

- [ ] Tested triggering on obvious tasks
- [ ] Tested triggering on paraphrased requests
- [ ] Verified doesn’t trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Tool integration works (if applicable)
- [ ] Compressed as `.zip` file

### After Upload

- [ ] Test in real conversations
- [ ] Monitor for under/over-triggering
- [ ] Collect user feedback
- [ ] Iterate on description and instructions
- [ ] Update version in metadata

## Reference B – YAML Frontmatter

### Required Fields

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

### All Optional Fields

```yaml
name: skill-name
description: [required description]
license: MIT
allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"
metadata:
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
```

### Security Notes

**Allowed:**

- Any standard YAML types (strings, numbers, booleans, lists, objects)
- Custom metadata fields
- Long descriptions (up to 1024 characters)

**Forbidden:**

- XML angle brackets (`< >`)
- Code execution in YAML
- Skills named with platform-reserved prefixes

## Reference C – Complete Skill Examples

For full, production-ready skills demonstrating the patterns in this guide:

- **Document Skills** — PDF, DOCX, PPTX, XLSX creation
- **Example Skills** — Various workflow patterns
- **Partner Skills Directory** — Skills from Asana, Atlassian, Canva, Figma, Sentry, Zapier, and more

> These repositories stay up-to-date and include additional examples beyond what’s covered here. Clone them, modify them for your use case, and use them as templates.
