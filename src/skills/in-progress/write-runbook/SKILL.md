---
name: write-runbook
description: Write or revise executable operational runbooks. Use for routine maintenance, deployment, recovery, secret rotation, diagnostics, alert response, on-call triage, mitigation, verification, rollback, communication, and escalation procedures.
license: Apache-2.0
tags:
  - writer
  - docs
  - operations
  - runbook
metadata:
  author: Oleg Shulyakov
  version: "1.0.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
---

# write-runbook

Write an operational procedure that another operator can execute safely under the conditions where it is needed.

## Mode Detection

Use **routine mode** for planned or repeatable operations such as deployment, maintenance, migration, backup, restoration, key rotation, or diagnostics.

Use **on-call mode** when an alert, incident, outage, service degradation, or urgent customer impact requires rapid assessment and mitigation.

If both apply, lead with the urgent on-call path and link to or include the routine recovery procedure only where needed.

## Shared Workflow

1. Identify the trigger, service or system, audience, environment, frequency, risk, and desired end state.
2. Inspect repository and operational evidence: scripts, deployment configuration, monitoring, alerts, dashboards, existing procedures, ownership, tests, and rollback mechanisms.
3. Establish prerequisites, access, safety constraints, communication requirements, and stop conditions.
4. Write ordered steps with exact commands, expected results, decision points, and failure handling.
5. Define verification, rollback or mitigation, escalation, and completion criteria.
6. Check every destructive or production-changing action for scope, reversibility, and operator confirmation.

## Routine Mode

Include, when applicable:

- Purpose and conditions for use
- Estimated duration and risk level
- Required access, tools, backups, approvals, and preflight checks
- Numbered procedure with exact commands and expected output
- Failure handling at the step where failure can occur
- Post-operation verification
- Rollback conditions and ordered rollback steps
- Troubleshooting, escalation, notification, and completion records

Skip rollback only for genuinely read-only procedures, and state that the procedure is read-only.

## On-Call Mode

Optimize for fast scanning under pressure. Include, when applicable:

- Alert name, service, severity, symptoms, customer or SLO impact, owner, and escalation target
- A quick-reference mapping from observed symptoms to likely causes and safe immediate actions
- Initial scope and severity assessment
- Communication actions and timing
- Diagnosis ordered by probability, impact, and speed
- Mitigation options with conditions, risks, and verification
- Resolution criteria and monitoring duration
- Time-based and condition-based escalation
- Post-incident closure, follow-up, and runbook-update requirements

Separate mitigation from root-cause investigation. Restore service first when ongoing impact justifies it.

## Writing Rules

- Assume the operator is competent but unfamiliar with this system.
- Use exact scoped commands; explain placeholders that must be replaced.
- Put expected output and failure handling next to each consequential step.
- Never embed real secrets, tokens, private keys, or unsafe credential examples.
- Identify irreversible, destructive, or customer-impacting actions before execution.
- Prefer the established automation path; document manual steps only when needed for recovery or understanding.
- Link authoritative dashboards, alerts, service docs, and escalation policies rather than duplicating volatile data.
- Mark unverified operational facts with `[assumed]`.
- Do not leave generic placeholders in an active runbook.

## Error Paths

- If commands, owners, escalation paths, or rollback steps cannot be verified, produce a draft and identify the missing operational evidence.
- If no safe rollback exists, state that explicitly and define stop and escalation conditions.
- If a requested action is destructive without adequate safeguards, add confirmation, backup, scope, and recovery requirements before the action.
- If routine and incident procedures conflict, prioritize current operational configuration and surface the discrepancy.

## Verification

- The trigger, scope, owner, prerequisites, risk, and intended result are explicit.
- Every consequential step has an exact action, expected result, and failure path.
- Verification proves the desired state rather than merely proving that commands ran.
- Rollback or mitigation is executable and has clear activation conditions.
- On-call procedures include rapid assessment, communication, escalation, and resolution criteria.
- Commands, links, names, thresholds, and responsibilities match current operational evidence.
- No secrets, unresolved placeholders, contradictions, or unmarked assumptions remain.
