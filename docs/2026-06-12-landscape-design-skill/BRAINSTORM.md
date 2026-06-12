---
topic: Landscape Design Skill
method: adaptive questioning
date: "2026-06-12"
---

# Brainstorm - Landscape Design Skill

## Goal

Build a standalone skill that guides homeowners through an adaptive conversation about their outdoor space, then compiles the gathered information into a structured landscape design plan document.

## Context

No existing landscape skill in the project. Skill lives under `src/skills/landscape-design/`. No MCP integration needed — purely model-driven, no hardcoded styles, plant lists, or regional presets. Optimized for homeowners; professionals can use it but it is not the primary target.

## Agenda

1. Define primary audience and scope
2. Choose conversation structure (linear vs. adaptive vs. user-led)
3. Define information gathering fields
4. Decide role of visual input (photos, cadastral plans)
5. Define output format and document structure

## Ideas Considered

### Option A — Linear intake funnel

- **Description:** Fixed question order: region → size → use → budget → style → maintenance → output.
- **Benefits:** Predictable, easy to implement clearly.
- **Trade-offs:** Feels like filling in a form; wastes questions on irrelevant branches.

### Option B — Adaptive conversation *(chosen)*

- **Description:** Starts with core questions (region, yard size, intended use), branches based on answers. Prompts for visuals at contextually appropriate moments. Ends with a structured plan document.
- **Benefits:** Feels like talking to a designer; reliably gathers what's needed without being mechanical; easily extensible.
- **Trade-offs:** Slightly more complex to write, but keeps skill general and non-prescriptive.

### Option C — User-led with gap-filling

- **Description:** Opens with "tell me about your space", user dumps info freely, skill asks targeted follow-ups.
- **Benefits:** Most natural entry point.
- **Trade-offs:** Risks missing key inputs; less consistent output quality.

## Outcomes

### Summary

The skill runs an adaptive intake conversation, branching intelligently based on each answer. At the right moments it prompts the user to share photos of the current yard or a cadastral/site plan — not upfront, but contextually (e.g. after yard size is established, ask for a photo; after boundaries are mentioned, suggest the cadastral plan). Once enough information is gathered, it compiles a structured design plan document within the conversation, following the same pattern as the brainstorm skill.

### Decisions

- **Audience:** Homeowners primary; professionals welcome but not optimized for.
- **Conversation style:** Adaptive (Option B). One question at a time.
- **Visual prompts:** Woven into the conversation at natural moments, not listed upfront.
- **No hardcoded content:** No preset styles, plant lists, or regional databases — model reasons from context.
- **Output:** Structured design plan document (zones, priorities, considerations, phasing, open questions).
- **Scope:** Standalone skill, no MCP, no cross-session persistence.
- **Start small:** Not all fields are mandatory; skill produces the best plan it can from what's been shared.

### Information Fields (gathered adaptively)

Core (always asked):

- Climate / region / hardiness zone
- Yard size and rough dimensions
- Primary intended use (entertaining, play, food garden, privacy, etc.)

Contextual (asked when relevant):

- Sun exposure per zone
- Existing features to keep or remove
- Budget and phasing preference (all-at-once vs. multi-season)
- Maintenance commitment (hours per week/month)
- Soil type and drainage
- Water access and irrigation
- Privacy needs
- Pets or children (affects plant safety and lawn durability)
- HOA or local restrictions
- Photos of current yard (prompted after size/use established)
- Cadastral or site plan (prompted when boundaries or dimensions are discussed)

### Resolved Questions

- **Output document structure:** Flexible — model structures the plan based on what was actually gathered. No fixed template imposed.
- **Session model:** The skill suggests a follow-up conversation for refinement at the end of each session, encouraging the user to return with the saved plan.
- **Output workspace:** On first run the skill creates a project folder (e.g. `my-garden/`) the user can point back to in future sessions.

### Output Workspace Structure

Inspired by mattpocock/skills `teach` skill pattern — a stateful folder the user owns and re-shares across sessions.

```
my-garden/
├── PLAN.md              # master design plan, updated each session
├── NOTES.md             # user preferences and gathered facts scratchpad
├── RESOURCES.md         # useful links, inspiration, references
├── zones/
│   ├── backyard.html    # spatial design, plants, intent per zone
│   ├── front-yard.html
│   └── patio.html
└── phases/
    ├── phase-1-prep.html
    ├── phase-2-structure.html
    └── phase-3-finishing.html
```

Zones and phases serve distinct purposes:

- **zones/** — *what* each area looks like (spatial, plant-focused, design intent)
- **phases/** — *when* things happen (timeline, sequencing, budget chunks)

### Skill Reference Files

Internal format guides bundled in `references/` — loaded by the skill as needed:

```
src/skills/landscape-design/
├── SKILL.md
└── references/
    ├── PLAN-FORMAT.md
    ├── NOTES-FORMAT.md
    ├── ZONE-FORMAT.md
    └── PHASE-FORMAT.md
```

## Next Steps

1. ~~Write frontmatter for `src/skills/landscape-design/SKILL.md`~~ ✅
2. Write reference format files (`PLAN-FORMAT.md`, `NOTES-FORMAT.md`, `ZONE-FORMAT.md`, `PHASE-FORMAT.md`)
3. Write instructions body in `SKILL.md` (adaptive conversation flow, visual prompts, output compilation)
4. Test triggering on all six target phrases
5. Test adaptive branching with a few homeowner scenarios
