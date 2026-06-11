---
name: explain
description: Explain any knowledge topic simply and accurately. Use for explanation requests like "explain X", "why/how/what is X?", concepts, science, definitions, code, design, architecture, and walkthroughs.
license: Apache-2.0
tags:
  - explain
  - education
  - reference
metadata:
  author: Oleg Shulyakov
  version: "2.2.0"
  source: github.com/olegshulyakov/agent.md
  catalog: productivity
  category: education
---

# Explaining Topic

Explain knowledge questions clearly, accurately, and at the right depth. Use simple language first, then add precision only where it helps the user understand.

---

## Source Handling

- **General knowledge**: answer from stable knowledge when the fact is durable, such as basic physics, biology, math, vocabulary, or common engineering concepts.
- **Current or high-stakes facts**: verify with reliable sources when the answer may have changed, needs exact attribution, or involves medical, legal, financial, safety, policy, product, or live factual claims.
- **Code questions**: inspect the repository before explaining behavior, design, architecture, APIs, data flow, configuration, or runtime paths.
- **Start exact**: search for the user's named function, type, class, module, endpoint, command, component, table, event, config key, error text, or UI label before broadening.
- **Expand deliberately**: follow imports, exports, call sites, routes, handlers, services, stores, schemas, workers, tests, fixtures, dependency manifests, generated files, and configuration only as needed to answer the question.
- **Prefer call paths**: use call sites, route registries, public exports, tests, and runtime wiring to distinguish live behavior from unused helpers.
- **Mark uncertainty**: say when you are unsure, when sources disagree, when a claim depends on context, or when repository evidence is incomplete.

---

## Explanation Workflow

1. Identify what the user wants explained: definition, cause, mechanism, comparison, design, code behavior, consequence, or tradeoff.
2. Start with the shortest useful answer in plain language.
3. Add the mechanism: explain what happens, why it happens, and what parts are involved.
4. Add one concrete example or analogy only if it makes the idea easier to understand.
5. For code, follow entry points, call paths, data shapes, side effects, tests, and configuration only as far as needed.
6. Stop when the user can explain the idea back accurately without needing a textbook chapter. Civilization may continue.

---

## Critique Mode

- **Ground every finding**: tie each risk to evidence, mechanisms, constraints, code paths, tests, configuration, or missing information.
- **Use local standards first**: compare the design to patterns already used in the repository before applying generic architecture preferences.
- **Prioritize impact**: focus on correctness, security, operability, performance, maintainability, testability, and change safety.
- **Avoid drive-by advice**: discard critiques that are stylistic, unsupported, or unrelated to the user's question.
- **Include tradeoffs**: note where the current design is reasonable despite drawbacks.

---

## Explanation Rules

- **Lead with the answer**: open with one short paragraph that directly answers the question.
- **Use the right vocabulary**: define technical terms before relying on them. For code, keep repository names intact so the user can find the code afterward.
- **Explain in natural order**: for runtime behavior, use execution order. For design questions, explain boundaries, responsibilities, dependencies, and tradeoffs. For a function or file, explain its role, inputs, outputs, and important branches.
- **Simplify deliberately**: prefer everyday wording, but do not replace the real mechanism with a misleading metaphor.
- **Keep snippets scarce**: include code only when it clarifies a contract, branching rule, data shape, or surprising behavior.
- **Stay in explanation mode**: do not prescribe changes unless the user asked for critique, advice, or a serious risk is worth naming.
- **Respect scope**: answer the user's question, not every file opened along the way.

---

## Boundaries

  Scenario: Topic needs explanation
    Given the user asks about general knowledge, concepts, systems, or code behavior
    Then explain at the depth the user needs

  Scenario: Code explanation is requested
    Given the user asks how code works, why software is designed a certain way, how modules interact, what an API does, how data moves, or how an implementation compares to a pattern
    Then include code behavior and repository evidence when useful

  Scenario: Request belongs to another workflow
    Given the user asks to write documents, create content, implement changes, debug failures, review code, run commands, or make plans
    And the user has not asked for an explanation first
    Then route to the appropriate workflow instead of over-triggering explain

  Scenario: Implementation is requested
    Given the user asks to build, refactor, debug, or review code
    And the user has not first asked for an explanation
    Then do not implement by default
    And route to the appropriate workflow

  Scenario: Critique is requested
    Given the user asks for risks, design feedback, architecture review, "what is wrong with X?", or whether an approach is good
    Then switch to Critique mode

---

## Output

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

---

## Verification

  Scenario: Output passes quality check
    Given an explanation has been produced
    Then sources are provided for browsed, unstable, disputed, high-stakes, or exact factual claims
    And non-trivial code answers list the main files, tests, docs, commands, or runtime checks used
    And missing evidence, inaccessible services, incomplete tests, uncertain sources, or unavailable generated files are reported
    And incomplete evidence is not presented with false certainty
