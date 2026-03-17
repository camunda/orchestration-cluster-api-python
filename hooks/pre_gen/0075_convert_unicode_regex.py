"""Convert Unicode property escapes in regex patterns to Python-compatible syntax.

The upstream OpenAPI spec may use ECMAScript-style Unicode property escapes
such as ``\\p{L}`` (Unicode letter) and ``\\p{N}`` (Unicode digit).  Python's
built-in ``re`` module does not support these.  This hook rewrites them to
equivalent character-class ranges that work with ``re``.

Runs early in the pre-gen pipeline so all downstream hooks and the generator
see Python-compatible patterns.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Mapping from Unicode property escape to Python re-compatible equivalent.
# These replacements are used inside character classes (i.e. inside [...]).
_UNICODE_PROPERTY_MAP: dict[str, str] = {
    r"\p{L}": r"\w",  # Close enough: \w = [a-zA-Z0-9_] with re.UNICODE includes letters
    r"\p{N}": r"0-9",  # Unicode digits — ASCII subset is sufficient for IDs
}

# For standalone (outside character class) occurrences
_STANDALONE_MAP: dict[str, str] = {
    r"\p{L}": r"\w",
    r"\p{N}": r"\d",
}


def _convert_pattern(pattern: str) -> str:
    """Replace Unicode property escapes in a regex pattern string."""
    result = pattern
    for esc, replacement in _UNICODE_PROPERTY_MAP.items():
        result = result.replace(esc, replacement)
    return result


def _walk_and_convert(node: Any, converted: list[str]) -> None:
    """Recursively walk a parsed spec and convert any 'pattern' values."""
    if isinstance(node, dict):
        if "pattern" in node and isinstance(node["pattern"], str):
            original = node["pattern"]
            updated = _convert_pattern(original)
            if updated != original:
                node["pattern"] = updated
                converted.append(f"  {original!r} -> {updated!r}")
        for value in node.values():  # type: ignore[reportUnknownVariableType]
            _walk_and_convert(value, converted)
    elif isinstance(node, list):
        for item in node:  # type: ignore[reportUnknownVariableType]
            _walk_and_convert(item, converted)


def run(context: dict[str, str]) -> None:
    spec_path = Path(context["bundled_spec_path"])
    if not spec_path.exists():
        print(f"Spec file not found at {spec_path}")
        return

    with open(spec_path, "r") as f:
        spec: dict[str, Any] = yaml.safe_load(f)

    converted: list[str] = []
    _walk_and_convert(spec, converted)

    if converted:
        with open(spec_path, "w") as f:
            yaml.safe_dump(spec, f, sort_keys=False, allow_unicode=True)
        print(
            f"Converted {len(converted)} Unicode regex patterns to Python-compatible syntax:"
        )
        for line in converted:
            print(line)
    else:
        print("No Unicode regex patterns found to convert.")
