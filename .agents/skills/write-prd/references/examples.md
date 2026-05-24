# PRD Examples

**Use this example to calibrate tone, specificity, section depth, and table usage when drafting a PRD.**

## Complete PRD Example

**Show frontmatter metadata followed by the PRD body.**

**Input:** "Write a PRD for workspace-level audit logs in our B2B SaaS admin console. Enterprise admins need to see who changed settings, exports must be available for compliance, and the goal is to reduce support tickets about unexplained changes."

**Output:**

```markdown
---
status: "[DRAFT | IN_REVIEW | APPROVED]"
documentType: PRD
phase: "[discovery | delivery | maintenance]"
createdAt: "2026-05-19"
updatedAt: "2026-05-19"
author: Product Manager, Admin Experience [assumed]
owner: Product Manager, Admin Experience [assumed]
stakeholders: Enterprise customers, Customer Support, Security, Compliance, Sales [assumed]
tags:
  - "[audit-logs]"
  - "[admin-console]"
related:
  - SPEC.md
---

# PRD: Workspace Audit Logs

## Objective

Enterprise workspace admins need a reliable way to understand who changed critical workspace settings, when the change happened, and what changed. Today, admins must contact support when a configuration changes unexpectedly, which slows incident investigation and creates avoidable support work.

This feature gives admins and compliance teams a self-serve audit trail for workspace-level administrative activity. It should reduce support tickets about unexplained changes, improve enterprise trust, and provide a foundation for compliance exports without turning the admin console into a full security information system.

## Goals

| Goal | Success Metric |
| --- | --- |
| Reduce support dependency for admin-change investigations | 25% reduction in support tickets tagged `settings-change` within 90 days of launch [assumed] |
| Help admins find relevant changes quickly | 80% of audit-log searches return results or an empty state in under 2 seconds [assumed] |
| Support compliance workflows | 90% of enterprise admins who need audit evidence can export logs without contacting support [assumed] |

## Target Users / Personas

Enterprise workspace admins manage workspace settings, membership, authentication, billing, and security controls. They need fast answers when settings change unexpectedly and usually investigate under time pressure.

Compliance and security reviewers periodically need evidence of administrative activity for audits, internal reviews, or customer questionnaires. They care about completeness, exportability, timestamps, actor identity, and retention.

Customer support agents currently investigate settings-change questions manually. They need fewer avoidable tickets and enough audit-log visibility to guide customers when issues are escalated.

## User Stories

| User Story | Priority | Success / Acceptance Signal |
| --- | --- | --- |
| As an enterprise admin, I want to see recent workspace setting changes so that I can identify who made an unexpected change. | High | Admin can view actor, action, timestamp, target, and previous/new values where available. |
| As an enterprise admin, I want to filter audit logs by actor, action, date range, and target so that I can narrow an investigation quickly. | High | Admin can apply filters and clear them without losing context. |
| As a compliance reviewer, I want to export audit logs so that I can attach evidence to an audit request. | High | Reviewer can export filtered logs in CSV format with stable column headers. |
| As a support agent, I want customers to self-serve common change investigations so that fewer tickets require manual log lookup. | Medium | Support ticket volume for unexplained changes decreases after launch. |

## Scope

### In Scope

- Workspace-level audit log page in the admin console.
- Log entries for settings changes, role changes, authentication configuration changes, member invitations/removals, and export events [assumed].
- Filtering by actor, action type, target, and date range.
- CSV export for the current filtered result set.
- Empty, loading, error, and permission-denied states.
- Role-based access limited to workspace owners and admins [assumed].

### Out of Scope

- Real-time alerting for suspicious changes.
- Audit logs for end-user content activity.
- Cross-workspace organization-level audit search.
- SIEM integrations or webhook streaming.
- Retroactive reconstruction of events that were not previously captured.

## Requirements

| Requirement | User Story / Need | Importance | Tracker | Notes |
| --- | --- | --- | --- | --- |
| The admin console must show a chronological list of workspace audit events with timestamp, actor, action, target, and event details. | Admin investigates unexpected changes. | High | TBD | Default sort is newest first. |
| Admins must be able to filter logs by date range, actor, action type, and target. | Admin narrows investigation. | High | TBD | Filters should be shareable by URL if the app supports query-state patterns [assumed]. |
| Admins must be able to export the filtered log view as CSV. | Compliance reviewer needs evidence. | High | TBD | Export includes active filters and generated timestamp in metadata or filename. |
| Users without admin permissions must not be able to view audit logs or export data. | Protect sensitive administrative activity. | High | TBD | Show permission-denied state instead of partial data. |
| The page must explain when no events match the current filters. | Prevent confusion during investigations. | Medium | TBD | Empty state should distinguish no logs from no filter matches. |
| Audit events must use consistent, human-readable action names. | Admin scans logs quickly. | Medium | TBD | Avoid exposing raw internal event names. |

## Non-Functional Requirements

- Audit log list loads within 2 seconds for the default 30-day view at p95 [assumed].
- CSV exports support at least 10,000 rows per export [assumed].
- Audit data is retained for at least 1 year for enterprise workspaces [assumed].
- All audit-log access and export actions are themselves logged.
- Timestamps are displayed in the workspace's configured timezone when available, with UTC preserved in exports [assumed].

## Milestones

| Milestone | Target Date | Exit Criteria | Owner |
| --- | --- | --- | --- |
| Requirements review | TBD | Product, design, engineering, support, and security agree on event coverage and permissions. | Product |
| Design review | TBD | Audit-log page, filters, export flow, and empty states are approved. | Design |
| Beta launch | TBD | Feature enabled for 5-10 enterprise workspaces with support monitoring. | Product / Engineering |
| General availability | TBD | Success metrics baseline is captured and rollout risks are addressed. | Product |

## User Interaction & Design

Designs should cover the audit log table, filter controls, CSV export action, permission-denied state, loading state, empty state, and export error state. The page should prioritize fast scanning and investigation over decorative presentation.

## User Journeys / Key Flows

1. Admin opens the admin console and navigates to Audit Logs.
2. Admin notices a recent authentication settings change and filters by action type.
3. Admin reviews actor, timestamp, and change details.
4. Admin exports the filtered view for internal incident notes.

## Assumptions & Dependencies

| Item | Type | Detail | Validation / Owner |
| --- | --- | --- | --- |
| Event availability | Dependency | Required workspace settings events are already emitted or can be emitted by platform services [assumed]. | Engineering |
| Retention period | Assumption | Enterprise customers expect at least 1 year of audit history [assumed]. | Product / Compliance |
| Permissions | Assumption | Workspace owners and admins are the only roles that should access audit logs [assumed]. | Product / Security |
| Export size | Assumption | CSV export is sufficient for launch; API export is later work. | Product |

## Open Questions

| Question | Answer / Decision | Owner | Date Answered |
| --- | --- | --- | --- |
| Which exact event types are required for beta? | TBD | Product / Engineering | TBD |
| What retention period is contractually required for enterprise plans? | TBD | Compliance | TBD |
| Should support agents have impersonation-free read access to customer audit logs? | TBD | Support / Security | TBD |
| Do exports need signed URLs, watermarking, or access expiry? | TBD | Security | TBD |

## Reference Links

- Customer support ticket analysis: TBD
- Enterprise security questionnaire themes: TBD
- Design exploration: TBD
- Work tracker epic: TBD
```
