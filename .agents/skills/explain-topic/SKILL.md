---
name: explain-topic
description: Explain any knowledge topic simply and accurately. Use for "explain X", "why/how/what is X?", concepts, science, definitions, code, design, architecture, and walkthroughs.
license: MIT
version: 2.1.0
tags:
  - explain
  - education
  - reference
author: Oleg Shulyakov
metadata:
  catalog: utility
---

# explain-topic

Explain knowledge questions clearly, accurately, and at the right depth. Use simple language first, then add precision only where it helps the user understand.

## Scope

**Use this skill for explanations of general knowledge, concepts, systems, and code.**

- **Explain broadly**: use this for "why birds fly", "why the sky is blue", "what is the speed of light", "what is a planet", "how does X work", "explain X like I am new to it", and similar knowledge questions.
- **Include code**: also use this for questions about how code works, why software is designed a certain way, how modules interact, what an API does, how data moves, or how an implementation compares to a pattern.
- **Do not over-trigger**: do not use this for requests to write documents, create content, implement changes, debug failures, review code, run commands, or make plans unless the user asks for an explanation first.
- **Do not implement by default**: if the user asks to build, refactor, debug, or review code, route to the appropriate workflow unless they first ask for an explanation.
- **Critique only on request**: switch to Critique when the user asks for risks, design feedback, architecture review, "what is wrong with X?", or whether an approach is good.

## Source Handling

**Use the right source of truth for the topic before simplifying it.**

- **General knowledge**: answer from stable knowledge when the fact is durable, such as basic physics, biology, math, vocabulary, or common engineering concepts.
- **Current or high-stakes facts**: verify with reliable sources when the answer may have changed, needs exact attribution, or involves medical, legal, financial, safety, policy, product, or live factual claims.
- **Code questions**: inspect the repository before explaining behavior, design, architecture, APIs, data flow, configuration, or runtime paths.
- **Start exact**: search for the user's named function, type, class, module, endpoint, command, component, table, event, config key, error text, or UI label before broadening.
- **Expand deliberately**: follow imports, exports, call sites, routes, handlers, services, stores, schemas, workers, tests, fixtures, dependency manifests, generated files, and configuration only as needed to answer the question.
- **Prefer call paths**: use call sites, route registries, public exports, tests, and runtime wiring to distinguish live behavior from unused helpers.
- **Mark uncertainty**: say when you are unsure, when sources disagree, when a claim depends on context, or when repository evidence is incomplete.

## Explanation Workflow

**Choose the smallest trace that answers the question clearly.**

1. Identify what the user wants explained: definition, cause, mechanism, comparison, design, code behavior, consequence, or tradeoff.
2. Start with the shortest useful answer in plain language.
3. Add the mechanism: explain what happens, why it happens, and what parts are involved.
4. Add one concrete example or analogy only if it makes the idea easier to understand.
5. For code, follow entry points, call paths, data shapes, side effects, tests, and configuration only as far as needed.
6. Stop when the user can explain the idea back accurately without needing a textbook chapter. Civilization may continue.

## Critique Mode

**Explain the current idea or design before judging it.**

- **Ground every finding**: tie each risk to evidence, mechanisms, constraints, code paths, tests, configuration, or missing information.
- **Use local standards first**: compare the design to patterns already used in the repository before applying generic architecture preferences.
- **Prioritize impact**: focus on correctness, security, operability, performance, maintainability, testability, and change safety.
- **Avoid drive-by advice**: discard critiques that are stylistic, unsupported, or unrelated to the user's question.
- **Include tradeoffs**: note where the current design is reasonable despite drawbacks.

## Explanation Rules

**Make the topic understandable in plain language while preserving the facts that matter.**

- **Lead with the answer**: open with one short paragraph that directly answers the question.
- **Use the right vocabulary**: define technical terms before relying on them. For code, keep repository names intact so the user can find the code afterward.
- **Explain in natural order**: for runtime behavior, use execution order. For design questions, explain boundaries, responsibilities, dependencies, and tradeoffs. For a function or file, explain its role, inputs, outputs, and important branches.
- **Simplify deliberately**: prefer everyday wording, but do not replace the real mechanism with a misleading metaphor.
- **Keep snippets scarce**: include code only when it clarifies a contract, branching rule, data shape, or surprising behavior.
- **Stay in explanation mode**: do not prescribe changes unless the user asked for critique, advice, or a serious risk is worth naming.
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

How it works:
[Plain-language explanation in the order that best matches the question.]

Example:
[Optional concrete example, analogy, or code reference.]

Important caveat:
[Optional uncertainty, exception, context limit, or edge case.]
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

- **Cite when needed**: provide sources for browsed, unstable, disputed, high-stakes, or exact factual claims.
- **List inspected evidence**: for non-trivial code answers, end with the main files, tests, docs, commands, or runtime checks used.
- **Report limits**: if evidence could not be inspected, or if the trace depends on missing generated files, inaccessible services, incomplete tests, or uncertain sources, say so plainly.
- **Do not fake certainty**: when evidence is incomplete, give the best-supported explanation and name what would confirm it.
