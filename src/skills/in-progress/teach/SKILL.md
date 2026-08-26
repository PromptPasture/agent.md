---
name: teach
description: Teaches a topic across multiple sessions from a persistent learning workspace, producing short markdown lessons grounded in a stated mission. Use when the user asks to be taught or coached on something over time.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
license: MIT
metadata:
  author: github.com/mattpocock/skills
  version: "1.1.0"
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

One lesson written to `lessons/NNNN-<slug>.md`, tied to the mission and inside the user's zone of proximal development, plus the state updates that lesson earned.

### Setup

1. Locate the workspace: a `README.md` sitting beside a `lessons/` directory, in the current directory, `./learning/*/`, or `docs/learning/*/`. A `README.md` alone is not a workspace — every repository has one. If none exists, ask where it should live (default `./learning/<topic>/`) and create it. Never scatter workspace files into an unrelated project's root.
2. Read `README.md`, `NOTES.md`, `GLOSSARY.md`, `RESOURCES.md`, and `learning-records/`. List `lessons/` and `reference/` to see what has been taught, and to catch a drifted lesson table.
3. If `README.md` is missing or its mission is vague, interview the user on why they want this before teaching anything, then write the README and confirm. A bad mission is worse than no mission.
4. Choose the lesson target: what the user asked for, otherwise derive it — see Zone of Proximal Development.

### Loop

1. Ground the knowledge — see Grounding. Add any new source to `RESOURCES.md` with its annotation.
2. Draft one lesson — see Lesson Design and the `lessons/` template. Number it above the highest existing lesson.
3. Write the lesson file, add its row to the `README.md` lesson table, move the **Latest lesson** pointer, then offer to open it.
4. Promote durable knowledge out of the lesson: a `reference/` sheet when the material will be consulted again, a `GLOSSARY.md` term once the user can use it correctly.
5. Write a learning record only if the session earned one — see Learning Records.

### Exit

The lesson file is written, the user knows where it is, and earned state updates are recorded.

### Report

The lesson path, what it teaches, how it serves the mission, its primary source, which state files changed, and the likely next lesson.

## Workspace Files

Create each lazily, on first need. Reuse is the default: read `reference/` and `assets/` before authoring, and build on what is there.

|Path|Holds|
|---|---|
|`README.md`|Landing page: the mission, the lesson index, where a visitor starts.|
|`RESOURCES.md`|Annotated high-trust sources and communities. Gaps listed explicitly.|
|`GLOSSARY.md`|Canonical terms the user already understands. Once here, use them everywhere.|
|`lessons/NNNN-*.md`|The lessons. One tight win each.|
|`reference/*.md`|Cheat sheets: syntax, algorithms, sequences, poses, routines.|
|`learning-records/NNNN-*.md`|Evidence-grade insights that set what to teach next. The ADRs of learning.|
|`assets/*`|Reusable artifacts lessons link to — diagrams, drill banks, printable cards.|
|`NOTES.md`|User preferences and working notes.|

## Philosophy

Deep learning needs **knowledge** from high-trust sources, **skills** from practice the user actually performs, and **wisdom** from the real world. Some topics lean knowledge-heavy (theoretical physics), others skill-heavy (yoga) — calibrate.

Separate **fluency strength** (in-the-moment retrieval) from **storage strength** (long-term retention). Fluency feels like mastery and isn't. Build storage strength through desirable difficulty: retrieval practice, spacing across sessions, interleaving related skills. For acquiring knowledge, difficulty is the enemy — it eats the working memory needed to understand. For practicing skills, difficulty is the tool.

## Lesson Design

