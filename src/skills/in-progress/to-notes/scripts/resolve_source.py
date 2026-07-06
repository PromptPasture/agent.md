#!/usr/bin/env python3
"""
to-notes skill helper — resolve a video URL, local video/audio file, or
transcript/text file down to plain transcript text.

Usage:
    python3 scripts/resolve_source.py <url-or-path>

Prints:
    LANGUAGE: <code-or-unknown>
    ---
    <plain transcript text>
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

VIDEO_AUDIO_EXTS = {
    ".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v",
    ".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac",
}
TRANSCRIPT_EXTS = {".vtt", ".srt", ".txt", ".md"}

_TIMESTAMP_RE = re.compile(r"\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[.,]\d{3}")
_CUE_NUM_RE = re.compile(r"^\d+$")
_INLINE_TAG_RE = re.compile(r"<[^>]+>")
_LANG_SUFFIX_RE = re.compile(r"\.([a-zA-Z]{2}(?:-[A-Za-z0-9]+)?)$")


def _is_url(s: str) -> bool:
    return urlparse(s).scheme in ("http", "https")


def _ensure_ytdlp() -> None:
    if shutil.which("yt-dlp"):
        return
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "yt-dlp", "--break-system-packages", "-q"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if not shutil.which("yt-dlp"):
        raise RuntimeError("yt-dlp could not be installed; install it manually and retry")


def _parse_lang_section(output: str, marker: str) -> list:
    idx = output.find(marker)
    if idx == -1:
        return []
    langs = []
    for line in output[idx:].splitlines()[1:]:
        line = line.strip()
        if not line or line.startswith("Language formats"):
            continue
        if line.startswith("["):
            break
        langs.append(line.split()[0])
    return langs


def _download_subtitle(url: str, lang: str, auto: bool, workdir: Path) -> Path:
    flag = "--write-auto-subs" if auto else "--write-subs"
    outtmpl = str(workdir / "%(id)s.%(ext)s")
    cmd = [
        "yt-dlp", "--skip-download", flag,
        "--sub-langs", lang, "--convert-subs", "vtt",
        "-o", outtmpl, url,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    matches = list(workdir.glob(f"*.{lang}.vtt")) or list(workdir.glob("*.vtt"))
    if not matches:
        raise RuntimeError(f"yt-dlp reported {lang} captions but wrote no .vtt file")
    return matches[0]


def _fetch_transcript_from_url(url: str):
    _ensure_ytdlp()
    result = subprocess.run(
        ["yt-dlp", "--skip-download", "--list-subs", url],
        capture_output=True, text=True,
    )
    manual_langs = _parse_lang_section(result.stdout, "Available subtitles for")
    auto_langs = _parse_lang_section(result.stdout, "Available automatic captions for")

    if manual_langs:
        lang, auto = ("en" if "en" in manual_langs else manual_langs[0]), False
    elif auto_langs:
        lang, auto = ("en" if "en" in auto_langs else auto_langs[0]), True
    else:
        raise RuntimeError("no manual or automatic captions are available for this video")

    with tempfile.TemporaryDirectory() as tmp:
        vtt_path = _download_subtitle(url, lang, auto, Path(tmp))
        text = vtt_path.read_text(encoding="utf-8", errors="replace")
    return lang, _strip_vtt_or_srt(text)


def _find_sibling_transcript(path: Path):
    for ext in (".vtt", ".srt", ".txt"):
        exact = path.with_suffix(ext)
        if exact.exists():
            return exact
        lang_coded = sorted(path.parent.glob(f"{path.stem}.*{ext}"))
        if lang_coded:
            return lang_coded[0]
    return None


def _detect_lang_from_filename(path: Path) -> str:
    match = _LANG_SUFFIX_RE.search(path.stem)
    return match.group(1) if match else "unknown"


def _strip_vtt_or_srt(text: str) -> str:
    lines_out = []
    prev = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        upper = line.upper()
        if upper.startswith(("WEBVTT", "NOTE", "KIND:", "LANGUAGE:")):
            continue
        if _TIMESTAMP_RE.search(line) or _CUE_NUM_RE.match(line):
            continue
        line = _INLINE_TAG_RE.sub("", line).strip()
        if line and line != prev:
            lines_out.append(line)
            prev = line
    return "\n".join(lines_out)


def _read_transcript_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in (".vtt", ".srt"):
        return _strip_vtt_or_srt(text)
    return text.strip()


def resolve(arg: str):
    if _is_url(arg):
        return _fetch_transcript_from_url(arg)

    path = Path(arg)
    if not path.exists():
        raise RuntimeError(f"not a URL and no such file: {arg}")

    suffix = path.suffix.lower()
    if suffix in VIDEO_AUDIO_EXTS:
        sibling = _find_sibling_transcript(path)
        if sibling is None:
            raise RuntimeError(
                f"no sibling .vtt/.srt/.txt transcript found next to {path.name}; "
                "this skill does not transcribe audio/video"
            )
        return _detect_lang_from_filename(sibling), _read_transcript_file(sibling)

    if suffix in TRANSCRIPT_EXTS:
        return _detect_lang_from_filename(path), _read_transcript_file(path)

    raise RuntimeError(f"unsupported file type: {suffix or '(none)'}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/resolve_source.py <url-or-path>")

    try:
        lang, text = resolve(sys.argv[1])
    except RuntimeError as e:
        sys.exit(f"Error: {e}")
    except subprocess.CalledProcessError as e:
        sys.exit(f"Error: yt-dlp failed: {e}")

    if not text.strip():
        sys.exit("Error: resolved transcript is empty")

    print(f"LANGUAGE: {lang}")
    print("---")
    print(text)


if __name__ == "__main__":
    main()
