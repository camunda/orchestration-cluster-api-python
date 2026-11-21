"""generate.py must use metadata matching the selected spec, never an unrelated snapshot."""

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location("_gen", REPO_ROOT / "generate.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    spec.loader.exec_module(mod)
    return mod


def test_sibling_of_bundled_spec(tmp_path: Path) -> None:
    (tmp_path / "spec-metadata.json").write_text("{}")
    bundle = tmp_path / "x.json"
    bundle.write_text("{}")
    assert _load().resolve_metadata_path(None, bundle) == tmp_path / "spec-metadata.json"


def test_explicit_wins(tmp_path: Path) -> None:
    m = tmp_path / "m.json"
    m.write_text("{}")
    assert _load().resolve_metadata_path(str(m), None) == m.resolve()


@pytest.mark.parametrize("variant", ["no_bundle", "missing_sibling", "missing_explicit"])
def test_fails_closed(tmp_path: Path, variant: str) -> None:
    gen = _load()
    with pytest.raises(FileNotFoundError):
        if variant == "no_bundle":
            gen.resolve_metadata_path(None, None)
        elif variant == "missing_sibling":
            gen.resolve_metadata_path(None, tmp_path / "x.json")
        else:
            gen.resolve_metadata_path(str(tmp_path / "nope.json"), None)
