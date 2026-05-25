---
name: review-code
description: >
  Review code changes, diffs, pull requests, branches, or patches. Use for
  review findings covering correctness, regressions, security, performance, and
  test gaps.
license: MIT
tags:
  - review
  - code
  - quality
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-team-roles
  category: development
---

# review-code

Review concrete code changes. Prioritize defects that could ship, regressions that change behavior, security or performance risks, and missing tests that make the change hard to trust.

---

## Workflow

1. Identify the review target: supplied diff, PR, commit range, branch comparison, staged changes, or working tree changes.
2. Read `references/checklist.md` before reviewing so the concern areas match the expected code review checklist.
3. Inspect the changed files and nearby code that defines contracts, callers, tests, migrations, configuration, or runtime behavior affected by the change.
4. Check behavior in this order: correctness, regressions and compatibility, security, data integrity, concurrency or async behavior, performance, observability, and tests.
5. Load one focused reference when the diff needs deeper review: `references/regressions.md`, `references/security.md`, `references/performance.md`, or `references/test-gaps.md`.
6. Validate assumptions against existing tests, fixtures, type definitions, API contracts, docs, and dependency manifests when available.
7. Report only actionable findings. Skip style preferences, broad refactors, and speculative issues without a concrete failure mode.
8. If no issues are found, say so directly and name any residual risk or test coverage gap.

---

## Boundaries

Review the requested diff, pull request, branch, commit, patch, or recently changed code files, including security-sensitive review of those changes. If the user asks how code works before judging it, use the explanatory workflow first and then review only if requested.

Do not rewrite code during a review unless the user explicitly asks for fixes. Do not produce a praise sandwich. The useful artifact is a findings list grounded in file and line evidence.

---

## Finding Standard

Each finding should include:

- **Severity**: `P0` for immediate production breakage or severe security exposure, `P1` for likely user-visible bugs or data loss, `P2` for meaningful edge-case regressions or maintainability risks with clear impact, `P3` for minor issues worth fixing before merge.
- **Location**: file path and tight line reference from the changed code or the smallest relevant surrounding line.
- **Problem**: what fails, under what condition, and why the current change causes it.
- **Impact**: who or what is affected.
- **Fix direction**: the minimal correction or test that would resolve the issue.

Prefer fewer, stronger findings over a long list of low-confidence commentary. If a concern depends on missing context, label it as an assumption or open question instead of presenting it as fact.

---

## Output

For normal reviews, use this shape:

```text
Findings:
- [P1] Short title — path/to/file.ext:42
  The changed code does X when Y happens, which causes Z. Fix by ...

Open questions:
- ...

Test gaps:
- ...

Summary:
One short paragraph, only after findings.
```

If there are no findings:

```text
No blocking findings.

Test gaps:
Mention missing or unverified coverage, or "None found" if applicable.

Residual risk:
Mention any area not inspected or dependent on environment/runtime behavior.
```

When the runtime supports inline code comments, use them only for actionable findings with tight line ranges. Keep the normal review summary concise.

---

## Review Rules

- **Changed behavior**: tie findings to changed behavior, not generic best practices.
- **Missing tests**: do not flag missing tests as a finding unless the missing test hides a concrete bug or high-risk behavior; otherwise put it under `Test gaps`.
- **Generated files**: treat generated files, snapshots, lockfiles, and vendored code as supporting evidence unless the change directly edits them.
- **Public contracts**: verify public API, schema, and data migration changes against compatibility expectations.
- **Frontend changes**: check user-visible state, accessibility regressions, responsive behavior, and data loading errors when relevant.
- **Backend changes**: check validation, authorization, idempotency, transaction boundaries, error handling, and observability when relevant.
- **Test changes**: check false positives, order dependence, leaked state, sleeps, network dependence, and assertions that do not prove behavior.

---

## Verification

Confirm each finding is tied to changed code, includes impact and a fix direction, and has a tight file or line reference. When no findings are reported, state the test gaps and residual risk instead of leaving the review empty.
