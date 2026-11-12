"""The generated SDK must stay runnable on its declared Python floor (3.10), see issue #383.

openapi-python-client >= 0.29 requires Python 3.11 and emits 3.11-only code. Post-gen hook
``0030_py310_compat`` rewrites it back. This guards the class (3.11+ constructs in the shipped
package), not just the three that prompted it. ``fromisoformat`` is included because it's a
runtime-only break on 3.10: it rejects the gateway's ``...Z`` timestamps, and type checkers
don't see it.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIRS = [
    REPO_ROOT / "generated" / "camunda_orchestration_sdk",
    REPO_ROOT / "stubs" / "camunda_orchestration_sdk",
]

_hook_path = REPO_ROOT / "hooks" / "post_gen" / "0030_py310_compat.py"
_spec = importlib.util.spec_from_file_location("_py310_compat_hook", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

# Constructs that import or behave differently on Python 3.10.
_PY311_ONLY = {
    "enum.StrEnum": re.compile(r"\bStrEnum\b"),
    "typing.Self": re.compile(r"^\s*from typing(_extensions)? import [^\n]*\bSelf\b", re.MULTILINE),
    "Self annotation": re.compile(r"->\s*Self\b|:\s*Self\b"),
    "fromisoformat (no 'Z' on 3.10)": re.compile(r"\.fromisoformat\("),
    "typing.LiteralString/Never/assert_never/reveal_type": re.compile(
        r"^\s*from typing import [^\n]*\b(LiteralString|Never|assert_never|reveal_type)\b",
        re.MULTILINE,
    ),
    "ExceptionGroup / except*": re.compile(r"\bExceptionGroup\b|except\*"),
    "tomllib": re.compile(r"^\s*import tomllib|^\s*from tomllib", re.MULTILINE),
}


def _shipped_sources() -> list[Path]:
    files: list[Path] = []
    for directory in PACKAGE_DIRS:
        files.extend(sorted(directory.rglob("*.py")))
        files.extend(sorted(directory.rglob("*.pyi")))
    return files


def test_generated_package_has_no_py311_only_constructs() -> None:
    sources = _shipped_sources()
    assert sources, "generated package not found; run `make generate` first"
    offenders: list[str] = []
    for path in sources:
        text = path.read_text(encoding="utf-8")
        for label, pattern in _PY311_ONLY.items():
            if pattern.search(text):
                offenders.append(f"{path.relative_to(REPO_ROOT)}: {label}")
    assert not offenders, "3.11-only constructs in the shipped SDK:\n" + "\n".join(offenders)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "from enum import StrEnum\n\n\nclass Mode(StrEnum):\n    A = 'a'\n",
            "from enum import Enum\n\n\nclass Mode(str, Enum):\n    A = 'a'\n",
        ),
        (
            "from typing import Any, Self\n\n\nclass Client:\n"
            "    def __enter__(self) -> Self:\n        return self\n\n\n"
            "class AuthenticatedClient:\n    def __enter__(self) -> Self:\n        return self\n",
            "from typing import Any\n\n\nclass Client:\n"
            '    def __enter__(self) -> "Client":\n        return self\n\n\n'
            "class AuthenticatedClient:\n"
            '    def __enter__(self) -> "AuthenticatedClient":\n        return self\n',
        ),
    ],
    ids=["str-enum", "self"],
)
def test_downlevel_rewrites(source: str, expected: str) -> None:
    assert _hook.downlevel(source) == expected


def test_downlevel_fromisoformat_uses_dateutil_and_survives_multiline_imports() -> None:
    source = (
        "import datetime\n"
        "from attrs import define as _attrs_define\n"
        "from attrs import field as _attrs_field\n"
        "\n"
        "from ..models.x import (\n"
        "    X,\n"
        ")\n"
        "\n"
        "a = datetime.datetime.fromisoformat(d.pop('a'))\n"
        "b = datetime.date.fromisoformat(f(d['b']))\n"
    )
    out = _hook.downlevel(source)
    assert "fromisoformat" not in out
    assert "a = isoparse(d.pop('a'))\n" in out
    assert "b = isoparse(f(d['b'])).date()\n" in out
    assert "from attrs import field as _attrs_field\nfrom dateutil.parser import isoparse\n" in out
    compile(out, "<generated>", "exec")
