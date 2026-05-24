# Skill Evaluation

Use this reference when creating eval cases, running skill iterations, benchmarking outputs, or collecting human feedback.

## Test Cases

**Create prompts that exercise the skill's real decision points.**

Create 8-10 realistic prompts for a focused skill. For router skills, create 8-10 prompts per route and include near-miss prompts that could be confused with another route.

Save test cases to `<skill-path>/evals/evals.json`. Keep evals inside the skill folder so prompts, fixtures, outputs, and benchmark history travel with the skill.

For router skills, add a `reference` field to every eval using the exact relative path, such as `references/postgres.md`. Every reference file that the router can load must have 8-10 evals. Near-miss prompts still count toward the route they are intended to test.

Start with prompt-level expectations. Add objective assertions after the test set is agreed or while runs are in progress.

## Run Iterations

**Keep every run reproducible enough to compare later.**

Put run results in `<skill-path>/evals/iterations/iteration-N/`. Each test case gets its own directory. For each case, save the prompt, generated outputs, timing when available, and grading results.

For new skills, compare `with_skill` against `without_skill`. For existing skills, snapshot the old skill before editing and use that snapshot as the baseline when useful. Exclude previous `evals/iterations/` from snapshots.

When subagents are available, launch skill-enabled and baseline runs in the same round so results are comparable. Without subagents, run cases serially and treat results as a qualitative sanity check.

## Assertions and Grading

**Prefer objective checks, but do not fake objectivity where judgment is required.**

Good assertions are objective, specific, and named clearly enough to make benchmark output readable. Do not force quantitative assertions onto outputs that require human judgment.

Grade each run using `agents/grader.md` or a deterministic script. Save `grading.json` with expectation objects that use exactly `text`, `passed`, and `evidence`.

Use scripts for checks that can be automated. They are usually faster, less fragile, and reusable in later iterations.

## Benchmark and Review

**Summarize results with the bundled tools before asking the user to inspect outputs.**

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

## Improve from Feedback

**Revise from repeated evidence, not one-off prompt quirks.**

Read `feedback.json` after the user finishes reviewing. Empty feedback means the output was acceptable. Focus revisions on specific complaints, repeated misses, and benchmark patterns.

Generalize from examples instead of overfitting to one prompt. Remove instructions that cause wasted work. Bundle scripts when repeated helper code appears across runs.

Repeat until feedback is resolved, results stop improving, or the user says the skill is good enough.
