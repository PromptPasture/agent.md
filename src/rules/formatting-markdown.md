---
name: formatting-markdown
description: Keep Markdown files linted, tidy, and token-efficient.
license: MIT
applies_to: ["**/*.md", "**/*.markdown"]
priority: medium
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  category: documentation
---

# Markdown Formatting

- **Linting**: Run `markdownlint` or `markdownlint-cli2` on changed Markdown files before finalizing edits.
- **Lint fixes**: Fix findings instead of suppressing them unless a rule conflicts with required document format or generated content.
- **Token efficiency**: Trim trailing whitespace, extra spaces, redundant blank lines, filler text, and repeated wording.
- **Headings**: Start each document with one `#` heading. Keep headings unique, sequential, descriptive, and no deeper than the structure requires.
- **Code blocks**: Use fenced code blocks with language identifiers when the language or format is known.
- **Block spacing**: Surround lists, tables, and fenced code blocks with blank lines.
- **List numbering**: Keep list indentation consistent. Use `1.` for every ordered-list item unless the document requires visible numbering.
- **Tables**: Format tables compactly: trim each cell and keep exactly one padding space around `|` separators, for example `| Name | Purpose |`.
- **File ending**: End each file with exactly one trailing newline.
- **Preservation**: Preserve semantic line breaks, quoted text, and generated text when reflowing would reduce clarity or change meaning.
