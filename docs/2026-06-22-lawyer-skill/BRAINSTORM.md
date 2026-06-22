---
topic: Lawyer Skill
method: comparative analysis
date: "2026-06-22"
related:
  - src/skills/in-progress/lawyer/
---

# Brainstorm - Lawyer Skill

## Goal

Create a conversational `lawyer` skill that acts as a knowledgeable friend with legal expertise — plain language, no jargon — for regular people without legal education.

## Context

The agent.md skill system uses YAML frontmatter + a markdown workflow document. Skills are triggered by user invocation and follow a defined workflow. Existing skills (e.g. `brainstorm`, `review-code`) follow a conversational, question-by-question pattern. The `lawyer` skill should mirror that UX pattern.

## Agenda

1. Define primary use cases
2. Define target audience
3. Define interaction style
4. Decide on document output behavior
5. Decide on skill structure (unified vs. split)
6. Define jurisdiction, language, tone, and disclaimer handling

## Ideas Considered

### Split skills (one per legal mode)

- **Description:** Separate skills — `lawyer-contracts`, `lawyer-draft`, `lawyer-research`, `lawyer-compliance`
- **Benefits:** Each skill is focused and tight
- **Trade-offs:** User must know which to invoke; mid-conversation mode switches require changing skills

### Single unified skill (chosen)

- **Description:** One skill handles all four modes, routes by asking what help is needed at the start
- **Benefits:** Simple trigger, consistent UX, easy to extend
- **Trade-offs:** Skill file grows longer; one extra opening question before substantive work begins

### Unified skill with internal phase documents

- **Description:** One invocation point, but each mode's guidance lives in a separate file (like `brainstorm` + supporting refs)
- **Benefits:** Modular guidance per mode
- **Trade-offs:** More files to maintain; overkill for a first version

## Outcomes

### Summary

A single `lawyer` skill that covers contract review, legal document drafting, legal research/Q&A, and compliance review. It operates as a conversational advisor for laypeople — asking one question at a time, responding in the user's language, and always framing output in plain terms. It opens with a disclaimer, asks for jurisdiction early, and optionally produces a written legal memo at the end of a session.

### Decisions

- **Scope:** Contract review, drafting, legal research/Q&A, compliance review — all in one skill
- **Audience:** Regular people without legal education
- **Interaction style:** Conversational, one question at a time (mirrors `brainstorm` flow)
- **Language:** Responds in the user's language; asks if ambiguous
- **Jurisdiction:** Asks country/region early in every session; flags that laws vary by location
- **Risk tiers:** Two levels — "worth knowing" and "serious red flag — consult a lawyer"
- **Disclaimer:** Shown at the start of every session and as the final section of any written memo: "This is not legal advice. I am an AI assistant, not a licensed attorney. For any significant legal matter, consult a qualified lawyer in your jurisdiction."
- **Document output:** Conversation-first; user can request a written legal memo at any point
- **Multi-document sessions:** Supported — the skill can review, compare, or cross-reference multiple documents within a single session if the user requests it
- **Memo format:** Sections: Summary, Jurisdiction, Key Findings (tiered), Recommendations, Open Questions, Disclaimer
- **Memo location:** User-specified path if provided; otherwise `docs/YYYY-MM-DD-[topic]/LEGAL-MEMO.md`
- **Structure:** Single `skill.md` saved to `src/skills/in-progress/lawyer/`

### Open Questions

None.

## Next Steps

- Write `src/skills/in-progress/lawyer/skill.md` following the decided workflow
- Define the opening disclaimer text and two-tier risk flag wording
- Define the memo template inline in the skill
