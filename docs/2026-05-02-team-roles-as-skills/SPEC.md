# SPEC: Software Team Roles as Skills — Technical Specification

## Concept

Each skill encodes a specific capability of a software team role. A role (e.g. System Analyst) produces multiple artifact types (functional specs, use cases, data flow diagrams, gap analyses), so it maps to multiple skills. Conversely, one skill type (e.g. `codegen-backend`) serves multiple roles (Backend Dev, Team Lead). The library works both ways:

- **Role → Skills:** install all skills for a role to give the agent a complete role capability
- **Skill → Roles:** install individual skills across roles to solve a specific artifact need

## Naming Convention

All skills use prefix-first naming: `<type>-<subject>`

This groups related skills together on the filesystem automatically. The type is the kind of artifact produced; the subject is the domain or topic.

```text
<type>-<subject>[-<variant>]
```

**Valid types:**
`audit` · `checklist` · `codegen` · `design` · `diagram` · `model` · `patterns` · `planner` · `report` · `review` · `setup` · `strategy` · `template` · `tracker` · `writer`

**Multi-variant skills** use references and detection logic inside one router skill whenever related artifacts share the same role context.

---

## Filesystem Layout

```text
skills/
├── audit-a11y/
├── audit-gap/
├── audit-security/
├── audit-test-flaky/
├── checklist-release/
├── codegen-backend/
├── codegen-database/
├── codegen-frontend/
├── codegen-mobile/
├── codegen-test/
├── design-api/
├── design-arch/
├── diagram-dfd/
├── diagram-integration/
├── diagram-ux-flow/
├── model-dbt/
├── patterns-auth/
├── patterns-graphql/
├── patterns-realtime/
├── planner-capacity/
├── planner-sprint/
├── report-cve/
├── report-db-health/
├── report-team-health/
├── review-code/
├── setup-developer-portal/
├── setup-eval-harness/
├── setup-infra/
├── setup-monorepo/
├── setup-rag/
├── strategy-api-versioning/
├── strategy-backup/
├── strategy-dependency-upgrade/
├── strategy-feature-flag/
├── template-creator/
├── tracker-velocity/
├── writer-alert-rules/
├── writer-backlog/
├── writer-compliance/
├── writer-epic/
├── writer-lineage/
├── writer-mentorship/
├── writer-ml-experiment/
├── writer-postmortem/
├── writer-prd/
├── writer-prompt/
├── writer-slo/
├── writer-spec/
├── writer-stakeholder/
├── writer-tech-docs/
├── writer-team-agreement/
├── writer-test-strategy/
├── writer-tech-radar/
├── writer-use-case/
└── writer-user-story/
```

---

## Skill Structure (per skill)

```text
<skill-name>/
├── SKILL.md              # Required. YAML frontmatter + instructions. Max 500 lines.
├── evals/
│   └── evals.json        # Min 10 test cases
└── references/           # Optional. Large reference files, loaded on demand.
    ├── <variant-a>.md
    └── <variant-b>.md
```

### SKILL.md Frontmatter (required fields)

```yaml
---
name: <skill-name>
description: >
  <When to trigger + what it produces. Be specific about output artifact.
   Lean toward over-triggering — mention related keywords and contexts.>
---
```

---

## Full Skill Catalog (55 skills)

### 📋 Requirements (6)

| Skill | Roles | Output Artifact |
| --------------------- | ----------------- | ------------------------------------------------------------------------- |
| `writer-prd` | PM, PO | Product Requirements Document with goals, personas, scope, metrics |
| `writer-spec` | SA, Architect, UX | Specification doc (functional, technical, NFR, design, data-contract) |
| `writer-use-case` | System Analyst | Use case document with actors, preconditions, main/alt flows |
| `diagram-dfd` | System Analyst | Data flow diagram (Mermaid or structured text) |
| `audit-gap` | System Analyst | Gap analysis report: current state vs target state, with remediation list |
| `diagram-integration` | System Analyst | Integration map: systems, APIs, data flows, ownership |

**Trigger disambiguation:**

- `writer-prd` → triggered by business goals, personas, success metrics language
- `writer-spec` → triggered by "write a spec", "tech spec", "TDD", "functional requirements", "non-functional requirements", "NFR", "data contract", "UI spec", "handoff doc"

