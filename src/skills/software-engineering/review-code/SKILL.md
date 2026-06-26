---
name: review-code
description: Reviews code for correctness, security, performance, and style with structured findings. Use when the user asks to review code, including code changes, diffs, pull requests, branches, or patches.
license: Apache-2.0
metadata:
  author: github.com/wpank/ai
  version: "2.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: software-engineering
  category: review
  tags: [review, code quality]
---

# Reviewing Code

Review concrete code changes and surface defects, regressions, security or performance risks, maintainability problems with clear impact, and test gaps that make the change difficult to trust.

## Workflow

### Setup

Identify the target and comparison base. Inspect repository guidance, the linked issue, changed files, and minimum context needed to understand intended behavior, contracts, and blast radius. Separate verified intent from assumptions.

### Loop

1. Trace the changed paths: inputs, state transitions, side effects, outputs, errors, retries, and cleanup.
2. Apply the relevant checklists, ordered by the changed surface. Prioritize trust-boundary, data-loss, and availability risks. Use checklists as coverage prompts, not reasons to invent findings.
3. Validate each suspected problem against contracts and evidence:
   - Supported → keep with severity and location.
   - Unsupported → dismiss.
   - Impact overstated → downgrade.
   - Tests, linters, or reproductions available → run them.
   - Dismissal uncovers an unexamined surface → re-enter step 1.

### Exit

When all remaining findings are evidence-backed and no new surface was identified.

## Checklists

Use only the checklists relevant to the changed surface.
A checked item means the concern was investigated; it does not require a finding.

### Correctness

- [ ] **Edge Cases** — Empty, zero, negative, maximum, and boundary values follow the contract
- [ ] **Nullable Values** — Missing or optional values are handled before use through guards, defaults, types, or equivalent mechanisms
- [ ] **Off-by-One Errors** — Loop bounds, array slicing, pagination offsets, and range calculations are verified
- [ ] **Race Conditions** — Concurrent access preserves ordering and shared-state invariants
- [ ] **Time Handling** — Storage, comparison, conversion, locale, and daylight-saving behavior match the contract
- [ ] **Unicode & Encoding** — String operations preserve expected characters and use the required encoding
- [ ] **Overflow / Precision** — Arithmetic uses types and rounding appropriate to the domain
- [ ] **Error Propagation** — Errors from asynchronous work and external services are surfaced or handled; failures are never silently swallowed
- [ ] **State Consistency** — Multi-step mutations, retries, and partial failures leave the system in a valid state
- [ ] **Boundary Validation** — Values at the boundaries of valid ranges (min, max, exactly-at-limit) are tested

### Compatibility and Rollout

- [ ] **Public Contracts** — APIs, schemas, events, configuration, defaults, and serialized formats remain compatible or are intentionally versioned
- [ ] **Data Changes** — Migrations and backfills are safe for existing data, production scale, retries, and interruption
- [ ] **Mixed Versions** — Old and new application versions can coexist safely during deployment
- [ ] **Release Order** — Code, configuration, feature flags, generated clients, and migrations do not require an unsafe atomic release
- [ ] **Rollback** — Reverting the change does not lose data, reinterpret persisted state, or repeat irreversible side effects

### Security and Privacy

- [ ] **Injection** — Untrusted values cannot alter queries, commands, paths, URLs, templates, headers, or parser behavior
- [ ] **XSS** — Untrusted content is encoded or sanitized before rendering; raw HTML APIs such as `dangerouslySetInnerHTML` are justified and safe
- [ ] **Request Integrity** — State-changing requests have appropriate CSRF, origin, signature, and replay protections
- [ ] **Authentication** — Every protected endpoint verifies the user is authenticated before processing
- [ ] **Object-Level Authorization** — Resource access is scoped to the requesting user's permissions; identifier-based access cannot bypass ownership or tenant checks
- [ ] **Input Validation** — All external input (params, headers, body, files) is validated for type, length, format, and range on the server side
- [ ] **Secrets Management** — Credentials are not committed or exposed and use the repository's approved secret mechanism
- [ ] **Dependency Safety** — New dependencies are justified, trusted, compatible, and checked for relevant known vulnerabilities
- [ ] **Sensitive Data** — PII, tokens, and secrets are never logged, included in error messages, or returned in API responses
- [ ] **Abuse Controls** — Public, authentication, upload, and expensive paths have risk-appropriate limits and validation
- [ ] **Browser Security** — Cookies, CORS, content types, and security headers remain appropriate where affected
- [ ] **AI and Agent Boundaries** — Untrusted instructions, tool arguments, retrieved context, actions, and cross-user data access are constrained

### Performance

- [ ] **N+1 Queries** — Database access patterns are batched or joined; no loops issuing individual queries
- [ ] **Unnecessary Re-renders** — Views, components, templates, or renderers avoid repeated work with measurable user or resource impact
- [ ] **Memory Leaks** — Event listeners, subscriptions, timers, and intervals are cleaned up on unmount/disposal
- [ ] **Payload and Bundle Size** — New code, dependencies, responses, and assets do not add disproportionate transfer or startup cost
- [ ] **Loading Strategy** — Expensive work is deferred, streamed, cached, or moved off critical paths when required by measured usage
- [ ] **Database Access** — Query plans, indexes, transaction length, and connection use fit expected data size and access patterns
- [ ] **Bounded Work** — Lists, queries, payloads, concurrency, polling, recursion, and fan-out have appropriate limits
- [ ] **Resource Cost** — Memory, CPU, latency, and external-service cost scale acceptably with traffic and customer data

