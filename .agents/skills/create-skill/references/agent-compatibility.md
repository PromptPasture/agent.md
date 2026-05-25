# Agent Compatibility

Use this reference when adapting skill creation, evaluation, or packaging to a specific agent runtime.

The core rule is simple: preserve the skill's behavior, then swap only the runtime mechanics that do not exist in the current environment.

## Start From Capability Gaps

Before changing a workflow, identify what the current agent can and cannot do.

Check for:

- **Subagents:** Can it run skill and baseline attempts in parallel?
- **Trigger telemetry:** Can it tell whether a skill would activate?
- **File access:** Can it read and write the target skill directory?
- **Browser/display:** Can it show the review UI?
- **Command shape:** Does it take prompts through stdin, arguments, files, or an interactive session?

Do not rewrite portable instructions just because a runtime lacks one convenience. Adapt the missing mechanism, not the skill's intent.

---

## Agents Without Subagents

Follow the same draft, test, review, and improve loop, but run test cases serially yourself.

Baseline comparisons are weaker without isolated runs. Skip them unless another local mechanism can produce them fairly. Treat results as qualitative unless deterministic assertions can be checked locally.

When review UI support is limited, use one of these fallbacks:

- **Static review:** save a static HTML review file.
- **Inline summary:** summarize outputs directly in the conversation.
- **Focused questions:** ask concise inline review questions.
- **Deterministic checks:** use scripts for checks that do not need human judgment.

### What changes

The process gets slower and less statistically clean. The standard should not get lower. Keep transcripts, outputs, and grading results organized so another reviewer can reproduce the judgment.

---

## Claude Code

Claude Code can use native trigger detection through the optimization scripts:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent claude-code \
  --verbose
```

Use the user's normal Claude Code configuration. Do not silently switch models or tool settings, because trigger behavior should reflect the user's actual environment.

---

## Generic CLI Agents

Use the generic command adapter unless the agent exposes better trigger telemetry:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent codex-cli \
  --verbose
```

For CLIs that need arguments or files instead of stdin, use `--agent-command`:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --agent custom \
  --agent-command "agent run --input {prompt_file}" \
  --verbose
```

Use `{prompt}` when the CLI accepts inline prompt text. Use `{prompt_file}` when prompt files are safer for quoting, long inputs, or multiline content.

---

## Cowork

Cowork has subagents, so parallel skill and baseline runs can work. If timeouts become a problem, run prompts in smaller batches instead of dropping coverage.

Cowork may not have a display. Generate a static review file with:

```bash
python <skill-creator-path>/eval-viewer/generate_review.py \
  <iteration-dir> \
  --skill-name "<name>" \
  --benchmark <iteration-dir>/benchmark.json \
  --static <output_path>
```

Use the generated review UI before revising from test outputs. When feedback is downloaded as `feedback.json`, copy it into the current iteration directory before continuing.

---

## Updating Installed Skills

Preserve the original skill directory name and `name` frontmatter. Installed skills often rely on those identifiers for discovery.

If the installed skill path is read-only:

1. Copy the skill to a writable location.
2. Edit and validate the copy.
3. Package from the copy.
4. Tell the user which artifact or directory should replace the installed version.

When packaging manually, stage temporary package contents in `/tmp/` first if direct writes fail.

---

## Portability Checklist

Before finishing a compatibility adaptation, verify:

- **Core behavior:** the workflow still describes the same skill behavior.
- **Runtime isolation:** runtime-specific commands are isolated to compatibility notes.
- **Fallbacks:** unavailable features have explicit alternatives.
- **Result confidence:** eval results are described with the right confidence level.
- **Packaging:** package and install instructions match the user's actual runtime.
