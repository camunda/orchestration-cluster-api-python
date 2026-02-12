#!/usr/bin/env python3
"""Generate the configuration reference table in README.md.

Introspects ``CamundaSdkConfiguration`` (Pydantic model) at runtime to extract
field names, types, defaults, and descriptions.  The result is injected between
marker comments in README.md so the table stays in sync with the source code.

Usage::

    uv run scripts/generate_config_reference.py   # default: ./README.md
    uv run scripts/generate_config_reference.py --check  # CI: fail if out-of-date
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the runtime package is importable.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runtime"))
# Also allow importing from the generated package (not strictly needed here).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generated"))

from configuration_resolver import CamundaSdkConfiguration  # noqa: E402

BEGIN_MARKER = "<!-- BEGIN_CONFIG_REFERENCE -->"
END_MARKER = "<!-- END_CONFIG_REFERENCE -->"

# CAMUNDA_LOAD_ENVFILE is consumed by the resolver before Pydantic validation,
# so it does not appear as a model field.  We append it manually.
_EXTRA_ROWS: list[dict[str, str]] = [
    {
        "variable": "CAMUNDA_LOAD_ENVFILE",
        "default": "—",
        "description": "Load configuration from a `.env` file. Set to `true` (or a file path).",
    },
]


def _format_default(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return f"`{str(value).lower()}`"
    if isinstance(value, str):
        if not value:
            return '`""`'
        return f"`{value}`"
    return f"`{value}`"


def _build_table() -> str:
    rows: list[str] = []

    for name, field_info in CamundaSdkConfiguration.model_fields.items():
        default = _format_default(field_info.default)
        desc = field_info.description or ""
        rows.append(f"| `{name}` | {default} | {desc} |")

    for extra in _EXTRA_ROWS:
        rows.append(
            f"| `{extra['variable']}` | {extra['default']} | {extra['description']} |"
        )

    header = "| Variable | Default | Description |\n|----------|---------|-------------|"
    return header + "\n" + "\n".join(rows)


def _inject(readme_text: str, table: str) -> str:
    begin = readme_text.find(BEGIN_MARKER)
    end = readme_text.find(END_MARKER)

    if begin == -1 or end == -1:
        print(
            f"ERROR: Could not find {BEGIN_MARKER} and/or {END_MARKER} in README.md.\n"
            "Add the markers where you want the configuration reference table.",
            file=sys.stderr,
        )
        sys.exit(1)

    before = readme_text[: begin + len(BEGIN_MARKER)]
    after = readme_text[end:]

    return before + "\n\n" + table + "\n\n" + after


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--readme",
        default=str(Path(__file__).resolve().parent.parent / "README.md"),
        help="Path to README.md (default: repo root)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: exit 1 if the README would change (for CI).",
    )
    args = parser.parse_args()

    readme_path = Path(args.readme)
    old_text = readme_path.read_text(encoding="utf-8")
    table = _build_table()
    new_text = _inject(old_text, table)

    if args.check:
        if old_text != new_text:
            print(
                "ERROR: Configuration reference in README.md is out-of-date.\n"
                "Run: uv run scripts/generate_config_reference.py",
                file=sys.stderr,
            )
            sys.exit(1)
        print("OK: Configuration reference is up-to-date.")
        return

    if old_text == new_text:
        print("README.md is already up-to-date.")
        return

    readme_path.write_text(new_text, encoding="utf-8")
    print("README.md updated with configuration reference.")


if __name__ == "__main__":
    main()
