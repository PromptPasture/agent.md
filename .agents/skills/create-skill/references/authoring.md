# Skill Authoring

Use this reference when creating a new skill or revising an existing `SKILL.md`.

A good skill is not a long prompt. It is a compact operating procedure that tells another agent when to activate, what context to load, what steps to follow, and how to verify the result.

## Capture Intent

Use what the user already gave you. Do not interview them for information that is already in the request, the repo, examples, or existing skill folder.

Identify:

- **Capability:** what the skill enables the calling agent to do
- **Activation:** which user phrases, artifacts, or contexts should trigger it
- **Output:** what the skill should produce or change
- **Inputs:** files, prompts, external tools, or structured data it consumes
- **Verification:** whether objective evals, validators, or review loops are useful

Ask at most one focused question when the missing answer would materially change the skill. Otherwise, make a conservative assumption and keep moving.

---

## Research Before Writing

For existing skills, inspect the current folder before editing. Check `SKILL.md`, `references/`, `scripts/`, `assets/`, and `evals/` so you preserve local conventions.

Ground the draft in real source material when available:

- **Task traces:** prior runs that show how the skill is actually used.
- **Docs and runbooks:** existing durable guidance.
- **Review and issues:** comments, bugs, and decisions from prior work.
- **Eval failures:** outputs that reveal recurring misses.
- **Examples and fixtures:** files with known structure or expected results.
- **Project context:** local rules or memory.

Use concrete project facts and corrections over generic best practices. Fall back to general domain knowledge only when no better source exists.

---

## Write The Frontmatter

- **Required fields:** Use `name` and `description`. Optional top-level fields are `license`, `tags`, and `metadata`.
- **Nested metadata:** Put `author`, `version`, `source`, `catalog`, `category`, and `references` inside `metadata`.
- **Trigger signal:** The `description` is the primary trigger signal. Write it as action plus activation cues: name the task the skill performs, the contexts that should trigger it, representative user phrases, and exclusions only when they prevent likely misfires.
- **Budget:** Keep the frontmatter `description` under 100 tokens. If it grows past that budget, make it shorter.

### Metadata fields

| Field | Meaning |
| --- | --- |
| `name` | Unique skill identifier. |
| `description` | Concise purpose and activation signal. |
| `license` | License name, such as `MIT` or `Apache-2.0`. |
| `tags` | Searchable discovery and filtering keywords. |
| `metadata.author` | Creator name or GitHub profile URL. |
| `metadata.version` | Semantic versioning string, such as `1.2.0`. |
| `metadata.source` | Repository or canonical source reference. |
| `metadata.catalog` | Optional catalog grouping string. |
| `metadata.category` | Optional lowercase kebab-case category. |
| `metadata.references` | Local skills or rules this skill explicitly uses. |

Use `metadata.references` only when the body tells the agent to use, apply, delegate to, run, or route follow-up work to that skill or rule.
Do not include route-away mentions, adjacent alternatives, near misses, exclusions, boundaries, or examples of work this skill should not handle.

### Versioning

Use Semantic Versioning for agent skills:

- **Major:** breaking changes to the skill contract, such as redefining the trigger, splitting the skill, removing required workflow steps, or changing expected output formats.
- **Minor:** backward-compatible additions, such as new references, expanded trigger coverage, or optional output sections.
- **Patch:** safe reliability tweaks, such as clearer wording, typo fixes, or boundaries that prevent common mistakes.

Always bump `metadata.version` when making a material change to a skill's files.

---

## Write The Body

Keep the Markdown body under 500 lines.
If the body grows past that budget, move detailed procedures, examples, platform notes, and variant-specific guidance into `references/`.
Router skills are the preferred shape for broad domains: keep the main file focused on routing and shared rules, then load only the relevant reference.

The default shape is:

```text
# Skill Name

One short purpose sentence.

---

## Workflow
## Output
## Boundaries
## Verification
```

Add `## Error Paths` when failures need explicit handling.
Use specialized sections such as `## Route the Work`, `## Source Handling`, or `## Bundled Resources` only when they replace or extend the default flow.

Start with the section that helps the activated agent act.
Usually that is `## Workflow`, `## Source Handling`, or `## Route the Work`.
Put `## Boundaries` after the main workflow unless safety or destructive behavior must be checked before any action.

Do not use a body `## Scope` section to describe activation criteria.
Skill-call scope belongs in the frontmatter `description`.

### House Markdown style

Apply style while writing, not as a cleanup pass:

