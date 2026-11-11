"""Guard runtime dependencies that are performance-critical but not pulled in transitively.

httpcore calls ``import sniffio`` on every async lock/event/shield. When
``sniffio`` is missing, Python re-searches ``sys.path`` on every call (failed
imports are not cached), costing ~17% CPU per request in ``CamundaAsyncClient``.
anyio no longer depends on sniffio and httpcore does not declare it, so the SDK
must declare it itself (see issue #376).
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"

# Modules that must be importable in the installed environment and declared as
# direct runtime dependencies of the SDK.
REQUIRED_RUNTIME_MODULES = {"sniffio": "sniffio"}


def _declared_dependency_names() -> set[str]:
    # Parsed with a regex rather than tomllib so the test also runs on Python 3.10.
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r"^dependencies\s*=\s*\[(.*?)^\]", text, re.S | re.M)
    assert match, "could not find [project].dependencies in pyproject.toml"
    names: set[str] = set()
    for spec in re.findall(r'"([^"]+)"', match.group(1)):
        name = spec
        for sep in ("[", "<", ">", "=", "!", "~", ";", " "):
            name = name.split(sep, 1)[0]
        names.add(name.strip().lower().replace("_", "-"))
    return names


@pytest.mark.parametrize("module,distribution", sorted(REQUIRED_RUNTIME_MODULES.items()))
def test_required_module_is_installed(module: str, distribution: str) -> None:
    assert importlib.util.find_spec(module) is not None, (
        f"{module!r} is not installed; httpcore falls back to a per-call import "
        "search that costs significant CPU in the async client."
    )


@pytest.mark.parametrize("module,distribution", sorted(REQUIRED_RUNTIME_MODULES.items()))
def test_required_module_is_declared_dependency(module: str, distribution: str) -> None:
    assert distribution in _declared_dependency_names(), (
        f"{distribution!r} must be a direct runtime dependency in pyproject.toml"
    )
