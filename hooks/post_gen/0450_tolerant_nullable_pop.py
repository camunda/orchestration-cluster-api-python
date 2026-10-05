"""Hook 0450 — let models decode when a server omits a field the spec marks ``nullable``.

For a required field the generator emits a bare ``d.pop("field")``, which raises ``KeyError``
when the key is absent. For a nullable field absent and null mean the same thing: servers omit
null-valued keys, and released servers omit fields the spec has since added. So the whole
response failed to decode over a value that should have been ``None`` (issue #287: an omitted
``jobLeaseToken`` stopped the job worker and surfaced as a gateway 504).

Every field the bundled spec marks ``nullable`` (on the property or on the schema it references,
and including fields inherited through ``allOf``) gets ``d.pop("field", None)``. The list is derived from the spec on every run rather than
hardcoded, so a renamed or newly added nullable field is covered without maintenance. A schema
whose model file cannot be found, a field with no ``d.pop`` site, or a spec with no nullable
fields at all fails generation rather than being skipped.
"""

from __future__ import annotations

import json
from pathlib import Path

from openapi_python_client.utils import ClassName, snake_case

_REF_PREFIX = "#/components/schemas/"


def _get(node: object, key: str) -> object:
    # Not `node.get(key)`: ty narrows `object` to `dict[Never, Never]`, which rejects a str key.
    if isinstance(node, dict):
        return next((v for k, v in node.items() if k == key), None)
    return None


def _ref_name(ref: object) -> str | None:
    if isinstance(ref, str) and ref.startswith(_REF_PREFIX):
        return ref[len(_REF_PREFIX) :]
    return None


def _fields(
    schemas: dict[str, object], schema: object, seen: frozenset[str]
) -> dict[str, object]:
    """Properties of ``schema`` including those merged in through ``allOf``; own ones win."""
    merged: dict[str, object] = {}
    parts = _get(schema, "allOf")
    for part in parts if isinstance(parts, list) else []:
        name = _ref_name(_get(part, "$ref"))
        if name is None:
            merged.update(_fields(schemas, part, seen))
        elif name not in seen and name in schemas:
            merged.update(_fields(schemas, schemas[name], seen | {name}))
    props = _get(schema, "properties")
    if isinstance(props, dict):
        merged.update({str(k): v for k, v in props.items()})
    return merged


def _is_nullable(schemas: dict[str, object], prop: object) -> bool:
    """Nullable on the property itself, or on a schema it references directly or via ``allOf``.

    Inline objects lifted into named schemas carry ``nullable`` on the schema, not on the
    referencing property (e.g. ``DeploymentMetadataResult.processDefinition``).
    """
    if _get(prop, "nullable") is True:
        return True
    parts = _get(prop, "allOf")
    refs = [
        _get(prop, "$ref"),
        *(_get(p, "$ref") for p in (parts if isinstance(parts, list) else [])),
    ]
    seen: set[str] = set()
    for ref in refs:
        name = _ref_name(ref)
        while name is not None and name not in seen and name in schemas:
            seen.add(name)
            if _get(schemas[name], "nullable") is True:
                return True
            name = _ref_name(_get(schemas[name], "$ref"))
    return False


def derive_nullable_fields(schemas: dict[str, object]) -> dict[str, set[str]]:
    """Map each schema name to the wire names of its nullable fields."""
    result: dict[str, set[str]] = {}
    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        nullable = {
            wire
            for wire, prop in _fields(schemas, schema, frozenset({name})).items()
            if _is_nullable(schemas, prop)
        }
        if nullable:
            result[name] = nullable
    if not result:
        raise SystemExit(
            "hook 0450: the bundled spec declares no nullable fields. Either the bundler is "
            "stripping `nullable` or this walk no longer matches the spec; patching nothing "
            "would let every omitted nullable key raise KeyError again."
        )
    return result


def tolerate_absent_keys(source: str, fields: set[str]) -> str:
    """Give every bare ``d.pop("<field>")`` for ``fields`` a ``None`` default. Idempotent."""
    for field in fields:
        source = source.replace(f'd.pop("{field}")', f'd.pop("{field}", None)')
    return source


def model_file(models_dir: Path, schema_name: str) -> Path:
    """The generated module for a schema, named the way openapi-python-client names it."""
    return models_dir / f"{snake_case(ClassName(schema_name, prefix=''))}.py"


def apply(models_dir: Path, nullable: dict[str, set[str]]) -> int:
    patched = 0
    for schema_name in sorted(nullable):
        target = model_file(models_dir, schema_name)
        if not target.exists():
            raise SystemExit(
                f"hook 0450: {target.name} not found for {schema_name}, which declares "
                f"nullable fields {sorted(nullable[schema_name])}."
            )
        source = target.read_text(encoding="utf-8")
        missing = sorted(
            f for f in nullable[schema_name] if f'd.pop("{f}"' not in source
        )
        if missing:
            raise SystemExit(
                f"hook 0450: no d.pop() site in {target.name} for nullable fields {missing}; "
                "the schema-to-model mapping no longer matches the generator output."
            )
        updated = tolerate_absent_keys(source, nullable[schema_name])
        if updated != source:
            patched += sum(source.count(f'd.pop("{f}")') for f in nullable[schema_name])
            target.write_text(updated, encoding="utf-8")
    return patched


def _load_spec(path: Path) -> object:
    with open(path, encoding="utf-8") as f:
        if path.suffix == ".json":
            return json.load(f)
        import yaml

        return yaml.safe_load(f)


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"]).resolve()
    spec_path = context.get("bundled_spec_path") or context.get("spec_path")
    if not spec_path:
        raise SystemExit("hook 0450: no spec path in context")
    schemas = _get(_get(_load_spec(Path(spec_path)), "components"), "schemas")
    if not isinstance(schemas, dict):
        raise SystemExit(f"hook 0450: no components.schemas in {spec_path}")

    nullable = derive_nullable_fields({str(k): v for k, v in schemas.items()})
    patched = apply(out_dir / "camunda_orchestration_sdk" / "models", nullable)
    print(
        f"[0450_tolerant_nullable_pop] {sum(map(len, nullable.values()))} nullable field(s) "
        f"in {len(nullable)} schema(s); defaulted {patched} bare d.pop() call(s)"
    )