#### Multi-variant: `writer-spec`

```text
writer-spec/
├── SKILL.md
└── references/
    ├── functional.md     # Business rules, actors, main/alt flows
    ├── technical.md      # System architecture, integrations, data flow
    ├── non-functional.md # Performance, security, scalability targets
    ├── design-ui.md      # UI tokens, spacing, component states
    └── data-contract.md  # Schema, ownership, versioning, SLA
```

---

### 🔄 Planning & Agile (8)

| Skill | Roles | Output Artifact |
| ----------------------- | ------------- | --------------------------------------------------------------------------- |
| `writer-prd` | PM, PO | (see Requirements) |
| `writer-epic` | PO | Epic: goal, value, child story list, definition of done |
| `writer-user-story` | PO, Team Lead | Hierarchical: story with AC → developer tasks with file hints and estimates |
| `writer-backlog` | PO | Groomed backlog: prioritized, sized, dependency-flagged |
| `writer-stakeholder` | PM, PO | Stakeholder update: progress, risks, decisions needed |
| `planner-sprint` | Scrum Master | Sprint plan: goal, stories, capacity, impediment section |
| `template-creator` | Team Lead, Scrum Master, PM, PO | Reusable team templates for PRs, retros, issues, meetings, decisions, incidents, and releases |
| `tracker-velocity` | Scrum Master | Sprint metrics report: velocity, completion rate, trend |
| `writer-team-agreement` | Scrum Master | Working agreements: DoD, DoR, communication norms |

**Trigger disambiguation:**

- `writer-user-story` → triggered by breaking down a story into tasks, implementation steps
- `writer-epic` → triggered by creating or defining an epic, feature grouping
- `planner-sprint` → triggered by sprint planning, capacity, sprint goal

---

### 🏛️ Architecture (2)

| Skill | Roles | Output Artifact |
| ------------------- | -------------------- | ---------------------------------------------------------------------- |
| `design-arch` | Architect | Architecture router: system design document, ADR, or C4 diagram |
| `writer-tech-radar` | Architect | Tech radar: adopt / trial / assess / hold, with rationale |

**Trigger disambiguation:**

- `design-arch` → triggered by architecture design, ADR, trade-off analysis, or C4 diagram requests
- `writer-tech-radar` → triggered by portfolio-level technology assessment, not a single system design decision

#### Multi-variant: `design-arch`

```text
design-arch/
├── SKILL.md
└── references/
    ├── system-design.md # Components, interactions, constraints, trade-offs
    ├── adr.md           # Context, options, decision, consequences
    └── c4.md            # Context, Container, Component, and Code diagrams
```

---

### 🗄️ Database (4)

| Skill | Roles | Output Artifact |
| ---------------------- | ------------- | ------------------------------------------------------------------------- |
| `codegen-database` | DBA, Backend, Data Eng | Database code router: schema, OLTP SQL, analytics SQL, and migration scripts |
| `report-db-health` | DBA | DB health report: slow queries, bloat, index usage, replication lag |
| `strategy-backup` | DBA | Backup strategy: schedule, retention, restore SLAs, tooling |

**Trigger disambiguation:**

- `codegen-database` → produces executable SQL, DDL, schema definitions, migration scripts, or dialect-specific database code
- `report-db-health` → analyzes an existing database state and produces findings
- `strategy-backup` → defines backup/recovery policy, not SQL code

#### Multi-variant: `codegen-database`

```text
codegen-database/
├── SKILL.md          # Detects artifact type and dialect from context or asks once
└── references/
    ├── schema-design.md  # Normalized schema design, relationships, constraints, indexes
    ├── migration.md      # Up/down migrations, idempotency, validation, rollback safety
    ├── common.md         # Dialect-neutral query and DDL patterns
    ├── postgres.md       # JSONB, CTEs, EXPLAIN ANALYZE, pg-specific types
    ├── mysql.md          # Engine differences, EXPLAIN, charset considerations
    ├── mssql.md          # T-SQL, execution plans, TempDB patterns
    ├── sqlite.md         # Type affinity, limitations, WITHOUT ROWID
    ├── oracle.md         # PL/SQL, hints, dual table, sequences
    ├── bigquery.md       # ARRAY/STRUCT, partitioning, INFORMATION_SCHEMA
    ├── snowflake.md      # Variant type, clustering, time travel
    ├── clickhouse.md     # MergeTree, materialized views, sparse indexes
    └── cockroachdb.md    # Distributed SQL, geo-partitioning, follower reads
```