- **Short.** Completable in one sitting. Working memory is small; one tangible win per lesson.
- **Only the knowledge the skill needs.** Teach that, then have the user practice it.
- **Self-contained feedback.** Practice carries its own answer key: recall prompts with collapsed answers, and real-world reps the user performs away from the screen. Close by inviting the user to bring answers or sticking points back to the session.
- **Answer-key discipline.** Keep answers collapsed. Hold every multiple-choice option to the same word count, and character count where possible — formatting must not leak the answer.
- **Spacing and interleaving.** Open with two or three recall items from earlier lessons, and mix related skills into practice sets rather than drilling one in isolation.
- **Linked.** Link the `reference/` sheets, glossary terms, and prior lessons a reader would want next.
- **One primary source.** Name the single best source found for the user to read or watch.
- **Readable.** These get revisited: clean headings, short paragraphs, no walls of text.

## Grounding

Read `RESOURCES.md` before reaching for parametric knowledge. When a claim is factual, version-sensitive, or contested and lookup is available, verify it, cite it inline, and add the source to `RESOURCES.md` with a one-line annotation.

When lookup is unavailable or the material is stable and uncontested, teach from model knowledge — but never dress an uncited claim as sourced, and record what is missing under `## Gaps` so a later session can close it. Prune sources that turn out to be shallow, wrong, or off-mission.

## Zone of Proximal Development

Every lesson should feel challenging just enough. When the user hasn't named a target, derive it: the learning records give the current floor, the mission gives the direction, and the lesson goes in the gap between them.

## Learning Records

Write one when the session produced any of:

- Evidence the user can use a non-trivial concept correctly, not merely that it was covered.
- Prior knowledge the user disclosed, including the depth claimed, so it isn't re-taught.
- A corrected misconception — these predict future stumbling blocks.
- A shift in the mission driven by what the user learned.

Coverage is not learning. Do not log session activity, and do not restate a definition that already lives in `GLOSSARY.md`. When a later record overturns an earlier one, mark the old one `Status: superseded by LR-NNNN` rather than deleting it.

## Wisdom

When a question needs judgment rather than facts, answer it as well as you can — then point the user at a community where they can test the answer against practitioners: a well-moderated forum, a local group, a class. Find high-reputation options rather than naming the obvious one. If the user says they don't want a community, respect it and record that in `RESOURCES.md` so later sessions stop proposing them.

## Error Paths

- The user wants a second, unrelated topic → that is a second workspace, not a second mission.
- The mission appears to have changed → confirm with the user, then update the mission in `README.md` and write a learning record.

## Verification

Before presenting the lesson, confirm:

- Every answer key is correct and collapsed, with no formatting tells.
- Terminology matches `GLOSSARY.md`.
- No placeholders remain, and every link resolves.
- The `README.md` table has a row for the new lesson, and the **Latest lesson** pointer names it.

## Formats

### `README.md`

The landing page GitHub renders when someone opens the repository. Carries the mission that grounds every teaching decision, and the index of what has been taught.

```md
# Learning: {Topic}

{1-3 sentences. The concrete real-world goal. What changes in the user's life or work when they have this skill? Avoid "to understand X" — push for the outcome underneath.}

**Latest lesson:** [{NNNN} — {Title}](lessons/NNNN-slug.md)

## Success looks like

- {A specific, observable thing the user will be able to do}

## Constraints

- {Time, budget, prior commitments, learning preferences — anything that bounds the approach}

## Out of scope

- {Adjacent topics the user does not want to chase now}

## Lessons

Work through these in order.

|#|Lesson|Teaches|
|---|---|---|
|[0001](lessons/0001-slug.md)|{Title}|{The one win it delivers}|

## Reference

- [Glossary](GLOSSARY.md) — canonical terms for this topic
- [Resources](RESOURCES.md) — trusted sources and communities
- [{Cheat sheet}](reference/slug.md) — {when to reach for it}

## How this works

Each lesson is short and self-contained. Answer keys are collapsed — recall first, then open them. The real-world reps matter more than the reading, and spacing them out is the point. Bring anything unclear back to the teaching session.
```

Rules:

