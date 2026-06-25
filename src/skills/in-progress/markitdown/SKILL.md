---
name: markitdown
description: Reads .pdf, .docx, .pptx, .xlsx, .msg, and .epub files by converting them to Markdown with markitdown, then ingests the result. Use when a file with one of those extensions is uploaded or a local path to one is given and the goal is to read, summarize, or understand its content. Also use when the user explicitly asks to "convert to markdown" or "save as markdown" for a supported file. Proactively convert on upload — do not wait for the user to ask. Do NOT use for creating or editing documents, for web URLs, for HTML files, or for plain text.
license: Apache-2.0
metadata:
  author: Oleg Shulyakov
  version: "1.1.2"
  source: github.com/olegshulyakov/agent.md
  catalog: utility
  category: document-conversion
  tags: [documents, markdown, conversion, markitdown]
---

# MarkItDown

Converts .pdf, .docx, .pptx, .xlsx, .msg, and .epub files to Markdown using [markitdown](https://github.com/microsoft/markitdown), then reads the result.

## Supported Formats

|Extension|Format|
|---|---|
|`.pdf`|PDF documents|
|`.docx`|Word documents|
|`.pptx`|PowerPoint presentations|
|`.xlsx`|Excel workbooks|
|`.msg`|Outlook email messages|
|`.epub`|EPUB ebooks|

## Mode 1 — Read (primary)

Use whenever a supported file is uploaded or the user gives a local path and the goal is to understand its content. **Do not wait for the user to ask — convert and read proactively.**

### Step 1: Resolve the file path

- **Uploaded file:** path is at `/mnt/user-data/uploads/<filename>`
- **Typed path:** use it as-is

### Step 2: Convert and read

```bash
python3 scripts/run.py --read <path>
```

The script prints the Markdown content to stdout (capped at 50 000 characters).
Ingest the output, then respond to the user normally.

### Step 3: If the output is truncated

The script appends `[truncated — content exceeds 50 000 characters]` when the file is large.
Tell the user the file was partially read and offer to answer questions about specific sections.

## Mode 2 — Convert (secondary)

Use only when the user explicitly asks to convert a file to Markdown or save it as a `.md` file.

### Step 1: Resolve the file path (same as Mode 1)

### Step 2: Convert and save

```bash
python3 scripts/run.py --convert <path> --out /mnt/user-data/outputs/<stem>.md
```

Where `<stem>` is the original filename without extension (e.g. `report.pdf` → `report.md`). If the output file already exists, append `_1`, `_2`, etc.

### Step 3: Present the file

Call `present_files` with the output path so the user can download it.

## Examples

### Uploaded PDF — proactive read

User uploads `annual_report.pdf` and asks: "What were the key findings?"

```bash
python3 scripts/run.py --read /mnt/user-data/uploads/annual_report.pdf
```

Ingest the output, then answer the question.

### Local path — proactive read

User says: "Summarise /home/user/docs/proposal.docx"

```bash
python3 scripts/run.py --read /home/user/docs/proposal.docx
```

### Explicit conversion

User says: "Convert this spreadsheet to Markdown" (after uploading `data.xlsx`)

```bash
python3 scripts/run.py --convert /mnt/user-data/uploads/data.xlsx \
  --out /mnt/user-data/outputs/data.md
```

Then present `data.md` for download.

## Troubleshooting

### Error: file not found

Verify the path with `ls <path>`. For uploads, confirm the filename matches exactly — paths are case-sensitive.

### Error: unsupported format

Only the six extensions above are supported. For other formats, use the appropriate skill or tool.

### Error: conversion failed

markitdown may fail on corrupted or password-protected files. Tell the user the file could not be read and ask them to verify it opens correctly in its native application.