---

### 💻 Code Generation (10)

| Skill | Roles | Output Artifact |
| ------------------------- | ---------------------- | ---------------------------------------------------------------- |
| `codegen-frontend` | Frontend Dev | Frontend code: components, pages, state management |
| `codegen-backend` | Backend Dev | Backend code: routes, services, middleware, tests |
| `codegen-database` | DBA, Backend, Data Eng | Database code: schema, queries, DDL, migrations, analytics SQL |
| `codegen-mobile` | Mobile Dev | Mobile code: screens, navigation, platform-specific patterns |
| `design-api` | Backend Dev | API contract: OpenAPI/AsyncAPI spec, endpoints, schemas |
| `strategy-api-versioning` | Backend Dev, Architect | API versioning strategy + deprecation guide + migration notes |
| `patterns-auth` | Backend Dev | Auth implementation: JWT, OAuth2, session, RBAC patterns |
| `patterns-graphql` | Backend Dev | GraphQL: schema, resolvers, N+1 prevention, pagination |
| `patterns-realtime` | Backend Dev | Real-time: WebSocket, SSE, polling strategy selection |
| `strategy-feature-flag` | Team Lead, Backend | Feature flag strategy: rollout plan, flag lifecycle, kill switch |

**Trigger disambiguation:**

- `design-api` → contract-first, produces OpenAPI spec before any code is written
- `writer-tech-docs` (api-docs variant) → reference documentation for an existing API

#### Multi-variant: `codegen-frontend`

```text
codegen-frontend/
├── SKILL.md                    # Detects language/runtime first, then framework and capability refs
└── references/
    ├── javascript.md           # Language-level JS frontend guidance
    ├── typescript.md           # Types, strictness, generics, module boundaries
    ├── html.md                 # Semantic markup, templates, metadata, progressive enhancement
    ├── css.md                  # Design system: tokens, layout, responsive styling
    ├── css-tailwind.md         # Utility-first styling, tokens, variants, responsive states
    ├── css-bootstrap.md        # Bootstrap components, grid, utilities, theming
    ├── css-component-libraries.md # MUI, Chakra, Mantine, Ant Design, Radix, shadcn/ui
    ├── javascript-react.md     # Hooks, component composition, React Query
    ├── javascript-react-nextjs.md  # App Router, server actions, metadata API, RSC
    ├── javascript-react-remix.md   # Loaders, actions, nested routes
    ├── javascript-vue.md       # Composition API, Pinia, Vue Router
    ├── javascript-vue-nuxt.md  # Auto-imports, composables, Nitro, SSR
    ├── javascript-angular.md   # Services, RxJS, NgModules, signals
    ├── javascript-svelte.md    # Stores, reactive declarations, actions
    ├── javascript-svelte-sveltekit.md
    ├── javascript-astro.md     # Islands, content collections, SSG/SSR
    ├── javascript-solidjs.md   # Signals, createStore, SolidStart
    ├── accessibility.md        # WCAG, keyboard UX, focus, semantics, screen readers
    ├── internationalization.md # Locale routing, ICU messages, formatting, RTL
    ├── forms.md                # Validation, errors, dirty state, complex inputs
    ├── state.md                # Client/server state, caching, stores, optimistic UX
    ├── performance.md          # Bundle size, rendering, Core Web Vitals
    ├── pwa.md                  # Service workers, manifest, installability, offline UX
    └── visualization.md        # Charts, dashboards, data density, interaction
```

#### Multi-variant: `codegen-backend`

