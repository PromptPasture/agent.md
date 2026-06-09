---
status: READY
documentType: USER_STORY
phase: delivery
storyId: US-1
priority: MEDIUM
owner: Skill library maintainers
epic: MarkItDown document conversion skill
tags:
  - skills
  - documents
  - markdown
  - markitdown
related:
  - https://github.com/microsoft/markitdown
---

# US-1: Convert local documents into model-readable Markdown

## Story

**As an** agent working with a local document,\
**I want** to convert the document to Markdown through MarkItDown,\
**so that** I can reliably inspect its structured text and continue the user's original task.

## Context

The skill is named `markitdown` and uses the existing `markitdown` command-line
interface directly. It does not include wrapper scripts.

For model use, conversion output is written to a disposable temporary Markdown
file. If the same unchanged source file is needed again during the current
session, the agent reuses that conversion. Session-local reuse is an agent
workflow rule, not a persistent cache.

When the user explicitly requests converted output, the agent writes to the
requested file or emits Markdown to stdout.

Supported scope:

- PDF
- Word
- PowerPoint
- Excel
- Outlook messages
- EPUB

## Acceptance Criteria

### Scenario: Convert a local document for model use

**Given** the source is one accessible local file in a supported format\
**And** the `markitdown` command and required format dependencies are available\
**When** the agent needs the document's contents to complete a task\
**Then** it converts the source to a temporary Markdown file\
**And** reads the Markdown\
**And** continues the user's original task without requiring the user to manage
the intermediate file.

### Scenario: Reuse a conversion during the current session

**Given** the agent already converted the source during the current session\
**And** the source path, size, and modification time have not changed\
**When** the agent needs the document again\
**Then** it reuses the existing temporary Markdown file instead of converting
the source again.

### Scenario: Reconvert a changed source

**Given** the source was converted earlier in the current session\
**And** its path, size, or modification time has changed\
**When** the agent needs the document again\
**Then** it creates a new conversion before reading the content.

### Scenario: Save converted output for the user

**Given** the user requests a Markdown file at a specific local path\
**When** the source is converted successfully\
**Then** the agent invokes MarkItDown with that output path\
**And** reports the resulting file location.

### Scenario: Emit converted output to stdout

**Given** the user explicitly requests the converted Markdown in stdout\
**When** the source is converted successfully\
**Then** the agent emits MarkItDown's Markdown output without creating a
user-facing output file.

### Scenario: Reject input outside the skill scope

**Given** the input is a directory, remote URL, or more than one file\
**When** conversion is requested\
**Then** the agent does not invoke MarkItDown\
**And** explains that the skill accepts one local file\
**And** for a remote resource, explains that it must first be downloaded through
the agent's normal tools.

### Scenario: Request consent before dependency installation

**Given** the `markitdown` command or a required format dependency is unavailable\
**When** conversion cannot proceed\
**Then** the agent identifies the missing dependency\
**And** asks for permission before installing it\
**And** does not modify the environment without approval.

### Scenario: Report conversion failure

**Given** MarkItDown cannot convert an unsupported, encrypted, malformed, or
inaccessible file\
**When** the command fails\
**Then** the agent reports the relevant error concisely\
**And** does not present partial or missing output as a successful conversion\
**And** preserves the original file.

### Scenario: Run in a constrained cloud environment

**Given** the runtime can execute MarkItDown and access the uploaded file\
**But** persistent user cache storage is unavailable\
**When** the agent converts the file for model use\
**Then** it uses an available temporary location\
**And** does not require the temporary output to survive beyond the session.

## Non-Goals

- Downloading or converting remote URLs
- Converting directories or multiple files in one invocation
- Converting HTML, CSV, JSON, XML, or plain-text files for model consumption
- Persistent or cross-session caching
- Wrapper scripts around the MarkItDown CLI
- Cleaning, rewriting, summarizing, or chunking converted Markdown
- Configuring external OCR, transcription, YouTube, or Azure services
- Guaranteeing high-fidelity visual reproduction of the source document

## Developer Tasks

1. Create `src/skills/utility/markitdown/SKILL.md` with metadata and trigger
   guidance for supported local document conversion.
2. Document the model-use workflow for temporary output and session-local reuse
   based on source path, size, and modification time.
3. Document explicit user-output workflows for `-o <path>` and stdout.
4. Add input validation guidance for one local file and rejection of directories
   and URLs.
5. Add dependency detection and approval guidance that prevents automatic
   environment modification.
6. Add failure handling for inaccessible, unsupported, encrypted, and malformed
   files.
7. Add `markitdown` to the Utility Skills section of `src/skills/README.md`.
8. Validate the skill using the repository's established skill validation and
   Markdown linting workflows.

## Verification

- Confirm the skill contains no `scripts/` dependency or wrapper command.
- Confirm every supported format and non-goal matches this story.
- Confirm model-use output targets temporary storage and user-use output supports
  a requested file or stdout.
- Confirm unchanged files may be reused only within the current session.
- Confirm missing dependencies require explicit user approval before installation.
- Run repository skill validation against the new skill.
- Run Markdown linting against the changed Markdown files.
