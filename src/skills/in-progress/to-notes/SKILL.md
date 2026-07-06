---
name: to-notes
description: Converts a video URL, local video/audio file, or existing transcript/text into structured, concept-first lecture notes.
disable-model-invocation: true
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.0.1"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: notes
  tags: [notes, transcript, video, lecture-notes]
---

# To Notes

Turns a video URL, local video/audio file, or existing transcript into **concept-first** lecture notes — organized by idea, not by transcript chronology. No speech-to-text: this skill assumes a transcript already exists or can be fetched as captions. Does not handle `.pdf`/`.docx`/`.pptx`/`.xlsx`/`.msg`/`.epub` documents.

## Step 1 — Resolve the source to plain text

```bash
python3 scripts/resolve_source.py <url-or-path>
```

The script handles all three source shapes:

- **Video URL** — fetches captions via `yt-dlp` (never downloads the video). Prefers manual captions over auto-generated; prefers `en`, falling back to whichever single language track is available.
- **Local video/audio file** — looks for a sibling `.vtt`/`.srt`/`.txt` transcript next to it, matching either the exact stem (`talk.vtt`) or a language-coded variant (`talk.en.vtt`).
- **Transcript/text file** (`.vtt`/`.srt`/`.txt`/`.md`) — reads it directly, stripping timestamps/cues if present.

If the input is pasted transcript text rather than a file or URL, skip the script and use the pasted text as-is.

The script prints `LANGUAGE: <code>` on the first line, a `---` separator, then the plain transcript text.

**Done when** the script prints resolved transcript text, or exits with a specific error (no manual/auto captions found, no sibling transcript, unsupported file type) — never fall back to transcribing audio yourself.

## Step 2 — Draft concept-first notes

Read the resolved transcript and draft lecture notes organized by the source's actual ideas — group related points under topic headers, do not follow the transcript's timeline.

Write the notes to `<kebab-case-title>.md` in the current working directory, unless the user names a different location, with this frontmatter:

```yaml
---
title: <title>
author: <speaker/author, if identifiable, else omit>
source: <original URL or file path>
---
```

If the resolved language (from Step 1's `LANGUAGE:` line) isn't `en`, add a `language: <code>` field. Redact sensitive information (API keys, passwords, personally identifiable information) before writing the notes.

**Done when** the file is written with complete frontmatter and headers reflect the source's real concepts rather than its chronology.