```text
codegen-backend/
├── SKILL.md          # Detects language first, then optionally one framework
└── references/
    ├── python.md     # Language-level Python backend guidance
    ├── python-fastapi.md
    ├── python-django.md
    ├── nodejs.md     # Language-level Node.js/TypeScript backend guidance
    ├── nodejs-express.md
    ├── nodejs-fastify.md
    ├── nodejs-nestjs.md
    ├── go.md         # Language-level Go backend guidance
    ├── go-gin.md
    ├── go-chi.md
    ├── go-echo.md
    ├── java.md       # Language-level Java backend guidance
    ├── java-spring-boot.md
    ├── java-quarkus.md
    ├── ruby.md       # Rails conventions, ActiveRecord, gems, RSpec
    ├── rust.md       # Cargo, ownership, Axum, error handling with anyhow
    ├── csharp.md     # .NET minimal APIs, EF Core, LINQ, async/await
    ├── php.md        # Laravel, Eloquent, Artisan, Pest
    ├── kotlin.md     # Spring Boot / Ktor, coroutines, data classes
    └── elixir.md     # Phoenix, Ecto, OTP, pattern matching
```

#### Multi-variant: `codegen-mobile`

```text
codegen-mobile/
├── SKILL.md          # Detects platform from file extension or project structure
└── references/
    ├── swift.md          # SwiftUI, Combine, Swift concurrency, SPM
    ├── kotlin-android.md # Jetpack Compose, Coroutines, Hilt, Room
    ├── react-native.md   # Expo, navigation, NativeWind, MMKV
    └── flutter.md        # Widgets, Riverpod, go_router, freezed
```

---

### 🎨 UI/UX (2)

| Skill | Roles | Output Artifact |
| ----------------- | ---------------- | ------------------------------------------------------------------- |
| `diagram-ux-flow` | UX Designer | User flow / journey map in structured Mermaid or text format |
| `audit-a11y` | Frontend Dev, UX | Accessibility audit: WCAG violations, severity, fix recommendations |

---

### 🧪 Testing (3)

| Skill | Roles | Output Artifact |
| ---------------------- | ------- | ---------------------------------------------------------------- |
| `codegen-test` | AQA | Test suites and test framework setup with fixtures, scripts, benchmark harnesses, config, and CI integration |
| `writer-test-strategy` | AQA, QA | Test strategy: scope, types, coverage targets, tooling decisions |
| `audit-test-flaky` | AQA | Flaky test report: root cause analysis, fix recommendations |

#### Multi-variant: `codegen-test`

```text
codegen-test/
├── SKILL.md
├── scripts/
│   ├── validate_evals.py      # Validate eval route coverage and JSON shape
│   ├── scaffold_ai_eval.py    # Create starter AI output/tool-use/perf eval folders
│   └── summarize_ai_perf.py   # Summarize AI benchmark results.jsonl files
└── references/
    ├── e2e.md    # Playwright, Cypress, Selenium patterns
    ├── api.md    # Supertest, Jest-extended, Postman/Newman
    ├── perf.md   # k6, JMeter, Locust scripts
    ├── framework-setup.md # Test runner config, folder structure, fixtures, CI wiring
    ├── ai-output.md   # LLM output quality, RAG, structured output, prompt regression evals
    ├── ai-tool-use.md # Agent tool-call trace, argument, sequencing, and recovery evals
    └── ai-perf.md     # AI latency, token, cost, throughput, and quality-per-dollar benchmarks
```

**Trigger disambiguation:**

- `ai-output.md` → LLM answer quality, structured output validity, RAG grounding, citation checks, prompt regression suites
- `ai-tool-use.md` → agent tool selection, argument correctness, call sequencing, recovery from tool errors, stop conditions
- `ai-perf.md` → latency, first-token time, token usage, cost per successful task, retry rate, throughput, quality-per-dollar
- `audit-security` → AI safety, prompt injection, jailbreak, data exfiltration, malicious tool-use, or policy-boundary testing
- `perf.md` → non-AI application load, stress, soak, spike, and throughput scripts
- `writer-test-strategy` → planning document for test scope, risk, levels, tools, and coverage targets

---

### 🚀 DevOps / SRE (4)

| Skill | Roles | Output Artifact |
| --------------------- | ----------- | ------------------------------------------------------------ |
| `setup-infra` | DevOps, Data Eng | Ops setup router: IaC, CI/CD, ETL, observability config |
| `planner-capacity` | DevOps, SRE | Capacity plan: traffic and storage projections, sizing |
| `writer-slo` | SRE | SLO definition: SLI, target, error budget, alerting policy |
| `writer-alert-rules` | SRE | Alert rules: conditions, severity, routing, runbook links |

