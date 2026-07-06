# AGENTS.md

## Scope

- These instructions govern authoring rules, commands, skills, and related assets only.

## Shared Requirements

- Every artifact MUST have one clear purpose and MUST contain only instructions or resources needed for that purpose.
- You MUST preserve the established artifact format, terminology, and metadata fields unless the requested change requires otherwise.
- You MUST NOT add speculative behavior, unused extension points, duplicate guidance, or runtime-specific requirements to tool-agnostic artifacts.
- References, relative paths, examples, commands, and named tools MUST resolve to real repository content or clearly identified external dependencies.
- When materially changing a command, rule, or skill, you MUST increment `metadata.version` using semantic versioning.
- Metadata MUST use the repository's compact format, including `author`, `version`, `source`, and `category` when those fields apply.

## Rules

- Rules MUST address one concern and use the narrowest practical scope.
- Rules MUST state observable behavior using direct, unambiguous instructions.
- Rules MUST NOT embed multi-step workflows that belong in a skill or user-invoked operations that belong in a command.

## Commands

- Commands MUST represent an explicit user-invoked operation with a clear terminal outcome.
- Commands MUST define required inputs, ordered actions, confirmation boundaries, and failure behavior when applicable.
- Commands MUST NOT silently broaden their operation beyond the user's invocation.
- Commands that cause external, destructive, or irreversible effects MUST require explicit confirmation before the effect occurs.

## Skills

- You MUST follow `pages/BUILDING_SKILLS.md` when writing or modifying any file under `src/skills/`.
- Skill folder names MUST use the repository's verb-first naming convention: `<verb>[-<subject>]` or a concise verb.
- Every skill folder MUST contain `SKILL.md` and MUST NOT contain a `README.md`.
- `SKILL.md` frontmatter `name` MUST match the skill folder name.
- Skills invoked only by name MUST set `disable-model-invocation: true`; skills the agent or another skill must reach autonomously MUST keep a model-facing description.
- Skill descriptions MUST include BOTH: what the skill does AND when to use it.
- Skill body sections MUST be selected from the structures and workflow patterns in `pages/BUILDING_SKILLS.md` according to the skill's actual needs. You MUST NOT impose a fixed section template or add a section that has no distinct purpose.
- Each skill step MUST end on a checkable completion criterion.
- You MUST keep `SKILL.md` focused on the core workflow and place optional detail in `references/`, deterministic helpers in `scripts/`, and reusable output resources in `assets/`.
- Referenced skill resources MUST exist at the stated relative paths.
- When a skill is added, removed, renamed, or moved, you MUST update `src/skills/README.md` and affected relative links in the same change.

## Completion Gate

- Before completing an artifact change, you MUST self-review changed files for conflicting instructions, ambiguous triggers, missing failure paths, stale references, unsupported claims, unnecessary content, and metadata errors.
- You MUST fix issues found during self-review before presenting the result.
- You MUST run Markdown validation for changed Markdown files and any established artifact-specific validation available in the repository.
