---
topic: Skill Catalog
method: comparative analysis
date: "2026-06-11"
related:
  - src/skills/README.md
  - src/skills/
  - .plugins/.codex-plugin/plugin.json
  - https://github.com/mattpocock/skills
---

# Brainstorm - Skill Catalog

## Goal

Make the stable Prompt Pasture skill library easy to consume as a downloadable
archive and as complete Codex and Claude plugins, without introducing an npm
package or duplicating skill content.

## Context

The repository already separates stable skills into catalog folders under
`src/skills/` and unfinished skills under `src/skills/in-progress/`. It also
maintains `src/skills/README.md` as the stable library index and has an existing
Codex plugin manifest.

The distribution model should preserve that separation. Stable skill folders
remain the source of truth; unfinished skills are not published.

## Agenda

1. Choose the distribution formats.
2. Define which skills are included.
3. Decide how plugins discover stable skills.
4. Define the tagged release archive.
5. Decide how release artifacts are produced and published.

## Ideas Considered

### npm or `npx` installer

- **Description:** Publish a command-line installer through npm.
- **Benefits:** Familiar installation command and potential interactive
  selection.
- **Trade-offs:** Adds package maintenance, registry publishing, and installer
  behavior that are unnecessary for a repository of portable skill folders.
- **Outcome:** Excluded.

### Generated self-contained plugin copies

- **Description:** Copy stable skills into separate generated Codex and Claude
  plugin directories.
- **Benefits:** Each plugin is independently packaged and avoids runtime path
  assumptions.
- **Trade-offs:** Duplicates skill content in the repository and creates drift
  risk between canonical and generated copies.
- **Outcome:** Rejected in favor of explicit references to canonical paths.

### Explicit plugin manifests over canonical skills

- **Description:** Codex and Claude plugin manifests explicitly list every
  stable skill while the skill content remains under `src/skills/`.
- **Benefits:** Avoids duplicated content, makes inclusion explicit to each
  runtime, and supports nested catalog folders.
- **Trade-offs:** Manifest entries must remain synchronized with the stable
  skill folders.
- **Outcome:** Selected. All stable skills are included automatically; there is
  no per-skill publication flag.

### Catalog-specific ZIP archives

- **Description:** Produce one archive for each stable catalog.
- **Benefits:** Smaller downloads and selective installation.
- **Trade-offs:** More release assets and more decisions for users who want the
  complete library.
- **Outcome:** Rejected in favor of one complete archive.

### Complete tagged ZIP archive

- **Description:** Produce one archive containing all stable catalogs and
  skills.
- **Benefits:** Simple release surface and one portable download.
- **Trade-offs:** Users who need only one catalog must select folders after
  extraction.
- **Outcome:** Selected.

### Standalone generation script

- **Description:** Add a repository script that generates manifests and release
  archives.
- **Benefits:** Reusable locally and in CI.
- **Trade-offs:** Adds another maintained interface when distribution is
  intended to occur through GitHub.
- **Outcome:** Rejected. GitHub Actions will own release assembly and
  publication.

## Outcomes

### Summary

Prompt Pasture will distribute its complete stable skill library through Codex
and Claude plugins on `main` and through one ZIP archive on each tagged GitHub
Release. Stable folders remain canonical, and no npm package or copied plugin
payload is introduced.

### Decisions

- Include every stable skill under `src/skills/<catalog>/<skill>/`.
- Exclude `src/skills/in-progress/` from plugins and release archives.
- Keep stable skill content in its canonical repository location.
- Use explicit stable skill paths in both Codex and Claude plugin manifests.
- Make the complete Codex and Claude plugins usable from `main`.
- Use GitHub Actions rather than an npm command or standalone generator script
  for release artifact creation.
- Trigger archive creation from repository tags.
- Automatically create the corresponding GitHub Release.
- Attach one archive named `prompt-pasture-agent-<tag>.zip` to the release.
- Preserve the tag exactly, including a leading `v` when present.
- Preserve catalog structure inside the archive as
  `skills/<catalog>/<skill>/...`.
- Copy `src/skills/README.md` to `skills/README.md` in the archive.
- Keep ZIP instructions generic; do not add runtime-specific installation
  guidance to the archive.

### Open Questions

- The implementation plan must confirm the exact Codex and Claude manifest
  schemas and installation paths supported by their current runtimes.
- The implementation plan must define how CI detects plugin manifest drift when
  stable skills are added, moved, or removed.
- The implementation plan must define tag validation and the behavior when a
  release with the same tag already exists.

## Next Steps

1. Review and approve these brainstorm notes.
2. Create an implementation plan covering plugin manifests, validation, the
   tag-triggered release workflow, and archive verification.
