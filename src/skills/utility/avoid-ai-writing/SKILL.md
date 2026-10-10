---
name: avoid-ai-writing
description: Audits and rewrites text to remove AI writing patterns. Use when asked to "remove AI-isms", "clean up AI writing", or "make this sound less like AI".
license: MIT
metadata:
  author: Conor Bronsdon
  version: 3.11.0
  source: github.com/conorbronsdon/avoid-ai-writing
  catalog: utility
  category: editing
  tags: [writing, editing, quality]
  openclaw:
    emoji: "\u270D\uFE0F"
---

# Avoid AI Writing — Audit & Rewrite

You are editing content to remove AI writing patterns ("AI-isms") that make text sound machine-generated.

## What this skill is and isn't

This is a **writing-quality tool**, not a verdict. The patterns flagged here are statistically more common in LLM output, but humans on autopilot — especially writing under deadline pressure, in unfamiliar genres, or in a second language — produce the same shapes. Independent audits of commercial AI detectors have found false-positive rates above 60% on non-native English writers (Liang et al., Stanford, _Patterns_ 2023) and overall misclassification rates above 70% on open-source detectors (Jabarian & Imas, BFI Working Paper 2025-116, 2025). Adversarial paraphrase reduces detection accuracy by ~88% across every method tested (arXiv:2506.07001, 2025).

The patterns are useful as a signal — both for cleaning up your own writing and for assessing whether a piece reads as AI-generated. Just don't make them the sole basis for a consequential decision (academic integrity, hiring, publication, attribution). Several rules here also fire on second-language writing, deadline-pressed humans, and technical genres that compress vocabulary by design. Pair the signal with context: who wrote it, what genre, what the writer's normal voice looks like, what other evidence you have.

In short: signals, not proof. Worth acting on; not worth ruining someone's day over.

## Modes

This skill operates in one of three modes:

**`rewrite`** (default) — Flag AI-isms and rewrite the text to fix them.

**`detect`** — Flag AI-isms only. No rewriting. Use this mode when:

