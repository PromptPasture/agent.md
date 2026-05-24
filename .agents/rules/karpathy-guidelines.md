---
name: karpathy-guidelines
description: Keep coding work simple, surgical, explicit, and verifiable.
license: MIT
applies_to: ["**/*"]
priority: high
metadata:
  author: multica-ai
  version: "1.1.0"
  source: github.com/multica-ai/andrej-karpathy-skills
  category: development
---

# Karpathy Guidelines

## Before Coding

**Clarify the goal and assumptions before changing code.**

- Before non-trivial code changes, state the working assumptions, the simplest viable approach, and any ambiguity that changes the implementation.
- Ask one concise question when ambiguity blocks a correct implementation. Do not silently choose among materially different interpretations.
- Prefer declarative goals and success criteria over prescribing every implementation step; use the criteria to loop independently.
- Prefer the minimum code that satisfies the request. Do not add speculative features, unused extension points, single-use abstractions, or configurability the user did not ask for.
- If an implementation grows noticeably larger than the problem requires, simplify before finalizing.

## During Editing

**Change only what the request requires.**

- Keep edits surgical. Touch only files and lines that trace directly to the request, required cleanup, or verification.
- Match existing project style even when another style would be personally preferable.
- Do not refactor, reformat, delete, or "improve" adjacent code unless it is required for the requested change.
- Remove imports, variables, functions, files, and tests made obsolete by your own changes. Mention unrelated pre-existing dead code instead of deleting it.

## Verification

**Define success and prove it.**

- For bug fixes, add or identify a check that reproduces the bug before relying on the fix.
- For new behavior, define concrete success criteria and verify them with the narrowest relevant tests, linters, or manual checks.
- For complex logic, implement the simplest likely-correct version first, verify it, then optimize while preserving the same checks.
- Review agent-written code for subtle conceptual errors, wrong assumptions, and brittle abstractions, not only syntax or test failures.
- For multi-step tasks, use a brief plan where each step includes its verification check.
- In the final response, report the behavior changed, the verification performed, and any assumptions or residual risk that still matters.
