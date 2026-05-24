# Skill Authoring

Use this reference when creating a new skill or revising an existing `SKILL.md`.

## Capture Intent

Extract what the user already provided before asking questions. Identify what the skill enables the calling agent to do, when it should trigger, what output it should produce, and whether test cases should be created. Put the trigger scope in frontmatter `description`, not in a body `Scope` section.

Ask at most one focused question when a missing answer would materially change the skill.

---

## Research and Interview

Ask about edge cases, input formats, output formats, success criteria, dependencies, and example files. For existing skills, inspect the current folder before editing. Check bundled scripts, references, assets, and evals so you preserve local conventions.

Ground the draft in real source material when available: prior task traces, existing docs, runbooks, review comments, issue history, example files, or failed eval outputs. Prefer concrete project facts and corrections over generic best practices. Fall back to general domain knowledge only when no better source exists.

---

## Write `SKILL.md`

Required frontmatter fields are `name` and `description`. Optional top-level fields are `license`, `tags`, and `metadata`. Put `author`, `version`, `source`, `catalog`, `category`, and `references` inside `metadata`. Keep the complete frontmatter under 100 tokens. The description is the primary trigger signal, so write it as action plus activation cues: name the task the skill performs, the contexts that should trigger it, representative user phrases, and exclusions only when they prevent likely misfires.

Use these metadata fields:

| Field | Meaning |
| --- | --- |
| `name` | A unique identifier for the skill. |
| `description` | A concise explanation of the skill's purpose and when to use it. |
| `license` | The name of the license, such as `MIT` or `Apache-2.0`. |
| `tags` | A list of searchable keywords for discovery and filtering. |
| `metadata` | A nested mapping for arbitrary key-value pairs. |

Common nested metadata fields:

| Field | Meaning |
| --- | --- |
| `metadata.author` | The creator's name or GitHub profile URL. |
| `metadata.version` | Semantic versioning string, such as `1.2.0`. |
| `metadata.source` | Repository or canonical source reference, such as `github.com/org/repo`. |
| `metadata.catalog` | Optional catalog grouping string. |
| `metadata.category` | Optional domain category string in lowercase kebab-case, such as `development`, `documentation`, or `project-management`. |
| `metadata.references` | Optional list of local skill or rule names this skill explicitly uses or routes to. |

Use `metadata.references` when this skill actually uses another local skill or rule as part of its workflow. Include a referenced item when the body tells the agent to use, apply, delegate to, run, or route follow-up work to that skill/rule. Do not include skills that appear only as adjacent alternatives, near misses, exclusions, boundaries, or examples of work this skill should not handle.

---

## Write `SKILL.md` Body

Keep the Markdown body under 500 lines. The default body shape is a `#` title, one short purpose sentence, a standalone `---`, then `## Workflow`, `## Output`, `## Boundaries`, and `## Verification`. Add `## Error Paths` when failures need explicit handling. Use specialized sections such as `## Route the Work`, `## Source Handling`, or `## Bundled Resources` only when they replace or extend the default flow. Move deep detail into `references/` and point to it clearly. Do not use a body `Scope` section to describe when the skill should be called; that belongs in `description` per the Agent Skills spec.

Start the body with the section that helps the activated agent act: usually `## Workflow`, `## Source Handling`, or `## Route the Work`. Put `## Boundaries` after the main workflow or output guidance so the file opens with execution, not limits. Place boundaries first only when safety or destructive behavior must be checked before any action.

Apply the house Markdown style while writing, not as a later cleanup pass:

- **Section delimiters**: place a standalone `---` between `##` sections in `SKILL.md`. Keep the YAML frontmatter delimiters unchanged, and do not add an extra delimiter immediately after the frontmatter or before the `#` title.
- **Intro purpose**: after the `#` title, write one short sentence that states what the skill does, then place `---` before the first `##` section.
- **Scan anchors**: use bold labels inside steps or bullets when they make distinct actions, fields, or rules easier to scan. Do not require a bold principle sentence after each `##` heading.
- **Template exceptions**: do not force bold labels into schemas, command examples, literal output templates, or checklist items where they would make the example less accurate.

After editing, run `create-skill/scripts/quick_validate.py <target-skill-directory>` when this skill's scripts are available. Treat style failures as authoring bugs, not optional polish.

Prefer deterministic helper scripts for repetitive validation, grading, packaging, report generation, or other mechanical checks that would otherwise be reimplemented by hand.

For router skills with `references/*.md`, create `evals/evals.json` before validation is considered complete. Each eval must include a `reference` field that points to the routed reference, and every non-schema reference must have 8-10 evals. This keeps the router honest instead of giving it one polite smoke test and hoping for the best.

---

## Write References

Use `references/*.md` for details that would bloat `SKILL.md`: variant workflows, platform notes, review checklists, schemas, long examples, eval guidance, or compatibility instructions.

Each reference should start with a `#` title and one short purpose sentence. Use task-specific `##` sections instead of forcing the `SKILL.md` default body shape. Put standalone `---` delimiters between `##` sections in long references. Start with the most actionable section for that reference, not background or boundaries.

Use bold scan anchors inside steps or bullets when they make distinct actions, fields, or rules easier to scan. Do not add bold principle sentences after `##` headings just for style compliance. Schema references, command examples, literal templates, and field lists may use their natural formatting instead.

Keep references loaded by clear conditions from `SKILL.md`. Do not create placeholder references, and do not use references as a dumping ground for detail that no workflow loads.

---

## Length Budgets

Follow these budgets for every `SKILL.md`:

- **Metadata/frontmatter**: no more than 100 tokens
- **Main instruction body**: no more than 500 lines

If a skill exceeds either budget, shorten trigger metadata first, then move detailed procedures, examples, platform notes, and variant-specific guidance into `references/`. Router skills are the preferred shape for broad domains: keep the main file focused on routing and shared rules, then load only the relevant reference.

Use this shape when helpful:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── evals/
```

Do not create placeholder directories. Add a folder only when it contains useful files.

---

## Progressive Disclosure

Use three levels: metadata loaded by the runtime, main body loaded when the skill triggers, and bundled resources loaded only when needed.

Router skills should classify the request, choose the relevant reference, read only that reference, and act.

---

## Compatibility

Write core instructions so they work in any agent runtime. Put runtime-specific notes under a short compatibility section or in `references/agent-compatibility.md`.

Avoid relying on one agent's tool names, slash commands, event stream, or UI unless the skill is explicitly for that agent.

---

## Writing Style

Use imperative instructions. Explain why constraints matter instead of stacking brittle all-caps rules. Include a `### Example` subsection under the relevant `##` section only when it clarifies behavior, boundaries, or output shape. Write examples and eval prompts so reviewers can see the situation, task, expected action, and result criteria. Keep examples short and move large examples into references.

Use bold scan anchors where they help another agent skim distinct actions, fields, or rules before reading details. Do not add bold principle sentences after `##` headings just for style compliance.

Use standalone `---` delimiters between `##` sections so long skill files segment cleanly in model context.

For code-generation skills and bundled helper scripts, keep responsibilities clear, interfaces small, and dependencies explicit without adding unnecessary layers.

Skills must not contain malware, hidden exfiltration behavior, credential capture, or instructions that would surprise the user relative to the skill description.
