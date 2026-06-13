---
topic: markitdown skill
method: comparative analysis
date: "2026-06-13"
related:
  - https://github.com/microsoft/markitdown
  - pages/BUILDING_SKILLS.md
---

# Brainstorm — markitdown skill

## Goal

Create a skill that teaches the model to use markitdown to read uploaded or locally-pathed files (PDF, DOCX, PPTX, XLSX, Outlook MSG, EPUB) as Markdown, and — on explicit request — convert and deliver a `.md` file for download.

## Context

- markitdown 0.1.5 is already installed in the environment.
- Existing skills (pdf, docx, pptx, xlsx) handle creation and editing of those formats. This skill handles **reading** them — ingesting content the model cannot natively parse.
- Two input sources: files attached to the chat (present at `/mnt/user-data/uploads/`) and local filesystem paths the user types or pastes.

## Agenda

1. Clarify primary vs secondary mode
2. Clarify input sources
3. Clarify conversion output format
4. Choose script architecture

## Ideas Considered

### Approach A — Direct CLI calls (no script)

- **Description:** SKILL.md instructs the model to run `markitdown <path>` in bash and capture stdout directly.
- **Benefits:** Zero maintenance, no script to write or update.
- **Trade-offs:** No control over error messages, output truncation, or file-write behavior for conversion mode. Inconsistent model behavior when the CLI output is noisy or large.

### Approach B — Single Python script, two modes *(chosen)*

- **Description:** `scripts/run.py --read <file>` prints markdown to stdout. `scripts/run.py --convert <file> --out <dest>` writes a `.md` file.
- **Benefits:** Consistent error handling, controlled output length for large files, clean two-mode interface the model can call reliably every time.
- **Trade-offs:** One script to maintain; trivial given the narrow scope.

### Approach C — Script + metadata header

- **Description:** Like B, but prepends a YAML header (title, page count, word count, source format) to stdout.
- **Benefits:** Richer structured context before content.
- **Trade-offs:** Extra tokens per invocation; the model already extracts this from content. Complexity not justified by benefit.

## Outcomes

### Summary

A reading-first skill backed by a single Python script with two modes. On any supported file upload the model proactively converts and reads the content before answering. When the user explicitly asks to convert a file, the script writes a `.md` file the user can download. Input sources are both chat uploads and typed local paths.

### Decisions

- **Primary mode:** Proactive read — convert on upload or typed path, ingest result, then respond.
- **Secondary mode:** Explicit convert — write `.md` to `/mnt/user-data/outputs/` and present for download.
- **Script:** Single `scripts/run.py` with `--read` and `--convert --out <dest>` modes.
- **No metadata header** — keeps token cost minimal; model extracts context from content.
- **Supported formats:** PDF, DOCX, PPTX, XLSX, Outlook MSG (`.msg`), EPUB. HTML and plain text are natively readable by the model and excluded to avoid overtriggering.
- **URLs are out of scope** — skill only handles local file paths and chat uploads; web URLs must not trigger it.
- **Auto-install covers extras** — install command is `pip install "markitdown[outlook,epub]" --break-system-packages` to ensure MSG and EPUB optional dependencies (`extract-msg`, `ebooklib`) are present. `MissingDependencyException` is caught alongside `ImportError` and triggers the same install-and-retry path.
- **Truncation limit:** Read mode output is capped at 50 000 characters. If converted content exceeds this, the script appends `\n\n[truncated — content exceeds 50 000 characters]` and exits cleanly.
- **Output filename:** Convert mode writes `<source-stem>.md` (e.g. `report.pdf` → `report.md`) to `/mnt/user-data/outputs/`. On collision, appends `_1`, `_2`, etc.
- **Images:** Alt text only — LLM-based image description is disabled. No API key required; no extra latency or cost.

### Open Questions

- None — scope is fully resolved for implementation.

## Next Steps

1. Write `src/skills/markitdown/SKILL.md` with correct frontmatter, trigger phrases, and step-by-step instructions for both modes.
2. Write `src/skills/markitdown/scripts/run.py` with `--read` and `--convert` modes, error handling, and output truncation for large files.
3. Verify: upload a test PDF and DOCX; confirm proactive read triggers; confirm convert mode writes a downloadable file.
