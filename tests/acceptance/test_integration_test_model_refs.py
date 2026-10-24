"""Guard: integration tests must only reference model names the generated SDK exports.

Defect class (issue #323): an upstream spec change renamed / removed a generated
model, and integration tests kept importing the stale name. Because integration
tests are skipped without CAMUNDA_INTEGRATION=1, the breakage only surfaced at
``make generate`` time as ``ty check`` errors (e.g. "Object of type `object` is
not callable" when a model class became a plain object alias).

This test statically resolves every ``camunda_orchestration_sdk[.models]`` import
in ``tests/integration/`` against the generated package's export surface, so any
stale reference fails fast in the acceptance suite — for any model, not just the
instance fixed in #323.
"""

from __future__ import annotations

import ast
from pathlib import Path

import camunda_orchestration_sdk
import camunda_orchestration_sdk.models

INTEGRATION_DIR = Path(__file__).parent.parent / "integration"

_SDK_EXPORTS: dict[str, set[str]] = {
    "camunda_orchestration_sdk": set(dir(camunda_orchestration_sdk)),
    "camunda_orchestration_sdk.models": set(dir(camunda_orchestration_sdk.models)),
}


def _imported_sdk_names(path: Path) -> list[tuple[int, str, str]]:
    """Return (line, module, imported name) for every SDK import in the file."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    refs: list[tuple[int, str, str]] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.ImportFrom)
            and node.module in _SDK_EXPORTS
            and node.col_offset == 0  # top-level imports only; lazy ones are intentional
        ):
            for alias in node.names:
                refs.append((node.lineno, node.module, alias.name))
    return refs


def test_integration_tests_import_only_exported_sdk_names() -> None:
    stale: list[str] = []
    for test_file in sorted(INTEGRATION_DIR.glob("test_*.py")):
        for line, module, name in _imported_sdk_names(test_file):
            if name not in _SDK_EXPORTS[module]:
                stale.append(f"{test_file.name}:{line}: {name} not exported by {module}")
    assert not stale, (
        "Integration tests import names the generated SDK no longer exports "
        "(stale model references — see issue #323):\n" + "\n".join(stale)
    )
