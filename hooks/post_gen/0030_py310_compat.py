"""Post-generation hook: keep generated code runnable on the SDK's Python floor (3.10).

openapi-python-client >= 0.29 requires Python 3.11 and emits 3.11-only code. Only maintainers
and CI run the generator, so its floor can move. The published SDK still supports Python 3.10
(``requires-python`` in pyproject.toml), so this hook rewrites three constructs back to the
3.10-compatible forms that 0.28 emitted:

* ``class X(StrEnum)`` (3.11+) -> ``class X(str, Enum)``.
* ``typing.Self`` (3.11+) -> a quoted reference to the enclosing class.
* ``datetime.datetime.fromisoformat(s)`` / ``datetime.date.fromisoformat(s)`` -> dateutil's
  ``isoparse(s)`` / ``isoparse(s).date()``. On 3.10, ``fromisoformat`` rejects the ``Z``
  suffix and fractional seconds that aren't 3 or 6 digits, which the gateway sends. That
  fails at runtime, and a type checker can't see it.

Unused ``datetime`` imports left behind are removed by the ``ruff check --fix`` step that
follows generation.
"""

from __future__ import annotations

import re
from pathlib import Path

_STR_ENUM_IMPORT = re.compile(r"^from enum import StrEnum$", re.MULTILINE)
_STR_ENUM_BASE = re.compile(r"^(class \w+)\(StrEnum\):", re.MULTILINE)
_CLASS_DEF = re.compile(r"^class (\w+)\b")
_SELF_IMPORT = re.compile(r"^from typing import (.*)$", re.MULTILINE)
_FROMISOFORMAT = re.compile(r"\bdatetime\.(datetime|date)\.fromisoformat\(")
_ISOPARSE_IMPORT = "from dateutil.parser import isoparse"


def _replace_str_enum(source: str) -> str:
    if "StrEnum" not in source:
        return source
    source = _STR_ENUM_IMPORT.sub("from enum import Enum", source)
    return _STR_ENUM_BASE.sub(r"\1(str, Enum):", source)


def _replace_self(source: str) -> str:
    if not re.search(r"\bSelf\b", source):
        return source

    def _drop_self(match: re.Match[str]) -> str:
        names = [n.strip() for n in match.group(1).split(",")]
        kept = [n for n in names if n != "Self"]
        return f"from typing import {', '.join(kept)}" if kept else ""

    source = _SELF_IMPORT.sub(_drop_self, source)
    out: list[str] = []
    current: str | None = None
    for line in source.splitlines(keepends=True):
        match = _CLASS_DEF.match(line)
        if match:
            current = match.group(1)
        if current is not None and re.search(r"\bSelf\b", line):
            line = re.sub(r"\bSelf\b", f'"{current}"', line)
        out.append(line)
    return "".join(out)


def _closing_paren(source: str, open_idx: int) -> int:
    depth = 0
    for i in range(open_idx, len(source)):
        if source[i] == "(":
            depth += 1
        elif source[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("unbalanced parentheses in generated source")


def _replace_fromisoformat(source: str) -> str:
    if not _FROMISOFORMAT.search(source):
        return source
    while match := _FROMISOFORMAT.search(source):
        open_idx = match.end() - 1
        close_idx = _closing_paren(source, open_idx)
        call = f"isoparse{source[open_idx : close_idx + 1]}"
        if match.group(1) == "date":
            call += ".date()"
        source = source[: match.start()] + call + source[close_idx + 1 :]
    if _ISOPARSE_IMPORT not in source:
        lines = source.splitlines(keepends=True)
        lines.insert(_isoparse_import_index(lines), _ISOPARSE_IMPORT + "\n")
        source = "".join(lines)
    return source


def _isoparse_import_index(lines: list[str]) -> int:
    """Where 0.28 placed the dateutil import: after the third-party ``attrs`` imports.

    Falls back to after the last complete top-level import statement in the module header.
    Multi-line ``from x import (...)`` statements are skipped over as a unit.
    """
    attrs_idx = [i for i, line in enumerate(lines) if line.startswith("from attrs import ")]
    if attrs_idx:
        return attrs_idx[-1] + 1
    insert_at = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(("import ", "from ")):
            if line.rstrip().endswith("("):
                while i < len(lines) and not lines[i].startswith(")"):
                    i += 1
            insert_at = i + 1
        elif line.strip() and not line.startswith("#") and insert_at:
            break
        i += 1
    return insert_at


def downlevel(source: str) -> str:
    """Apply all 3.10-compat rewrites to one module's source."""
    return _replace_fromisoformat(_replace_self(_replace_str_enum(source)))


def run(context: dict[str, str]) -> None:
    package_dir = Path(context["out_dir"]) / "camunda_orchestration_sdk"
    changed = 0
    for path in sorted(package_dir.rglob("*.py")):
        original = path.read_text(encoding="utf-8")
        updated = downlevel(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"py310 compat: rewrote {changed} module(s)")
