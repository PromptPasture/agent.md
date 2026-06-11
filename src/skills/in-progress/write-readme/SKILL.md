---
name: write-readme
description: You MUST use this to write or revise project README files. Use for repository, library, CLI, service, internal-tool, and open-source project introductions, installation, quick starts, usage, configuration, development, contribution, support, and license guidance.
license: Apache-2.0
tags:
  - writer
  - docs
  - readme
metadata:
  author: Oleg Shulyakov
  version: "1.1.0"
  source: github.com/olegshulyakov/agent.md
  catalog: documentation
  category: documentation
---

# Writing README

Write or revise a README that helps its intended audience understand, adopt, use, and contribute to the documented project or component.

## Workflow

1. **Identify the target:** Determine the README path, intended audience, and task: create, complete, correct, reorganize, or refresh.
2. **Detect the scope:** Classify the target as:
   - **Repository root:** Orient users and contributors to the whole project, including purpose, key capabilities, setup, common usage, development, and links to project-wide policies or detailed documentation.
   - **Package or module:** Document the local component's purpose, role, consumers, interfaces, setup, usage, configuration, limitations, and local development. Link to repository-wide policies instead of repeating them.

   Treat the target directory as the ownership boundary unless repository evidence shows otherwise. Do not present local behavior as repository-wide or repeat root onboarding unless local steps differ.
3. **Inspect authoritative evidence:** Read the target directory, existing README, manifests, entry points, configuration, commands, examples, tests, contribution guidance, license, and relevant repository-level documentation.
   If sources conflict, follow current implementation, tests, and configuration, and surface unresolved conflicts.
4. **Establish conventions:** Preserve the repository's language, voice, heading hierarchy, link style, terminology, badges, and documentation boundaries unless the task explicitly changes them.
5. **Select sections:** Include only sections that help the target audience complete a real task. Order them from orientation to first success, then deeper usage and project participation.
6. **Write for first success:** Provide the shortest verified path from prerequisites through installation or setup to a meaningful working result.
7. **Add deeper guidance:** Document applicable usage, configuration, architecture, development, testing, deployment, contribution, support, security, and license information without duplicating authoritative docs.
8. **Revise safely:** Preserve accurate content and stable anchors, correct stale or unsupported claims, and avoid rewriting unrelated sections.
9. **Verify the result:** Check every command, path, link, example, requirement, and cross-reference against repository evidence.

## Writing Rules

- **Lead with purpose:** Explain what the target is, who it serves, and why it matters before implementation details.
- **Optimize for scanning:** Use descriptive headings, short paragraphs, lists, tables, and focused examples where they improve retrieval.
- **Keep the quick start complete:** State prerequisites and working directory, then show commands in execution order and the expected successful result.
- **Use verified examples:** Keep names, paths, flags, environment variables, ports, versions, and output consistent with the current repository.
- **Separate required from optional:** Distinguish mandatory setup from alternatives, advanced configuration, and development-only tooling.
- **Explain configuration precisely:** Document defaults, allowed values, precedence, secrets handling, and restart or rebuild requirements when evidence supports them.
- **Respect documentation boundaries:** Summarize essential information and link to maintained API docs, runbooks, contribution guides, security policies, or design documents for detail.
- **Preserve useful anchors:** During revisions, avoid renaming headings that may be externally linked unless the change is required.
- **Use badges selectively:** Keep only accurate, maintained badges that help readers assess status, compatibility, release, or license information.
- **Avoid unsupported claims:** Do not invent compatibility, performance, stability, security, support, roadmap, installation, or deployment details.
- **Handle missing evidence:** Do not present unverified commands or examples as working. Request required values or identify missing facts; do not fabricate policies or leave placeholders in a completed README.
- **Avoid generic filler:** Omit empty overview prose, exhaustive file trees, redundant feature lists, obvious command narration, and sections with no actionable content.

## Verification

- **Scope:** The README clearly describes the correct repository or component boundary and does not overstate local behavior.
- **First success:** A qualified reader can follow prerequisites, setup, and the quick start in order and recognize successful completion.
- **Accuracy:** Commands, paths, imports, flags, environment variables, defaults, versions, examples, links, and requirements match repository evidence.
- **Content quality:** The README contains no placeholders, contradictions, unsupported claims, stale instructions, broken links, inconsistent examples, unnecessary duplication, or generic filler.
- **Change isolation:** Revisions preserve accurate content, stable anchors, and unrelated documentation.
