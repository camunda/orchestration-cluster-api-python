"""Guard declared runtime dependency ranges against versions known to break the SDK (#401)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from packaging.specifiers import SpecifierSet

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"

# Runtime dependencies with a released (or pre-released) version known to break the SDK.
# The declared range must exclude them, pre-releases included: resolvers pick a pre-release
# whenever the user allows them (`pip --pre`, `uv --prerelease allow`, or a pre-release pin
# anywhere in the tree), and pick the final as soon as it ships. httpx 1.0 removes
# AsyncClient, Timeout, HTTPTransport, TimeoutException and URL.raw_path (#401).
KNOWN_INCOMPATIBLE = {"httpx": ["1.0.dev6", "1.0.0", "1.9.9"]}


def _declared_dependency_specs() -> dict[str, str]:
    # Parsed with a regex rather than tomllib so the test also runs on Python 3.10.
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
    declared = _declared_dependency_specs()[distribution]
    assert not SpecifierSet(declared).contains(version, prereleases=True), (
        f"pyproject.toml declares {distribution}{declared}, which admits {version}: "
        f"the SDK does not work with {distribution} {version}. Add an upper bound."
    )
