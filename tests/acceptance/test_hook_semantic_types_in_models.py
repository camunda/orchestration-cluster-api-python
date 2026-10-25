"""Regression guards for hooks/post_gen/1000_patch_semantic_types_in_models.py.

Since b81c24fd the ambiguity guard drops ``tenantId`` / ``businessId`` from the
global semantic-type map (``ExpressionEvaluationRequest.tenantId`` is a bare
``type: string`` and filter properties carry no annotation), so those fields
rely on the per-schema fallback. That fallback had two gaps that regressed many
models from ``TenantId`` / ``BusinessId`` back to plain ``str`` (issues #329 /
#330):

1. a property declared as a ``$ref`` (or single-element ``allOf`` ``$ref``) to a
   semantic-key schema was ignored, because only inline ``x-semantic-type`` was
   counted;
2. models that openapi-python-client names from the schema ``title`` (e.g.
   ``process_creation_by_id.py`` from schema
   ``ProcessInstanceCreationInstructionById``, title "Process creation by id")
   never matched, because the map was keyed by the raw schema name.

The first group of tests exercises the extraction logic directly on synthetic
specs so the guard stays meaningful regardless of the current upstream spec. The
second scans the generated models for the class of defect: no field may be typed
bare ``str`` where the spec gives it a semantic type.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = REPO_ROOT / "generated" / "camunda_orchestration_sdk" / "models"

_hook_path = REPO_ROOT / "hooks" / "post_gen" / "1000_patch_semantic_types_in_models.py"
# The hook imports a sibling helper (_identifier_guard) by bare name, so its
# directory must be importable.
sys.path.insert(0, str(_hook_path.parent))
_spec = importlib.util.spec_from_file_location("_patch_semantic_types", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_model_key = _hook._model_key
_property_semantic_type = _hook._property_semantic_type
_extract_per_schema = _hook._extract_per_schema_semantic_mappings


_TENANT_ID = {
    "type": "string",
    "format": "TenantId",
    "x-semantic-type": "TenantId",
}
_BUSINESS_ID = {
    "type": "string",
    "format": "BusinessId",
    "x-semantic-type": "BusinessId",
}


def _make_spec(schemas: dict[str, Any]) -> dict[str, Any]:
    base = {"TenantId": _TENANT_ID, "BusinessId": _BUSINESS_ID}
    base.update(schemas)
    return {"components": {"schemas": base}}


# --- _model_key -------------------------------------------------------------


class TestModelKey:
    def test_title_with_spaces_matches_generated_file_pascal_case(self) -> None:
        # openapi-python-client turns title "Process creation by id" into class
        # ProcessCreationById / file process_creation_by_id.py; run() reverses
        # the stem to the same PascalCase, so the key must match.
        assert _model_key("Process creation by id") == "ProcessCreationById"
        assert _model_key("Process creation by key") == "ProcessCreationByKey"

    def test_acronym_title_lowercased_like_generator(self) -> None:
        assert _model_key("Decision evaluation by ID") == "DecisionEvaluationById"

    def test_plain_schema_name_is_idempotent(self) -> None:
        assert _model_key("ProcessInstanceResult") == "ProcessInstanceResult"
        assert _model_key("DeploymentMetadataResultForm") == "DeploymentMetadataResultForm"


# --- _property_semantic_type ------------------------------------------------


class TestPropertySemanticType:
    def test_inline_annotation(self) -> None:
        schemas = _make_spec({}).get("components", {}).get("schemas", {})
        assert _property_semantic_type(dict(_TENANT_ID), schemas) == "TenantId"

    def test_ref_to_semantic_schema(self) -> None:
        schemas = _make_spec({}).get("components", {}).get("schemas", {})
        prop = {"$ref": "#/components/schemas/TenantId"}
        assert _property_semantic_type(prop, schemas) == "TenantId"

    def test_single_element_allof_ref(self) -> None:
        schemas = _make_spec({}).get("components", {}).get("schemas", {})
        prop = {"allOf": [{"$ref": "#/components/schemas/BusinessId"}]}
        assert _property_semantic_type(prop, schemas) == "BusinessId"

    def test_bare_string_is_not_branded(self) -> None:
        schemas = _make_spec({}).get("components", {}).get("schemas", {})
        prop = {"type": "string", "description": "tenant-scoped"}
        assert _property_semantic_type(prop, schemas) is None


# --- _extract_per_schema_semantic_mappings ----------------------------------


class TestPerSchemaExtraction:
    def test_ref_property_is_resolved(self) -> None:
        """Gap 1: a ``$ref`` to a semantic-key schema must brand the field."""
        spec = _make_spec(
            {
                "ProcessInstanceResult": {
                    "properties": {
                        "tenantId": {"$ref": "#/components/schemas/TenantId"},
                        "businessId": dict(_BUSINESS_ID),
                    }
                }
            }
        )
        result = _extract_per_schema(spec)
        assert result["ProcessInstanceResult"]["tenantId"] == "TenantId"
        assert result["ProcessInstanceResult"]["businessId"] == "BusinessId"

    def test_title_named_model_is_keyed_by_generated_name(self) -> None:
        """Gap 2: a schema named from its title is keyed by the model name."""
        spec = _make_spec(
            {
                "ProcessInstanceCreationInstructionById": {
                    "title": "Process creation by id",
                    "properties": {
                        "tenantId": dict(_TENANT_ID),
                        "businessId": {"$ref": "#/components/schemas/BusinessId"},
                    },
                }
            }
        )
        result = _extract_per_schema(spec)
        # Keyed by the generated model name, not the raw schema name.
        assert "ProcessInstanceCreationInstructionById" not in result
        assert result["ProcessCreationById"]["tenantId"] == "TenantId"
        assert result["ProcessCreationById"]["businessId"] == "BusinessId"

    def test_allof_parent_properties_are_inherited(self) -> None:
        """Spec ``main`` declares the shared fields through an ``allOf`` parent."""
        spec = _make_spec(
            {
                "ProcessCreationBase": {
                    "properties": {
                        "tenantId": {"$ref": "#/components/schemas/TenantId"},
                    }
                },
                "ProcessInstanceCreationInstructionById": {
                    "title": "Process creation by id",
                    "allOf": [
                        {"$ref": "#/components/schemas/ProcessCreationBase"},
                        {"properties": {"businessId": {"$ref": "#/components/schemas/BusinessId"}}},
                    ],
                },
            }
        )
        result = _extract_per_schema(spec)
        assert result["ProcessCreationById"]["tenantId"] == "TenantId"
        assert result["ProcessCreationById"]["businessId"] == "BusinessId"

    def test_bare_string_property_is_not_branded(self) -> None:
        """``ExpressionEvaluationRequest.tenantId`` is a bare string upstream."""
        spec = _make_spec(
            {
                "ExpressionEvaluationRequest": {
                    "properties": {
                        "tenantId": {"type": "string", "description": "d"},
                    }
                }
            }
        )
        result = _extract_per_schema(spec)
        assert "ExpressionEvaluationRequest" not in result

    def test_name_ambiguity_preserved(self) -> None:
        """b81c24fd's ClusterVariableName case must keep working.

        ``name`` is ``ClusterVariableName`` on cluster-variable schemas and a
        plain string elsewhere; the per-schema map must brand only the former.
        """
        spec = _make_spec(
            {
                "ClusterVariableName": {
                    "type": "string",
                    "x-semantic-type": "ClusterVariableName",
                },
                "ClusterVariableResult": {
                    "properties": {
                        "name": {"$ref": "#/components/schemas/ClusterVariableName"},
                    }
                },
                "GroupResult": {
                    "properties": {
                        "name": {"type": "string"},
                    }
                },
            }
        )
        result = _extract_per_schema(spec)
        assert result["ClusterVariableResult"]["name"] == "ClusterVariableName"
        assert "GroupResult" not in result


# --- generated-model scan (class of defect) ---------------------------------

from openapi_python_client.utils import snake_case  # noqa: E402

BUNDLED_SPEC = REPO_ROOT / "generated" / "bundled_spec.yaml"


def _load_spec() -> dict[str, Any]:
    import yaml

    with open(BUNDLED_SPEC, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _generated_semantic_types() -> set[str]:
    """The semantic types the generator actually emits, mirroring run()'s
    filter: string-backed semanticKeys plus union aliases. Types the bundler
    dropped (e.g. integer-backed ``IterationId``) are absent, so the hook leaves
    their fields at the native type and the guard must not expect branding."""
    import json

    meta_path = REPO_ROOT / "external-spec" / "bundled" / "spec-metadata.json"
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    names = {entry["name"] for entry in meta.get("semanticKeys", [])}
    names |= {entry["name"] for entry in meta.get("unions", [])}
    return names


def _bare_str_fields(path: Path, field: str) -> list[str]:
    """Return lines where ``field`` is typed as a bare ``str`` (not a semantic
    type, not an ``Advanced*Filter`` union, not a nested object)."""
    pattern = re.compile(rf"^    {field}: (?:None \| )?str(?: \| Unset)?(?: = .*)?$")
    content = path.read_text(encoding="utf-8")
    return [line for line in content.splitlines() if pattern.match(line)]


def test_generated_models_exist() -> None:
    assert MODELS_DIR.is_dir(), f"Generate the SDK first (missing {MODELS_DIR})"


def test_every_spec_semantic_field_is_branded_in_generated_models() -> None:
    """Class of defect: for every ``tenantId`` / ``businessId`` property the spec
    resolves to a semantic type (inline, via ``$ref``, or ``allOf``), the
    generated field must NOT be a bare ``str``. This is spec-driven, so it needs
    no hardcoded exception list: fields the spec declares as a bare string (e.g.
    ``ExpressionEvaluationRequest.tenantId``, the cluster-variable models) are
    simply never in the expected set.

    Scoped to the ``tenantId`` / ``businessId`` property family that regressed
    (#329/#330). Other semantic fields are covered by the extraction unit tests;
    ``$``-prefixed filter operators (``$eq``/``$neq``) are a separate, unrelated
    naming limitation.
    """
    semantic_id_props = {"tenantId", "businessId"}
    spec = _load_spec()
    expected = _extract_per_schema(spec)
    generated_types = _generated_semantic_types()

    offenders: list[str] = []
    for model_name, props in expected.items():
        model_file = MODELS_DIR / f"{snake_case(model_name)}.py"
        if not model_file.exists():
            # Not every schema produces a top-level model file (e.g. inlined or
            # merged schemas); skip those rather than guessing their file name.
            continue
        for prop_name, semantic_type in props.items():
            if prop_name not in semantic_id_props:
                continue
            if semantic_type not in generated_types:
                # The generator never emits this type, so the field stays native.
                continue
            field = snake_case(prop_name)
            bare = _bare_str_fields(model_file, field)
            if bare:
                offenders.append(
                    f"{model_file.name}:{field} is bare str, expected {semantic_type}"
                )
    assert not offenders, (
        "Spec declares a semantic type for these fields but the generated model "
        "types them as bare str (regression #329/#330):\n" + "\n".join(offenders)
    )


def test_specific_models_pin_semantic_types() -> None:
    """Pin the representative fields called out in the issue."""
    expectations = {
        "process_instance_result.py": [("tenant_id", "TenantId"), ("business_id", "BusinessId")],
        "user_task_result.py": [("tenant_id", "TenantId")],
        "job_search_result.py": [("tenant_id", "TenantId")],
        "message_subscription_result.py": [("tenant_id", "TenantId")],
        "process_creation_by_id.py": [("tenant_id", "TenantId"), ("business_id", "BusinessId")],
        "process_creation_by_key.py": [("tenant_id", "TenantId"), ("business_id", "BusinessId")],
    }
    for file_name, fields in expectations.items():
        path = MODELS_DIR / file_name
        assert path.exists(), f"Missing generated model {file_name}"
        content = path.read_text(encoding="utf-8")
        for field, semantic_type in fields:
            field_pattern = re.compile(
                rf"^    {field}: (?:None \| )?{semantic_type}\b", re.MULTILINE
            )
            assert field_pattern.search(content), (
                f"{file_name}: expected {field} typed as {semantic_type}"
            )


def test_expression_evaluation_request_keeps_bare_str() -> None:
    """The one field that must stay ``str`` (bare string in the spec)."""
    path = MODELS_DIR / "expression_evaluation_request.py"
    assert path.exists()
    assert _bare_str_fields(path, "tenant_id"), (
        "ExpressionEvaluationRequest.tenant_id should remain bare str"
    )
