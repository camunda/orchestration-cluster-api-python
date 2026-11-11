"""Guard: runtime dependencies required for performance must be declared and installed.

httpcore retries ``import sniffio`` on every lock/event/cancel-shield call when
sniffio is absent (encode/httpcore#1103), costing ~17% CPU per request on the
async client. Ensure it is both declared and importable.
"""

import importlib.util
import re
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _declared_names() -> set[str]:
    # Plain-text parse: tomllib is unavailable on Python 3.10.
    match = re.search(r"^dependencies = \[(.*?)^\]", PYPROJECT.read_text(), re.S | re.M)
    assert match, "dependencies block not found in pyproject.toml"
    deps = re.findall(r'"([^"]+)"', match.group(1))
    names: set[str] = set()
    for dep in deps:
        name = dep
        for sep in "<>=!~;[ ":
            name = name.split(sep)[0]
        names.add(name.strip().lower())
    return names


def test_sniffio_declared_as_runtime_dependency() -> None:
    assert "sniffio" in _declared_names()


def test_sniffio_installed() -> None:
    assert importlib.util.find_spec("sniffio") is not None
