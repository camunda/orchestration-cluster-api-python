"""Pre-gen hook: make ``nullable`` explicit on shapes openapi-python-client ignores it on.

The generator converts OpenAPI 3.0 ``nullable: true`` into a 3.1 null type for most schemas,
but drops it in two shapes the bundled spec uses (issue #300):

* an inline enum, which it only treats as nullable when ``null`` is one of the ``enum`` values
  (and adding ``null`` there makes it emit nested ``...Type1 | ...Type2Type1`` unions);
* ``type`` beside ``oneOf``/``anyOf``, where its conversion takes the ``type`` branch and the
  union never gains a null member.

Those fields were generated non-optional, so an explicit ``null`` (which the gateway always
sends since 8.9) failed the whole response with ``ValueError``. This hook rewrites both into
shapes the generator already handles:

* the inline enum is lifted into a named schema called ``<Schema><Field>`` (the name the
  generator gave the inline enum, so the public enum class keeps its name) and the property
  becomes ``nullable`` + ``allOf: [$ref]``;
* the redundant ``type`` beside the union is dropped.

Runs after 0100, which inlines referenced enums into the properties that use them.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

import yaml

Json: TypeAlias = "dict[str, Json] | list[Json] | str | int | float | bool | None"

_REF_PREFIX = "#/components/schemas/"


def _is_nullable_enum(node: Json) -> bool:
    return isinstance(node, dict) and node.get("nullable") is True and "enum" in node


def _lift_enum(
    schemas: dict[str, Json], owner: str, field: str, prop: dict[str, Json]
) -> dict[str, Json]:
    name = owner + field[:1].upper() + field[1:]
    lifted = {k: v for k, v in prop.items() if k != "nullable"}
    existing = schemas.get(name)
    if existing is not None and existing != lifted:
        raise SystemExit(
            f"hook 0150: cannot lift nullable enum {owner}.{field} to {name}; "
            "a different schema already has that name."
        )
    schemas[name] = lifted
    out: dict[str, Json] = {"nullable": True, "allOf": [{"$ref": _REF_PREFIX + name}]}
    for doc_key in ("description", "example"):
        if doc_key in prop:
            out[doc_key] = prop[doc_key]
    return out


def lift_nullable_enums(schemas: dict[str, Json]) -> int:
    """Lift every nullable inline enum on a component's properties; return how many."""
    lifted = 0
    for owner in list(schemas):
        schema = schemas[owner]
        if not isinstance(schema, dict):
            continue
        all_of = schema.get("allOf")
        parts = [schema] + (
            [p for p in all_of if isinstance(p, dict)] if isinstance(all_of, list) else []
        )
        for part in parts:
            props = part.get("properties")
            if not isinstance(props, dict):
                continue
            for field, prop in list(props.items()):
                if isinstance(prop, dict) and _is_nullable_enum(prop):
                    props[field] = _lift_enum(schemas, owner, field, prop)
                    lifted += 1
    return lifted


def drop_type_beside_nullable_union(node: Json) -> int:
    """Drop ``type`` where it sits beside a nullable ``oneOf``/``anyOf``; return how many."""
    changed = 0
    if isinstance(node, dict):
        union = node.get("oneOf") or node.get("anyOf")
        if node.get("nullable") is True and "type" in node and union:
            del node["type"]
            changed += 1
        for value in node.values():
            changed += drop_type_beside_nullable_union(value)
    elif isinstance(node, list):
        for item in node:
            changed += drop_type_beside_nullable_union(item)
    return changed


def _remaining_nullable_enums(node: Json, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        if _is_nullable_enum(node):
            found.append(path or "/")
        for key, value in node.items():
            found += _remaining_nullable_enums(value, f"{path}/{key}")
    elif isinstance(node, list):
        for i, item in enumerate(node):
            found += _remaining_nullable_enums(item, f"{path}/{i}")
    return found


def make_nullable_explicit(spec: dict[str, Json]) -> int:
    """Rewrite every ignored-nullable shape in ``spec`` in place; return how many changed."""
    components = spec.get("components")
    schemas = components.get("schemas") if isinstance(components, dict) else None
    if not isinstance(schemas, dict):
        raise SystemExit("hook 0150: spec has no components.schemas")
    changed = lift_nullable_enums(schemas) + drop_type_beside_nullable_union(spec)
    leftover = _remaining_nullable_enums(spec)
    if leftover:
        raise SystemExit(
            f"hook 0150: nullable enums in places this hook cannot lift: {leftover}. "
            "The generator would type them non-optional; teach the hook this placement."
        )
    return changed


def run(context: dict[str, str]) -> None:
    spec_path = Path(context["bundled_spec_path"])
    with open(spec_path, encoding="utf-8") as f:
        spec: dict[str, Json] = yaml.safe_load(f)

    changed = make_nullable_explicit(spec)
    if changed:
        with open(spec_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(spec, f, sort_keys=False, allow_unicode=True)
    print(f"[0150_nullable_enums_and_unions] made nullable explicit on {changed} schema(s)")
