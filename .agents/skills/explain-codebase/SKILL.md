---
name: explain-codebase
description: Explain how code works by tracing repository evidence. Use for "how does X work?", subsystem walkthroughs, data/control flow questions, and critique only when asked for risks, design feedback, or "what is wrong with X?"
author: Oleg Shulyakov
license: MIT
version: 1.1.0
---

# explain-codebase

Answer codebase understanding questions by tracing real repository evidence first, then explaining the system at the level a senior engineer needs to navigate or change it safely.

## Mode Selection

**Match the mode to the user's intent before opening the map.**

- **Explain by default**: use this mode for "how does X work?", subsystem walkthroughs, data flow, control flow, configuration flow, entry points, runtime behavior, and onboarding questions.
- **Critique only on request**: switch to Critique when the user asks for problems, risks, design review, architecture feedback, "what is wrong with X?", or whether an approach is good.
- **Do not over-trigger**: do not use this workflow for plain README summaries, implementation requests, refactors, debugging fixes, or code review unless the user asks for an explanation or architecture critique first.

## Evidence First

**Build the explanation from code paths, tests, and configuration instead of memory.**

- **Start exact**: search for the user's named endpoint, command, module, feature flag, table, event, type, function, error text, or UI label before broadening.
- **Expand deliberately**: follow routes, handlers, services, stores, schemas, workers, tests, fixtures, dependency manifests, generated files, and configuration only as needed to answer the question.
- **Prefer call paths**: use call sites, route registries, public exports, tests, and runtime wiring to distinguish live behavior from unused helpers.
- **Verify vocabulary**: reuse the repository's own names for concepts. If you add a simplifying label, say that it is your label.
- **Mark uncertainty**: separate what you found from what you infer. Say when a path appears unused, generated, deprecated, ambiguous, or absent.

## Trace Workflow

**Trace enough of the runtime path to make the answer operationally useful.**

1. Identify entry points such as UI actions, CLI commands, HTTP routes, jobs, event consumers, public APIs, scheduled tasks, or exported modules.
2. Follow the main control flow through orchestration, domain logic, persistence, external integrations, and response or output boundaries.
3. Follow the data shape from input to transformation, storage, side effects, and returned output.
4. Check important side paths, including validation, authorization, idempotency, caching, retries, async work, feature flags, configuration, errors, logging, metrics, and tracing.
5. Read representative tests, fixtures, docs, or examples when available, using them to confirm behavior and user-facing terminology.
6. Stop when you can name the entry points, owner files, runtime sequence, key data structures, external dependencies, and main failure modes.

## Critique Mode

**Explain the current design before judging it.**

- **Ground every finding**: tie each risk to concrete files, flows, tests, configuration, or missing evidence.
- **Use local standards first**: compare the design to patterns already used in the repository before applying generic architecture preferences.
- **Prioritize impact**: focus on correctness, security, operability, performance, maintainability, testability, and change safety.
- **Avoid drive-by advice**: discard critiques that are stylistic, unsupported, or unrelated to the user's question.
- **Include tradeoffs**: note where the current design is reasonable despite drawbacks.

## Explanation Rules

**Make the system legible without flattening important complexity.**

- **Lead with the answer**: open with one short paragraph explaining what the subsystem does and where the behavior starts.
- **Name concrete evidence**: reference files, functions, types, routes, commands, tables, events, tests, and configuration by name. Use clickable file references when possible.
- **Explain in execution order**: describe control flow in the order it runs and data flow by naming what enters, how it changes, where it is stored or sent, and what comes back.
- **Keep snippets scarce**: include code only when it clarifies a contract, branching rule, data shape, or surprising behavior.
- **Stay in explanation mode**: do not prescribe changes unless the user asked for critique or the trace exposes a serious risk worth naming.
- **Respect scope**: answer the user's question, not every file opened along the way.

## Output Format

**Choose the lightest structure that still makes the path easy to follow.**

- **Short answers**: use concise prose with inline file references.
- **Walkthroughs**: use the template below when the behavior spans multiple files, runtime boundaries, or side paths.
- **Critiques**: append the critique sections only after the explanation.

Walkthrough template:

```text
Short answer:
[One paragraph.]

Entry points:
[Where the behavior starts.]

Flow:
[Ordered explanation of the main runtime path.]

Key pieces:
[Important modules, types, storage, integrations, and tests.]

Edge cases:
[Validation, authorization, errors, async behavior, configuration, or missing evidence.]
```

Critique add-on:

```text
Architecture risks:
[Findings ordered by severity, each with evidence and impact.]

Tradeoffs:
[Where the current design is reasonable despite drawbacks.]
```

## Verification

**Leave the user with a trail they can verify.**

- **List inspected evidence**: for non-trivial answers, end with the main files, tests, docs, commands, or runtime checks used.
- **Report limits**: if the repository could not be inspected, or if the trace depends on missing generated files, inaccessible services, or incomplete tests, say so plainly.
- **Do not fake certainty**: when evidence is incomplete, give the best-supported explanation and name what would confirm it.
