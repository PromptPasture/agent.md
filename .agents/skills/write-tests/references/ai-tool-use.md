# AI Tool-Use Eval Generation

Use this reference for testing agents that call tools, functions, APIs, shell commands, browser actions, database queries, or local code-modification utilities.

Do not use this reference for malicious tool-use, data exfiltration, prompt-injection, or policy bypass testing. Route those to `audit-security`.

## What To Test

**Evaluate tool behavior by trace, state, and completion discipline.**

- **Tool selection:** The agent chooses the right tool for the task and avoids tools when no tool is needed.
- **Argument correctness:** Tool arguments match schema, paths, IDs, filters, and user constraints.
- **Sequencing:** Tool calls happen in a valid order, especially for search-read-edit-verify workflows.
- **Error recovery:** The agent handles failed, empty, or partial tool results without looping or inventing success.
- **Stop condition:** The agent stops after completion instead of continuing to make unnecessary calls.
- **State discipline:** The agent does not overwrite unrelated files, reuse stale observations, or ignore newer user instructions.

## Eval Case Shape

**Define the task, controlled environment, expected trace, and final state.**

Each case should define:

- **Task:** User task and starting state.
- **Tools:** Available tools and schemas.
- **Mocks:** Mocked tool responses or fixture workspace.
- **Trace:** Expected tool-call trace, allowing harmless equivalent calls when appropriate.
- **Final state:** Expected final output or changed files.
- **Failure budget:** Max calls, max retries, or forbidden calls.

## Trace Assertions

**Assert the important properties of the trace without overfitting harmless choices.**

Use trace-level assertions:

- **Required calls:** Required tool was called at least once.
- **Forbidden calls:** Forbidden tool was not called.
- **Arguments:** Tool arguments match schema and include required constraints.
- **Order:** Calls happen in order: inspect before edit, execute before summarize, verify after change.
- **Failure handling:** On simulated failure, the agent retries with a changed input or reports the blocker.
- **Call budget:** Total tool calls stay under a reasonable limit for the scenario.

Avoid overfitting exact traces unless the workflow is deterministic. Two different valid search queries are not a failure; deleting the wrong directory very much is.

## Fixture Design

**Keep fixtures small enough to inspect and realistic enough to fail meaningfully.**

Make fixtures small but realistic:

- **Relevant noise:** Include one relevant file and one tempting irrelevant file.
- **Stale data:** Include stale or ambiguous data when testing recency handling.
- **Mocked outcomes:** Mock both success and failure responses for external tools.
- **Edge cases:** Include spaces in paths, empty search results, pagination, or malformed API responses.

## Runner Pattern

**Capture tool calls, results, outputs, and diffs for deterministic grading.**

Generate or extend a runner that:

- **Execution:** Runs the agent against fixture tasks with a controlled tool registry.
- **Trace capture:** Captures every tool call, argument payload, result, final answer, and file diff.
- **Assertions:** Applies deterministic assertions to the trace and final state.
- **Artifacts:** Writes artifacts per case so failures can be inspected without rerunning.

## Output Files

**Store cases, fixtures, harnesses, and trace checks together.**

Common outputs:

- **Cases:** `evals/tool-use/cases.jsonl` for tasks and expected traces.
- **Fixtures:** `evals/tool-use/fixtures/` for local files and mocked tool responses.
- **Harness:** `evals/tool-use/run.*`.
- **Assertions:** `evals/tool-use/assertions.*` for reusable trace checks.
