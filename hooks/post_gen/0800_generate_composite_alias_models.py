from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, Optional, cast

import yaml


def _snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.replace("__", "_").lower()


def _resolve_ref(schemas: Dict[str, Any], ref: str) -> Optional[Dict[str, Any]]:
    if not ref.startswith("#/components/schemas/"):
        return None
    name = ref.split("/")[-1]
    return schemas.get(name)


def _emit_array_alias_model(models_dir: Path, alias: str, item_schema: Dict[str, Any], array_schema: Dict[str, Any]) -> None:
    filename = models_dir / f"{_snake(alias)}.py"

    # Determine python base type for item
    item_type = item_schema.get("type", "string")
    py_item = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
    }.get(item_type, "str")

    # Use semantic type if available (e.g. Tag instead of str)
    semantic_type = item_schema.get("x-semantic-type")
    if isinstance(semantic_type, str):
        py_item = semantic_type

    pattern = item_schema.get("pattern") if item_type == "string" else None
    min_len = item_schema.get("minLength") if item_type == "string" else None
    max_len = item_schema.get("maxLength") if item_type == "string" else None
    enum_vals = item_schema.get("enum") if isinstance(item_schema.get("enum"), list) else None

    unique_items = bool(array_schema.get("uniqueItems", False))
    min_items = array_schema.get("minItems")
    max_items = array_schema.get("maxItems")

    lines: list[str] = []
    lines.append("from __future__ import annotations\n")
    lines.append("import re\n")
    lines.append("from pydantic import RootModel, field_validator\n")
    if semantic_type:
        lines.append(f"\nfrom ..semantic_types import {py_item}\n")
    lines.append(f"\n\nclass {alias}(RootModel[list[{py_item}]]):\n")

    # Array-level validation
    lines.append("\t@field_validator('root')\n")
    lines.append("\t@classmethod\n")
    lines.append(f"\tdef _validate_array(cls, v: list[{py_item}]) -> list[{py_item}]:\n")
    if min_items is not None:
        lines.append(f"\t\tif len(v) < {int(min_items)}: raise ValueError('minItems {int(min_items)}')\n")
    if max_items is not None:
        lines.append(f"\t\tif len(v) > {int(max_items)}: raise ValueError('maxItems {int(max_items)}')\n")
    if unique_items:
        lines.append("\t\tif len(v) != len(set(v)): raise ValueError('uniqueItems violated')\n")

    # Item-level validation
    if pattern or min_len is not None or max_len is not None or enum_vals is not None:
        if pattern:
            lines.append(f"\t\t_pat = re.compile(r{pattern!r})\n")
        lines.append("\t\tfor _i, _x in enumerate(v):\n")
        if pattern:
            lines.append("\t\t\tif _pat.fullmatch(str(_x)) is None: raise ValueError(f'item {{_i}} pattern mismatch')\n")
        if min_len is not None:
            lines.append(f"\t\t\tif len(str(_x)) < {int(min_len)}: raise ValueError(f'item {{_i}} minLength {int(min_len)}')\n")
        if max_len is not None:
            lines.append(f"\t\t\tif len(str(_x)) > {int(max_len)}: raise ValueError(f'item {{_i}} maxLength {int(max_len)}')\n")
        if enum_vals is not None:
            lines.append(f"\t\t\tif _x not in {enum_vals!r}: raise ValueError(f'item {{_i}} not in enum')\n")

    lines.append("\t\treturn v\n")

    filename.write_text("".join(lines), encoding="utf-8")


def run(context: dict[str, str]) -> None:
    spec_path = Path(context["spec_path"]).resolve()
    out_dir = Path(context["out_dir"]).resolve()
    models_dir = out_dir / "camunda_orchestration_sdk" / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    with open(spec_path, "r", encoding="utf-8") as f:
        spec: dict[str, Any] | None = yaml.safe_load(f)

    schemas: Dict[str, Any] = (spec or {}).get("components", {}).get("schemas", {})

    for name, schema_val in schemas.items():
        if not isinstance(schema_val, dict):
            continue
        schema = cast(dict[str, Any], schema_val)
        if schema.get("type") == "array" and "items" in schema:
            items: dict[str, Any] = cast(dict[str, Any], schema["items"])
            item_schema: Optional[Dict[str, Any]] = None
            if "$ref" in items:
                item_schema = _resolve_ref(schemas, items["$ref"]) or {}
            else:
                item_schema = items
            # Only synthesize when item resolves to a primitive alias or primitive
            base_type = item_schema.get("type")
            if base_type in {"string", "integer", "number", "boolean"} or "x-semantic-type" in item_schema:
                _emit_array_alias_model(models_dir, name, item_schema, schema)








