# Skill Evaluation

Use this reference when creating eval cases, running skill iterations, benchmarking outputs, or collecting human feedback.

## Test Cases

Create 8-10 realistic prompts for a focused skill. For router skills, create 8-10 prompts per route and include near-miss prompts that could be confused with another route.

Save test cases to `<skill-path>/evals/evals.json`. Keep evals inside the skill folder so prompts, fixtures, outputs, and benchmark history travel with the skill.

For router skills, add a `reference` field to every eval using the exact relative path, such as `references/postgres.md`. Every reference file that the router can load must have 8-10 evals. Near-miss prompts still count toward the route they are intended to test.

Start with prompt-level expectations. Add objective assertions after the test set is agreed or while runs are in progress.

---

## Assertion Design

Read this when drafting assertions for a skill's `evals/evals.json`. It answers one question: **what makes an assertion actually useful?**

### Start with the contract, not the test cases

Before writing a single assertion, extract the skill's contract from `SKILL.md`:

- **What does it produce?** File format, structure, and content type.
- **What inputs does it consume?** Files, prompt content, or structured data.
- **What does it explicitly promise?** For example, "always produces a two-sheet workbook" or "never modifies the input file".
- **What would a user reasonably assume even if unstated?** Values are accurate, nothing is hallucinated, and the output is complete.

This is the ground truth. Every assertion should trace back to something in the contract.

### Enumerate failure modes first

Don't jump to assertions. Reason about what can go wrong first:

| Failure mode | What it looks like |
| --- | --- |
| **Structural** | Wrong file type, corrupt output, unparseable JSON, missing required sheets |
| **Completeness** | Missing rows, fields, or sections; the output exists but is partial |
| **Accuracy** | Wrong values; hallucinated, miscalculated, or copied incorrectly from the input |
| **Fidelity** | Input data was transformed unintentionally; reworded, rounded, or reformatted |
| **Contamination** | Placeholders, leftover content from a previous run, apology text, or defaults |
| **Process** | The skill's documented steps were skipped in favor of improvisation |

Each assertion should target at least one of these. If you can't name which failure mode an assertion catches, it is probably not worth including.

### Cover the input space with equivalence classes

Write at least one eval per useful class rather than many similar prompts:

| Class | Purpose |
| --- | --- |
| `smoke` | Simplest possible input; catches total breakdowns |
| `happy_path` | Realistic, typical use case; the core regression test |
| `complex` | High-volume or multi-part input; catches partial completion and off-by-one errors |
| `edge` | Boundary condition the skill implies but does not explicitly handle |
| `invalid` | Malformed, missing, or contradictory input; catches error handling |

Skip classes that do not apply. For skills with file inputs, use real files with known content. Do not write accuracy assertions unless you know the correct answer before running.

### Write discriminating assertions

An assertion that always passes is worse than no assertion; it creates false confidence. Every assertion should be hard to satisfy accidentally.

**Structural** assertions check output shape, regardless of content:

> `"The output file has the extension .docx"`
> `"The spreadsheet contains exactly two sheets named 'Summary' and 'Line Items'"`

**Completeness** assertions check that required content is present:

> `"Sheet 'Line Items' has exactly 7 data rows, one per item in the input"`
> `"No cell in column B is empty in rows 2 through 9"`

**Accuracy** assertions check values against ground truth:

> `"Cell B8 contains 3240.00, the correct subtotal of the 7 line items"`
> `"The vendor name in A1 is exactly 'Apex Industrial S.A.', copied from the PDF header"`

**Fidelity** assertions check that input data was preserved:

> `"Product descriptions in column A match the input verbatim, not paraphrased"`
> `"Numeric values are not rounded; '1247.50' appears, not '1248'"`

**Negative** assertions check things that must not be present:

> `"No cell contains '[PLACEHOLDER]' or is empty in the required range"`
> `"The total in B10 does not equal the subtotal in B8; tax was applied"`
> `"The word 'approximately' does not appear in any numeric field"`
> `"No text matching 'I was unable to' appears in the output file"`

Every eval with objective checks should include at least one negative assertion. These catch cases where the model attempted the task but gave up, left defaults, or produced a plausible-looking wrong result.

### Use `[MUST]` for blockers