#### Multi-variant: `setup-infra`

```text
setup-infra/
├── SKILL.md
└── references/
    ├── iac.md            # Terraform/Pulumi modules for target cloud
    ├── cicd.md           # GitHub Actions, GitLab CI, Jenkins
    ├── etl.md            # dbt, Airflow, Glue patterns
    └── observability.md  # Metrics, logs, traces, dashboards
```

#### Multi-variant: `planner-capacity`

```text
planner-capacity/
├── SKILL.md
└── references/
    ├── db.md      # Storage, IOPS, connection pool sizing
    └── infra.md   # Compute, memory, scaling thresholds
```

---

### 🏗️ Platform (2)

| Skill | Roles | Output Artifact |
| ------------------------ | ------------ | ---------------------------------------------------------------------- |
| `setup-monorepo` | Platform Eng | Monorepo setup: tooling config (Nx/Turborepo), workspace structure |
| `setup-developer-portal` | Platform Eng | Developer portal: service catalog, internal docs structure, onboarding |

---

### 🔐 Security (4)

| Skill | Roles | Output Artifact |
| ------------------- | --------------- | ------------------------------------------------------------------------ |
| `audit-security` | Security Eng | Security router: OWASP review, secrets exposure audit, or STRIDE threat model |
| `writer-compliance` | Security, Legal | Compliance doc: GDPR/SOC2/HIPAA controls, evidence checklist |
| `report-cve` | Security Eng | CVE triage report: affected versions, severity (CVSS), remediation steps |

#### Multi-variant: `audit-security`

```text
audit-security/
├── SKILL.md
└── references/
    ├── owasp.md       # OWASP-aligned application security review
    ├── secrets.md     # Exposed credentials, rotation plan, vault migration
    └── threat-model.md# STRIDE analysis, attack surface, mitigations
```

---

### 📊 Data & ML (6)

| Skill | Roles | Output Artifact |
| ---------------------- | ---------- | ---------------------------------------------------------------------- |
| `model-dbt` | Data Eng | dbt model: SQL + schema.yml + tests + documentation |
| `writer-lineage` | Data Eng | Data lineage doc: source → transformation → consumer map |
| `writer-ml-experiment` | ML Eng | ML experiment: hypothesis, setup, metrics, results, model card section |
| `writer-prompt` | ML, AI Eng | Prompt engineering: system prompt, few-shot examples, eval criteria |
| `setup-rag` | AI Eng | RAG pipeline: chunking strategy, embedding, retrieval, reranking |
| `setup-eval-harness` | ML Eng | Eval harness: metrics, dataset, scoring rubric, benchmark runner |

---

### 📝 Documentation (1)

| Skill | Roles | Output Artifact |
| ------------------ | -------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `writer-tech-docs` | Tech Writer, Backend, SRE, Release Mgr | Technical documentation: README, API docs, runbooks, changelog, release notes, scoped by variant |

**Trigger disambiguation:**

- `writer-tech-docs` → any technical documentation request. The router dispatches to the correct variant.
- `design-api` → contract-first spec before implementation (not docs for an existing API)

#### Multi-variant: `writer-tech-docs`

```text
writer-tech-docs/
├── SKILL.md          # Detects variant from keywords, file patterns, or user mention
└── references/
    ├── readme.md         # README: overview, install, usage, contributing
    ├── api-docs.md       # API reference docs for existing endpoints
    ├── runbook-routine.md# Standard operational procedures
    ├── runbook-oncall.md # Emergency response, alert triage
    ├── changelog.md      # Changelog: grouped by type, linked to PRs
    └── release-notes.md  # User-facing release notes: what's new, what's fixed, upgrade notes
```

---

### 👥 Team & Leadership (5)

| Skill | Roles | Output Artifact |
| ----------------------- | -------------- | ----------------------------------------------------------------------- |
| `review-code` | Team Lead | Code review findings: correctness, regression, security, performance, test gaps |
| `writer-postmortem` | Team Lead, SRE | Postmortem: timeline, root cause, impact, action items |
| `template-creator` | Team Lead | Reusable team templates, including PR templates with context, testing, risk, and screenshot sections |
| `report-team-health` | Team Lead | Team health report: delivery metrics, morale signals, risks |
| `writer-mentorship` | Team Lead | Mentorship guide: growth areas, resources, milestones, feedback cadence |

