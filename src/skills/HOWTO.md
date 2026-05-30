# HOWTO: Write a Skill

Write a skill when an agent needs reusable task-specific judgment, workflow steps, project conventions, tools, templates, or validation that it would not reliably infer on its own.
Do not write a skill for one-off advice or generic knowledge the model already handles.

Use the [Agent Skills standard](https://agentskills.io) for structure.
Start authoring from real expertise, choose a coherent scope, then make the standard structure valid.

## Start From Real Expertise

Do not ask a model to invent a skill from generic knowledge if better source material exists.
Ground the skill in evidence from real work:

- completed agent tasks and the steps that actually worked
- user corrections, preferences, and repeated steering
- project docs, runbooks, style guides, schemas, APIs, and configuration
- code review comments, issues, incidents, fixes, and failure cases
- real input and output examples

Extract the reusable pattern, not the one-off answer.
If the source material is thin, draft narrowly and mark assumptions instead of inflating the skill with generic advice.

## Choose The Skill Scope

Choose one coherent unit of work before writing files.
Skills that are too narrow force several skills to load for one task; skills that are too broad become hard to trigger precisely.

Prefer action-oriented names that describe what the skill helps the agent do.
Verb-first names such as `review-code`, `write-prd`, and `code-tests` work well; concise verbs such as `ask` also work when the scope is clear.

## Refine With Real Execution

After the first draft, run the skill against real or realistic tasks, then revise from evidence:

1. Check whether the skill triggered for the right prompts and stayed quiet for near-misses.
2. Read execution traces, not only final outputs.
3. Cut instructions the agent followed unnecessarily.
4. Clarify vague steps that caused wandering or retries.
5. Add gotchas for mistakes a user had to correct.
6. Move conditional detail into references when it bloats the main body.
7. Add scripts or validation loops for deterministic work the agent keeps redoing by hand.

Use both failures and successful runs.
Successful traces reveal useful defaults; failed traces reveal missing boundaries.

## Standard Baseline

### Directory Structure

A skill is a folder with a required `SKILL.md` file:

```text
skill-name/
├── SKILL.md
├── references/   # Optional focused docs loaded only when needed
├── scripts/      # Optional deterministic helpers or validators
├── assets/       # Optional templates, examples, images, or data files
├── evals/        # Optional development-time eval prompts and fixtures
└── ...           # Any additional files or directories
```

### Minimal `SKILL.md`

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---

# skill-name

Write the instructions the agent should follow after this skill activates.
```

### Expanded `SKILL.md`

```markdown
---
name: pdf-processing
description: Extract text and tables from PDFs, fill PDF forms, and merge PDF files. Use when working with PDF documents, forms, document extraction, or PDF assembly.
license: MIT
compatibility: Requires Python 3 and pdfplumber for text extraction.
allowed-tools: Bash(python:*) Read
tags:
  - pdf
  - documents
metadata:
  author: example-org
  version: "1.0.0"
  source: github.com/example-org/example-skills
  category: documents
---

# pdf-processing

Use this skill to process PDF files with repeatable tooling and validation.

---

## Workflow

1. Identify whether the user needs extraction, form filling, merging, or validation.
2. Use `pdfplumber` for text extraction and table extraction.
3. Use OCR only when the PDF is scanned or text extraction fails.
4. Save extracted text or tables to the requested output path.
5. Verify the output exists, opens successfully, and contains representative content from the source PDF.

---

## Boundaries

Use this skill for PDF processing.
Do not use it for general document writing unless the task requires PDF-specific handling.

---

## Verification

- [ ] The description explains both what the skill does and when to use it
- [ ] The main instructions are short enough to load every time
- [ ] Text extraction was attempted before OCR
- [ ] Output checks are explicit
```

### Frontmatter Rules

- **`name`:** Required. Match the folder name, use only lowercase letters, numbers, and hyphens, keep it under 64 characters, and do not start or end with a hyphen or use consecutive hyphens.
- **`description`:** Required. Keep it under 1024 characters. Agents load only `name` and `description` before deciding whether to read the full skill, so write activation-focused "Use when..." guidance.
- **`license`:** Optional. Keep it short: use a license name or a reference to a bundled license file.
- **`compatibility`:** Optional. Keep it under 500 characters and use it only for real environment requirements.
- **`allowed-tools`:** Optional. Use a space-separated string of pre-approved tools; support varies by agent runtime.
- **`tags`:** Optional. Use short discovery labels.
- **`metadata`:** Optional. Keep it compact; `author`, `version`, `source`, and `category` are the usual fields.

### Versioning

Use Semantic Versioning in `metadata.version`:

- **Major:** breaking changes to the skill contract, such as redefining the trigger, splitting the skill, removing required workflow steps, or changing expected output formats.
- **Minor:** backward-compatible additions, such as new references, expanded trigger coverage, or optional output sections.
- **Patch:** safe reliability tweaks, such as clearer wording, typo fixes, or boundaries that prevent common mistakes.

Always bump `metadata.version` when making a material change to a skill's files.

### Description Checklist

A good description answers three questions:

- **Activation:** when should this skill load?
- **Capability:** what work does it improve?
- **Boundary:** what adjacent tasks should not trigger it?

Focus on user intent and useful contexts, not the skill's internal implementation.

Prefer:

```yaml
description: >
  Review code changes, diffs, pull requests, branches, or patches. Use for
  review findings covering correctness, regressions, security, performance, and
  test gaps.
```

Avoid:

```yaml
description: Helps with code.
```

Test descriptions with realistic prompts: 8-10 that should trigger and 8-10 near-misses that should not.
Include casual wording, file paths, partial context, and adjacent tasks.
If positives miss, broaden by intent.
If negatives trigger, clarify the boundary.
Do not stuff failed-query keywords into the description; that overfits.

Simple one-step tasks may not trigger a skill because the agent can handle them without specialized help.
Test prompts should represent tasks where the skill adds real workflow, domain, or tool value.

### Optimize Description Triggering

Build about 20 labeled trigger queries: 8-10 should trigger and 8-10 should not.
Should-trigger prompts should vary phrasing, explicitness, detail, and complexity.
Strong should-not-trigger prompts are near-misses that share keywords or concepts but need a different skill.

Use realistic prompts with file paths, personal context, specific fields or values, casual wording, abbreviations, and typos.
Avoid obviously irrelevant negative prompts; they prove little.

Run each query multiple times because triggering is nondeterministic.
Start with 3 runs and compute trigger rate.
If positives miss, broaden by intent or context.
If negatives trigger, clarify boundaries.
Do not add exact failed-query keywords unless they represent a real general category.

For iterative optimization, split queries into train and validation sets.
Use train failures to revise the description, keep validation results out of the rewrite, and select the best description by validation pass rate.

### Body Rules

The Markdown body after the frontmatter contains the skill instructions.
The spec does not require a fixed body format. Write whatever helps the agent perform the task effectively.

Recommended content:

- Step-by-step instructions.
- Examples of inputs and outputs.
- Common edge cases.

Optional section names such as `Workflow`, `Boundaries`, `Output`, `Gotchas`, `Verification`, and `Bundled Resources` are useful conventions, not spec requirements. Use them only when they make the skill easier to follow.

- **Aim for moderate detail:** Concise, stepwise guidance with a working example usually beats exhaustive coverage.
- **Calibrate control to task fragility:** Give the agent freedom when several approaches are valid; be prescriptive when sequence, safety, consistency, or external tooling matters.

### Progressive Disclosure

Agent Skills are loaded in three layers:

1. **Metadata:** `name` and `description` are loaded at startup for all skills.
2. **Instructions:** the full `SKILL.md` body is loaded when the skill activates.
3. **Resources:** files in `scripts/`, `references/`, and `assets/` are loaded only when needed.

Every token in `SKILL.md` competes with conversation context, system context, and other active skills.
Keep the main `SKILL.md` under 500 lines and under about 5,000 tokens.
Put only activation-critical and always-needed instructions in it.
Move detailed reference material into optional files when it is large, conditional, or domain-specific:

```text
references/security.md      # Load when reviewing auth, data exposure, or injection risk
references/output-format.md # Load when the user requests the formal deliverable
scripts/validate.py         # Run after editing a skill folder
assets/report-template.md   # Use only when producing that report format
```

Reference files from the skill root:

```markdown
Read `references/security.md` when the change touches authentication, authorization, secrets, user data, SQL, shell commands, or external input.
```

Avoid vague pointers such as "see references for more." The agent needs to know exactly when to load each file.
Keep reference chains shallow; `SKILL.md` should point directly to the file needed.

Keep reference files focused and directly linked from `SKILL.md` with clear loading conditions.

### Spend Context Wisely

Include concrete project conventions, tool commands, schemas, templates, edge cases, reviewer expectations, and validation loops.
Include examples when output shape matters.

Add what the agent lacks and omit what it already knows.
Cut generic background, long explanations of common concepts, broad best-practice lists, and content that does not change agent behavior.
Ask: would the agent likely get this wrong without the instruction? If not, remove it.
If uncertain, test the skill with and without that instruction.

Favor procedures over declarations. "Run `scripts/validate.py` after editing and fix failures before reporting" is stronger than "ensure quality."
Pick defaults instead of presenting menus. Mention alternatives only as escape hatches.

### Effective Instruction Patterns

Use these patterns when they fit:

- **Gotchas:** list non-obvious facts the agent would plausibly miss.
- **Templates:** provide exact output formats instead of describing them in prose.
- **Checklists:** track multi-step workflows where skipped steps matter.
- **Validation loops:** instruct the agent to do the work, validate, fix failures, and repeat.
- **Plan-validate-execute:** require a checked intermediate plan before fragile, batch, or destructive work.

Keep always-relevant gotchas inline in `SKILL.md`.
Move long or conditional templates, examples, and variant guidance into resources with clear load conditions.

### Bundled Resources

Add `references/`, `scripts/`, `assets/`, or `evals/` only when the skill actually uses them.

#### Scripts

Use a pinned one-off command when an existing CLI already does the job:

```bash
npx eslint@9 --fix .
uvx ruff@0.8.0 check .
go run golang.org/x/tools/cmd/goimports@v0.28.0 .
```

State prerequisites in `compatibility` or `SKILL.md`.
Move a command into `scripts/` when it grows complex, repeats across runs, or is easy to get wrong.
Compare execution traces across cases; repeated hand-built parsing, validation, charting, conversion, or report-generation logic is a signal to bundle a tested script.

List bundled scripts in `SKILL.md` and reference them with paths relative to the skill root:

```markdown
## Available scripts

- `scripts/validate.py` — validates generated output
- `scripts/process.py` — converts input data into normalized JSON
```

Commands shown in `SKILL.md` or `references/*.md` should also use paths relative to the skill root.

Prefer self-contained scripts with inline dependencies where the runtime supports them.
For example, use Python PEP 723 with `uv run`, Deno or Bun versioned imports, or Ruby `bundler/inline`.
Pin dependency versions when practical.

#### Script Checklist

- [ ] **No prompts:** accept input through flags, environment variables, or stdin.
- [ ] **`--help`:** document usage, flags, defaults, and examples.
- [ ] **Helpful errors:** say what went wrong, what was expected, and what to try.
- [ ] **Structured output:** write JSON, CSV, or TSV to stdout; write diagnostics to stderr.
- [ ] **Safe retries:** make operations idempotent where possible.
- [ ] **Input constraints:** reject ambiguous input with clear errors; use enums or closed sets where possible.
- [ ] **Dry run:** support `--dry-run` for destructive or stateful changes.
- [ ] **Safe defaults:** require explicit flags such as `--confirm` or `--force` for risky operations.
- [ ] **Exit codes:** use meaningful exit codes and document them.
- [ ] **Bounded output:** default to summaries, limits, pagination, or output files for large results.

#### Assets

Add `assets/` for reusable templates, sample files, images, schemas, or static resources.

#### Evals

Add `evals/` for development-time prompts and fixtures that test whether the skill triggers and produces useful output.
Evals are not runtime instructions.

## Validation

### Trigger Checks

- [ ] Run labeled should-trigger and near-miss prompts multiple times.
- [ ] Check trigger rates; broaden positives or narrow boundaries as needed.

### Output Evals

1. Run 2-3 realistic evals before expanding the suite.
2. Define each eval with a user prompt, expected output, and optional input files.
3. Compare skill output against a baseline: no skill or previous skill version.
4. Use clean contexts and save skill and baseline outputs separately.
5. Grade specific, observable assertions with concrete evidence.
6. Use scripts for mechanical checks such as file existence, JSON validity, row counts, dimensions, or schema conformance.
7. Record pass rate, timing, token cost, and useful human feedback.
8. Use human review for quality issues that assertions miss; use blind comparison when assertion results tie but outputs differ.
9. Inspect traces for failures, flaky cases, wasted steps, and outliers.

### Final Checks

- [ ] Useful steps, corrections, gotchas, and defaults made it into the skill.
- [ ] Folder name and `name` match.
- [ ] `description` is specific, intent-focused, and under 1024 characters.
- [ ] Optional references have clear load conditions.
- [ ] Examples and templates are complete enough to use.
- [ ] Run a skill validator when available.

Skill creator validator:

```bash
python3 src/skills/create-skill/scripts/validate.py src/skills/<skill-name>
```

External reference implementation:

```bash
skills-ref validate ./src/skills/<skill-name>
```

### Iterate

Repeat the loop until results are satisfactory, feedback is consistently empty, or changes no longer improve outcomes.

## Sources

- [Agent Skills specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
