"""Tests for the link validation in ``scripts/generate_landing_page.py``.

A README link to a repo-root file (``[MIGRATION.md](MIGRATION.md)``) has no
``/``, so it was treated as a sibling page and passed validation, then broke the
camunda-docs build (camunda/camunda-docs#10069). A bare filename is only valid
if that page was generated alongside the linking page.
"""

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "generate_landing_page.py"
_spec = importlib.util.spec_from_file_location("generate_landing_page", _SCRIPT)
assert _spec and _spec.loader
generate_landing_page = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(generate_landing_page)

validate_generated_links = generate_landing_page.validate_generated_links


def _write(root: Path, pages: dict[str, str]) -> Path:
    for name, body in pages.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return root


def test_rejects_bare_filename_with_no_generated_page(tmp_path: Path) -> None:
    _write(
        tmp_path, {"sdk/guide.md": "See [the guide](MIGRATION.md) and [x](NOTES.md#a)."}
    )
    errors = validate_generated_links(tmp_path)
    assert len(errors) == 2, errors
    assert any("MIGRATION.md" in e for e in errors)
    assert any("NOTES.md#a" in e for e in errors)


def test_accepts_bare_filename_of_generated_sibling(tmp_path: Path) -> None:
    _write(
        tmp_path,
        {
            "sdk/configuration.md": "See [resilience](resilience.md#backpressure).",
            "sdk/resilience.md": "# Resilience",
        },
    )
    assert validate_generated_links(tmp_path) == []
