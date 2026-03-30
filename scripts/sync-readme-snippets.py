#!/usr/bin/env python3
"""
Synchronize code snippets in README.md from compilable example files.

Replaces code blocks between snippet markers in README.md with the
corresponding region-tagged code from examples/*.py.

Usage:
    python3 scripts/sync-readme-snippets.py          # update README.md in-place
    python3 scripts/sync-readme-snippets.py --check   # CI mode: exit 1 if out of sync

Region tags in .py files use ``# region RegionName`` ... ``# endregion RegionName``.
Markers in README.md use the descriptive format::

    <!-- snippet-source: examples/readme.py | regions: RegionName -->

Legacy markers (``<!-- snippet:RegionName -->``) are auto-migrated.

Composite regions: ``regions: A+B`` concatenates multiple regions
separated by blank lines.
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
EXAMPLES_DIR = REPO_ROOT / "examples"


# ---------------------------------------------------------------------------
# Region extraction
# ---------------------------------------------------------------------------

def parse_region_tags(py_path: Path) -> dict[str, str]:
    """Extract region-tagged code blocks from a .py file."""
    text = py_path.read_text(encoding="utf-8")
    regions: dict[str, str] = {}
    current_tag: str | None = None
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        m_open = re.match(r"^#\s*region\s+(\w+)\s*$", stripped)
        m_close = re.match(r"^#\s*endregion\s+(\w+)\s*$", stripped)
        if m_open:
            current_tag = m_open.group(1)
            lines = []
        elif m_close and current_tag == m_close.group(1):
            regions[current_tag] = textwrap.dedent("\n".join(lines))
            current_tag = None
            lines = []
        elif current_tag is not None:
            lines.append(line)
    return regions


def load_all_regions() -> tuple[dict[str, str], dict[str, str]]:
    """Load regions from all .py files under examples/.

    Returns (region_content, region_source) where region_source maps
    region name -> relative source file path.
    """
    all_regions: dict[str, str] = {}
    region_source: dict[str, str] = {}
    for py_file in sorted(EXAMPLES_DIR.glob("*.py")):
        rel = py_file.relative_to(REPO_ROOT).as_posix()
        for name, content in parse_region_tags(py_file).items():
            all_regions[name] = content
            region_source[name] = rel
    return all_regions, region_source


# ---------------------------------------------------------------------------
# README rewriting
# ---------------------------------------------------------------------------

# New descriptive format:
#   <!-- snippet-source: examples/readme.py | regions: RegionName -->
_NEW_MARKER = re.compile(
    r"^<!--\s*snippet-source:\s*\S+\s*\|\s*regions:\s*([\w+]+)\s*-->$"
)
# Legacy format (for migration):
#   <!-- snippet:RegionName -->
_OLD_MARKER = re.compile(r"^<!--\s*snippet:([\w+]+)\s*-->$")

# Exempt marker: <!-- snippet-exempt: reason -->
_EXEMPT_MARKER = re.compile(r"^<!--\s*snippet-exempt:.*-->$")


def _match_marker(line: str) -> re.Match[str] | None:
    """Match either new or legacy snippet marker."""
    return _NEW_MARKER.match(line) or _OLD_MARKER.match(line)


def _build_marker(region_name: str, region_source: dict[str, str]) -> str:
    """Build a descriptive snippet marker line for *region_name*."""
    parts = region_name.split("+") if "+" in region_name else [region_name]
    source_file = region_source.get(parts[0], "examples/?.py")
    return f"<!-- snippet-source: {source_file} | regions: {region_name} -->"


def resolve_region(name: str, regions: dict[str, str]) -> str | None:
    """Resolve a region name, supporting ``A+B`` composite syntax."""
    if "+" not in name:
        return regions.get(name)
    parts = name.split("+")
    resolved = [regions.get(p) for p in parts]
    if any(r is None for r in resolved):
        return None
    return "\n\n".join(r for r in resolved if r)


def sync_readme(
    regions: dict[str, str],
    region_source: dict[str, str],
    *,
    check: bool = False,
) -> bool:
    """Replace snippet-marked code blocks in README.md.

    Also upgrades legacy ``<!-- snippet:X -->`` markers to the new
    ``<!-- snippet-source: file | regions: X -->`` format.

    Returns True if the file was (or would be) changed.
    """
    readme_text = README_PATH.read_text(encoding="utf-8")
    lines = readme_text.splitlines(keepends=True)

    out: list[str] = []
    i = 0
    changed = False
    missing: list[str] = []
    errors: list[str] = []
    snippet_count = 0

    while i < len(lines):
        line = lines[i].rstrip("\n")
        m = _match_marker(line.strip())

        if not m:
            out.append(lines[i])
            i += 1
            continue

        region_name = m.group(1)
        content = resolve_region(region_name, regions)

        if content is None:
            missing.append(region_name)
            out.append(lines[i])
            i += 1
            continue

        snippet_count += 1

        # Upgrade legacy marker to the new descriptive format
        new_marker = _build_marker(region_name, region_source) + "\n"
        if lines[i] != new_marker:
            changed = True
        out.append(new_marker)
        i += 1

        # Skip whitespace between marker and opening fence
        while i < len(lines) and lines[i].strip() == "":
            out.append(lines[i])
            i += 1

        # Expect opening fence
        if i >= len(lines) or not lines[i].strip().startswith("```"):
            errors.append(f"snippet:{region_name} — expected ``` after marker")
            continue

        fence_lang = lines[i].strip()  # e.g. ```python

        # Find closing fence
        close_idx = i + 1
        while close_idx < len(lines) and lines[close_idx].strip() != "```":
            close_idx += 1

        if close_idx >= len(lines):
            errors.append(f"snippet:{region_name} — no closing ``` found")
            out.append(lines[i])
            i += 1
            continue

        # Build replacement block
        new_block = fence_lang + "\n" + content + "\n```\n"
        old_block = "".join(lines[i : close_idx + 1])

        if old_block != new_block:
            changed = True

        out.append(new_block)
        i = close_idx + 1

    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)

    if missing:
        print(f"ERROR: missing regions: {', '.join(missing)}", file=sys.stderr)

    if errors or missing:
        sys.exit(1)

    new_text = "".join(out)

    if check:
        if changed:
            print("README.md is out of sync with example snippets. Run:")
            print("  python3 scripts/sync-readme-snippets.py")
        return changed

    if changed:
        README_PATH.write_text(new_text, encoding="utf-8", newline="")
        print(f"README.md updated ({snippet_count} snippets synced)")
    else:
        print("README.md is already up to date")

    return changed


# ---------------------------------------------------------------------------
# Un-injected code block detection
# ---------------------------------------------------------------------------

_CHECKED_LANGUAGES = {"python", "py"}


def detect_uninjected_code_blocks(readme_path: Path) -> list[tuple[int, str]]:
    """Find fenced code blocks in *readme_path* that use a checked language
    but are NOT preceded by a snippet marker or exempt marker.

    Returns a list of ``(line_number, fence_line)`` tuples (1-based).
    """
    text = readme_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    uninjected: list[tuple[int, str]] = []

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("```"):
            continue
        lang = stripped.removeprefix("```").strip().lower()
        if lang not in _CHECKED_LANGUAGES:
            continue
        # Look backward for a snippet marker or exempt marker (skip blank lines)
        prev = idx - 1
        while prev >= 0 and lines[prev].strip() == "":
            prev -= 1
        if prev >= 0:
            prev_stripped = lines[prev].strip()
            if _match_marker(prev_stripped) or _EXEMPT_MARKER.match(prev_stripped):
                continue
        uninjected.append((idx + 1, stripped))

    return uninjected


def main() -> None:
    check = "--check" in sys.argv
    regions, region_source = load_all_regions()
    print(f"Loaded {len(regions)} regions from examples/*.py")

    changed = sync_readme(regions, region_source, check=check)

    # Detect un-injected Python code blocks
    uninjected = detect_uninjected_code_blocks(README_PATH)
    if uninjected:
        print(
            f"\nWARNING: {len(uninjected)} Python code block(s) in README.md are NOT "
            "snippet-injected (not type-checked):",
            file=sys.stderr,
        )
        for lineno, fence in uninjected:
            print(f"  line {lineno}: {fence}", file=sys.stderr)
        if check:
            print(
                "\nAll Python code blocks must be injected from compilable examples in "
                "examples/. Add a snippet marker above each block, or move the "
                "code to examples/readme.py with region tags.",
                file=sys.stderr,
            )
            sys.exit(1)

    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
