# Description Optimization

Use this reference when optimizing a skill's frontmatter `description` for trigger accuracy.

The description is the main signal native skill runtimes use to decide whether to invoke a skill. Optimize it after the skill behavior is stable; otherwise the trigger will faithfully route users into a moving target.

## Start With Trigger Behavior

Before changing words, define what the description must separate.

Write down:

- **Should trigger:** realistic prompts where this skill should help
- **Should not trigger:** near misses that mention similar words but need another skill or no skill
- **Ambiguous cases:** prompts where the right answer depends on missing context

This prevents the common failure mode: adding keywords from one missed prompt and accidentally widening the trigger for everything else.

---

## Choose The Agent Adapter

Use the adapter that matches the calling agent's normal behavior. If the runtime exposes native trigger detection, use it. Otherwise, use routing-judgment evals.

Examples:

```bash
python -m scripts.run_eval \
  --eval-set <skill-path>/evals/trigger-evals.json \
  --skill-path <skill-path> \
  --agent codex-cli

python -m scripts.run_loop \
  --eval-set <skill-path>/evals/trigger-evals.json \
  --skill-path <skill-path> \
  --agent my-agent
```

For CLIs with unusual invocation shapes, pass `--agent-command` with `{prompt}` or `{prompt_file}` placeholders:

```bash
python -m scripts.run_loop \
  --eval-set <skill-path>/evals/trigger-evals.json \
  --skill-path <skill-path> \
  --agent custom \
  --agent-command "agent run --input {prompt_file}"
```

Do not override the model unless the user explicitly asks. The eval should match the agent's real operating conditions.

---

## Create Trigger Evals

Create about 20 realistic queries split between should-trigger and should-not-trigger cases. Use concrete prompts that resemble real user requests: file paths, domain details, typos, abbreviations, shorthand, and ambiguous phrasing.

Positive cases should cover varied ways users ask for the skill's core capability. Negative cases should be near misses, not obviously irrelevant prompts.

Save them as:

```json
[
  { "query": "the user prompt", "should_trigger": true },
  { "query": "a near miss", "should_trigger": false }
]
```

### Weak vs strong eval prompts

Weak positive:

```text
Use the spreadsheet skill.
```

Strong positive:

```text
Can you turn data/q4-orders.csv into an .xlsx workbook with formulas and a summary chart?
```

Weak negative:

```text
Tell me a joke.
```

Strong negative:

```text
Summarize the CSV schema in prose; do not create or edit a workbook.
```

The strong cases test boundaries. The weak cases mostly test whether the word "spreadsheet" exists.

---

## Review The Eval Set

When possible, show the eval set to the user before running optimization. People spot mislabeled near misses faster than benchmark charts do.

Use `assets/eval_review.html` by replacing:

- **Eval data:** replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array
- **Skill name:** replace `__SKILL_NAME_PLACEHOLDER__` with the skill name
- **Current description:** replace `__SKILL_DESCRIPTION_PLACEHOLDER__` with the current description

The user can edit queries and export the final eval set.

---

## Run The Optimization Loop

Run:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent <calling-agent-label> \
  --results-dir <skill-path>/evals/description-optimization \
  --max-iterations 5 \
  --verbose
```

The loop splits train and held-out test data, evaluates the current description, proposes revisions, and selects `best_description` by held-out test score.

Apply the best description to `SKILL.md`, then report:

- **Old description:** the previous frontmatter text.
- **New description:** the applied replacement text.
- **Scores:** train and held-out results.
- **Misses:** notable false positives and false negatives.
- **Generalization:** why the new wording should hold beyond the train set.

Keep the updated metadata under 100 tokens.

---

## Interpret Results

Do not chase a perfect score blindly. A worse held-out score means the change probably overfit the train set. A better score with new false positives may still be unacceptable if those false positives trigger an expensive or risky workflow.

Common fixes:

- **False negatives:** add missing intent phrases or artifact types
- **False positives:** add narrower action verbs, required context, or exclusions
- **High variance:** add repeated runs or simplify ambiguous eval labels
- **Overlong description:** remove examples and move detailed routing into the body or references

Tiny prompts like "read this file" are poor trigger tests even if the skill technically could help. Trigger eval prompts should be substantive enough that a specialized skill would actually add value.
