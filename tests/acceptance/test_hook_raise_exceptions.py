"""Tests for hooks/post_gen/0200_raise_exceptions.py.

The hook derives the return annotation of ``sync``/``asyncio`` from the body of
the generated ``_parse_response``. Whatever it derives must be a type, never the
name of a helper function the generator emitted to parse that response.
"""

from __future__ import annotations

import ast
import builtins
import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

_root = Path(__file__).resolve().parents[2]
_HOOK_DIR = _root / "hooks" / "post_gen"

# The hook imports a sibling module (_identifier_guard); make it resolvable
# only while loading so the sys.path mutation does not leak into other tests.
_added_to_path = str(_HOOK_DIR) not in sys.path
if _added_to_path:
    sys.path.insert(0, str(_HOOK_DIR))
try:
    _spec = importlib.util.spec_from_file_location(
        "_raise_exceptions_hook", _HOOK_DIR / "0200_raise_exceptions.py"
    )
    assert _spec and _spec.loader
    _hook = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_hook)
finally:
    if _added_to_path:
        sys.path.remove(str(_HOOK_DIR))

_API = _root / "generated" / "camunda_orchestration_sdk" / "api"

# openapi-python-client's output for a response whose schema is a oneOf union:
# a nested helper that tries each member, called to produce response_200.
_UNION_RESPONSE = textwrap.dedent(
    """
    def _parse_response(*, client, response) -> A | B | ProblemDetail | None:
        if response.status_code == 200:

            def _parse_response_200(data: object) -> A | B:
                try:
                    return A.from_dict(data)
                except TypeError:
                    pass
                return B.from_dict(data)

            response_200 = _parse_response_200(response.json())
            return response_200
        if response.status_code == 400:
            response_400 = ProblemDetail.from_dict(response.json())
            return response_400
        return None
    """
)


def test_union_response_resolves_to_the_helper_return_type() -> None:
    status_types = _hook._extract_status_type_map(ast.parse(_UNION_RESPONSE))
    assert status_types == {200: "A | B", 400: "ProblemDetail"}


def _bound_names(tree: ast.Module) -> set[str]:
    names = set(dir(builtins))
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((a.asname or a.name).split(".")[0] for a in node.names)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return names


@pytest.mark.parametrize(
    "module",
    sorted(_API.rglob("*.py")),
    ids=lambda p: str(p.relative_to(_API)),
)
def test_every_sync_return_annotation_is_resolvable(module: Path) -> None:
    tree = ast.parse(module.read_text(encoding="utf-8"))
    bound = _bound_names(tree)
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name not in {"sync", "asyncio"} or node.returns is None:
            continue
        unresolved = {
            n.id
            for n in ast.walk(node.returns)
            if isinstance(n, ast.Name) and n.id not in bound
        }
        assert not unresolved, f"{node.name} returns unbound name(s) {unresolved}"
