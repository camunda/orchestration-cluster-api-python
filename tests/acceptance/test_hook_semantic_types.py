"""Tests for hooks/post_gen/1000_patch_semantic_types_in_models.py.

Regression guards for issue #329: since b81c24fd many model fields that
v10.0.0 branded with semantic types (``TenantId``, ``BusinessId``) were
generated as plain ``str``. The global property-name map drops ambiguous names
such as ``tenantId``/``businessId`` (they appear unannotated on filter
properties and on ``ExpressionEvaluationRequest``), so branding those fields
relies entirely on the per-schema map. That map had two gaps:

1. ``$ref``-only properties (``$ref: '#/components/schemas/TenantId'``) and
   single-element ``allOf`` ``$ref``s were ignored — only inline
   ``x-semantic-type`` was read.
2. Schemas named from a ``title`` (e.g. ``ProcessInstanceCreationInstructionById``,
   title "Process creation by id", file ``process_creation_by_id.py``) were
   keyed by their schema name and never matched the model file.

The hook functions are unit-tested on synthetic specs so the guards stay
meaningful regardless of the current upstream spec, and a class-scoped guard
over the real generated tree asserts that no model is branded ``tenant_id: str``
unless the spec itself declares a bare string.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
BUNDLED_SPEC = REPO_ROOT / "generated" / "bundled_spec.yaml"
MODELS_DIR = REPO_ROOT / "generated" / "camunda_orchestration_sdk" / "models"

# The hook imports ``_identifier_guard`` as a sibling module; make it importable.
_POST_GEN = REPO_ROOT / "hooks" / "post_gen"
if str(_POST_GEN) not in sys.path:
    sys.path.insert(0, str(_POST_GEN))

_hook_path = _POST_GEN / "1000_patch_semantic_types_in_models.py"
_spec = importlib.util.spec_from_file_location("_patch_semantic_types", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)


def _components(schemas: dict[str, Any]) -> dict[str, Any]:
    return {"components": {"schemas": schemas}}


# --- unit: $ref / allOf resolution -----------------------------------------------------------


def test_ref_property_is_branded() -> None:
    """A property declared only as ``$ref`` to an annotated schema is branded."""
    spec = _components(
        {
            "TenantId": {"type": "string", "x-semantic-type": "TenantId"},
            "Thing": {"properties": {"tenantId": {"$ref": "#/components/schemas/TenantId"}}},
        }
    )
    result = _hook._extract_per_schema_semantic_mappings(spec)
    assert result["Thing"]["tenantId"] == "TenantId"


def test_single_element_allof_ref_is_branded() -> None:
    spec = _components(
        {
            "BusinessId": {"type": "string", "x-semantic-type": "BusinessId"},
            "Thing": {
                "properties": {
                    "businessId": {"allOf": [{"$ref": "#/components/schemas/BusinessId"}]}
                }
            },
        }
    )
    result = _hook._extract_per_schema_semantic_mappings(spec)
    assert result["Thing"]["businessId"] == "BusinessId"


def test_allof_parent_properties_are_inherited() -> None:
    """Spec ``main`` composes the process-creation variants via ``allOf`` parents."""
    spec = _components(
        {
            "TenantId": {"type": "string", "x-semantic-type": "TenantId"},
            "Base": {
                "properties": {"tenantId": {"$ref": "#/components/schemas/TenantId"}}
            },
            "Child": {
                "allOf": [
                    {"$ref": "#/components/schemas/Base"},
                    {"properties": {"name": {"type": "string"}}},
                ]
            },
        }
    )
    result = _hook._extract_per_schema_semantic_mappings(spec)
    assert result["Child"]["tenantId"] == "TenantId"


def test_bare_string_property_is_not_branded() -> None:
    spec = _components(
        {"Thing": {"properties": {"tenantId": {"type": "string"}}}}
    )
    result = _hook._extract_per_schema_semantic_mappings(spec)
    assert "Thing" not in result or "tenantId" not in result.get("Thing", {})


# --- unit: title keying ----------------------------------------------------------------------


def test_schema_is_keyed_by_generated_model_name_from_title() -> None:
    """A title-named schema is keyed by the model name, not the schema name."""
    spec = _components(
        {
            "TenantId": {"type": "string", "x-semantic-type": "TenantId"},
            "ProcessInstanceCreationInstructionById": {
                "title": "Process creation by id",
                "properties": {"tenantId": {"$ref": "#/components/schemas/TenantId"}},
            },
        }
    )
    result = _hook._extract_per_schema_semantic_mappings(spec)
    assert "ProcessCreationById" in result
    assert result["ProcessCreationById"]["tenantId"] == "TenantId"


def test_title_with_acronym_matches_generated_file_name() -> None:
    """"Decision evaluation by ID" generates ``decision_evaluation_by_id.py``."""
    assert (
        _hook._model_name_for_schema("DecisionEvaluationById", {"title": "Decision evaluation by ID"})
        == "DecisionEvaluationById"
    )


def test_untitled_schema_is_keyed_by_its_name() -> None:
    assert _hook._model_name_for_schema("ProcessInstanceResult", {}) == "ProcessInstanceResult"


# --- class guard over the real generated tree ------------------------------------------------


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


def _model_annotations() -> dict[str, dict[str, str]]:
    """Generated-model-name -> {attribute: annotation} for every model file."""
    out: dict[str, dict[str, str]] = {}
    for module in sorted(MODELS_DIR.glob("*.py")):
        if module.stem == "__init__":
            continue
        model_name = "".join(word.capitalize() for word in module.stem.split("_"))
        out[model_name] = _annotations(module)
    return out


def test_pinned_result_models_keep_semantic_tenant_id() -> None:
    models = _model_annotations()
    assert models["ProcessInstanceResult"].get("tenant_id") == "TenantId"
    assert models["UserTaskResult"].get("tenant_id") == "TenantId"


def test_process_creation_by_id_keeps_semantic_tenant_and_business_id() -> None:
    models = _model_annotations()
    by_id = models["ProcessCreationById"]
    assert by_id.get("tenant_id") == "TenantId | Unset"
    assert by_id.get("business_id") == "BusinessId | Unset"


def _models_with_plainly_typed(spec: dict[str, Any], wire: str) -> set[str]:
    """Model names whose effective ``wire`` property carries no semantic type.

    These are the only models allowed to generate the field as a plain string.
    """
    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})
    allowed: set[str] = set()
    for schema_name, schema_def in schemas.items():
        if not isinstance(schema_def, dict):
            continue
        props = _hook._collect_schema_properties(schema_def, schemas)
        if wire not in props:
            continue
        if _hook._semantic_type_of_prop(props[wire], schemas) is None:
            allowed.add(_hook._model_name_for_schema(schema_name, schema_def))
    return allowed


def _assert_no_unexpected_plain(wire: str, attr: str) -> None:
    spec = yaml.safe_load(BUNDLED_SPEC.read_text(encoding="utf-8"))
    allowed = _models_with_plainly_typed(spec, wire)
    offenders: list[str] = []
    for model_name, anns in _model_annotations().items():
        annotation = anns.get(attr)
        if annotation is None:
            continue
        is_plain_str = annotation in {"str", "str | Unset", "None | str"}
        if is_plain_str and model_name not in allowed:
            offenders.append(f"{model_name}.{attr}: {annotation}")
    assert offenders == [], (
        f"models branded '{attr}: str' though the spec gives them a semantic type: {offenders}"
    )


def test_no_model_has_plain_tenant_id_unless_spec_declares_a_bare_string() -> None:
    _assert_no_unexpected_plain("tenantId", "tenant_id")


def test_no_model_has_plain_business_id_unless_spec_declares_a_bare_string() -> None:
    _assert_no_unexpected_plain("businessId", "business_id")


def test_expression_evaluation_request_keeps_bare_string_tenant_id() -> None:
    """The one legitimate bare ``tenant_id: str`` must stay a plain string."""
    models = _model_annotations()
    assert models["ExpressionEvaluationRequest"].get("tenant_id") == "str | Unset"


def test_name_ambiguity_still_resolves_per_schema() -> None:
    """b81c24fd's fix: ``name`` is ``ClusterVariableName`` only where annotated."""
    models = _model_annotations()
    assert models["ClusterVariableResult"].get("name") == "ClusterVariableName"
    assert models["GroupResult"].get("name") == "str"
