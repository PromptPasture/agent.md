# Workspace File Formats

Templates and rules for every file the `teach` skill maintains. Create each file lazily, on first need.

## MISSION.md

Lives at the workspace root. Captures why the user is learning this. Every teaching decision traces back to it.

```md
# Mission: {Topic}

## Why

{1-3 sentences. The concrete real-world goal. What changes in the user's life or work when they have this skill? Avoid "to understand X" — push for the outcome underneath.}

## Success looks like

- {A specific, observable thing the user will be able to do}
- {Another}

## Constraints

- {Time, budget, prior commitments, learning preferences — anything that bounds the approach}

## Out of scope

- {Adjacent topics the user does not want to chase now}
```

Rules:

- One mission per workspace. Two unrelated topics are two workspaces.
- Concrete beats abstract: "Run a half marathon by October" over "get fitter"; "Ship a Rust CLI to my team" over "learn Rust".
- If the user can't say why, interview before writing.
- Revise when the goal moves. A stale mission steers every future session wrong.
- Keep it under a screen. Past that it has stopped being a compass.

## RESOURCES.md

The curated set of trusted sources. Knowledge comes from here; wisdom comes from the communities listed here.

```md
# {Topic} Resources

## Knowledge

- [Book: _The Science and Practice of Strength Training_ by Zatsiorsky & Kraemer](https://example.com)
  Foundational text on programming and adaptation. Use for: periodisation, recovery, intensity zones.
- [Article: "How Much Should I Train?" — Greg Nuckols, Stronger By Science](https://example.com)
  Evidence-based review of volume landmarks. Use for: weekly set targets per muscle group.

## Wisdom (Communities)

- [r/weightroom](https://reddit.com/r/weightroom)
  High-signal, moderated against bro-science. Use for: programme critique, plateau troubleshooting.
- Local: Tuesday strength class at {gym}
  Use for: real-time coaching feedback on lifts.

## Gaps

- {An area the mission needs and no good source covers yet}
```

Rules:

- High-trust only. Primary sources, recognised experts, peer-reviewed work, well-moderated communities. Marketing dressed as education stays out.
- Annotate every entry with one line: what it covers, when to reach for it. A bare link is useless in three months.
- Keep `## Gaps` honest — it drives the next search, and it records claims currently taught uncited.
- Prune rather than bury. Five sharp sources beat thirty mediocre ones.
- Record a community opt-out here so later sessions stop proposing them.

## GLOSSARY.md

The canonical language of the workspace. Lessons, reference sheets, and records all adhere to it.

```md
# {Topic} Glossary

{One or two sentences on what this glossary covers.}

## Terms

**Hypertrophy**:
Muscle growth driven by mechanical tension and metabolic stress over repeated training sessions.
_Avoid_: bulking, getting big

**Progressive overload**:
Systematically increasing the demand on a muscle over time, via load, volume, or intensity.
_Avoid_: pushing harder, levelling up
```

Rules:

- Add a term only once the user can use it correctly. This is a record of compressed understanding, not a dictionary to read.
- Be opinionated. Pick the best word for a concept and list the rest as aliases to avoid.
- Definitions are one or two sentences and say what the term **is**, not how to do it.
- Use glossary terms inside glossary definitions.
- Group under subheadings when clusters emerge; a flat list is fine when terms cohere.
- Resolve loose field usage explicitly: "In this workspace, 'set' always means a working set."
- Revise in place as understanding deepens.

## Learning Records

`learning-records/NNNN-<slug>.md`, numbered one above the highest existing file.

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned, or what prior knowledge was established, and why it changes what to teach next.}
```

That is the whole format. A single paragraph is a complete record — the value is capturing that this is now known and why it matters.

Add these only when they genuinely help:

- `Status:` frontmatter (`active` | `superseded by LR-NNNN`) when a later record overturns this one.
- **Evidence**: how the user demonstrated the understanding.
- **Implications**: what this unlocks or rules out, when non-obvious.

## Lessons

`lessons/NNNN-<slug>.md`, numbered one above the highest existing lesson.

```md
# Lesson {N} — {Title}

**Mission link:** {the one line connecting this to MISSION.md}
**Primary source:** [{title}]({url})
**Prerequisites:** [Lesson {N-1}](NNNN-slug.md), [{term}](../GLOSSARY.md)

## Warm-up

{Two or three recall prompts from earlier lessons, answers collapsed. Skip in lesson 0001.}

1. ▢ {Prompt}

<details markdown="1"><summary>Check</summary>

{Answer.}

</details>

## Know this

{The minimum knowledge the skill needs. Short paragraphs. Cite claims inline where a source exists.}

## Practice

{Retrieval prompts, ordered easy to hard, with collapsed answers. Interleave a related skill where it fits.}

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

Rules:

- One win per lesson. If it teaches three things, it is three lessons.
- Answers stay collapsed. Multiple-choice options hold to the same word count, and character count where possible — no formatting tells.
- Keep `markdown="1"` on every `<details>`. Without it, kramdown — the default renderer for GitHub Pages — emits the markdown inside as literal text. GitHub's own renderer ignores the attribute, so lessons stay correct in both.
- Every factual claim is cited when a source exists; uncited claims are not presented as sourced.
- Link out to `reference/`, `assets/`, glossary terms, and prior lessons instead of restating them.

## Reference Sheets

`reference/<slug>.md`. The compressed essence of what lessons taught, in a form built for quick lookup: syntax tables, algorithms, flowcharts, pose sequences, routines, checklists.

Lessons are rarely revisited; these are. Optimise for scanning — tables and short lists over prose — and keep them printable.
