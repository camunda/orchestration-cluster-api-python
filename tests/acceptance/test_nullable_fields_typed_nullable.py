"""Every field the spec marks nullable must be typed and decoded as nullable (issue #300).

openapi-python-client honours ``nullable`` for most shapes but dropped it for inlined enums and
for ``type`` + ``oneOf`` unions, so those fields were typed non-optional and an explicit
``null`` (which the gateway always sends since 8.9) failed the whole response with
``ValueError``. Pre-gen hook 0150 rewrites those shapes; this guards the class, not the nine
fields that prompted it.
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
from typing import Any

import pytest
import yaml
from openapi_python_client.utils import ClassName, PythonIdentifier, snake_case

REPO_ROOT = Path(__file__).resolve().parents[2]
BUNDLED_SPEC = REPO_ROOT / "generated" / "bundled_spec.yaml"
MODELS_DIR = REPO_ROOT / "generated" / "camunda_orchestration_sdk" / "models"

_hook_path = REPO_ROOT / "hooks" / "pre_gen" / "0150_nullable_enums_and_unions.py"
_spec = importlib.util.spec_from_file_location("_nullable_shapes_hook", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_strict_path = REPO_ROOT / "hooks" / "post_gen" / "1220_strict_nullable_enums.py"
_strict_loader = importlib.util.spec_from_file_location("_strict_nullable_enums", _strict_path)
assert _strict_loader and _strict_loader.loader
_strict = importlib.util.module_from_spec(_strict_loader)
_strict_loader.loader.exec_module(_strict)


# --- rewrite ----------------------------------------------------------------------------------


def _spec_with(props: dict[str, Any], **extra_schemas: Any) -> dict[str, Any]:
    return {"components": {"schemas": {"AuditLogResult": {"properties": props}, **extra_schemas}}}


def test_lifts_a_nullable_inline_enum_under_the_generators_class_name() -> None:
    enum = {"type": "string", "nullable": True, "enum": ["A", "B"], "description": "d"}
    spec = _spec_with({"actorType": enum})
    assert _hook.make_nullable_explicit(spec) == 1
    schemas = spec["components"]["schemas"]
    # The generator named the inline enum `<Schema><Field>`; keeping that name keeps the class.
    assert schemas["AuditLogResultActorType"] == {
        "type": "string",
        "enum": ["A", "B"],
        "description": "d",
    }
    assert schemas["AuditLogResult"]["properties"]["actorType"] == {
        "nullable": True,
        "allOf": [{"$ref": "#/components/schemas/AuditLogResultActorType"}],
        "description": "d",
    }


def test_lifting_keeps_the_property_example() -> None:
    enum = {"nullable": True, "type": "string", "enum": ["dev"], "example": "dev"}
    spec = _spec_with({"stage": enum})
    _hook.make_nullable_explicit(spec)
    assert spec["components"]["schemas"]["AuditLogResult"]["properties"]["stage"]["example"] == "dev"


def test_lifts_enums_on_inline_allof_parts() -> None:
    spec = {
        "components": {
            "schemas": {
                "Child": {
                    "allOf": [
                        {"properties": {"e": {"nullable": True, "type": "string", "enum": ["A"]}}}
                    ]
                }
            }
        }
    }
    assert _hook.make_nullable_explicit(spec) == 1
    assert "ChildE" in spec["components"]["schemas"]


def test_drops_type_beside_a_nullable_union() -> None:
    spec = _spec_with({"k": {"type": "string", "nullable": True, "oneOf": [{"$ref": "#/x"}]}})
    assert _hook.make_nullable_explicit(spec) == 1
    assert "type" not in spec["components"]["schemas"]["AuditLogResult"]["properties"]["k"]


def test_leaves_non_nullable_and_supported_shapes_alone() -> None:
    spec = _spec_with(
        {
            "a": {"type": "string", "enum": ["A"]},
            "c": {"oneOf": [{"$ref": "#/x"}], "nullable": True},
            "d": {"type": "string", "nullable": True},
        }
    )
    before = yaml.safe_dump(spec)
    assert _hook.make_nullable_explicit(spec) == 0
    assert yaml.safe_dump(spec) == before


def test_is_idempotent() -> None:
    spec = _spec_with({"e": {"nullable": True, "type": "string", "enum": ["A"]}})
    assert _hook.make_nullable_explicit(spec) == 1
    assert _hook.make_nullable_explicit(spec) == 0


def test_a_name_collision_is_an_error() -> None:
    spec = _spec_with(
        {"actorType": {"nullable": True, "type": "string", "enum": ["A"]}},
        AuditLogResultActorType={"type": "object"},
    )
    with pytest.raises(SystemExit):
        _hook.make_nullable_explicit(spec)


def test_a_nullable_enum_it_cannot_lift_is_an_error() -> None:
    # Nested below a property, e.g. as array items: the generator would still drop `nullable`.
    items = {"type": "array", "items": {"nullable": True, "type": "string", "enum": ["A"]}}
    with pytest.raises(SystemExit):
        _hook.make_nullable_explicit(_spec_with({"list": items}))


# --- strict parser (post-gen 1220) ------------------------------------------------------------

_LENIENT = (
    "        def _parse_actor_type(data: object) -> AuditLogResultActorType | None:\n"
    "            if data is None:\n"
    "                return data\n"
    "            try:\n"
    "                if not isinstance(data, str):\n"
    "                    raise TypeError()\n"
    "                actor_type_type_1 = AuditLogResultActorType(data)\n"
    "\n"
    "                return actor_type_type_1\n"
    "            except (TypeError, ValueError, AttributeError, KeyError):\n"
    "                pass\n"
    "            return cast(AuditLogResultActorType | None, data)\n"
)


def test_strict_rewrite_drops_the_lenient_fallback_and_is_idempotent() -> None:
    once = _strict.make_strict(_LENIENT, "actor_type", "AuditLogResultActorType")
    assert "cast(" not in once and "except" not in once
    assert "return AuditLogResultActorType(data)" in once
    assert _strict.make_strict(once, "actor_type", "AuditLogResultActorType") == once


def test_strict_rewrite_rejects_an_unrecognised_parser() -> None:
    with pytest.raises(SystemExit):
        _strict.make_strict(
            _LENIENT.replace("cast(AuditLogResultActorType | None, data)", "data"),
            "actor_type",
            "AuditLogResultActorType",
        )


# --- class guard over the real generated tree -------------------------------------------------


def _nullable_fields() -> list[tuple[str, str]]:
    """(schema, wire field) pairs the generator's input spec marks nullable, inherited ones too.

    A field also counts when it references a schema marked nullable, since the bundler lifts
    inline objects into named schemas and leaves the flag there.
    """
    schemas = yaml.safe_load(BUNDLED_SPEC.read_text(encoding="utf-8"))["components"]["schemas"]
    nullable_schemas = {
        n for n, s in schemas.items() if isinstance(s, dict) and s.get("nullable") is True
    }

    def is_nullable(prop: dict[str, Any]) -> bool:
        refs = [prop.get("$ref", "")] + [p.get("$ref", "") for p in prop.get("allOf", [])]
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
        if isinstance(schema, dict)
        for wire, prop in fields(schema, frozenset({name})).items()
        if isinstance(prop, dict) and is_nullable(prop)
    )


def _annotations(module: Path) -> dict[str, str]:
    """Attribute name -> annotation source for the model class in ``module``."""
    tree = ast.parse(module.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    out[stmt.target.id] = ast.unparse(stmt.annotation)
    return out


def test_every_nullable_field_is_typed_as_nullable() -> None:
    nullable = _nullable_fields()
    assert nullable, "the bundled spec declares no nullable fields; the guard would be vacuous"

    not_nullable, unmatched = [], []
    for schema, wire in nullable:
        module = MODELS_DIR / f"{snake_case(ClassName(schema, prefix=''))}.py"
        attr = PythonIdentifier(wire, prefix="field_")
        annotation = _annotations(module).get(attr) if module.exists() else None
        if annotation is None:
            unmatched.append(f"{schema}.{wire}")
        elif "None" not in annotation and annotation != "Any":
            not_nullable.append(f"{schema}.{wire}: {annotation}")
    assert unmatched == [], "nullable fields with no generated attribute"
    assert not_nullable == [], "nullable fields generated with a non-nullable type"


def test_no_nullable_enum_field_accepts_values_outside_the_enum() -> None:
    """The generator's nullable-reference parser falls back to ``cast(..., data)``, so an enum
    reached that way accepted any value while claiming to be the enum. Every nullable property
    whose single ``allOf`` reference is an enum schema must decode strictly."""
    schemas = yaml.safe_load(BUNDLED_SPEC.read_text(encoding="utf-8"))["components"]["schemas"]
    checked, lenient = 0, []
    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        for wire, prop in (schema.get("properties") or {}).items():
            refs = [p.get("$ref", "") for p in prop.get("allOf", [])] if isinstance(prop, dict) else []
            if not (prop.get("nullable") is True and len(refs) == 1):
                continue
            target = schemas.get(refs[0].rsplit("/", 1)[-1], {})
            if "enum" not in target:
                continue
            checked += 1
            source = (MODELS_DIR / f"{snake_case(ClassName(name, prefix=''))}.py").read_text()
            attr = PythonIdentifier(wire, prefix="field_")
            enum_class = ClassName(refs[0].rsplit("/", 1)[-1], prefix="")
            if f"cast({enum_class} | None, data)" in source or f"def _parse_{attr}(" not in source:
                lenient.append(f"{name}.{wire}")
    assert checked > 0, "no nullable enum references found; the guard would be vacuous"
    assert lenient == []


# --- behaviour --------------------------------------------------------------------------------


def _valid_payload(schema_name: str) -> dict[str, Any]:
    """A minimal payload with every required field of ``schema_name`` set to a valid scalar."""
    schemas = yaml.safe_load(BUNDLED_SPEC.read_text(encoding="utf-8"))["components"]["schemas"]
    schema = schemas[schema_name]
    payload: dict[str, Any] = {}
    for field in schema["required"]:
        prop = schema["properties"][field]
        while "$ref" in prop or len(prop.get("allOf", [])) == 1:
            ref = prop.get("$ref") or prop["allOf"][0]["$ref"]
            prop = schemas[ref.rsplit("/", 1)[1]]
        if "enum" in prop:
            payload[field] = next(v for v in prop["enum"] if v is not None)
        elif prop.get("format") == "date-time":
            payload[field] = "2026-01-01T00:00:00Z"
        else:
            payload[field] = "1"
    return payload


@pytest.mark.parametrize(
    "field", ["batchOperationType", "actorType", "relatedEntityType", "resourceKey"]
)
def test_an_audit_log_entry_with_a_null_field_decodes(field: str) -> None:
    from camunda_orchestration_sdk.models.audit_log_result import AuditLogResult

    # A non-batch entry carries `batchOperationType: null`; it raised ValueError before.
    payload = {**_valid_payload("AuditLogResult"), field: None}
    result = AuditLogResult.from_dict(payload)
    assert getattr(result, PythonIdentifier(field, prefix="field_")) is None


@pytest.mark.parametrize("value", ["NOT_A_MEMBER", 42])
@pytest.mark.parametrize("field", ["batchOperationType", "actorType", "relatedEntityType"])
def test_a_nullable_enum_field_still_rejects_a_value_outside_the_enum(field: str, value: object) -> None:
    from camunda_orchestration_sdk.models.audit_log_result import AuditLogResult

    with pytest.raises(ValueError):
        AuditLogResult.from_dict({**_valid_payload("AuditLogResult"), field: value})
