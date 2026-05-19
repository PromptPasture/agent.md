---
name: explain-codebase
description: Explain how something works in this codebase by exploring code and producing a clear architectural explanation. Optionally critique the architecture for issues.
author: Oleg Shulyakov
license: MIT
version: 1.0.0
---

# explain-codebase

Explore the codebase to answer "how does X work?" questions. Produce clear architectural explanations at the level of a senior engineer onboarding onto a subsystem: enough to build a working mental model, not so much that it reads like annotated source code.

## Mode Selection

**Choose the smallest mode that answers the user.**

Use **Explain** by default. Use **Critique** only when the user asks for problems, risks, design review, architecture feedback, "what is wrong with this?", or similar evaluation after understanding the system.

## Explain Mode

**Trace the code before explaining it.**

Start from the user's named concept, endpoint, command, module, behavior, or error path. Search for exact names first, then expand to related routes, handlers, services, types, tests, docs, configuration, and generated code. Prefer `rg`, file tree inspection, dependency manifests, route registries, test names, and call sites over guesses.

Follow this workflow:

1. Identify the entry points: UI actions, CLI commands, HTTP routes, jobs, event consumers, public APIs, or exported modules.
2. Trace the main path through orchestration, domain logic, persistence, external integrations, and output boundaries.
3. Trace important side paths: validation, authorization, caching, retries, async work, error handling, feature flags, configuration, and observability.
4. Read representative tests or fixtures when available; use them to confirm behavior and terminology.
5. Distinguish verified facts from inferences. Say when a path appears unused, generated, deprecated, or ambiguous.
6. Stop when the explanation can name the owner files, the runtime flow, the key data structures, and the main failure modes.

## Critique Mode

**Explain first, then evaluate design risks.**

In Critique mode, produce the normal explanation before listing issues. Judge architecture against the repository's own patterns before applying generic preferences. Focus on risks that affect correctness, operability, maintainability, security, performance, or change safety.

When the runtime and user request allow independent review, use parallel reviewers for substantial critiques and give each one a narrow concern such as data flow, boundaries, tests, or operational risks. Otherwise, perform the critique directly. Integrate findings yourself and discard weak or unsupported claims.

## Explanation Rules

**Make the system legible without pretending the code is simpler than it is.**

- Lead with the answer: one short paragraph describing what the subsystem does and where it starts.
- Name concrete files, functions, types, routes, commands, tables, and events. Use clickable file references when possible.
- Explain control flow in execution order. Explain data flow by naming the shape that enters, how it is transformed, where it is stored or sent, and what comes back.
- Include only code snippets that clarify a contract or surprising behavior. Do not paste long source excerpts.
- Prefer project vocabulary over invented labels. If you introduce a label for clarity, say it is your label.
- Surface uncertainty directly. Use phrases like "I found", "this appears to", or "I did not find" when evidence is incomplete.
- Avoid prescribing changes in Explain mode unless the user asked for critique or a serious risk is visible.

## Output Format

**Structure the answer around the user's question, not around every file you opened.**

For short explanations, use concise prose with file references inline.

For broader walkthroughs, use this shape:

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

For Critique mode, append:

```text
Architecture risks:
[Findings ordered by severity, each with evidence and impact.]

Tradeoffs:
[Where the current design is reasonable despite drawbacks.]
```

## Verification

**Show enough evidence for the user to trust the map.**

End with the main files inspected when the answer is non-trivial. If the repository could not be inspected, say so and answer only from provided context. If tests, docs, or runtime checks were used to confirm behavior, mention them briefly.
