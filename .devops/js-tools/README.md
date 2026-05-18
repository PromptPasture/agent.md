# JS Tools

This directory contains shared JavaScript tooling.
The canonical markdownlint configuration lives at `.markdownlint.yaml`
in the repository root so VS Code, local runs, and CI use the same rules.

## Install

```bash
npm install --prefix .devops/js-tools
```

## Count Tokens

The token tally helper writes reports to `dist/TOKEN_TALLY.md` and
`dist/TOKEN_TALLY.json`. It tracks `library/rules/*.md`,
`library/commands/*.md`, `library/skills/*/SKILL.md`, and
`library/skills/*/agents/*.md`.

Generate the reports:

```bash
npm run token-tally --prefix .devops/js-tools
```

## Auto-Fix

Some markdownlint findings can be fixed automatically:

```bash
.devops/js-tools/node_modules/.bin/markdownlint-cli2 \
  --config .markdownlint.yaml \
  --fix \
  "**/*.md"
```

Review the diff after `--fix`; not every rule is safely fixable.

## CI Helper

The release workflow runs the token tally helper:

```bash
npm run token-tally --prefix .devops/js-tools -- --output-dir dist
```
