"""Post-gen hook: decode nullable enum references strictly.

For a property that is ``nullable`` + ``allOf: [$ref: <enum>]`` (the shape pre-gen hook 0150
lifts nullable inline enums into), openapi-python-client emits a union parser that tries the enum
and, on failure, falls back to ``cast(<Enum> | None, data)``. Any unknown string or non-string
then decodes into a field typed as the enum, where a non-nullable enum field raises
``ValueError``. This rewrites each such parser to return ``None`` for ``None`` and otherwise
call the enum constructor, so only the nullability differs from a non-nullable enum field.

Runs before 1250, which drops the ``cast`` import where it becomes unused.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TypeAlias

import yaml
from openapi_python_client.utils import ClassName, PythonIdentifier, snake_case

Json: TypeAlias = "dict[str, Json] | list[Json] | str | int | float | bool | None"

_REF_PREFIX = "#/components/schemas/"


def nullable_enum_refs(schemas: dict[str, Json]) -> list[tuple[str, str, str]]:
    """(owning schema, wire field, enum schema) for every nullable single-``allOf`` enum ref."""
    found: list[tuple[str, str, str]] = []
    for owner, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        props = schema.get("properties")
        if not isinstance(props, dict):
            continue
        for wire, prop in props.items():
            if not isinstance(prop, dict) or prop.get("nullable") is not True:
                continue
            parts = prop.get("allOf")
            if not isinstance(parts, list) or len(parts) != 1 or not isinstance(parts[0], dict):
                continue
            ref = parts[0].get("$ref")
            if not isinstance(ref, str) or not ref.startswith(_REF_PREFIX):
                continue
            target = schemas.get(ref[len(_REF_PREFIX) :])
            if isinstance(target, dict) and "enum" in target:
                found.append((owner, wire, ref[len(_REF_PREFIX) :]))
    return found


def make_strict(source: str, attr: str, enum_class: str) -> str:
    """Replace ``_parse_<attr>``'s lenient fallback with a strict enum constructor. Idempotent."""
    strict = (
        f"        def _parse_{attr}(data: object) -> {enum_class} | None:\n"
        "            if data is None:\n"
        "                return data\n"
        f"            return {enum_class}(data)\n"
    )
    if strict in source:
        return source
    lenient = re.compile(
        rf"        def _parse_{re.escape(attr)}\(.*?"
        rf"            return cast\({re.escape(enum_class)} \| None, data\)\n",
        re.S,
    )
    match = lenient.search(source)
    # ruff may already have wrapped the constructor call as `Enum(\n    data\n)`.
    constructs = match is not None and re.search(
        rf"{re.escape(enum_class)}\(\s*data\s*\)", match.group(0)
    )
    if match is None or not constructs:
        raise SystemExit(
            f"hook 1220: _parse_{attr} is not the expected nullable {enum_class} parser; "
            "it would keep accepting values outside the enum."
        )
    return source[: match.start()] + strict + source[match.end() :]


def run(context: dict[str, str]) -> None:
    with open(context["bundled_spec_path"], encoding="utf-8") as f:
        spec: dict[str, Json] = yaml.safe_load(f)
    components = spec.get("components")
    schemas = components.get("schemas") if isinstance(components, dict) else None
    if not isinstance(schemas, dict):
        raise SystemExit("hook 1220: spec has no components.schemas")

    models = Path(context["out_dir"]) / "camunda_orchestration_sdk" / "models"
    refs = nullable_enum_refs(schemas)
    for owner, wire, enum_schema in refs:
        module = models / f"{snake_case(ClassName(owner, prefix=''))}.py"
        source = module.read_text(encoding="utf-8")
        attr = PythonIdentifier(wire, prefix="field_")
        updated = make_strict(source, attr, ClassName(enum_schema, prefix=""))
        if updated != source:
            module.write_text(updated, encoding="utf-8")
    print(f"[1220_strict_nullable_enums] {len(refs)} nullable enum field(s) decode strictly")
