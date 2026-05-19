# JS Tools

This directory contains shared JavaScript tooling.
The canonical markdownlint configuration lives at `.markdownlint.yaml`
in the repository root so VS Code, local runs, and CI use the same rules.

## Install

```bash
npm install --prefix .devops/js-tools
```

## Lint Markdown

Run markdownlint with the repository configuration:

```bash
npm run lint --prefix .devops/js-tools
```

Fix supported markdownlint findings:

```bash
npm run lint:fix --prefix .devops/js-tools
```

Review the diff after `lint:fix`; not every rule is safely fixable.

## Count Tokens

The token tally helper writes reports to `dist/TOKEN_TALLY.md` and
`dist/TOKEN_TALLY.json`. It tracks `.agents/rules/*.md`,
`.agents/commands/*.md`, `.agents/skills/*/SKILL.md`, and
`.agents/skills/*/agents/*.md`.

Generate the reports:

```bash
npm run token-count --prefix .devops/js-tools
```

## CI Helper

The markdown formatting workflow runs:

```bash
npm ci --prefix .devops/js-tools
npm run lint --prefix .devops/js-tools
```

The release workflow runs:

```bash
npm run token-count --prefix .devops/js-tools -- --output-dir dist
```