Some assertions represent total failure. If they do not pass, the output is worthless regardless of what else passes. Prefix these with `[MUST]`:

> `"[MUST] The output file has the extension .xlsx"`
> `"[MUST] Cell B10 contains the correct grand total"`

Do not overuse this. One or two per eval is usually enough. Treat `[MUST]` as a grading signal; do not imply deterministic tooling enforces it unless the grader or benchmark script actually does.

### Use the discrimination checklist

Before keeping each assertion, ask:

1. Could this pass on hallucinated output? If yes, anchor it to a specific value from a specific input.
2. Could this pass on an empty file? If yes, add a content assertion alongside it.
3. Does another assertion in this eval target the same failure mode? If yes, merge or drop one.
4. What would have to go wrong for this to fail? If you can't name it, the assertion is too vague.

### What good looks like

**Skill:** extract invoice data from a PDF and write it to an Excel spreadsheet.

Weak assertions:

```text
"A .xlsx file was created"                    # passes if file is empty
"The file contains invoice data"              # passes if one cell says "invoice"
"The total is calculated"                     # passes if any formula exists
```

Strong assertions for an eval with a known 7-item input totaling `$3,758.40`:

```text
"[MUST] The output file has the extension .xlsx"
"[MUST] Cell B10 contains 3758.40, the correct grand total including 16% VAT"
"Sheet 'Line Items' has exactly 7 data rows matching the input"
"The vendor name in A1 is exactly 'Apex Industrial S.A.', from the PDF header"
"No cell in column B contains a string; all values are numeric"
"Cell B10 does not equal cell B8; VAT was applied, not just the subtotal"
"No cell in the required range contains '[PLACEHOLDER]' or is empty"
```

Each assertion catches a different failure. If B10 equals B8, the VAT step was skipped. If column B has strings, the model wrote `"3,240.00"` instead of a number. If there are 8 rows, a line item was hallucinated. None of these pass on a plausible-looking wrong output.

### Use process assertions sparingly

Process assertions check that the documented steps were followed, not just that the output looks right:

> `"The skill's bundled script 'extract_fields.py' was called during execution"`

Use these when the skill has a specific required tool or script. A model that produces the right output by improvising a different approach may fail on harder inputs, and process assertions catch that early. One process assertion is usually enough.

---

## Run Iterations

Put run results in `<skill-path>/evals/iterations/iteration-N/`. Each test case gets its own directory. For each case, save the prompt, generated outputs, timing when available, and grading results.

For new skills, compare `with_skill` against `without_skill`. For existing skills, snapshot the old skill before editing and use that snapshot as the baseline when useful. Exclude previous `evals/iterations/` from snapshots.

When subagents are available, launch skill-enabled and baseline runs in the same round so results are comparable. Without subagents, run cases serially and treat results as a qualitative sanity check.

---

## Assertions and Grading

Good assertions are objective, specific, contract-derived, and named clearly enough to make benchmark output readable. Do not force quantitative assertions onto outputs that require human judgment.

Grade each run using `agents/grader.md` or a deterministic script. Save `grading.json` with expectation objects that use exactly `text`, `passed`, and `evidence`.

Use scripts for checks that can be automated. They are usually faster, less fragile, and reusable in later iterations.

---

## Benchmark and Review

Run:

```bash
python -m scripts.aggregate_benchmark <skill-path>/evals/iterations/iteration-N --skill-name <name>
```

This creates `benchmark.json` and `benchmark.md` with pass rate, time, and token summaries. Put each skill-enabled version before its baseline counterpart.

Create the human review UI with:

```bash
python <skill-creator-path>/eval-viewer/generate_review.py \
  <skill-path>/evals/iterations/iteration-N \
  --skill-name "<name>" \
  --benchmark <skill-path>/evals/iterations/iteration-N/benchmark.json
```

For headless environments, use `--static <output_path>` and share the generated HTML. Do not hand-roll a separate review UI.

---

## Improve from Feedback

Read `feedback.json` after the user finishes reviewing. Empty feedback means the output was acceptable. Focus revisions on specific complaints, repeated misses, and benchmark patterns.

Generalize from examples instead of overfitting to one prompt. Remove instructions that cause wasted work. Bundle scripts when repeated helper code appears across runs.

Repeat until feedback is resolved, results stop improving, or the user says the skill is good enough.
