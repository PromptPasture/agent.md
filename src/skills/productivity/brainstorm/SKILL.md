---
name: brainstorm
description: Explores user intent, requirements, and design before implementation. Use when the user asks "what should we do about X?", "ideas for…", "how should we approach…", or any open-ended design question before the team picks a direction.
license: Apache-2.0
metadata:
  author: github.com/obra/superpowers
  version: "3.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: research
  tags: [reason, framing, thinking]
---

# Brainstorming Ideas

Help explore ideas, compare alternatives, and capture conclusions through natural collaborative dialogue.

## Anti-Pattern: "This Is Too Simple To Brainstorm"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The conclusions can be short (a few sentences for truly simple projects), but you MUST present them and get approval.

## Workflow

### Goal

Brainstorm conclusions the user has approved, captured in `docs/YYYY-MM-DD-[topic]/BRAINSTORM.md` and ready to hand off to an implementation plan.

### Setup

1. Explore the current project context: files, docs, recent commits.
2. Assess scope. If the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), decompose it before refining details — see Decomposing Large Projects below.
3. If upcoming questions will involve visual content (mockups, layouts, diagrams), offer the Visual Companion in its own message before asking anything else — see Visual Companion below.

### Loop

1. Ask clarifying questions one at a time about purpose, constraints, and success criteria. Prefer multiple choice; open-ended is fine too.
2. Propose 2-3 approaches with trade-offs, leading with the recommended option and reasoning — apply Design for Isolation and Clarity and Working in Existing Codebases (below). Keep every approach lean: strip features not justified by a current stated requirement.
3. Present conclusions: summarize the goal, ideas considered, trade-offs, and emerging decisions. Scale the summary to the topic — a few sentences if straightforward, up to 200-300 words if nuanced. Keep technical design details out unless needed to explain a decision.
4. Ask whether the conclusions look right. If not, go back and clarify — repeat until approved.

### Exit

When the user approves the conclusions.

### Report

1. Write the brainstorm doc to `docs/YYYY-MM-DD-[topic]/BRAINSTORM.md` — see Output below for structure. (User preferences for document location override this default.)
2. Self-review the written notes and fix issues inline — see Verification below. No need to re-review after fixing; just fix and move on.
3. Ask the user to review the written file: "Brainstorm notes written to `[path]`. Please review them and let me know if you want to make any changes before we start writing the implementation plan." Wait for their response.
4. If they request changes, make them and repeat the self-review. Once approved, create a detailed implementation plan from the conclusions. Do not start implementation directly from brainstorming.

## Decomposing Large Projects

If the project is too large for one focused brainstorm, help the user decompose it into sub-projects: what are the independent pieces, how do they relate, and what order should they be explored? Then brainstorm the first sub-project through the normal flow. Each sub-project gets its own brainstorm → plan → implementation cycle.

## Design for Isolation and Clarity

Aim for **loose coupling, high cohesion**: each unit has one clear purpose, a well-defined interface, and can be understood, tested, and changed without touching its neighbors.

- For each unit, you should be able to answer: what does it do, how do you use it, and what does it depend on?
- Can someone understand what a unit does without reading its internals? Can you change the internals without breaking consumers? If not, the boundaries need work.
- A file or module growing large is often a sign it has taken on more than one responsibility.

## Working in Existing Codebases

- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work (e.g., a file that's grown too large, unclear boundaries, tangled responsibilities), include targeted improvements as part of the design — the way a good developer improves code they're working in.
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.

## Output

Write conclusions to `docs/YYYY-MM-DD-[topic]/BRAINSTORM.md`, adapting headings to the topic while preserving the frontmatter fields:

```markdown
---
topic: [Topic]
method: [Method]
date: "YYYY-MM-DD"
related:
  - [Optional path, issue, or URL]
---

# Brainstorm - [Topic]

## Goal

## Context

## Agenda

1. ...

## Ideas Considered

### [Idea]

- **Description:** ...
- **Benefits:** ...
- **Trade-offs:** ...

## Outcomes

### Summary

### Decisions

### Open Questions

## Next Steps
```

Omit `related` when there are no useful references. Use a concise method name that describes how ideas were explored, such as `comparative analysis`, `creative matrix`, `round robin`, or `idea prioritization`. Record substantive discussion in the body; frontmatter is only for document metadata. Capture general discovery and decisions, not a technical design or implementation specification.

## Error Paths

- If conclusions don't hold together, go back and clarify rather than pressing forward.
- If the user requests changes to the written notes, apply them and re-run the self-review before asking for approval again.

## Verification

Before asking the user to review the written notes, verify that:

- No placeholders remain ("TBD", "TODO", incomplete sections, or vague requirements).
- Sections are internally consistent — decisions follow from the ideas and trade-offs presented.
- The scope is focused enough for a single implementation plan, or decomposition has been flagged.
- No requirement is open to two different readings — pick one and make it explicit.

## Visual Companion

A browser-based companion for showing mockups, diagrams, and visual options during brainstorming. Available as a tool — not a mode. Accepting the companion means it's available for questions that benefit from visual treatment; it does NOT mean every question goes through the browser.

**Offering the companion:** When you anticipate that upcoming questions will involve visual content (mockups, layouts, diagrams), offer it once for consent:
> "Some of what we're working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? (Requires opening a local URL)"

**This offer MUST be its own message.** Do not combine it with clarifying questions, context summaries, or any other content. The message should contain ONLY the offer above and nothing else. Wait for the user's response before continuing. If they decline, proceed with text-only brainstorming.

**Per-question decision:** Even after the user accepts, decide FOR EACH QUESTION whether to use the browser or the terminal. The test: **would the user understand this better by seeing it than reading it?**

- **Use the browser** for content that IS visual — mockups, wireframes, layout comparisons, architecture diagrams, side-by-side visual designs
- **Use the terminal** for content that is text — requirements questions, conceptual choices, tradeoff lists, A/B/C/D text options, scope decisions

A question about a UI topic is not automatically a visual question. "What does personality mean in this context?" is a conceptual question — use the terminal. "Which wizard layout works better?" is a visual question — use the browser.