#### Multi-variant: `review-code`

```text
review-code/
├── SKILL.md
└── references/
    └── checklist.md # Code review checklist by concern area: correctness, tests, security, performance, maintainability
```

#### Multi-variant: `template-creator`

```text
template-creator/
├── SKILL.md
└── references/
    ├── pr.md       # Pull/merge request templates
    ├── retro.md    # Retrospective templates
    ├── issue.md    # Issue/ticket templates
    ├── meeting.md  # Meeting agenda and notes templates
    ├── decision.md # Decision log / lightweight ADR templates
    ├── incident.md # Incident response and postmortem intake templates
    └── release.md  # Release checklist and notes templates
```

---

### 📦 Release Management (2)

| Skill | Roles | Output Artifact |
| ----------------------------- | ----------------------- | ----------------------------------------------------------------------- |
| `checklist-release` | Release Manager | Release checklist: pre/during/post deployment steps, rollback criteria |
| `strategy-dependency-upgrade` | Release Manager, DevOps | Dependency upgrade strategy: audit, upgrade path, PR checklist, testing |

---

## Build Process (per skill)

Each skill is built using the `skill-creator` skill in this sequence:

1. **Draft** `SKILL.md` with frontmatter, instructions, output template
2. **Write** `evals/evals.json` with ≥2 test cases
3. **Run** test cases via `skill-creator` eval loop
4. **Review** outputs qualitatively; grade assertions quantitatively
5. **Iterate** until >80% assertion pass rate and user satisfied
6. **Optimize** description for triggering accuracy
7. **Package** via `scripts/package_skill` → `.skill` file

## Multi-Variant Router Pattern

For `audit-security`, `codegen-frontend`, `codegen-backend`, `codegen-database`, `codegen-mobile`, `codegen-test`, `design-arch`, `writer-spec`, `setup-infra`, `template-creator`, `writer-tech-docs`, `planner-capacity`:

The `SKILL.md` must:

1. Detect the target variant from context (file extensions, imports, `package.json`, explicit mention)
2. Load the correct `references/<variant>.md`
3. Only ask the user to specify if detection is genuinely ambiguous
4. Avoid loading multiple references unless the skill declares bounded secondary references, such as `codegen-backend` loading one language reference plus at most one framework reference, or `codegen-frontend` loading language/runtime, framework, styling, and capability references required by the task

```markdown
## Variant Detection

Check in this order:

1. File extensions in context (.tsx → React, .vue → Vue, .py → Python)
2. Import statements or package names
3. Explicit user mention
4. If still ambiguous: ask once with short options list
```

## Trigger Collision Prevention

Skills with overlapping domains must have explicit disambiguation in their descriptions. High-risk pairs and their resolution:

| Pair | Disambiguation Rule |
| --------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `writer-prd` vs `writer-spec` | PRD = business goals; spec = system behavior or technical detail |
| `design-api` vs `writer-tech-docs` (api-docs) | design-api = contract first (no code yet); writer-tech-docs api-docs variant = existing API |
| `design-arch` variants | system-design = broad prose design; adr = one decision; c4 = diagram output |
| `codegen-database` variants | OLTP dialect refs for app databases; analytics refs for warehouse/distributed SQL; migration ref for schema change scripts |
| `writer-user-story` vs `writer-epic` | user-story = single story → tasks; epic = feature grouping |
| `codegen-test` vs `writer-test-strategy` | codegen-test = test code/config; writer-test-strategy = planning document |
| `review-code` vs `audit-security` | review-code = change/diff review; audit-security = dedicated security audit/model |
| `template-creator` vs `writer-*` | template-creator = reusable blank template; writer-* = filled-in artifact |

## Totals

| Category | Count |
| ------------------------------------------- | ----- |
| Total skills | 55 |
| Multi-variant router skills | 12 |
| Total framework/language/dialect references | 50+ |
| Prefix types | 15 |
