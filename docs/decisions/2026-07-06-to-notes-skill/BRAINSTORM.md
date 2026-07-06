---
topic: to-notes skill
method: comparative analysis
date: "2026-07-06"
related:
  - pages/HOWTO_Write_Great_Skills.md
  - src/skills/utility/write-skill/SKILL.md
  - src/skills/in-progress/markitdown/SKILL.md
---

# Brainstorm — to-notes skill

## Goal

Create a skill, `to-notes`, that converts a video URL, local video/audio file, or existing transcript/text into structured, concept-first lecture notes — the same output shape as `pages/HOWTO_Write_Great_Skills.md`.

## Context

- This session manually converted a YouTube `.vtt` transcript into `pages/HOWTO_Write_Great_Skills.md` by hand. `to-notes` formalizes that workflow as a reusable skill.
- No speech-to-text is in scope. The skill assumes a transcript already exists or can be fetched (e.g. YouTube captions via `yt-dlp`) — it never transcribes raw audio.
- Closest existing analog: `markitdown` (external format → ingest via a bundled script, Mode 1 / Mode 2 split).
- `src/skills/utility/write-skill/SKILL.md`'s Trigger / Structure / Steering / Pruning checklist was used to shape the frontmatter and file layout decisions below.
- Naming precedent: `to-prd` and `to-issues` already establish a `to-<noun>` naming pattern in this repo, alongside the verb-first list in `docs/skills/skill-system.md`.

## Agenda

1. Decide skill scope: personal skill vs. cataloged product skill
2. Decide transcription scope: assume transcript exists/fetchable vs. full speech-to-text
3. Choose the source-resolution architecture
4. Decide trigger (model- vs. user-invoked) and name

## Ideas Considered

### Approach A — Single skill, script resolves source, agent drafts notes *(chosen)*

- **Description:** One skill, one bundled script collapses all input shapes (video URL, local video/audio file, transcript/text) into plain transcript text. The agent then drafts concept-first notes from that text.
- **Benefits:** Mirrors the proven `markitdown` pattern (Mode 1 resolve, Mode 2 draft). Single file to maintain, one clear entry point.
- **Trade-offs:** The script must branch internally across four input shapes rather than isolating each in its own file.

### Approach B — Router skill with per-source reference docs

- **Description:** `to-notes` acts as a router (the pattern `docs/skills/skill-system.md` documents for "one trigger, multiple variants"), detecting URL vs. local file vs. raw text and loading `references/from-url.md`, `references/from-file.md`, or `references/from-text.md`, converging on a shared note-drafting reference.
- **Benefits:** Keeps `SKILL.md` minimal; matches an already-documented repo pattern.
- **Trade-offs:** More scaffolding than warranted — all four branches reduce to the same "get plain text" outcome, so splitting them into separate reference files is premature structure.

### Approach C — Two separate skills (resolver + notes drafter)

- **Description:** Decouple "resolve media source to text" into its own reusable skill/utility, independent from "text to lecture notes."
- **Benefits:** Best long-term reuse if a future skill needs the same source-resolution logic.
- **Trade-offs:** No other consumer exists yet — speculative, YAGNI risk for a first version.

## Outcomes

### Summary

`to-notes` is a user-invoked, cataloged product skill in the Productivity catalog. It resolves a video URL, local video/audio file, or existing transcript/text down to plain transcript text via a single bundled script — `yt-dlp` caption fetch for URLs, sibling-caption lookup for local video/audio files, direct read for transcript/text — then the agent drafts concept-first lecture notes (organized by idea, not transcript chronology) in the shape of `pages/HOWTO_Write_Great_Skills.md`.

### Decisions

- **Skill scope:** Cataloged product skill (not personal). Catalog: Productivity. Starts at `src/skills/in-progress/to-notes/`, promoted to `src/skills/productivity/to-notes/` once it clears release-readiness criteria.
- **Name:** `to-notes` — matches the existing `to-prd`/`to-issues` precedent.
- **Trigger:** User-invoked (`disable-model-invocation: true`). The description is a plain one-line human-facing summary, not a set of trigger phrases.
- **Transcription scope:** Assumes a transcript exists or is fetchable. No speech-to-text; no `ffmpeg`/Whisper dependency bundled.
- **Architecture:** Approach A. One bundled script (`scripts/resolve_source.py`) plus agent-drafted notes, in two steps: (1) resolve source → text, (2) draft notes.
- **File layout:** `SKILL.md` + `scripts/resolve_source.py` only. No `references/` — there is one real branch (drafting), and its guidance is needed on every run, so it stays inline in `SKILL.md`.
- **Leading word:** *concept-first* — notes are organized by idea/topic, not by transcript timestamp or chronology.
- **Completion criteria:**
  - Step 1 (resolve): done when the script prints resolved transcript text, or a specific, surfaced error if no transcript exists or can be fetched — no silent fallback into transcription.
  - Step 2 (draft): done when the notes file is written with frontmatter (`title`/`author`/`source`/`type`) and headers organized by the source's actual concepts.
- **Pruning:** No `ffmpeg`/Whisper bundled — avoids sprawl from an unused capability. `SKILL.md`'s body notes (for human readers, not as a runtime negative trigger) that `.pdf`/`.docx`/`.pptx`/`.xlsx`/`.msg`/`.epub` belong to `markitdown`, not this skill.
- **Input resolution mechanics:**
  - Video URL → `yt-dlp`, captions only, never downloads the video itself.
  - Local video/audio file → look for a sibling `.vtt`/`.srt`/`.txt` by filename.
  - Transcript/text file or pasted text → used directly, no resolution needed.
- **Caption selection policy:** Prefer manual (human-written) captions; fall back to auto-generated captions when no manual track exists — matches the `.vtt` processed in this session.
- **Caption language policy:** Try `en` first; if no English track exists, fetch whichever single language track is available and record that language in the notes' frontmatter. Never prompts the user to choose.
- **Notes schema:** Minimal required frontmatter fields — `title`, `author`, `source`, `type` — matching the convention already used across `pages/*.md`. Body structure and headers are left entirely to the agent's judgment, adapted per source. No fixed section template, no validator script.

### Open Questions

- None — resolved above.

## Next Steps

1. Write `src/skills/in-progress/to-notes/SKILL.md` with frontmatter (`disable-model-invocation: true`, `name`, `description`, `license`, `metadata`) and step-by-step instructions for both modes.
2. Write `src/skills/in-progress/to-notes/scripts/resolve_source.py` handling URL/file/text resolution and the `yt-dlp` caption fetch.
3. Verify: run it against the `.vtt` file processed in this session and confirm the output matches `pages/HOWTO_Write_Great_Skills.md` in shape and quality.
4. Once release-readiness criteria are met, promote to `src/skills/productivity/to-notes/` and add it to `docs/skills/skill-catalog.md`.
