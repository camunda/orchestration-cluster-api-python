"""Every ``openapi_python_client`` symbol the generator pipeline uses must exist in the locked version.

Hooks and tests reach into openapi-python-client's internals (naming helpers, etc.), which are
not a stable API: 0.29 renamed ``openapi_python_client.utils`` to ``openapi_python_client.strings``
and generation crashed with ``ModuleNotFoundError`` (issue #383). A hook that wraps the import in a
fallback hides the break instead, so file-name derivation silently drifts.

This guards the class: it statically collects every ``openapi_python_client`` import in
``hooks/``, ``generate.py``, ``scripts/`` and ``tests/`` (including function-local imports) and
checks that each module and imported name resolves against the installed generator.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_ROOT_PACKAGE = "openapi_python_client"


def _source_files() -> list[Path]:
    files = [REPO_ROOT / "generate.py"]
    for directory in ("hooks", "scripts", "tests"):
        files.extend(sorted((REPO_ROOT / directory).rglob("*.py")))
    return [f for f in files if f.is_file()]


def _generator_imports() -> list[tuple[str, str, str | None]]:
    """Return (location, module, name) for each openapi_python_client import."""
    found: list[tuple[str, str, str | None]] = []
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        rel = path.relative_to(REPO_ROOT)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] == _ROOT_PACKAGE:
                        found.append((f"{rel}:{node.lineno}", alias.name, None))
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                if node.module.split(".")[0] == _ROOT_PACKAGE:
                    for alias in node.names:
                        found.append((f"{rel}:{node.lineno}", node.module, alias.name))
    return found


_IMPORTS = _generator_imports()


def test_generator_imports_are_discovered() -> None:
    # Guard the guard: if the scan finds nothing, the parametrized test below passes vacuously.
    assert _IMPORTS, "expected hooks/tests to import from openapi_python_client"


@pytest.mark.parametrize(
    ("location", "module", "name"),
    _IMPORTS,
    ids=[f"{loc}:{mod}{'.' + n if n else ''}" for loc, mod, n in _IMPORTS],
)
def test_generator_import_resolves(location: str, module: str, name: str | None) -> None:
    pytest.importorskip(_ROOT_PACKAGE, reason="generator not installed (Python < 3.11)")
    try:
        imported = importlib.import_module(module)
    except ImportError as exc:
        pytest.fail(f"{location}: cannot import {module!r} from the locked generator: {exc}")
    if name is None or name == "*":
        return
    if hasattr(imported, name):
        return
    # ``from pkg import submodule`` form.
    try:
        importlib.import_module(f"{module}.{name}")
    except ImportError:
        pytest.fail(f"{location}: {module!r} has no attribute or submodule {name!r}")
