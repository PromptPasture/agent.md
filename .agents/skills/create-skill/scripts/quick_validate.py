#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
import json
import yaml
from pathlib import Path


def iter_markdown_lines(path):
    """Yield non-code-fence Markdown lines with 1-based line numbers."""
    in_fence = False
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield line_number, line


def validate_markdown_style(skill_path):
    """Validate the preferred skill Markdown scan-anchor style."""
    markdown_files = [skill_path / 'SKILL.md']
    references_dir = skill_path / 'references'
    if references_dir.exists():
        markdown_files.extend(
            path for path in sorted(references_dir.glob('*.md'))
            if path.name != 'schemas.md'
        )

    for path in markdown_files:
        lines = path.read_text().splitlines()
        in_fence = False
        for index, line in enumerate(lines):
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            if line.startswith("## "):
                line_number = index + 1
                if index + 1 >= len(lines) or lines[index + 1] != "":
                    return False, f"{path}:{line_number}: expected blank line after heading"
                if index + 2 < len(lines):
                    candidate = lines[index + 2]
                    if (
                        candidate.startswith("**")
                        and candidate.endswith("**")
                        and candidate.count("**") == 2
                    ):
                        return False, (
                            f"{path}:{line_number + 2}: remove redundant bold "
                            "principle sentence after heading"
                        )

        for line_number, line in iter_markdown_lines(path):
            if line.startswith("- ") and not line.startswith("- **") and not line.startswith("- [ ]"):
                return False, f"{path}:{line_number}: expected bold label for rule bullet"

    return True, None


def validate_eval_coverage(skill_path):
    """Validate eval coverage for focused and router skills."""
    evals_path = skill_path / 'evals' / 'evals.json'
    references_dir = skill_path / 'references'

    if not evals_path.exists():
        if references_dir.exists() and any(references_dir.glob('*.md')):
            return False, "Router skills with references must include evals/evals.json"
        return True, None

    try:
        data = json.loads(evals_path.read_text())
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in {evals_path}: {e}"

    evals = data.get('evals')
    if not isinstance(evals, list):
        return False, f"{evals_path}: missing list field 'evals'"

    if len(evals) < 2:
        return False, f"{evals_path}: expected at least 2 evals, found {len(evals)}"

    if not references_dir.exists():
        return True, None

    reference_files = [
        f"references/{path.name}"
        for path in sorted(references_dir.glob('*.md'))
        if path.name != 'schemas.md'
    ]
    if not reference_files:
        return True, None

    counts = {reference: 0 for reference in reference_files}
    missing_reference = []
    unknown_references = {}

    for index, item in enumerate(evals, start=1):
        if not isinstance(item, dict):
            return False, f"{evals_path}: eval {index} must be an object"
        reference = item.get('reference')
        if not reference:
            missing_reference.append(str(item.get('id', index)))
            continue
        if reference not in counts:
            unknown_references[str(item.get('id', index))] = reference
            continue
        counts[reference] += 1

    if missing_reference:
        return False, (
            f"{evals_path}: router evals must include a 'reference' field; "
            f"missing on eval id(s): {', '.join(missing_reference[:10])}"
        )

    if unknown_references:
        examples = ', '.join(
            f"{eval_id} -> {reference}"
            for eval_id, reference in list(unknown_references.items())[:5]
        )
        return False, f"{evals_path}: evals reference unknown files: {examples}"

    bad_counts = {
        reference: count
        for reference, count in counts.items()
        if count < 8 or count > 10
    }
    if bad_counts:
        summary = ', '.join(
            f"{reference}={count}"
            for reference, count in bad_counts.items()
        )
        return False, (
            f"{evals_path}: router references must each have 8-10 evals; "
            f"found {summary}"
        )

    return True, None


def validate_metadata_references(skill_path, references):
    """Validate project-local metadata.references entries."""
    if not isinstance(references, list):
        return False, f"Metadata references must be a list, got {type(references).__name__}"

    skills_root = skill_path.parent
    repo_root = skills_root.parent.parent
    boundary_terms = re.compile(
        r'\b(route away|adjacent skills?|near[- ]miss|exclusions?|do not|don\'t|instead|rather than)\b',
        re.IGNORECASE,
    )

    for reference in references:
        if not isinstance(reference, str):
            return False, f"Metadata references must contain only strings, got {type(reference).__name__}"
        if not re.match(r'^[a-z0-9-]+$', reference):
            return False, f"Metadata reference '{reference}' should be kebab-case"

        skill_reference = skills_root / reference / 'SKILL.md'
        rule_reference = repo_root / 'rules' / f'{reference}.md'
        if not skill_reference.exists() and not rule_reference.exists():
            return False, (
                f"Metadata reference '{reference}' must match a local skill "
                f"or rule name"
            )

        for line_number, line in iter_markdown_lines(skill_path / 'SKILL.md'):
            if f"`{reference}`" in line and boundary_terms.search(line):
                return False, (
                    f"Metadata reference '{reference}' appears to be a route-away "
                    f"or boundary mention at line {line_number}"
                )

    return True, None


def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {
        'name',
        'description',
        'license',
        'tags',
        'metadata',
    }

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Validate license field if present (optional)
    license_name = frontmatter.get('license')
    if license_name is not None and not isinstance(license_name, str):
        return False, f"License must be a string, got {type(license_name).__name__}"

    # Validate tags field if present (optional)
    tags = frontmatter.get('tags')
    if tags is not None:
        if not isinstance(tags, list):
            return False, f"Tags must be a list, got {type(tags).__name__}"
        for tag in tags:
            if not isinstance(tag, str):
                return False, f"Tags must contain only strings, got {type(tag).__name__}"

    # Validate metadata field if present (optional)
    metadata = frontmatter.get('metadata')
    if metadata is not None and not isinstance(metadata, dict):
        return False, f"Metadata must be a mapping, got {type(metadata).__name__}"
    if isinstance(metadata, dict):
        author = metadata.get('author')
        if author is not None and not isinstance(author, str):
            return False, f"Metadata author must be a string, got {type(author).__name__}"
        version = metadata.get('version')
        if version is not None:
            if not isinstance(version, str):
                return False, f"Metadata version must be a string, got {type(version).__name__}"
            if not re.match(r'^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$', version):
                return False, f"Metadata version '{version}' must be a semantic versioning string like 1.2.0"
        source = metadata.get('source')
        if source is not None:
            if not isinstance(source, str):
                return False, f"Metadata source must be a string, got {type(source).__name__}"
            if not re.match(r'^(?:https?://)?[A-Za-z0-9.-]+(?:/[A-Za-z0-9._~!$&\'()*+,;=:@%-]+)*/?$', source):
                return False, "Metadata source must be a repository or source reference like github.com/org/repo"
        category = metadata.get('category')
        if category is not None:
            if not isinstance(category, str):
                return False, f"Metadata category must be a string, got {type(category).__name__}"
            if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', category):
                return False, "Metadata category must use lowercase kebab-case"
        references = metadata.get('references')
        if references is not None:
            valid_references, references_message = validate_metadata_references(skill_path, references)
            if not valid_references:
                return False, references_message

    valid_style, style_message = validate_markdown_style(skill_path)
    if not valid_style:
        return False, style_message

    valid_evals, eval_message = validate_eval_coverage(skill_path)
    if not valid_evals:
        return False, eval_message

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
