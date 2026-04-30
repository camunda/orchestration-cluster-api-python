"""Shared validation for spec-derived identifiers interpolated into generated Python source.

All post-generation hooks that embed spec-controlled strings into Python code
MUST validate them through these helpers before interpolation.

This module prevents CWE-94 (Code Injection) by ensuring that spec-controlled
values cannot escape their syntactic context in generated Python source.
"""

from __future__ import annotations

import keyword
import math
import re

# Use \Z (not $) to anchor at end-of-string.  $ allows a trailing \n
# which would bypass the check and enable newline injection.
_IDENTIFIER_RE = re.compile(r"\A[A-Za-z_][A-Za-z0-9_]*\Z")


def safe_py_identifier(value: object, context: str = "") -> str:
    """Validate that *value* is a safe Python identifier.

    Raises ``ValueError`` if the value contains characters that could
    escape an f-string interpolation context (newlines, quotes, etc.)
    or is a Python keyword.
    """
    ctx = f" ({context})" if context else ""
    if not isinstance(value, str) or not _IDENTIFIER_RE.match(value):
        raise ValueError(
            f"Spec-controlled value is not a safe Python identifier{ctx}: {value!r}"
        )
    if keyword.iskeyword(value):
        raise ValueError(
            f"Spec-controlled value is a Python keyword{ctx}: {value!r}"
        )
    return value


def safe_py_identifiers(values: list[str], context: str = "") -> list[str]:
    """Validate a list of values as safe Python identifiers."""
    return [safe_py_identifier(v, context) for v in values]


def safe_docstring(value: str | None) -> str:
    """Sanitise a spec-derived string for interpolation inside triple-quoted docstrings.

    Handles two escape vectors:
    1. Embedded ``\"\"\"`` sequences that would terminate the docstring boundary.
    2. Trailing backslashes that would escape the closing ``\"\"\"``, leaving
       the docstring unterminated and potentially consuming subsequent code.
    """
    if value is None:
        return ""
    # Replace triple-quote sequences that would terminate the docstring
    result = value.replace('"""', "'''")
    # An odd number of trailing backslashes would escape the first " of the
    # closing """, leaving the docstring unterminated.  Double the last
    # backslash to make the count even.
    stripped = result.rstrip("\\")
    trailing = len(result) - len(stripped)
    if trailing % 2 == 1:
        result += "\\"
    return result


def safe_version_string(value: object, context: str = "") -> str:
    """Validate that *value* is a safe version string (digits, dots, hyphens, alphanums).

    Used for deprecatedInVersion and similar spec-metadata values that are
    interpolated into comments and docstrings.
    """
    ctx = f" ({context})" if context else ""
    # Use \Z (not $) to prevent trailing-newline bypass
    if not isinstance(value, str) or not re.match(
        r"\A[A-Za-z0-9._\-]+\Z", value
    ):
        raise ValueError(
            f"Spec-controlled value is not a safe version string{ctx}: {value!r}"
        )
    return value


def safe_numeric_value(value: object, context: str = "") -> int | float:
    """Validate that *value* is a numeric type safe for direct interpolation.

    Rejects strings and other types that could inject code when interpolated
    into generated Python source via f-strings like ``f"if value < {minimum}:"``.
    """
    ctx = f" ({context})" if context else ""
    if isinstance(value, bool):
        raise ValueError(
            f"Spec-controlled value is boolean, expected numeric{ctx}: {value!r}"
        )
    if isinstance(value, (int, float)):
        if not math.isfinite(value):
            raise ValueError(
                f"Spec-controlled value is non-finite, expected finite numeric{ctx}: {value!r}"
            )
        return value
    raise ValueError(
        f"Spec-controlled value is not numeric{ctx}: {value!r}"
    )


def safe_dotted_import_path(value: object, context: str = "") -> str:
    """Validate that *value* is a safe dotted Python import path.

    Each segment between dots must be a valid Python identifier.
    Leading dots (relative imports) are permitted.
    """
    ctx = f" ({context})" if context else ""
    if not isinstance(value, str):
        raise ValueError(
            f"Spec-controlled value is not a string{ctx}: {value!r}"
        )
    # Strip leading dots (relative import prefix)
    stripped = value.lstrip(".")
    if not stripped:
        raise ValueError(
            f"Spec-controlled import path has no module segments{ctx}: {value!r}"
        )
    for segment in stripped.split("."):
        safe_py_identifier(segment, context)
    return value
