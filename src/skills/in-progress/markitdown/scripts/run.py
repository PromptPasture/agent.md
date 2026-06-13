#!/usr/bin/env python3
"""
markitdown skill helper — read or convert supported files to Markdown.

Usage:
    python3 scripts/run.py --read <path>
    python3 scripts/run.py --convert <path> --out <dest>
"""

import argparse
import subprocess
import sys
from pathlib import Path

TRUNCATION_LIMIT = 50_000
TRUNCATION_MSG = "\n\n[truncated — content exceeds 50 000 characters]"


def _install() -> None:
    """Install markitdown with extras covering all six supported formats.

    epub needs no extra (built-in); the others each have a named extra.
    """
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "markitdown[docx,pdf,pptx,xlsx,outlook]",
            "--break-system-packages",
            "-q",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _do_convert(path: str):
    from markitdown import MarkItDown

    # No llm_client — images render as alt text only, no API calls.
    return MarkItDown().convert(path)


def _is_missing_dependency(exc: Exception) -> bool:
    """Return True when *exc* signals an absent optional dependency.

    MissingDependencyException is wrapped inside FileConversionException by
    markitdown, so we inspect the string representation of the outer exception
    rather than the inner type directly.
    """
    return type(exc).__name__ == "MissingDependencyException" or (
        type(exc).__name__ == "FileConversionException"
        and "MissingDependency" in str(exc)
    )


def convert_file(path: str):
    """Convert *path* to Markdown, auto-installing markitdown if needed."""
    try:
        return _do_convert(path)
    except ImportError:
        _install()
        return _do_convert(path)
    except Exception as e:
        if _is_missing_dependency(e):
            _install()
            return _do_convert(path)
        raise


def resolve_output_path(dest: str) -> Path:
    """Return *dest* as a Path, incrementing a numeric suffix on collision."""
    path = Path(dest)
    if not path.exists():
        return path
    parent, stem, suffix = path.parent, path.stem, path.suffix
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


def cmd_read(path: str) -> None:
    try:
        result = convert_file(path)
    except FileNotFoundError:
        sys.exit(f"Error: file not found: {path}")
    except Exception as e:
        if type(e).__name__ == "UnsupportedFormatException":
            sys.exit(f"Error: unsupported format: {path}")
        sys.exit(f"Error: conversion failed: {e}")

    text = result.text_content or ""
    if len(text) > TRUNCATION_LIMIT:
        text = text[:TRUNCATION_LIMIT] + TRUNCATION_MSG
    print(text)


def cmd_convert(path: str, out: str) -> None:
    try:
        result = convert_file(path)
    except FileNotFoundError:
        sys.exit(f"Error: file not found: {path}")
    except Exception as e:
        if type(e).__name__ == "UnsupportedFormatException":
            sys.exit(f"Error: unsupported format: {path}")
        sys.exit(f"Error: conversion failed: {e}")

    text = result.text_content or ""
    out_path = resolve_output_path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    print(f"Saved: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert supported files to Markdown using markitdown."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--read", metavar="PATH", help="Convert and print to stdout.")
    group.add_argument("--convert", metavar="PATH", help="Convert and write to --out.")
    parser.add_argument(
        "--out", metavar="DEST", help="Output path (required with --convert)."
    )
    args = parser.parse_args()

    if args.read:
        cmd_read(args.read)
    else:
        if not args.out:
            sys.exit("Error: --out is required with --convert")
        cmd_convert(args.convert, args.out)


if __name__ == "__main__":
    main()
