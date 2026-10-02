---
name: tighten
description: 'Compress text to the shortest form that keeps every fact and meaning intact. Apply this proactively, before finalizing, to anything you (Claude) write — code comments, commit messages, PR/issue descriptions, docs, README updates, and chat replies — not only when the user explicitly asks to shorten something. Also use on demand when the user pastes text or points at a file and asks to "tighten," "shorten," "make concise," "cut the fluff," or "trim this down." Supports a --level light|moderate|aggressive flag (default: moderate).'
---

# Tighten

Cut every word that isn't carrying weight. Keep every fact, number, instruction, and caveat that is.

## Levels

Pick one; default to `moderate`. These percentages are **targets to hit, not flavor text to describe** — see Verify below. Measured in real words (count them; don't estimate), on the prose you touched, not the whole file if most of it is code.

- **light** — 5-15% shorter. Cut throat-clearing, filler, and dead words only. Keep sentence count and structure. Use for anything a reader will scrutinize closely (specs, legal-adjacent text, anything with nuance that could break if compressed).
- **moderate** — **20-30% shorter.** Light, plus: merge sentences making the same point, drop hedging, replace wordy phrases with the plain word, cut redundant clauses. Default for comments, commit messages, PR descriptions, chat replies.
- **aggressive** — **40-60% shorter.** Moderate, plus: fragments are fine, drop connective tissue between points, keep only what's needed to reconstruct the fact. Use for terse contexts (log messages, short Slack-style updates, one-line summaries) or when explicitly asked to cut hard.

**Dense or reasoning-heavy prose is not an exemption from the target — it's a constraint on *how* you hit it.** Some docs and comments use long causal sentences on purpose — cause → effect → why-it-matters is the point, not padding (a project changelog explaining *why* a change was made is a common case). Don't respond to that density by quietly downgrading to `light` and calling it `moderate` — that's the single most common way this skill under-delivers. Instead, keep the reasoning chain's *steps* intact while cutting the *wording* around each step (redundant phrasing, throat-clearing, hedges, "which is what," "the reason for this is that"). That alone gets most dense prose into the 20-30% range without flattening the argument. Reach for `aggressive`'s fragments only when asked for that level or the context calls for it (logs, terse summaries) — fragmenting a reasoning chain is what turns lossless compression into lossy flattening.

## Method

1. **Find the load-bearing content.** For each sentence, ask: what fact, instruction, or decision does this carry? That's what must survive.
2. **Cut what isn't load-bearing:** filler ("it's worth noting that," "in order to"), hedging ("might potentially," "it seems"), throat-clearing (restating the question before answering it), and repeated information.
3. **Merge**, don't just delete — two sentences making the same point become one.
4. **Prefer the concrete word.** "utilize" → "use," "in the event that" → "if." Say the number instead of describing it.
5. **Never cut for length at the cost of correctness.** A caveat, edge case, or number that changes what the reader should do stays, even if it costs words.
6. **Re-read as the reader**, not the writer. If a stranger would lose something they needed, restore it.
7. **Verify, don't estimate.** Count words before and after the pass (a real count — `wc -w`, or count them — never a guess or a round-number impression). If you're short of the level's target range, that's not acceptable as "close enough": go back over the sentences you left alone and ask, concretely, what's cuttable in each one — a first pass reliably leaves fat behind because it's easy to declare a sentence "already tight" without testing that claim. Do a second pass targeting the shortfall specifically. Stop when you're in range, or when you've genuinely tried to cut a specific sentence further and it would cost a fact — not when it merely "feels" tight.

## Applying to your own writing

Before you finalize a comment, commit message, PR/issue body, doc, or reply, run this pass silently — don't narrate that you're doing it. Default to `moderate`. Match the level to the medium: a one-line commit subject or a log line should already be near `aggressive`; a doc section or PR description explaining *why* usually wants `moderate` so the reasoning survives.

Don't over-apply: a short factual answer that's already tight doesn't need a pass, and code itself (identifiers, logic) is out of scope — this is about prose.

## Applying to user-supplied text

Return the tightened text. If asked, add a brief list of what was cut and why — otherwise just return the result without meta-commentary about the process.

## Example (moderate)

Before: "It's worth noting that in order to fix this bug, we will need to potentially update the configuration file, which could possibly involve changing several of the settings that are currently being used by the application."

After: "Fixing this bug requires updating the configuration file, possibly several settings."