### Maintainability and Operations

- [ ] **Naming Clarity** — Variables, functions, and classes have descriptive names that reveal intent
- [ ] **Responsibilities** — Module and function boundaries make the changed behavior understandable and hard to misuse
- [ ] **Duplication** — Repeated logic creates no concrete drift or inconsistent-behavior risk
- [ ] **Complexity** — Branching and nesting remain understandable and testable for the changed behavior
- [ ] **Error Handling** — Errors are caught at appropriate boundaries, logged with context, and surfaced meaningfully
- [ ] **Dead Code Removal** — Commented-out code, unused imports, unreachable branches, and obsolete feature flags are removed
- [ ] **Literal Semantics** — Values that encode a shared rule or non-obvious meaning are named or documented
- [ ] **Consistent Patterns** — New code follows the conventions already established in the codebase
- [ ] **Dependency Direction** — New dependencies preserve established ownership and architecture boundaries
- [ ] **Observability** — Critical paths have enough logs, metrics, traces, audit records, or alerts to diagnose failure
- [ ] **Recovery** — Operational controls and recovery guidance match changed behavior and failure modes

### Testing and User Impact

- [ ] **Test Coverage** — New logic paths have corresponding tests; critical paths have both happy-path and failure-case tests
- [ ] **Edge Case Tests** — Tests cover boundary values, empty inputs, nulls, and error conditions
- [ ] **No Flaky Tests** — Tests are deterministic; no reliance on timing, external services, or shared mutable state
- [ ] **Test Independence** — Each test sets up its own state and tears it down; test order does not affect results
- [ ] **Meaningful Assertions** — Tests assert on behavior and outcomes, not implementation details
- [ ] **Test Readability** — Tests follow repository conventions and describe the scenario and expected outcome
- [ ] **Mocking Discipline** — Mocks preserve realistic contracts and do not hide the behavior under review
- [ ] **Regression Tests** — Bug fixes include a test that reproduces the original bug and proves it is resolved
- [ ] **Accessibility** — Affected UI covers keyboard, focus, assistive technology, responsive, loading, empty, error, and permission states
- [ ] **Documentation** — User-facing behavior, public contracts, configuration, migrations, and operational changes are documented when needed

## Finding Standard

Include a finding only when the change creates a concrete failure mode or a clear engineering risk.

Each finding must contain:

- **Severity:**
  - `P0` for catastrophic production impact or severe active exposure;
  - `P1` for likely user-visible failure, data loss, security breach, or blocked rollout;
  - `P2` for a meaningful edge-case defect, compatibility issue, or maintainability risk with concrete future impact;
  - `P3` for a minor issue worth fixing.
- **Title and location:** a specific title with the tightest relevant file and line range.
- **Reasoning:** the triggering condition, observable impact, and supporting evidence.
- **Fix direction:** the smallest practical correction or test.

Prefer fewer high-confidence findings over speculative commentary.
If evidence is incomplete, label the concern as an open question rather than a defect.

## Output

Lead with findings ordered by severity, then list open questions or assumptions, test gaps, and a brief summary.
Omit empty sections except when explicitly stating that no findings were found.

```markdown
- **[P1] Short title** — `path/to/file.ext:42`
  Trigger, impact, evidence, and minimal fix direction.
```

After findings, add only substantive `Open Questions`, `Test Gaps`, and `Summary` sections.
If no findings remain, say `No findings.` and report test gaps, unverified behavior, and residual risk.

When the runtime supports inline comments, attach them only to findings with a fix direction and use tight line ranges.
Keep the summary separate so findings remain usable without the surrounding conversation.

## Review Rules

- Review the requested target and the minimum surrounding code needed to establish its behavior. Do not expand into unrelated refactoring.
- Do not rubber-stamp a change or treat checklist completion as evidence that it is correct. Trace behavior and validate conclusions against repository evidence.
- Tie findings to changed behavior. Do not report generic best practices, personal style preferences, praise, or pre-existing defects unless the change newly exposes or worsens them.
- Do not bikeshed, block on formatting that automation should enforce, or require a preferred implementation when the submitted approach is correct.
- Do not leave vague drive-by comments. Explain the triggering condition, impact, evidence, and practical correction.
- Critique the code and its behavior, never the author or presumed intent.
- Do not modify code during a review unless the user also asks for fixes.
- Treat generated files, snapshots, lockfiles, and vendored code as supporting evidence unless they are directly edited or reveal a generated-output defect.
- Do not promote missing tests to a severity finding unless the test itself is wrong, CI can pass while the behavior is broken, or the absence of coverage makes a high-risk change unverifiable.
- Distinguish confirmed findings, supported inferences, open questions, test gaps, and residual risk. Never present an assumption as a verified defect.
- If a command or environment cannot be run, state that limitation without treating the absence of verification as proof of correctness.

## Verification

Before finalizing the review, verify that:

- Every finding is tied to the reviewed change, evidence, impact, severity, location, and a practical fix direction.
- Findings are not duplicates, speculation, style comments, or broad redesign requests.
- Commands, failures, assumptions, gaps, and unverified areas are reported accurately.
- A review with no findings still reports meaningful residual risk.
