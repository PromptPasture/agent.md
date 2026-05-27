#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
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
    evals_path = skill_path / 'evals' / 'evals.yaml'
    references_dir = skill_path / 'references'
    yaml_key = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
    allowed_case_types = {
        'positive_trigger',
        'negative_trigger',
        'near_miss',
        'process',
        'outcome',
        'regression',
        'robustness',
    }
    allowed_kinds = {'routing', 'process', 'outcome', 'eval_quality'}
    allowed_grading = {'deterministic', 'transcript', 'artifact', 'human'}

    if not evals_path.exists():
        if references_dir.exists() and any(references_dir.glob('*.md')):
            return False, "Router skills with references must include evals/evals.yaml"
        return True, None

    try:
        data = yaml.safe_load(evals_path.read_text())
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in {evals_path}: {e}"
    if not isinstance(data, dict):
        return False, f"{evals_path}: expected a YAML mapping"
    eval_name = data.get('name')
    if not isinstance(eval_name, str) or not yaml_key.match(eval_name):
        return False, f"{evals_path}: field 'name' must be lowercase kebab-case"

    suites = data.get('suites')
    if not isinstance(suites, dict):
        return False, f"{evals_path}: missing mapping field 'suites'"

    evals = []
    for suite_name, suite in suites.items():
        if not isinstance(suite_name, str) or not yaml_key.match(suite_name):
            return False, f"{evals_path}: suite name '{suite_name}' must be lowercase kebab-case"
        if not isinstance(suite, dict):
            return False, f"{evals_path}: suite '{suite_name}' must be an object"
        cases = suite.get('cases')
        if not isinstance(cases, dict):
            return False, f"{evals_path}: suite '{suite_name}' missing mapping field 'cases'"
        for case_name, item in cases.items():
            if not isinstance(case_name, str) or not yaml_key.match(case_name):
                return False, (
                    f"{evals_path}: case name '{suite_name}.{case_name}' "
                    "must be lowercase kebab-case"
                )
            if not isinstance(item, dict):
                return False, f"{evals_path}: case '{suite_name}.{case_name}' must be an object"
            if 'reference' in item:
                return False, (
                    f"{evals_path}: case '{suite_name}.{case_name}' uses legacy "
                    "'reference'; use expect.routing.reference"
                )
            if 'expectations' in item:
                return False, (
                    f"{evals_path}: case '{suite_name}.{case_name}' uses legacy "
                    "'expectations'; use expect.assertions"
                )
            case_type = item.get('type')
            if case_type is not None and case_type not in allowed_case_types:
                return False, (
                    f"{evals_path}: case '{suite_name}.{case_name}' has invalid "
                    f"type '{case_type}'"
                )
            prompt = item.get('prompt')
            if not isinstance(prompt, str) or not prompt.strip():
                return False, f"{evals_path}: case '{suite_name}.{case_name}' requires non-empty prompt"
            files = item.get('files', [])
            if files is not None:
                if not isinstance(files, list) or not all(isinstance(path, str) for path in files):
                    return False, f"{evals_path}: case '{suite_name}.{case_name}' files must be a list of strings"
                for file_path in files:
                    if Path(file_path).is_absolute() or '..' in Path(file_path).parts:
                        return False, f"{evals_path}: fixture path '{file_path}' must stay inside the skill"
                    if not file_path.startswith('evals/files/'):
                        return False, f"{evals_path}: fixture path '{file_path}' must live under evals/files/"

            expect = item.get('expect')
            if not isinstance(expect, dict):
                return False, f"{evals_path}: case '{suite_name}.{case_name}' requires mapping field 'expect'"
            routing = expect.get('routing')
            if routing is not None:
                if not isinstance(routing, dict):
                    return False, f"{evals_path}: case '{suite_name}.{case_name}' expect.routing must be a mapping"
                if 'trigger' in routing and not isinstance(routing['trigger'], bool):
                    return False, f"{evals_path}: case '{suite_name}.{case_name}' expect.routing.trigger must be boolean"
                if 'reference' in routing and not isinstance(routing['reference'], str):
                    return False, f"{evals_path}: case '{suite_name}.{case_name}' expect.routing.reference must be a string"
                if 'evidence' in routing and routing['evidence'] != 'routing_judge':
                    return False, (
                        f"{evals_path}: case '{suite_name}.{case_name}' "
                        "expect.routing.evidence must be routing_judge"
                    )

            assertions = expect.get('assertions')
            if not isinstance(assertions, dict) or not assertions:
                return False, f"{evals_path}: case '{suite_name}.{case_name}' requires expect.assertions"
            for assertion_name, assertion in assertions.items():
                if not isinstance(assertion_name, str) or not yaml_key.match(assertion_name):
                    return False, (
                        f"{evals_path}: assertion name '{suite_name}.{case_name}.{assertion_name}' "
                        "must be lowercase kebab-case"
                    )
                if not isinstance(assertion, dict):
                    return False, (
                        f"{evals_path}: assertion '{suite_name}.{case_name}.{assertion_name}' "
                        "must be a mapping"
                    )
                if assertion.get('kind') not in allowed_kinds:
                    return False, (
                        f"{evals_path}: assertion '{suite_name}.{case_name}.{assertion_name}' "
                        "requires kind routing, process, outcome, or eval_quality"
                    )
                if assertion.get('grading') not in allowed_grading:
                    return False, (
                        f"{evals_path}: assertion '{suite_name}.{case_name}.{assertion_name}' "
                        "requires grading deterministic, transcript, artifact, or human"
                    )
                failure_mode = assertion.get('failure_mode')
                if not isinstance(failure_mode, str) or not failure_mode.strip():
                    return False, (
                        f"{evals_path}: assertion '{suite_name}.{case_name}.{assertion_name}' "
                        "requires non-empty failure_mode"
                    )
            evals.append((f"{suite_name}.{case_name}", item))

    if len(evals) < 2:
        return False, f"{evals_path}: expected at least 2 evals, found {len(evals)}"

    if not references_dir.exists():
        return True, None

    all_reference_files = [
        f"references/{path.name}"
        for path in sorted(references_dir.glob('*.md'))
    ]
    reference_files = [
        reference
        for reference in all_reference_files
        if reference != 'references/schemas.md'
    ]
    if not reference_files:
        return True, None

    seen_references = set()
    unknown_references = {}

    for case_id, item in evals:
        routing = item.get('expect', {}).get('routing')
        if not isinstance(routing, dict):
            continue
        reference = routing.get('reference')
        if not reference:
            continue
        if reference not in all_reference_files:
            unknown_references[case_id] = reference
            continue
        seen_references.add(reference)

    if unknown_references:
        examples = ', '.join(
            f"{eval_id} -> {reference}"
            for eval_id, reference in list(unknown_references.items())[:5]
        )
        return False, f"{evals_path}: evals reference unknown files: {examples}"

    missing_coverage = sorted(set(reference_files) - seen_references)
    if missing_coverage:
        return False, (
            f"{evals_path}: router references missing routed eval coverage: "
            f"{', '.join(missing_coverage)}"
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
        print("Usage: python validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