- The writer wants to see what's flagged and decide what to fix themselves
- The flagged patterns might be intentional (AI patterns aren't always bad — they can be effective in small doses)
- You're auditing text you don't want altered (published content, someone else's writing, reference material)
- You want a quick scan without waiting for a full rewrite

**`edit`** — Edit a file in place rather than returning rewritten text. Use this when the writer points you at a file ("clean up `draft.md`", "fix the AI-isms in this file directly") and wants the file changed, not a copy to paste back. Make **minimal, targeted edits** with the Edit tool — change the flagged spans, not the whole document. **Preserve passages that are already human**: if a paragraph has no tells, leave it untouched. **Don't edit quoted material, code blocks, or text attributed to someone else** — flag those instead of rewriting them. For a large file, confirm which section to clean before changing anything. After editing, re-read the file and confirm the flagged patterns are resolved.

Trigger detect mode when the user says "detect," "flag only," "audit only," "just flag," "scan," "what AI patterns are in this," or similar. Trigger edit mode when the user names a file and asks you to fix or clean it in place. Default to rewrite mode if not specified.

**Invocation.** Natural language is enough ("rewrite this in a blunt voice for LinkedIn," "edit `post.md` in place," "scan this, don't rewrite"). Power users can also pass explicit options, which map to the sections below: `[--mode rewrite|detect|edit]`, `[--voice casual|professional|technical|warm|blunt]`, `[--context linkedin|blog|technical-blog|investor-email|docs|casual]`, `[--file PATH]`, `[--iterate N]` (max 2).

**Iterate to convergence (optional).** Rewrite mode already runs one corrective second pass (see Output format) — that built-in pass _is_ pass 2, so `--iterate` does not stack on top of it. When the writer asks to "iterate," "keep going until it's clean," or passes `--iterate N`, repeat the audit→rewrite cycle until no patterns remain or **N passes** are reached. Cap **N at 2**: a rewrite plus one corrective pass clears the flagged patterns, and a third pass costs a full regeneration while rarely finding more. Report how many passes it took ("converged in 2 passes").

---

In **rewrite** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Rewrite it**: return a clean version with all AI-isms removed
3. **Show a diff summary**: briefly list what you changed and why

In **detect** mode, your job is to:

1. **Audit it**: identify every AI-ism present, citing the specific text
2. **Assess it**: note which flags are clear problems vs. patterns that may be intentional or effective in context

In **edit** mode, your job is to:

1. **Read** the file the writer named
2. **Edit in place**: apply minimal, targeted fixes to the flagged spans with the Edit tool, leaving already-human passages untouched
3. **Verify**: re-read the file and confirm the flagged patterns are resolved; report what you changed

---

## What to remove or fix

Read [references/patterns.md](references/patterns.md) before auditing. It catalogs every pattern to flag: formatting, sentence structure, word tiers, structural tells, and when to rewrite from scratch.

---

## Severity tiers

Not all AI-isms are equal. When doing a quick pass or triaging a large document, prioritize by tier:

### P0 — Credibility killers (fix immediately)

- Cutoff disclaimers ("As of my last update")
- Chatbot artifacts ("I hope this helps!", "Great question!")
- Vague attributions without sources ("Experts believe")
- Significance inflation on routine events
- Hashtag stuffing on `linkedin` and `investor-email` posts (severity varies by profile — same rule, lower priority on `blog`/`technical-blog` where a launch post may legitimately stack tags; see the context-profile table below)

### P1 — Obvious AI smell (fix before publishing)

- Word-list violations (delve, leverage, harness, robust, etc.)
- Template phrases and slot-fill constructions
- "Let's" transition openers
- Synonym cycling within a paragraph
- Formulaic openings ("In the rapidly evolving world of...")
- Bold overuse
- Em dash frequency (above 1 per 1,000 words)
- Generic future-narrative closers ("may become one of the most important narratives…")
- Social endorsement closers ("This one is worth your time:", "thank me later")
- Hedge-stacked predictions ("could potentially," "may eventually")
- Real/actual adjective inflation ("real on-chain tokenomics")
- Bullet lists of bare noun phrases (5+ short adj+noun items, no verbs)
- Tier 3 phrase clustering (≥3 distinct boilerplate phrases in one piece)

### P2 — Stylistic polish (fix when time allows)

- Generic conclusions ("The future looks bright")
- Compulsive rule of three
- Uniform paragraph length
- Copula avoidance (serves as, features, boasts)
- Transition phrases (Moreover, Furthermore, Additionally)
- Hashtag stuffing (`blog`/`technical-blog` profiles)
- Tier 3 phrase repetition (single phrase ≥2× — fine in isolation, suspect in stacks)

Use P0+P1 for quick passes. Full audit covers all three tiers.

---

## Self-reference escape hatch

When writing _about_ AI writing patterns (blog posts, tutorials, skill documentation like this file), quoted examples are exempt from flagging. Text inside quotation marks, code blocks, or explicitly marked as illustrative ("for example, AI might write...") should not be rewritten. Only flag patterns that appear in the author's own prose, not in cited examples of bad writing.

---

## Context profiles

Pass an optional context hint to adjust rule strictness. If no context is specified, auto-detect from content cues (short + hashtags = social, code blocks = technical, salutation = email, default = blog).

### Profile definitions

**`linkedin`** — Short-form social. Punchy fragments, visual formatting matter.
**`blog`** — Default. Standard long-form prose. All rules apply at full strength.
**`technical-blog`** — Long-form with code, architecture, APIs. Technical terms get a pass.
**`investor-email`** — High-trust audience. Tighten everything; promotional language is the biggest risk.
**`docs`** — Documentation, READMEs, guides. Clarity over voice.
**`casual`** — Slack messages, internal notes, quick replies. Only catch the worst offenders.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

|Rule|linkedin|blog|technical-blog|investor-email|docs|casual|
|---|---|---|---|---|---|---|
|Em dashes|relaxed (2/post OK)|strict|strict|strict|relaxed|skip|
|Bold overuse|relaxed (bold hooks OK)|strict|strict|strict|relaxed|skip|
|Emoji in headers|relaxed (1-2 end-of-line OK)|strict|strict|strict|skip|skip|
|Excessive bullets|skip (lists work on LinkedIn)|strict|relaxed (technical lists OK)|strict|skip (lists are docs)|skip|
|Hedging|strict|strict|relaxed ("may" is accurate in technical)|strict|relaxed|skip|
|Word table (full list)|strict|strict|**partial** (see below)|strict|relaxed|P0 only|
|Promotional language|relaxed (some sell is expected)|strict|strict|**extra strict**|strict|skip|
|Significance inflation|strict|strict|strict|**extra strict**|relaxed|skip|
|Copula avoidance|skip|strict|relaxed|strict|skip|skip|
|Uniform paragraph length|skip (short-form)|strict|strict|strict|relaxed|skip|
|Numbered list inflation|relaxed|strict|relaxed|strict|skip|skip|
|Rhetorical questions|relaxed (1 as hook OK)|strict|strict|strict|strict|skip|
|Transition phrases|skip (short-form)|strict|strict|strict|relaxed|skip|
|Generic conclusions|skip|strict|strict|**extra strict**|skip|skip|
|Hashtag stuffing|strict|strict|strict|**extra strict**|skip (no hashtags in docs)|skip|
|Bullet-NP lists|strict|strict|relaxed (technical option lists OK)|strict|relaxed (parameter lists OK)|skip|
|Tier 3 phrase clustering|strict|strict|strict|**extra strict**|relaxed|skip|
|Future-narrative closers|strict|strict|strict|**extra strict**|skip|skip|
|Social endorsement closers|strict (the LinkedIn share-post tell)|strict|strict|strict|skip|relaxed (1 OK in a DM)|
|Hedge-stacked predictions|strict|strict|relaxed ("could" is hedged accuracy)|**extra strict**|relaxed|skip|
|Real/actual inflation|strict|strict|strict|**extra strict**|relaxed|skip|

**Technical-blog word table exceptions:** These terms have legitimate technical meaning and should not be flagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual platform leverage/APIs), `facilitate`, `underpin`, `streamline`. Still flag: `delve`, `tapestry`, `beacon`, `embark`, `testament to`, `game-changer`, `harness`.

**"Extra strict"** means: flag even borderline instances. In investor emails, a single "thriving ecosystem" can undermine the whole message.

**"Skip"** means: don't audit this category for this profile. The rule doesn't apply or isn't worth the edit.

### Auto-detection cues

When no context is specified, infer from these signals:

|Signal|Inferred context|
|---|---|
|Under 300 words + hashtags or mentions|`linkedin`|
|Code blocks, API references, or technical architecture|`technical-blog`|
|Salutation ("Hi [name]", "Dear") + investor/fundraising language|`investor-email`|
|Step-by-step instructions, parameter docs, README structure|`docs`|
|No strong signals|`blog` (safest default — all rules apply)|

If auto-detection feels wrong, say which profile you're using and why. The user can override.

---

## Voice profiles

Context profiles (above) set _how strict_ to be for an audience. Voice profiles set _how the prose should sound_ — the persona. They're independent axes: you can write blunt for a blog or warm for docs. Voice is **optional** — if the writer doesn't name one, infer it from the input's existing register and don't impose a persona on text that already has one.

Each profile is a set of concrete targets, not a vibe:

**`casual`** — Contractions throughout; their absence reads stiff. Short sentences (aim for ≤14 words on average); fragments allowed. At least one first-person or concrete-anecdote touch. Near-zero jargon. Keep warm hedges ("honestly," "I think") but cut corporate ones ("it's worth noting"). _Blog posts, social, community._

**`professional`** — Active voice for most sentences. Vary sentence length; avoid three in a row within a few words of each other. One concrete claim per paragraph (a number, a name, a date), never "experts say." Make the ask explicit. Low tolerance for hedging. _LinkedIn, investor email, sponsor pitches._

**`technical`** — Prefer plain copulatives ("X is Y") over inflated substitutes ("serves as," "stands as a testament to"). One idea per sentence; imperative mood for instructions. Jargon is fine, but define it on first use. Tables and lists only where the content is genuinely list-shaped, not for decoration. _Docs, technical blog._

**`warm`** — Address the reader directly ("you") and acknowledge them at least once. Cut intensifiers ("very," "truly," "incredibly") in favor of stronger verbs. No performative-empathy openers ("I completely understand how you feel"). Medium sentences (15–20 words) for an unhurried cadence. _Mentorship, onboarding, thank-yous._

**`blunt`** — Lead with the claim; cut "It's important to note that" windups. Em-dashes are rare here; use periods for emphasis. No padding to hit a rule of three. Near-zero hedging; flag "may / could / potentially" stacks. Short declaratives, with the occasional long sentence for contrast. _Decision memos, thought leadership, hard feedback._

**Calibrate to a sample (optional).** If the writer gives you a sample of their own writing ("match my voice — here's a post"), analyze its sentence-length pattern, contraction rate, paragraph openings, and recurring word choices, then match those instead of a named profile. Don't "upgrade" their vocabulary: if they write "stuff" and "things," keep that register.

**How voice composes with context.** Voice sets the target; context sets how hard to enforce it. A voice _target_ always applies, even where a context profile would skip that category — `technical` voice still prefers plain copulatives in a `casual` context that otherwise ignores copula avoidance. Where both axes govern the same rule and agree, they reinforce: `blunt` voice wants near-zero em-dashes and a `blog` context is already strict on them, so it stays a hard edit. Where they disagree, resolve toward the **stricter** of the two — a `warm` voice on `docs` still doesn't get decorative tables. Sensible default pairings: casual↔casual, professional↔linkedin/investor-email, technical↔docs/technical-blog.

---

## Output format

### Rewrite mode (default)

Return your response in four sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted.

**2. Rewritten version**
The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

**3. What changed**
A brief summary of the major edits made. Not every word, just the meaningful changes.

**4. Second-pass audit**
Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, or anything else from [references/patterns.md](references/patterns.md). Fix them, return the corrected text inline, and note what changed in this pass. If the rewrite is clean, say so.

### Detect mode

Return your response in two sections:

**1. Issues found**
A bulleted list of every AI-ism identified, with the offending text quoted. Group by severity (P0, P1, P2).

**2. Assessment**
For each flag, note whether it's a clear problem or a judgment call. Some AI-associated patterns are effective writing techniques — uniform paragraph length is a problem, but a well-placed "however" isn't. Call out which flags the writer should definitely fix vs. which ones are worth a second look but might be fine in context. If the text is clean, say so.

### Edit mode

After editing the file in place, return a short report — not the full file:

**1. Edits made**
A bulleted list of the changes, each with the file location and the before → after. Only the spans you touched.

**2. Verification**
Confirm you re-read the file and the flagged patterns are resolved. Note anything you deliberately left alone because it was already human or intentional.

---

## Tone calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

Five principles for human-sounding rewrites:

1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece is supposed to take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it.

The replacement table provides defaults, not mandates. If a flagged word is clearly the right choice in context, preserve it.
