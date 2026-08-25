---
name: teach
description: Teaches a topic across multiple sessions from a persistent learning workspace, producing short markdown lessons grounded in a stated mission. Use when the user asks to be taught or coached on something over time.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
license: MIT
metadata:
  author: github.com/mattpocock/skills
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: learning
  tags: [learning, teaching, retention]
---

# Teach a Topic

Teaching is stateful. The user intends to learn this topic over many sessions, so each session reads the workspace, produces one short lesson, and records only what the session earned.

Any topic qualifies — a language, a framework, thermodynamics, yoga, sourdough.

## Workflow

### Goal

One lesson written to `lessons/NNNN-<slug>.md`, tied to the mission and sitting inside the user's zone of proximal development, plus the state updates that lesson earned.

### Setup

1. Locate the workspace: an existing `MISSION.md` in the current directory, `./learning/*/`, or `docs/learning/*/`. If none exists, ask the user where it should live (default `./learning/<topic>/`) and create that directory. Never scatter workspace files into the root of an unrelated project.
2. Read `MISSION.md`, `NOTES.md`, `GLOSSARY.md`, `RESOURCES.md`, and `learning-records/`. List `lessons/` and `reference/` to see what has already been taught.
3. If `MISSION.md` is missing or vague, interview the user on why they want this before teaching anything, then write it and confirm. A bad mission is worse than no mission.
4. Choose the lesson target: what the user explicitly asked for, otherwise derive it from the records and the mission — see Zone of Proximal Development.

### Loop

1. Ground the knowledge — see Grounding below. Add any new source to `RESOURCES.md` with its annotation.
2. Draft one lesson — see Lesson Design and the template in [references/formats.md](references/formats.md). Number it above the highest existing lesson.
3. Write the lesson file, then offer to open it (`open`, `code`, or the user's stated preference).
4. Promote durable knowledge out of the lesson: a `reference/` sheet when the material will be consulted again, a `GLOSSARY.md` term once the user can use it correctly.
5. Write a learning record when, and only when, the session produced one — see Learning Records.

### Exit

The lesson file is written, the user knows where it is, and earned state updates are recorded.

### Report

State the lesson path, what it teaches, how it serves the mission, its primary source, which state files changed, and what the next lesson is likely to cover.

## Workspace Files

Create each lazily, on first need.

|Path|Holds|
|---|---|
|`MISSION.md`|Why the user is learning this. Grounds every teaching decision.|
|`RESOURCES.md`|Curated high-trust sources and communities, each annotated. Gaps listed explicitly.|
|`GLOSSARY.md`|Canonical terms the user already understands. Once a term is here, use it everywhere.|
|`learning-records/NNNN-*.md`|Evidence-grade insights that set what to teach next. The ADRs of learning.|
|`lessons/NNNN-*.md`|The lessons themselves, one tight win each.|
|`reference/*.md`|Compressed cheat sheets: syntax, algorithms, sequences, poses, routines.|
|`assets/*`|Reusable artifacts lessons link to — diagrams, drill banks, printable cards.|
|`NOTES.md`|User preferences and working notes.|

Reuse is the default. Before authoring, read `reference/` and `assets/` and build on what is there rather than restating it inline.

## Philosophy

Deep learning needs three things:

- **Knowledge**, taken from high-trust sources.
- **Skills**, acquired through practice the user actually performs.
- **Wisdom**, which only comes from the real world — see Wisdom.

Some topics lean knowledge-heavy (theoretical physics), others skill-heavy (yoga). Calibrate.

Separate **fluency strength** (in-the-moment retrieval) from **storage strength** (long-term retention). Fluency feels like mastery and isn't. Build storage strength through desirable difficulty: retrieval practice, spacing across sessions, and interleaving related skills in practice sets.

For acquiring knowledge, difficulty is the enemy — it eats the working memory needed to understand. For practicing skills, difficulty is the tool.

## Lesson Design

- **Short.** Completable in one sitting. Working memory is small; one tangible win per lesson.
- **Tied to the mission**, and pitched inside the zone of proximal development.
- **Only the knowledge the skill needs.** Teach that, then have the user practice it.
- **Self-contained feedback.** Lessons are markdown, so practice carries its own answer key: recall prompts with collapsed `<details>` answers, and a checklist of real-world reps the user performs away from the screen. Close every lesson by inviting the user to bring answers or sticking points back to the session for grading.
- **Answer-key discipline.** Keep answers collapsed. In multiple-choice items, hold every option to the same word count, and character count where possible — formatting must not leak the answer.
- **Spacing and interleaving.** Open with two or three recall items drawn from earlier lessons, and mix related skills into practice sets rather than drilling one in isolation.
- **Linked.** Link to the `reference/` sheets, glossary terms, and prior lessons a reader would want next.
- **One primary source.** Name the single best source found on the topic for the user to read or watch.
- **Beautiful and readable.** These get revisited: clean headings, short paragraphs, no walls of text.

## Grounding

Read `RESOURCES.md` before reaching for parametric knowledge. When a claim is factual, version-sensitive, or contested and lookup is available, verify it and cite it inline; add the source to `RESOURCES.md` with a one-line annotation.

When lookup is unavailable or the material is stable and uncontested, teach from model knowledge — but never dress an uncited claim as sourced, and record what is missing under `## Gaps` in `RESOURCES.md` so a later session can close it.

Prune sources that turn out to be shallow, wrong, or off-mission.

## Zone of Proximal Development

Every lesson should feel challenging just enough. When the user hasn't named a target, derive it: read the learning records for the current floor, read the mission for direction, and teach the most relevant thing that fits the gap between them.

## Learning Records

Write one when the session produced any of:

- Evidence the user can use a non-trivial concept correctly, not merely that it was covered.
- Prior knowledge the user disclosed, including the depth claimed, so it isn't re-taught.
- A corrected misconception — these predict future stumbling blocks.
- A shift in the mission driven by what the user learned.

Coverage is not learning. Do not log session activity, and do not restate a definition that already lives in `GLOSSARY.md`. When a later record overturns an earlier one, mark the old one `Status: superseded by LR-NNNN` rather than deleting it.

## Wisdom

When a question needs judgment rather than facts, answer it as well as you can — then point the user at a community where they can test the answer against practitioners: a well-moderated forum, a local group, a class. Find high-reputation options rather than naming the obvious one.

If the user says they don't want a community, respect it and record that in `RESOURCES.md` so later sessions stop proposing them.

## Error Paths

- Mission missing or vague → interview the user first; do not teach against a guess.
- Workspace location unclear → ask before creating anything.
- The user wants a second, unrelated topic → that is a second workspace, not a second mission.
- The mission appears to have changed → confirm with the user, then update `MISSION.md` and write a learning record.
- Lookup unavailable for a factual claim → teach it uncited, mark the gap, move on.

## Verification

Before presenting the lesson, confirm:

- It traces to the mission, and to the current floor set by the learning records.
- Every answer key is correct, collapsed, and free of formatting tells; multiple-choice options are the same length.
- Terminology matches `GLOSSARY.md`.
- No placeholders remain, and every link resolves — `reference/` sheets, prior lessons, sources.
- Anything reusable lives in `reference/` or `assets/` and is linked, not duplicated inline.
- The lesson is one win, not three. If it teaches several things, split it.

## Formats

Templates and rules for `MISSION.md`, `RESOURCES.md`, `GLOSSARY.md`, learning records, and lessons: [references/formats.md](references/formats.md).
