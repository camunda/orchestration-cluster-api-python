"""Pre-gen hook: Strip ``default`` values from optional schema properties.

When the OpenAPI spec declares ``default`` on an optional property, the
generator emits the default eagerly in the Python field declaration.  This
means the SDK always sends the value on the wire — even when the user never
set it — which breaks forward-compatibility with older servers that reject
unknown properties (``additionalProperties: false``).

This hook:
1. Walks every schema property and query parameter in the spec.
2. Records the ``default`` value.
3. Appends a ``Server default: <value>`` note to the ``description`` so
   the information is still visible in docstrings.
4. Removes the ``default`` key so the generator falls through to ``UNSET``.

It also strips ``default`` from top-level enum schemas (e.g.
``TenantFilterEnum``) to prevent the generator from inheriting the value
when a property references the enum via ``$ref``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import yaml


def _append_server_default(description: str, default_value: object) -> str:
    """Append server default info to an existing description."""
    note = f"Server default: {default_value}"
    if description:
        return f"{description} {note}."
    return f"{note}."


def _strip_property_defaults(spec: dict[str, Any]) -> int:
    """Strip ``default`` from all optional schema properties.  Returns count."""
    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})
    count = 0

    for schema in list(schemas.values()):
        if not isinstance(schema, dict):
            continue
        schema = cast(dict[str, Any], schema)
        props: dict[str, Any] | None = schema.get("properties")
        if not isinstance(props, dict):
            continue
        required: set[str] = set(cast(list[str], schema.get("required", [])))

        for prop_name in list(props):
            prop: Any = props[prop_name]
            if not isinstance(prop, dict):
                continue
            prop = cast(dict[str, Any], prop)
            if prop_name in required:
                continue
            if "default" not in prop:
                continue

            default_val: object = prop.pop("default")
            existing_desc: str = cast(str, prop.get("description", ""))
            prop["description"] = _append_server_default(existing_desc, default_val)
            count += 1

    return count


def _strip_enum_schema_defaults(spec: dict[str, Any]) -> int:
    """Strip ``default`` from top-level enum schemas.  Returns count."""
    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})
    count = 0

    for _name in list(schemas):
        schema: Any = schemas[_name]
        if not isinstance(schema, dict):
            continue
        schema = cast(dict[str, Any], schema)
        if "enum" in schema and "default" in schema:
            schema.pop("default")
            count += 1

    return count


def _strip_parameter_defaults(spec: dict[str, Any]) -> int:
    """Strip ``default`` from query/path parameter schemas.  Returns count."""
    paths: dict[str, Any] = spec.get("paths", {})
    count = 0

    for methods in list(paths.values()):
        if not isinstance(methods, dict):
            continue
        methods = cast(dict[str, Any], methods)
        for op in list(methods.values()):
            if not isinstance(op, dict):
                continue
            op = cast(dict[str, Any], op)
            params: list[Any] = cast(list[Any], op.get("parameters", []))
            for param in params:
                if not isinstance(param, dict):
                    continue
                param = cast(dict[str, Any], param)
                param_schema: Any = param.get("schema", {})
                if not isinstance(param_schema, dict):
                    continue
                param_schema = cast(dict[str, Any], param_schema)
                if "default" not in param_schema:
                    continue

                default_val: object = param_schema.pop("default")
                existing_desc: str = cast(str, param.get("description", ""))
                param["description"] = _append_server_default(
                    existing_desc, default_val
                )
                count += 1

    return count


def run(context: dict[str, str]) -> None:
    spec_path = Path(context["bundled_spec_path"])
    if not spec_path.exists():
        print(f"Spec file not found at {spec_path}")
        return

    with open(spec_path, "r") as f:
        spec: dict[str, Any] = yaml.safe_load(f)

    n_props = _strip_property_defaults(spec)
    n_enums = _strip_enum_schema_defaults(spec)
    n_params = _strip_parameter_defaults(spec)
    total = n_props + n_enums + n_params

    if total > 0:
        with open(spec_path, "w") as f:
            yaml.safe_dump(spec, f, sort_keys=False, allow_unicode=True)
        print(
            f"Stripped {total} defaults from spec "
            f"({n_props} properties, {n_enums} enum schemas, {n_params} parameters)"
        )
    else:
        print("No defaults found to strip")
