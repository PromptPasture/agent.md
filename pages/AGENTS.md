# AGENTS.md

## Scope

- These instructions apply to every file and directory under `pages/`.
- These instructions govern writing and maintaining the published GitHub Pages site only.

## Published Content

- You MUST treat `pages/` as public, reader-facing content.
- Public pages MUST explain the subject directly and MUST NOT include internal bookkeeping, implementation logs, task status, agent scratch notes, or repository-only instructions.
- You MUST NOT publish content from `docs/`, `.agents/memory/`, or other internal sources unless the user explicitly requests its publication and the content is rewritten for a public audience.
- Public claims, examples, commands, paths, and version references MUST be accurate and consistent with the repository.
- Pages MUST be concise, scannable, and organized around reader goals.
- You MUST preserve the site's established terminology, voice, and document structure unless the request requires changing them.

## Page Structure

- Every new public page MUST have one clear purpose and a descriptive top-level heading.
- Headings MUST form a logical hierarchy and links MUST use descriptive reader-facing labels.
- New pages MUST be reachable from `index.md` or another appropriate published navigation page unless the user explicitly requests an unlisted page.
- You MUST use relative links for files within `pages/` and MUST account for the configured GitHub Pages `baseurl`.
- You MUST update affected navigation and cross-references when a published page is added, renamed, moved, or removed.
- You MUST NOT duplicate substantial content across pages; they MUST link to the canonical published explanation instead.

## Jekyll Compatibility

- Changes to Markdown, `_config.yml`, includes, layouts, and assets MUST remain compatible with the repository's GitHub Pages and Jekyll workflow.
- You MUST preserve valid YAML syntax and existing configuration values unless changing them is required by the request.
- Markdown intended for publication MUST render without relying on repository viewers, local-only paths, or unsupported extensions.
- You MUST NOT introduce plugins, themes, build dependencies, or custom rendering behavior unless the user explicitly requests them.

## Assets

- Published assets MUST live under `pages/assets/` unless the existing site structure requires another location.
- Asset filenames MUST be lowercase and hyphenated.
- Images MUST have meaningful alternative text when embedded in a page.
- You MUST use the smallest suitable asset and MUST NOT add unused, duplicate, private, or source-only files to the published site.
- Asset references MUST resolve correctly from the page where they are used and from the configured published base path.

## Completion Gate

- Before completing a Pages change, you MUST self-review changed public content for internal information, unsupported claims, placeholders, broken navigation, inconsistent terminology, and unnecessary content.
- You MUST fix issues found during self-review before presenting the result.
- You MUST run the repository's Markdown validation for changed Markdown files when available.
- When page structure, configuration, includes, or assets change, you MUST verify the rendered site path and relevant page output using the established GitHub Pages or Jekyll workflow when available.
