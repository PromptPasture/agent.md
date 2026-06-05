# Security Review

Use this reference for security-sensitive code review within concrete code changes. Also use it when the user asks for OWASP-style review, threat modeling, secrets exposure, abuse resistance, privacy risk, prompt injection, jailbreak, data exfiltration, malicious tool-use, or policy-boundary testing in the reviewed code.

---

## Review Focus

Do not report generic hardening advice unless the reviewed change creates a plausible exposure.

For broad security requests, first identify the reviewed surface and the relevant trust boundaries, then keep the output in normal code-review form: actionable findings with severity, file references, impact, and fix direction.

---

## Access Control

- **Permissions**: check authentication, authorization, tenant isolation, object-level access, role checks, ownership checks, and privilege escalation paths.
- **Server enforcement**: verify server-side enforcement even when the UI hides an action.
- **Noninteractive paths**: check background jobs, webhooks, admin routes, internal APIs, and batch endpoints for the same permission model as interactive paths.

---

## Input And Output Handling

- **Injection**: check SQL, NoSQL, shell, LDAP, template, path, URL, and header construction for injection risk.
- **Parsing**: check SSRF, open redirects, file uploads, archive extraction, deserialization, and parser behavior.
- **Output encoding**: verify output encoding, HTML rendering, markdown rendering, CSV export, and log formatting for unsafe content.

---

## Secrets And Privacy

- **Sensitive values**: confirm tokens, credentials, session identifiers, API keys, PII, PHI, and payment data are not logged, returned, cached, or sent to analytics.
- **Telemetry and clients**: check error messages, traces, metrics labels, screenshots, and client-side state for sensitive data exposure.
- **Credential lifecycle**: verify credential rotation or fallback behavior does not accept weaker credentials longer than intended.

---

## Sessions And Boundaries

- **Session controls**: check cookies, CSRF, CORS, session expiration, refresh tokens, webhook signatures, replay protection, rate limits, and abuse throttles.
- **Cryptography**: verify cryptography uses established project helpers and does not introduce custom primitives, weak randomness, or unsafe comparison.

---

## AI And Agent Surfaces

- **Prompt attacks**: check prompt injection, jailbreak paths, unsafe tool calls, untrusted tool output, policy-boundary bypasses, and data exfiltration through model context or logs.
- **Tool enforcement**: verify tools enforce authorization and argument validation server-side, not only through prompting.
- **Context leakage**: check retrieval, citations, memory, file access, connector access, and hidden/system prompt handling for cross-user or cross-tenant leakage.
- **Action outputs**: confirm model outputs that trigger actions are constrained, validated, audited, and recoverable.
