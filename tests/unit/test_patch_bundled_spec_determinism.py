"""Generation must be deterministic: the allOf flattener's merged `required` list."""

import importlib.util
from pathlib import Path
from typing import Any

_HOOK = (
    Path(__file__).resolve().parents[2]
    / "hooks"
    / "pre_gen"
    / "0100_patch_bundled_spec.py"
)
_spec = importlib.util.spec_from_file_location("patch_bundled_spec", _HOOK)
assert _spec is not None and _spec.loader is not None
patch_bundled_spec = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(patch_bundled_spec)


def test_flattened_allof_required_is_sorted() -> None:
    # A set's iteration order depends on PYTHONHASHSEED, so emitting it unsorted
    # reorders `required:` in generated/bundled_spec.yaml on every regeneration.
    names = [
        "zeta",
        "alpha",
        "kappa",
        "beta",
        "omega",
        "delta",
        "eta",
        "gamma",
        "iota",
        "theta",
    ]
    schema: dict[str, Any] = {
        "allOf": [
            {
                "type": "object",
                "properties": {n: {"type": "string"} for n in names[:5]},
                "required": names[:5],
            },
            {
                "type": "object",
                "properties": {n: {"type": "string"} for n in names[5:]},
                "required": names[5:],
            },
        ]
    }

    flattened = patch_bundled_spec.SpecFlattener({}).flatten_schema(schema)

    assert flattened["required"] == sorted(names)