- Concrete beats abstract: "Run a half marathon by October" over "get fitter"; "Ship a Rust CLI to my team" over "learn Rust".
- Keep the mission above the lesson table under a screen. Past that it has stopped being a compass.
- Keep each table row to number, title, and one clause. This is an index, not a summary. A table that has drifted from `lessons/` is worse than no table.
- Do not link `NOTES.md` or `learning-records/` from here. Working notes and a record of the user's corrected misconceptions stay unadvertised, whether or not the repository is public.

### `RESOURCES.md`

The curated set of trusted sources. Knowledge comes from here; wisdom comes from the communities listed here.

```md
# {Topic} Resources

## Knowledge

- [Article: "How Much Should I Train?" — Greg Nuckols, Stronger By Science](https://example.com)
  Evidence-based review of volume landmarks. Use for: weekly set targets per muscle group.

## Wisdom (Communities)

- [r/weightroom](https://reddit.com/r/weightroom)
  High-signal, moderated against bro-science. Use for: programme critique, plateau troubleshooting.

## Gaps

- {An area the mission needs and no good source covers yet}
```

Rules:

- High-trust only. Primary sources, recognised experts, peer-reviewed work, well-moderated communities. Marketing dressed as education stays out.
- Annotate every entry with one line: what it covers, when to reach for it. A bare link is useless in three months.

### `GLOSSARY.md`

The canonical language of the workspace. Lessons, reference sheets, and records all adhere to it.

```md
# {Topic} Glossary

{One or two sentences on what this glossary covers.}

## Terms

**Progressive overload**:
Systematically increasing the demand on a muscle over time, via load, volume, or intensity.
_Avoid_: pushing harder, levelling up
```

Rules:

- This records compressed understanding; it is not a dictionary the user reads to learn.
- Be opinionated. Pick the best word for a concept and list the rest as aliases to avoid.
- Definitions are one or two sentences and say what the term **is**, not how to do it.
- Use glossary terms inside glossary definitions.
- Resolve loose field usage explicitly: "In this workspace, 'set' always means a working set."
- Revise in place as understanding deepens.

### `learning-records/`

`learning-records/NNNN-<slug>.md`, numbered one above the highest existing file.

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned, or what prior knowledge was established, and why it changes what to teach next.}
```

That is the whole format — a single paragraph is a complete record. Add **Evidence** (how the user demonstrated it) or **Implications** (what it unlocks or rules out) only when non-obvious.

### `lessons/`

`lessons/NNNN-<slug>.md`, numbered one above the highest existing lesson.

```md
# Lesson {N} — {Title}

**Mission link:** {the one line connecting this to the mission}
**Primary source:** [{title}]({url})
**Prerequisites:** [Lesson {N-1}](NNNN-slug.md), [{term}](../GLOSSARY.md)

## Warm-up

{Two or three recall prompts from earlier lessons, same collapsed shape as Practice. Skip in lesson 0001.}

## Know this

{The minimum knowledge the skill needs. Short paragraphs. Cite claims inline where a source exists.}

## Practice

{Retrieval prompts, ordered easy to hard. Interleave a related skill where it fits.}

1. ▢ {Prompt}

<details markdown="1"><summary>Check</summary>

{Answer, plus why the wrong instinct is wrong.}

</details>

## Real-world reps

- [ ] {Something to do today, away from the screen}
- [ ] {Something to do tomorrow — spacing is the point}

## Going further

- [{Reference sheet}](../reference/slug.md)
- [{Primary source}]({url})
- {Community, when the next step needs judgment rather than facts}

---

Stuck on any of this, or unsure whether an answer counts? Bring it back to the session — that's what your teacher is for.
```

Keep `markdown="1"` on every `<details>`. Without it, kramdown — the default renderer for GitHub Pages — emits the markdown inside as literal text. GitHub's own renderer ignores the attribute, so lessons stay correct in both.

### `reference/`

`reference/<slug>.md`. The compressed essence of what lessons taught, built for quick lookup: syntax tables, algorithms, flowcharts, pose sequences, routines, checklists.

Lessons are rarely revisited; these are. Optimise for scanning — tables and short lists over prose — and keep them printable.