- **Section delimiters:** place standalone `---` delimiters between `##` sections in `SKILL.md`; do not add an extra delimiter after the YAML frontmatter or before the `#` title.
- **Intro purpose:** after the `#` title, write one short purpose sentence, then place `---` before the first `##` section.
- **Scan anchors:** use bold labels inside steps or bullets when they make distinct actions, fields, or rules easier to scan.
- **Template exceptions:** do not force bold labels into schemas, command examples, literal output templates, or checklist items.

### Example

Situation: the skill needs a workflow for editing existing skill folders. Task: make the instructions reusable, not tied to one edit.

Weak:

```text
## Workflow

- Analyze the files.
- Make improvements.
- Validate.
```

Strong:

```text
## Workflow

1. **Identify the target artifact:** Read the existing file before deciding whether to edit, replace, or add a reference.
2. **Preserve local conventions:** Match naming, metadata, validation scripts, and eval structure already present in the skill folder.
3. **Verify behavior:** Run the skill validator and any focused eval or schema check affected by the change.
```

The strong version tells the agent what decisions to make and what evidence to collect. The weak version is technically true and operationally soggy.

---

## Write References

- **Reference purpose:** Use `references/*.md` for details that would bloat `SKILL.md`: variant workflows, platform notes, review checklists, schemas, long examples, eval guidance, or compatibility instructions.
- **Reference shape:** Each reference should start with a `#` title and one short purpose sentence. Use task-specific `##` sections instead of forcing the `SKILL.md` default body shape. Put standalone `---` delimiters between `##` sections in long references. Start with the most actionable section for that reference, not background or boundaries.
- **Teaching format:** Write references in the format that best teaches the behavior. Use guide-style prose, concrete examples, checklists, weak/strong comparisons, and worked examples when they improve comprehension. Do not flatten references into terse operational bullets by default. Compress only repetition, stale context, or details that do not change agent behavior.
- **Reference scan anchors:** Use bold scan anchors inside steps or bullets when they make distinct actions, fields, or rules easier to scan. Schema references, command examples, literal templates, and field lists may use their natural formatting instead.
- **Load conditions:** Keep references loaded by clear conditions from `SKILL.md`. Do not create placeholder references, and do not use references as a dumping ground for detail that no workflow loads.

---

## Writing Style

- **Imperative voice:** Use imperative instructions. Explain why constraints matter instead of stacking brittle all-caps rules.
- **Examples:** Write examples and eval prompts so reviewers can see the situation, task, expected action, and result criteria. Include a `### Example` subsection under the relevant `##` section only when it clarifies behavior, boundaries, or output shape. Keep examples short and move large examples into references.
- **Scan anchors:** Use bold scan anchors where they help another agent skim distinct actions, fields, or rules before reading details.
- **Delimiters:** Use standalone `---` delimiters between `##` sections so long skill files segment cleanly in model context.
- **Code responsibilities:** For code-generation skills and bundled helper scripts, keep responsibilities clear, interfaces small, and dependencies explicit without adding unnecessary layers.

---

## Bundle Resources

Add folders only when they contain useful files.

Use this shape when helpful:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── evals/
```

Use deterministic helper scripts for repetitive validation, grading, packaging, report generation, or other mechanical checks that would otherwise be reimplemented by hand.

Move long templates, large examples, fixture files, and generated review assets out of `SKILL.md` when they would make the main body harder to scan.

---

## Add Evals

For router skills with `references/*.md`, create `evals/evals.json` before validation is considered complete.

Each eval must include a `reference` field pointing to the routed reference. Every non-schema reference must have 8-10 evals. Near-miss prompts count toward the route they are intended to test.

For objectively testable skills, include assertions, scripts, schemas, fixtures, or acceptance checks where practical. Use `references/evaluation.md` for deeper eval design guidance.

---

## Validate

After editing, run:

```bash
python <create-skill-path>/scripts/quick_validate.py <target-skill-directory>
```

Treat style failures as authoring bugs, not optional polish.

Also run focused checks for touched artifacts:

- **JSON parsing:** parser check for `evals/*.json`.
- **Script tests:** relevant unit or integration tests for bundled scripts.
- **Packaging:** packaging check when producing a distributable skill.
- **Eval reruns:** trigger or behavior evals when the description, workflow, or references changed materially.

---

## Portability And Safety

- **Portable core:** Write core instructions so they work in any agent runtime. Put runtime-specific notes under a short compatibility section or in `references/agent-compatibility.md`.
- **Runtime assumptions:** Avoid relying on one agent's tool names, slash commands, event stream, or UI unless the skill is explicitly for that agent.
- **User trust:** Skills must not contain malware, hidden exfiltration behavior, credential capture, or instructions that would surprise the user relative to the skill description.
