"""Tests for hooks/post_gen/1400_generate_stubs.py.

Regression guards for the .pyi stub generator. The stub generator must
preserve the *class* of declaration semantics from the source, not just the
happy path — e.g. a ``TypedDict`` declared with ``total=False`` must keep that
keyword in the stub, otherwise downstream type consumers (pyright-based API
changelog tooling) see every member as required.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

# Import the numbered hook module via importlib (filename starts with a digit).
_hook_path = (
    Path(__file__).resolve().parents[2]
    / "hooks"
    / "post_gen"
    / "1400_generate_stubs.py"
)
_spec = importlib.util.spec_from_file_location("_generate_stubs", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_generate_stub = _hook._generate_stub


def _stub_for(tmp_path: Path, source: str) -> str:
    py_file = tmp_path / "sample.py"
    py_file.write_text(source, encoding="utf-8")
    stub = _generate_stub(py_file)
    assert stub is not None
    return stub


class TestClassKeywords:
    """Class-level keywords (e.g. TypedDict total=False) survive stubbing."""

    def test_typeddict_total_false_preserved(self, tmp_path: Path) -> None:
        stub = _stub_for(
            tmp_path,
            "from typing import TypedDict\n"
            "\n"
            "class Config(TypedDict, total=False):\n"
            "    SOME_KEY: str\n"
            "    OTHER_KEY: str | bool\n",
        )
        assert "class Config(TypedDict, total=False):" in stub
        assert "    SOME_KEY: str\n" in stub
        assert "    OTHER_KEY: str | bool\n" in stub

    def test_typeddict_without_keywords_unchanged(self, tmp_path: Path) -> None:
        stub = _stub_for(
            tmp_path,
            "from typing import TypedDict\n"
            "\n"
            "class Config(TypedDict):\n"
            "    SOME_KEY: str\n",
        )
        assert "class Config(TypedDict):" in stub

    def test_multiple_bases_and_keywords(self, tmp_path: Path) -> None:
        stub = _stub_for(
            tmp_path,
            "from typing import TypedDict\n"
            "\n"
            "class Base(TypedDict, total=False):\n"
            "    a: str\n"
            "\n"
            "class Child(Base, total=False):\n"
            "    b: str\n",
        )
        assert "class Base(TypedDict, total=False):" in stub
        assert "class Child(Base, total=False):" in stub

    def test_metaclass_keyword_preserved(self, tmp_path: Path) -> None:
        stub = _stub_for(
            tmp_path,
            "from abc import ABCMeta\n"
            "\n"
            "class Plugin(metaclass=ABCMeta):\n"
            "    name: str\n",
        )
        assert "class Plugin(metaclass=ABCMeta):" in stub
