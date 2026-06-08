# Write Skill Catalogs

## Outcome

Split the current `write-*` skills out of the broad `software-engineering`
catalog into catalogs named consistently with the existing `productivity` and
`utility` catalogs.

## Catalogs

### `product`

Contains artifacts that define product intent, planned behavior, requirements,
and delivery work:

- `write-prd`
- `write-spec`
- `write-user-story`

`write-spec` belongs here because its primary purpose is to define what will be
built and the requirements that delivery must satisfy.

### `documentation`

Contains artifacts that explain, operate, or communicate an existing system:

- `write-tech-docs`

This includes READMEs, API references, runbooks, changelogs, and release notes.

## Boundary

Classify a writing skill by the purpose of its output:

- Use `product` when the artifact defines intended product behavior or delivery.
- Use `documentation` when the artifact explains, operates, or communicates an
  existing system.
- Keep general work artifacts such as 1:1 notes and meeting notes in
  `productivity`; they are not software-delivery artifacts.

## Naming Rationale

`product` and `documentation` are broad capability nouns. They match the
existing catalog style established by `productivity` and `utility` better than
role-oriented names such as `product-management`, `technical-writing`, or
`workplace-writing`.

## Scope

The subsequent implementation should:

- Move the four existing `write-*` skill folders to their agreed catalogs.
- Update each moved skill's `metadata.catalog`.
- Update the skill library index and affected relative links.
- Update project-scoped catalog documentation when it describes the old
  placement.

Renaming the skills or changing their runtime behavior is out of scope.

## Verification

- Every moved skill is indexed under exactly one catalog.
- Folder placement and `metadata.catalog` agree.
- Repository references no longer describe the four skills as members of the
  `software-engineering` catalog.
- Existing relative references within each skill still resolve.
