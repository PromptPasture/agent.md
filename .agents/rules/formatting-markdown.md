---
name: formatting-markdown
description: Keep Markdown files linted, tidy, and token-efficient.
applies_to: ["**/*.md", "**/*.markdown"]
priority: medium
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
---

# Markdown Formatting Rules

- Run `markdownlint` or `markdownlint-cli2` on changed Markdown files before finalizing edits.
- Fix lint findings instead of suppressing them unless a rule conflicts with required document format or generated content.
- Trim trailing whitespace, extra spaces, redundant blank lines, filler text, and repeated wording.
- Start each document with one `#` heading. Keep headings unique, sequential, descriptive, and no deeper than the structure requires.
- Use fenced code blocks with language identifiers when the language or format is known.
- Surround lists, tables, and fenced code blocks with blank lines.
- Keep list indentation consistent. Use `1.` for every ordered-list item unless the document requires visible numbering.
- Format tables in compact style: trim each cell and keep exactly one padding space around `|` separators, for example `| Name | Purpose |`.
- End each file with exactly one trailing newline.
- Preserve semantic line breaks, quoted text, and generated text only when reflowing would reduce clarity or change meaning.
