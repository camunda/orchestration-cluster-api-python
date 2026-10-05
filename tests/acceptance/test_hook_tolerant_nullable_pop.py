"""Tests for hooks/post_gen/0450_tolerant_nullable_pop.py (issue #287).

A server may omit a key the spec marks ``nullable`` — absent and null mean the same — but the
generator emits a bare ``d.pop("field")`` for required fields, so an omitted key raised
``KeyError`` and failed the whole response. The hook used to cover five hardcoded fields in one
model; it now derives every nullable field from the spec.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import pytest
import yaml
from openapi_python_client.utils import ClassName, snake_case

REPO_ROOT = Path(__file__).resolve().parents[2]
BUNDLED_SPEC = REPO_ROOT / "generated" / "bundled_spec.yaml"
MODELS_DIR = REPO_ROOT / "generated" / "camunda_orchestration_sdk" / "models"

_hook_path = REPO_ROOT / "hooks" / "post_gen" / "0450_tolerant_nullable_pop.py"
_spec = importlib.util.spec_from_file_location(
    "_tolerant_nullable_pop_hook", _hook_path
)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)


# --- derivation -------------------------------------------------------------------------------


def test_derives_direct_inherited_and_inline_allof_nullable_fields() -> None:
    schemas: dict[str, Any] = {
        "Base": {"properties": {"inherited": {"type": "string", "nullable": True}}},
        "Child": {
            "allOf": [
                {"$ref": "#/components/schemas/Base"},
                {"properties": {"inline": {"type": "string", "nullable": True}}},
            ],
            "properties": {
                "direct": {"allOf": [{"$ref": "#/x"}], "nullable": True},
                "plain": {"type": "string"},
            },
        },
    }
    assert _hook.derive_nullable_fields(schemas) == {
        "Base": {"inherited"},
        "Child": {"direct", "inherited", "inline"},
    }


def test_a_reference_to_a_nullable_schema_makes_the_field_nullable() -> None:
    # Lifted inline objects carry `nullable` on the schema, not the referencing property.
    schemas: dict[str, Any] = {
        "Lifted": {"nullable": True, "type": "object"},
        "Owner": {
            "properties": {
                "direct": {"$ref": "#/components/schemas/Lifted"},
                "wrapped": {"allOf": [{"$ref": "#/components/schemas/Lifted"}]},
                "plain": {"$ref": "#/components/schemas/Other"},
            }
        },
        "Other": {"type": "object"},
    }
    assert _hook.derive_nullable_fields(schemas) == {"Owner": {"direct", "wrapped"}}


def test_a_child_redeclaring_a_field_as_non_nullable_wins() -> None:
    schemas: dict[str, Any] = {
        "Base": {"properties": {"f": {"type": "string", "nullable": True}}},
        "Child": {
            "allOf": [{"$ref": "#/components/schemas/Base"}],
            "properties": {"f": {"type": "string"}},
        },
    }
    assert _hook.derive_nullable_fields(schemas) == {"Base": {"f"}}


def test_a_spec_with_no_nullable_fields_is_an_error() -> None:
    # An empty result means the bundler stripped `nullable` or the walk broke; silently
    # patching nothing would reintroduce the KeyError everywhere.
    with pytest.raises(SystemExit):
        _hook.derive_nullable_fields({"A": {"properties": {"x": {"type": "string"}}}})


# --- rewrite ----------------------------------------------------------------------------------

_SOURCE = (
    '        name = d.pop("name")\n'
    "        description = _parse_description(\n"
    '            d.pop("description")\n'
    "        )\n"
    '        other = d.pop("descriptionText")\n'
)


def test_defaults_only_the_listed_fields_including_wrapped_calls() -> None:
    out = _hook.tolerate_absent_keys(_SOURCE, {"description"})
    assert 'd.pop("description", None)' in out
    assert 'd.pop("name")' in out
    # Anchored on the closing quote, so a longer field name sharing the prefix is untouched.
    assert 'd.pop("descriptionText")' in out


def test_rewrite_is_idempotent() -> None:
    once = _hook.tolerate_absent_keys(_SOURCE, {"description"})
    assert _hook.tolerate_absent_keys(once, {"description"}) == once


def _models_dir(tmp_path: Path, files: dict[str, str]) -> Path:
    models = tmp_path / "camunda_orchestration_sdk" / "models"
    models.mkdir(parents=True)
    for name, body in files.items():
        (models / name).write_text(body, encoding="utf-8")
    return models


def test_a_missing_model_file_is_an_error(tmp_path: Path) -> None:
    models = _models_dir(tmp_path, {})
    with pytest.raises(SystemExit):
        _hook.apply(models, {"AgentTool": {"description"}})


def test_a_field_with_no_pop_site_is_an_error(tmp_path: Path) -> None:
    # The field-to-model mapping is wrong if the pop cannot be found; fail rather than skip.
    models = _models_dir(tmp_path, {"agent_tool.py": 'name = d.pop("name")\n'})
    with pytest.raises(SystemExit):
        _hook.apply(models, {"AgentTool": {"description"}})


def test_apply_patches_the_mapped_model(tmp_path: Path) -> None:
    models = _models_dir(tmp_path, {"agent_tool.py": _SOURCE})
    _hook.apply(models, {"AgentTool": {"description"}})
    assert 'd.pop("description", None)' in (models / "agent_tool.py").read_text()


# --- class guard over the real generated tree -------------------------------------------------


def _module_name(schema_name: str) -> str:
    return snake_case(ClassName(schema_name, prefix=""))


def _spec_nullable_fields() -> list[tuple[str, str]]:
    """Every (schema, wire field) the bundled spec marks nullable, inherited fields included.

    Walked here rather than reusing the hook, so a hook whose walk silently narrows cannot
    also narrow the guard.
    """
    schemas = yaml.safe_load(BUNDLED_SPEC.read_text(encoding="utf-8"))["components"][
        "schemas"
    ]
    nullable_schemas = {
        n
        for n, s in schemas.items()
        if isinstance(s, dict) and s.get("nullable") is True
    }

    def is_nullable(prop: dict[str, Any]) -> bool:
        refs = [prop.get("$ref", "")] + [
            p.get("$ref", "") for p in prop.get("allOf", [])
        ]
        return prop.get("nullable") is True or any(
            r.rsplit("/", 1)[-1] in nullable_schemas for r in refs if r
        )

    def fields(schema: dict[str, Any], seen: frozenset[str]) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        for part in schema.get("allOf", []):
            ref = part.get("$ref", "")
            if ref.startswith("#/components/schemas/"):
                name = ref.rsplit("/", 1)[1]
                if name not in seen:
                    merged.update(fields(schemas[name], seen | {name}))
            else:
                merged.update(fields(part, seen))
        merged.update(schema.get("properties", {}))
        return merged

    return sorted(
        (name, wire)
        for name, schema in schemas.items()
        for wire, prop in fields(schema, frozenset({name})).items()
        if isinstance(prop, dict) and is_nullable(prop)
    )


def test_no_generated_model_pops_a_nullable_field_without_a_default() -> None:
    nullable = _spec_nullable_fields()
    assert nullable, (
        "the bundled spec declares no nullable fields; the guard would be vacuous"
    )

    bare, unmatched = [], []
    for schema, wire in nullable:
        source = (MODELS_DIR / f"{_module_name(schema)}.py").read_text(encoding="utf-8")
        if f'd.pop("{wire}")' in source:
            bare.append(f"{schema}.{wire}")
        elif f'd.pop("{wire}",' not in source:
            unmatched.append(f"{schema}.{wire}")
    assert unmatched == [], "nullable fields with no d.pop() site in their model"
    assert bare == [], "nullable fields still decoded with a bare d.pop()"


# --- behaviour --------------------------------------------------------------------------------


def test_a_model_decodes_when_the_server_omits_its_nullable_fields() -> None:
    from camunda_orchestration_sdk.models.agent_tool import AgentTool

    # `description` and `elementId` are required but nullable; an omitted key must decode
    # exactly like an explicit null instead of raising KeyError.
    omitted = AgentTool.from_dict({"name": "lookup"})
    explicit = AgentTool.from_dict(
        {"name": "lookup", "description": None, "elementId": None}
    )
    assert (omitted.description, omitted.element_id) == (None, None)
    assert (explicit.description, explicit.element_id) == (None, None)
