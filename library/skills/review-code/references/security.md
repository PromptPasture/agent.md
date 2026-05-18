# Security Review

Use this reference for security-sensitive code review within concrete code changes. Also use it when the user asks for OWASP-style review, threat modeling, secrets exposure, abuse resistance, privacy risk, prompt injection, jailbreak, data exfiltration, malicious tool-use, or policy-boundary testing in the reviewed code.

## Review Focus

A security finding should describe the trust boundary, attacker capability, vulnerable path, and impact. Do not report generic hardening advice unless the reviewed change creates a plausible exposure.

For broad security requests, first identify the reviewed surface and the relevant trust boundaries, then keep the output in normal code-review form: actionable findings with severity, file references, impact, and fix direction.

## Access Control

- Check authentication, authorization, tenant isolation, object-level access, role checks, ownership checks, and privilege escalation paths.
- Verify server-side enforcement even when the UI hides an action.
- Check background jobs, webhooks, admin routes, internal APIs, and batch endpoints for the same permission model as interactive paths.

## Input And Output Handling

- Check SQL, NoSQL, shell, LDAP, template, path, URL, and header construction for injection risk.
- Check SSRF, open redirects, file uploads, archive extraction, deserialization, and parser behavior.
- Verify output encoding, HTML rendering, markdown rendering, CSV export, and log formatting for unsafe content.

## Secrets And Privacy

- Confirm tokens, credentials, session identifiers, API keys, PII, PHI, and payment data are not logged, returned, cached, or sent to analytics.
- Check error messages, traces, metrics labels, screenshots, and client-side state for sensitive data exposure.
- Verify credential rotation or fallback behavior does not accept weaker credentials longer than intended.

## Sessions And Boundaries

- Check cookies, CSRF, CORS, session expiration, refresh tokens, webhook signatures, replay protection, rate limits, and abuse throttles.
- Verify cryptography uses established project helpers and does not introduce custom primitives, weak randomness, or unsafe comparison.

## AI And Agent Surfaces

- Check prompt injection, jailbreak paths, unsafe tool calls, untrusted tool output, policy-boundary bypasses, and data exfiltration through model context or logs.
- Verify tools enforce authorization and argument validation server-side, not only through prompting.
- Check retrieval, citations, memory, file access, connector access, and hidden/system prompt handling for cross-user or cross-tenant leakage.
- Confirm model outputs that trigger actions are constrained, validated, audited, and recoverable.
