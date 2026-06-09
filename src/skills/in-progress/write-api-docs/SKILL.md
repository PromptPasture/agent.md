---
name: write-api-docs
description: Write or revise reference documentation for existing APIs. Use for REST endpoints, GraphQL operations, gRPC methods, WebSocket messages, authentication, parameters, schemas, responses, errors, limits, and executable request examples.
license: Apache-2.0
tags:
  - writer
  - docs
  - api
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
---

# write-api-docs

Document an implemented API so developers can integrate without reading its source.

## Workflow

1. Identify the API style, audience, scope, and target format.
2. Inspect authoritative implementation evidence: route or method definitions, schemas, validators, authorization, handlers, tests, generated contracts, and existing examples.
3. Establish global conventions such as base URLs, authentication, content types, versioning, pagination, rate limits, idempotency, and common errors.
4. Group operations by resource or domain.
5. Document each operation completely, including inputs, outputs, constraints, errors, and a realistic successful example.
6. Compare the finished documentation against implementation and tests.

## Per-Operation Requirements

For each endpoint, operation, method, or message, document:

- Name, method or operation type, path or channel, and purpose
- Authentication and authorization requirements
- Path, query, header, or operation parameters
- Request body or message schema
- Required and optional fields, defaults, constraints, formats, and valid values
- Successful response status and complete response schema
- Error statuses or codes, conditions, and response shape
- Rate limits, pagination, retries, idempotency, or ordering when applicable
- At least one complete request and response example

For sensitive values, explain how they are supplied and whether they are write-only, masked, or omitted from responses.

## Writing Rules

- Treat implementation and tests as authoritative over stale prose.
- Use tables for compact field references and code blocks for executable examples.
- Describe behavior and constraints, not only field names and types.
- Keep examples consistent with documented schemas, defaults, authentication, and status codes.
- Put shared authentication and error behavior in global sections rather than repeating it.
- Link related operations and schemas where that helps navigation.
- Mark description-derived behavior with `[assumed]` when no implementation or contract verifies it.
- Do not redesign the API; report undocumented or inconsistent behavior separately.

## Error Paths

- If code and an API contract disagree, expose the conflict and identify both sources.
- If an error response or constraint cannot be verified, omit the claim or mark it `[assumed]`.
- If the scope contains many operations, establish global conventions once and document complete resource groups rather than producing shallow coverage.

## Verification

- Every documented input and output field has a type and meaningful description.
- Requiredness, defaults, constraints, valid values, and sensitive-field behavior are explicit.
- Examples are complete and internally consistent.
- Authentication, authorization, errors, pagination, limits, and versioning are covered where applicable.
- All material behavior is traceable to implementation, contracts, tests, or marked assumptions.
