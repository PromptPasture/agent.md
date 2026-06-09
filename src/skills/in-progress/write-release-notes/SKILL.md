---
name: write-release-notes
description: Write or revise user-facing release notes. Use for product updates, version announcements, what's-new summaries, app-store notes, improvements, fixes, known issues, upgrade guidance, and action-required notices.
license: Apache-2.0
tags:
  - writer
  - docs
  - release-notes
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
---

# write-release-notes

Translate shipped changes into clear user-facing value, impact, and required action.

## Workflow

1. Identify the product, release identifier and date, audience, channel, tone, and length constraints.
2. Inspect authoritative release evidence: changelog, pull requests, shipped behavior, issue resolutions, migration guidance, known issues, and approved product language.
3. Select only changes relevant to the target audience.
4. Rank changes by user impact and lead with the most important benefits.
5. Translate implementation details into observable outcomes without overstating them.
6. Include known issues, compatibility changes, upgrade steps, or required action when applicable.
7. Verify every claim against the shipped release.

## Content

Use only sections that serve the release:

- Release title, product, version, platform, and date
- A short release theme or summary
- Major new capabilities
- Improvements with concrete user benefit
- User-visible bug fixes
- Known issues and available workarounds
- Breaking changes or action required
- Upgrade or rollout guidance
- Relevant screenshots, demos, or documentation links
- Optional acknowledgement or brief preview when approved

For minor releases, improvements and fixes may be enough. For app-store notes, reduce the release to the most important two or three user-visible changes within channel limits.

## Transformation Rules

- Replace internal component names with the user workflow they affect.
- Explain what users can now do, what became easier, or what problem was fixed.
- Preserve meaningful measured improvements only when verified.
- Describe bug fixes by symptom, not internal exception or implementation.
- Omit commit hashes, pull-request numbers, internal tickets, refactors, and infrastructure details unless the audience needs them.
- Keep administrator or developer actions precise when an upgrade requires intervention.

## Writing Rules

- Match the established product voice and the expectations of the release channel.
- Lead with user benefit, not implementation.
- Use plain language without hiding important limitations or required action.
- Distinguish shipped functionality from previews or future plans.
- Do not include generic claims such as "better performance" without evidence.
- Do not describe a fix as universal if it affects only a specific platform, plan, region, or configuration.
- Mark unverified statements with `[assumed]` in drafts; remove them from published notes.

## Error Paths

- If no version or date is confirmed, use the release's approved naming convention rather than inventing metadata.
- If technical changes have no demonstrated user impact, omit them.
- If release evidence conflicts, stop the disputed claim and identify what must be confirmed.
- If a breaking change or known issue lacks guidance, state the impact and identify the missing action or workaround.

## Verification

- Every included item shipped in the named release and matters to the target audience.
- Headlines and descriptions state user benefit accurately.
- Versions, dates, platforms, limitations, measurements, known issues, and upgrade actions are correct.
- Internal jargon and implementation noise are absent unless audience-appropriate.
- No future work is presented as shipped, and no placeholders or unsupported claims remain.
