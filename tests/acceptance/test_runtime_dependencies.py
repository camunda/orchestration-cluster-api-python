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


# Runtime dependencies with a released (or pre-released) version known to break the SDK.
# The declared range must exclude them, pre-releases included: resolvers pick a pre-release
# whenever the user allows them (`pip --pre`, `uv --prerelease allow`, or a pre-release pin
# anywhere in the tree), and pick the final as soon as it ships. httpx 1.0 removes
# AsyncClient, Timeout, HTTPTransport, TimeoutException and URL.raw_path (#401).
KNOWN_INCOMPATIBLE = {"httpx": ["1.0.dev6", "1.0.0", "1.9.9"]}


def _declared_dependency_specs() -> dict[str, str]:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r"^dependencies\s*=\s*\[(.*?)^\]", text, re.S | re.M)
    assert match, "could not find [project].dependencies in pyproject.toml"
    specs: dict[str, str] = {}
    for spec in re.findall(r'"([^"]+)"', match.group(1)):
        name = re.split(r"[\[<>=!~; ]", spec, maxsplit=1)[0]
        specs[name.strip().lower().replace("_", "-")] = spec[len(name) :].split(";", 1)[0]
    return specs


@pytest.mark.parametrize(
    "distribution,version",
    [(dist, v) for dist, versions in sorted(KNOWN_INCOMPATIBLE.items()) for v in versions],
)
def test_declared_range_excludes_incompatible_version(distribution: str, version: str) -> None:
    from packaging.specifiers import SpecifierSet

    declared = _declared_dependency_specs()[distribution]
    assert not SpecifierSet(declared).contains(version, prereleases=True), (
        f"pyproject.toml declares {distribution}{declared}, which admits {version}: "
        f"the SDK does not work with {distribution} {version}. Add an upper bound."
    )
