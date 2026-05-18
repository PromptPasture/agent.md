# Markdown Format

This directory contains the Markdown linting helper used by CI.
The canonical markdownlint configuration lives at `.markdownlint.yaml`
in the repository root so VS Code, local runs, and CI use the same rules.

## Install

```bash
npm install --prefix .devops/markdown-format
```

## Lint Markdown

Run markdownlint with the same config used by CI:

```bash
.devops/markdown-format/node_modules/.bin/markdownlint-cli2 \
  --config .markdownlint.yaml \
  "**/*.md"
```

Lint selected files by replacing the glob with file paths:

```bash
.devops/markdown-format/node_modules/.bin/markdownlint-cli2 \
  --config .markdownlint.yaml \
  README.md library/rules/formatting-markdown.md
```

## Auto-Fix

Some markdownlint findings can be fixed automatically:

```bash
.devops/markdown-format/node_modules/.bin/markdownlint-cli2 \
  --config .markdownlint.yaml \
  --fix \
  "**/*.md"
```

Review the diff after `--fix`; not every rule is safely fixable.

## CI Helper

The CI workflow writes changed Markdown paths to `changed-markdown-files.txt`,
then runs:

```bash
bash .devops/markdown-format/lint-changed-markdown.sh
```

That script expects `changed-markdown-files.txt` to exist in the repository root.
