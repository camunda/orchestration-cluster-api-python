#!/usr/bin/env python3
"""Ratcheting guard against new type-safety escape hatches.

Scans the hand-written ``runtime/`` and ``hooks/`` trees for the three escape
hatches that silently erode the maxed-out ``ty`` strictness (see #203):

* ``# type: ignore`` comments
* ``cast(...)`` calls
* the ``Any`` type

The current per-category counts are compared against a committed baseline
(``scripts/escape-hatch-baseline.json``). CI fails if any category *grows*,
which forces every new escape hatch through explicit human review instead of
relying on a reviewer to notice it. Removing escape hatches is encouraged: when
a count drops, the guard prints a reminder to run ``--update`` so the baseline
tightens and the removed hatch can't be silently reintroduced.

Usage::

    python scripts/check_escape_hatches.py            # verify (CI)
    python scripts/check_escape_hatches.py --update    # rewrite the baseline
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = REPO_ROOT / "scripts" / "escape-hatch-baseline.json"

# Directories scanned for escape hatches. Both are hand-written (not generated),
# so every occurrence is a deliberate authoring choice worth tracking.
SCAN_DIRS = ("runtime", "hooks")

# Each pattern is matched per line. Word boundaries keep ``cast`` and ``Any``
# from matching identifiers like ``broadcast`` or ``AnyOf``.
PATTERNS: dict[str, re.Pattern[str]] = {
    "type-ignore": re.compile(r"#\s*type:\s*ignore"),
    "cast": re.compile(r"(?<![A-Za-z0-9_.])cast\s*\("),
    "any": re.compile(r"(?<![A-Za-z0-9_])Any(?![A-Za-z0-9_])"),
}


def _iter_python_files() -> list[Path]:
    files: list[Path] = []
    for directory in SCAN_DIRS:
        files.extend(sorted((REPO_ROOT / directory).rglob("*.py")))
    return files


def scan() -> tuple[dict[str, int], dict[str, list[str]]]:
    """Return per-category counts and the matching ``path:line`` locations."""
    counts: dict[str, int] = {category: 0 for category in PATTERNS}
    locations: dict[str, list[str]] = {category: [] for category in PATTERNS}

    for path in _iter_python_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        with path.open(encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, start=1):
                for category, pattern in PATTERNS.items():
                    hits = len(pattern.findall(line))
                    if hits:
                        counts[category] += hits
                        locations[category].append(f"{rel}:{lineno}: {line.strip()}")

    return counts, locations


def load_baseline() -> dict[str, int]:
    if not BASELINE_PATH.exists():
        raise SystemExit(
            f"Baseline file not found: {BASELINE_PATH.relative_to(REPO_ROOT)}. "
            "Run with --update to create it."
        )
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    counts = data.get("counts")
    if not isinstance(counts, dict) or set(counts) != set(PATTERNS):
        raise SystemExit(
            f"Malformed baseline in {BASELINE_PATH.name}: expected a 'counts' object "
            f"with keys {sorted(PATTERNS)}."
        )
    return {category: int(counts[category]) for category in PATTERNS}


def write_baseline(counts: dict[str, int]) -> None:
    payload = {
        "_comment": (
            "Ratchet baseline for scripts/check_escape_hatches.py. Counts of "
            "escape hatches in runtime/ and hooks/. Lower is better; the guard "
            "fails if any count grows. Regenerate with --update."
        ),
        "counts": {category: counts[category] for category in PATTERNS},
    }
    BASELINE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update",
        action="store_true",
        help="Rewrite the baseline to the current counts instead of verifying.",
    )
    args = parser.parse_args()

    counts, locations = scan()

    if args.update:
        write_baseline(counts)
        print(f"Updated baseline: {counts}")
        return 0

    baseline = load_baseline()

    grew = {c: (counts[c], baseline[c]) for c in PATTERNS if counts[c] > baseline[c]}
    shrank = {c: (counts[c], baseline[c]) for c in PATTERNS if counts[c] < baseline[c]}

    if grew:
        print("New type-safety escape hatches detected in runtime/ and hooks/:\n")
        for category, (current, allowed) in grew.items():
            print(f"  {category}: {current} (baseline {allowed}, +{current - allowed})")
            for location in locations[category]:
                print(f"      {location}")
        print(
            "\nRemove the new escape hatch, or — if it is genuinely unavoidable "
            "(e.g. httpx interop) — justify it in review and run "
            "`python scripts/check_escape_hatches.py --update` to raise the baseline."
        )
        return 1

    if shrank:
        print("Escape-hatch counts dropped below the baseline (nice!):")
        for category, (current, allowed) in shrank.items():
            print(f"  {category}: {current} (baseline {allowed}, -{allowed - current})")
        print(
            "Run `python scripts/check_escape_hatches.py --update` to tighten the "
            "baseline so the removed hatch can't be silently reintroduced."
        )
        return 1

    print(f"Escape-hatch guard OK — no growth over baseline: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
