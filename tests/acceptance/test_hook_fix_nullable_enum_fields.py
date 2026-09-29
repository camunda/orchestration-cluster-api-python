"""Tests for hooks/post_gen/1225_fix_nullable_enum_fields.py.

``openapi-python-client`` drops ``nullable: true`` when a property also
carries an ``enum``, producing a field that cannot deserialise a ``null``.
The hook restores the nullability.

The transformation is exercised on synthetic snippets so the guard stays
meaningful even when no schema in the current upstream spec happens to hit
this codegen shape. The final test walks the real generated package and is
scoped to the defect *class*: no nullable enum field anywhere may be
non-optional.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]

_hook_path = _ROOT / "hooks" / "post_gen" / "1225_fix_nullable_enum_fields.py"
_spec = importlib.util.spec_from_file_location("_fix_nullable_enum_fields", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_patch_field = _hook._patch_field
_nullable_properties = _hook._nullable_properties
_snake = _hook._snake

_MODEL = Path("cluster_rebalance_operation_partition.py")

_BARE_ENUM_MODEL = (
    '    """\n'
    "    Attributes:\n"
    "        result (ClusterRebalanceOperationPartitionResult): The terminal outcome.\n"
    '    """\n'
    "\n"
    "    result: ClusterRebalanceOperationPartitionResult\n"
    "\n"
    "    def to_dict(self) -> dict[str, Any]:\n"
    "        result = self.result.value\n"
    "\n"
    "    @classmethod\n"
    "    def from_dict(cls, src_dict):\n"
    '        result = ClusterRebalanceOperationPartitionResult(d.pop("result"))\n'
)


class TestBareEnumShape:
    def test_annotation_becomes_optional(self) -> None:
        patched, changed = _patch_field(_BARE_ENUM_MODEL, "result", _MODEL)
        assert changed
        assert (
            "    result: None | ClusterRebalanceOperationPartitionResult\n" in patched
        )

    def test_docstring_becomes_optional(self) -> None:
        patched, _ = _patch_field(_BARE_ENUM_MODEL, "result", _MODEL)
        assert "result (None | ClusterRebalanceOperationPartitionResult):" in patched

    def test_to_dict_guards_the_value_access(self) -> None:
        patched, _ = _patch_field(_BARE_ENUM_MODEL, "result", _MODEL)
        assert "        result: None | str\n" in patched
        assert (
            "        result = self.result.value if self.result is not None else None\n"
            in patched
        )

    def test_from_dict_returns_none_for_null(self) -> None:
        patched, _ = _patch_field(_BARE_ENUM_MODEL, "result", _MODEL)
        assert (
            "        def _parse_result(data: object) "
            "-> None | ClusterRebalanceOperationPartitionResult:" in patched
        )
        assert '        result = _parse_result(d.pop("result"))' in patched

    def test_is_idempotent(self) -> None:
        once, _ = _patch_field(_BARE_ENUM_MODEL, "result", _MODEL)
        twice, changed = _patch_field(once, "result", _MODEL)
        assert not changed
        assert twice == once


class TestShapesLeftAlone:
    def test_already_optional_field_is_untouched(self) -> None:
        content = (
            "    result: None | ClusterRebalanceOperationPartitionResult\n"
            '        result = _parse_result(d.pop("result"))\n'
        )
        patched, changed = _patch_field(content, "result", _MODEL)
        assert not changed
        assert patched == content

    def test_plain_scalar_field_is_untouched(self) -> None:
        content = (
            "    current_leader: None | str\n"
            '        current_leader = d.pop("currentLeader")\n'
        )
        patched, changed = _patch_field(content, "currentLeader", _MODEL)
        assert not changed
        assert patched == content


class TestPartialShapeRaises:
    """A model the hook only half-understands must fail loudly, not silently."""

    def test_missing_to_dict_site_raises(self) -> None:
        content = (
            "    result: ClusterRebalanceOperationPartitionResult\n"
            '        result = ClusterRebalanceOperationPartitionResult(d.pop("result"))\n'
        )
        with pytest.raises(RuntimeError, match="Refusing to half-patch"):
            _patch_field(content, "result", _MODEL)


class TestGeneratedPackage:
    """Class-scoped guard against the real generated output."""

    def test_no_nullable_enum_field_is_non_optional(self) -> None:
        spec_path = _ROOT / "external-spec" / "bundled" / "rest-api.bundle.json"
        models = _ROOT / "generated" / "camunda_orchestration_sdk" / "models"
        if not spec_path.exists() or not models.exists():
            pytest.skip("SDK not generated")

        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        offenders: list[str] = []
        for schema_name, json_names in _nullable_properties(spec).items():
            model = models / f"{_snake(schema_name)}.py"
            if not model.exists():
                continue
            content = model.read_text(encoding="utf-8")
            for json_name in json_names:
                bare = re.search(
                    rf'^[ ]+(\w+) = [A-Z]\w*\(\s*d\.pop\("{re.escape(json_name)}"\)\s*\)',
                    content,
                    re.M,
                )
                if bare:
                    offenders.append(f"{model.name}:{bare.group(1)}")

        assert not offenders, (
            "nullable spec properties generated as non-optional enum fields: "
            + ", ".join(sorted(offenders))
        )
