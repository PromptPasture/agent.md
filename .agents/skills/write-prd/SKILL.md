---
name: write-prd
description: Use whenever the user asks to write or revise a PRD, product requirements, product brief, feature requirements, product scope, launch requirements.
license: MIT
tags:
  - writer
  - product
  - requirements
metadata:
  author: Oleg Shulyakov
  version: "1.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-team-roles
  category: project-management
---

# write-prd

Produce a complete, structured **Product Requirements Document (PRD)** for the described product, feature, or initiative.

## What makes a great PRD

**A PRD creates shared product understanding without becoming a frozen spec.**

A PRD bridges business intent and engineering execution. It must be specific enough to guide decisions, but light enough to evolve as the team learns. The goal is to answer: _Why are we building this? For whom? What does success look like? What is and isn't in scope?_

Treat the PRD as the shared source of truth for product purpose, user needs, features, behavior, and success criteria. It should create shared customer understanding across product, design, engineering, and stakeholders instead of specifying every implementation detail upfront.

Keep the document concise, collaborative, and easy to update. Treat it as a landing page for the initiative with links to research, designs, demos, Jira issues, technical docs, and related discussions when those details would bloat the PRD.

## Information gathering

**Extract known context first and ask only when a missing answer changes the document.**

Before writing, extract from the user's prompt, attached artifacts, or repo context. Ask once only if a missing answer changes the document materially:

- **What** is being built (feature, product, initiative)?
- **Why** — the customer problem, business opportunity, and cost of inaction
- **Who** — the target users, personas, and stakeholders
- **Success** — how will we know it worked? (goals, metrics, KPIs, OKRs)
- **Scope** — in-scope capabilities, non-goals, and future considerations
- **Execution context** — target date, status, team members, milestones, links, dependencies, and constraints

If the user provides a rough description, work with what's there. Make educated inferences and mark them clearly with `[assumed]` so the user can verify.

## Output format

**Load the detailed Markdown structure only when writing the PRD.**

Always produce a Markdown PRD, usually named `PRD.md` when writing to disk. Before drafting, read `references/output-format.md` for the required structure. Convert Confluence or DOC/DOCX templates into clean Markdown with YAML frontmatter for document metadata, then headings and tables for the document body; do not preserve export artifacts, emojis, styling, or application-specific markup.

## Writing guidance

**Keep requirements outcome-focused, testable, and scoped.**

- **Goals first, solutions second.** Resist the urge to specify UI or technical implementation in the requirements.
- **Keep the PRD alive and concise.** Prefer one source of truth with links to deeper research, designs, demos, Jira issues, or technical docs instead of copying every detail into the PRD.
- **Collaborate by design.** Name stakeholders and open questions so product, design, engineering, marketing, sales, support, and leadership can react to the same artifact.
- **Keep scope simple.** Prefer the smallest coherent product slice that can prove the goal before expanding into adjacent workflows.
- **Use STAR for evidence and examples.** Frame user problems with situation, task, action, and result when describing journeys, research notes, or success examples.
- **Make requirements testable.** "The page loads in under 2 seconds" is better than "the page should be fast."
- **Write user stories when behavior is user-facing.** Include "As a..., I want..., so that..." stories where they clarify user value, and connect each story to requirements or acceptance criteria.
- **Scope the out-of-scope.** Explicitly naming non-goals is as valuable as naming goals because it prevents future debate.
- **Mark inferences.** If you infer a persona, metric, or assumption, add `[assumed]` inline so the user can verify.
- **Track uncertainty.** Use assumptions for beliefs to validate and open questions for decisions or research still needed.
- **Keep it scannable.** Use YAML frontmatter for document metadata. Use tables for success metrics, requirements, assumptions, milestones, and open questions. Avoid walls of prose.

## Recommended content

**Include just enough context to explain requirements and user impact.**

- **Document metadata:** status, document type, phase, dates, author/owner, stakeholders, tags, and related docs in YAML frontmatter. Add optional fields such as `targetDate`, `tracker`, or `demoLink` only when they have real value.
- **Objective:** product goal, customer problem, business reason, and timing.
- **Success metrics:** goals paired with measurable indicators.
- **Assumptions:** beliefs about technology, business needs, user behavior, or constraints that should be validated.
- **User stories:** stories or links to stories, backed by customer interviews, screenshots, evidence, and success metrics when available.
- **User interaction and design:** links to design explorations, wireframes, prototypes, and relevant demos.
- **Open questions:** a table of items the team needs to decide or research.
- **Out of scope:** explicit non-goals and possible later work.

## Multi-section depth calibration

**Scale the document to the amount of source context.**

Scale depth to what the user provides:

- **Terse prompt** (one sentence): Write a lean PRD with 2–3 goals, 1–2 personas, and 5–10 requirements. Mark most things `[assumed]`.
- **Detailed prompt**: Fill out all sections thoroughly, infer less.
- **Existing draft**: Improve, restructure, and fill gaps rather than rewriting from scratch.

When examples would help calibrate tone, specificity, or section depth, read `references/examples.md`.
