# AI Output Eval Generation

Use this reference for testing model answers, generated artifacts, RAG responses, structured outputs, and prompt regressions.

Do not use this reference for jailbreak, prompt-injection, data leakage, or safety-policy audits. Route those to `audit-security`.

## What To Test

**Evaluate behavior that proves the model output is useful, grounded, and stable.**

- **Task success:** The response solves the user's actual request.
- **Completeness:** Required sections, constraints, edge cases, or artifacts are present.
- **Factual grounding:** Claims are supported by provided context, retrieved documents, or citations.
- **Structured output validity:** JSON, YAML, XML, SQL, code, OpenAPI, or other schemas parse and validate.
- **Instruction following:** Formatting, tone, length, refusal boundaries, and required/forbidden content.
- **Regression behavior:** Prompt, model, retrieval, or tool changes do not degrade known scenarios.

## Eval Case Shape

**Give each case enough structure to run, grade, and debug repeatedly.**

Each eval case should include:

- **`id`:** Stable identifier.
- **`input`:** User prompt plus relevant context.
- **`expected`:** Exact value, semantic expectation, or rubric.
- **`assertions`:** Deterministic checks first, model-graded checks only where needed.
- **`metadata`:** Scenario type, difficulty, source fixture, and owner.

Prefer a mix of deterministic and rubric checks. Deterministic checks catch boring breakage cheaply; rubrics catch semantic failures where exact matching would be theater with a JSON costume.

## Assertion Types

**Prefer deterministic assertions and reserve rubrics for semantic quality.**

Use deterministic assertions when possible:

- **Format parsing:** Parses as the required format.
- **Schema matching:** Matches JSON Schema, Zod, Pydantic, OpenAPI, or protobuf schema.
- **Field checks:** Contains required fields and no forbidden fields.
- **Citation checks:** Cites only source IDs that exist in the retrieval context.
- **Clarification behavior:** Refuses or asks a clarification only when the expected behavior says so.

Use rubric assertions for quality:

```text
Score 0: Fails the task or contradicts context.
Score 1: Partially correct but misses important constraints or invents unsupported facts.
Score 2: Correct, grounded, complete, and follows the requested format.
Pass threshold: score >= 2.
```

## RAG-Specific Checks

**Separate retrieval quality from answer grounding.**

For retrieval-augmented generation, separate retrieval quality from answer quality:

- **Retrieval assertions:** Expected source appears in top-k, irrelevant source count stays below a limit, source metadata is preserved.
- **Grounding assertions:** Answer uses retrieved context, unsupported claims are flagged, citations point to the right source chunks.
- **Missing-context behavior:** When retrieval has no answer, the model says it cannot determine the answer instead of improvising. Improvisation is charming at jazz night, less so in support automation.

## Prompt Regression Harness

**Make prompt regressions reproducible across model, retrieval, and dependency changes.**

Generate or extend a runner that:

- **Case loading:** Loads eval cases from a fixture file.
- **Entry point:** Calls the model or application entry point with the same settings each run.
- **Metadata capture:** Records model name, prompt version, temperature, retrieval index version, and dependency versions.
- **Result storage:** Stores raw outputs and assertion results.
- **CI gating:** Fails CI only on stable, deterministic checks unless the team explicitly accepts model-graded CI gates.

## Output Files

**Place eval cases, runners, rubrics, and reports where CI can find them.**

Common outputs:

- **Cases:** `evals/<feature>.jsonl` or `evals/<feature>.yaml`.
- **Runner:** `evals/run_<feature>.*`.
- **Rubrics:** `evals/rubrics/<feature>.md` for human/model grading criteria.
- **Reports:** `evals/reports/` for generated run results when the repo already stores benchmark artifacts.
