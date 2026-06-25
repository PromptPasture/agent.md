---
type: concept
title: Engineering principles
description: How SOLID, DRY, KISS, YAGNI, and related principles are applied in agent-generated code and skill authoring.
tags: [engineering, principles, dry, yagni, solid, kiss]
created: "2026-06-25T00:00:00Z"
updated: "2026-06-25T00:00:00Z"
---

# Engineering principles

These principles are **decision lenses**, not mechanical rules. They must be balanced against local context, requested scope, and verification needs.

Source: `wiki/sources/2026-05-23-design-principles/PRD.md` and `Most Popular Principles.md`.

## KISS and YAGNI (default brakes)

KISS and YAGNI are the default constraints for implementation. New abstractions require evidence of reduced complexity, duplicated knowledge, coupling, or test risk. The [`yagni` skill](/docs/skills/productivity.md) enforces this during review.

## DRY (knowledge deduplication)

DRY targets **duplicated knowledge or business logic**, not harmless repeated syntax, markup, or test setup. Two similar lines of HTML are not a DRY violation. Two places that encode the same business rule are. The [`dry` skill](/docs/skills/productivity.md) catches this during review.

## SOLID

Apply through clear responsibilities, small interfaces, and explicit dependencies — not ceremonial layers. An abstraction requires evidence that it reduces coupling, complexity, duplication of knowledge, or test risk.

|Principle|Practical agent behavior|
|---|---|
|SRP|One clear responsibility per class/module; no "god objects"|
|OCP|Extend via new files/types, not by modifying stable internals|
|LSP|Subtypes must be substitutable; no silent behavior overrides|
|ISP|Prefer small, focused interfaces over fat ones|
|DIP|Depend on abstractions at system boundaries, not concrete implementations|

## Law of Demeter

Don't chain through objects to reach distant collaborators. Pass what you need explicitly.

## Boy Scout Rule

Clean only touched code or code required for the requested change. Unrelated opportunistic refactors are out of scope.

## CQS (Command-Query Separation)

Methods either return a value (query) or change state (command) — not both.

## Composition over inheritance

Prefer composing behaviors from focused pieces over deep inheritance chains.

## Integration in skills

The global rule lives in `src/rules/engineering-principles.md`. Skills (`code-backend`, `code-frontend`, `code-database`, `code-tests`, `review-code`, `create-skill`) carry targeted principle lenses only where they change expected behavior — not the full source document.
