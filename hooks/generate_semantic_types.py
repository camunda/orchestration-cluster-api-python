from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.replace("__", "_").lower()


def _is_primitive_alias(name: str, schema: Dict[str, Any]) -> bool:
    if not isinstance(schema, dict):
        return False
    t = schema.get("type")
    if t in {"string", "integer", "number", "boolean"}:
        return True
    # Some aliases use allOf: [$ref: LongKey] without repeating type
    # Treat anything with x-semantic-type as an alias
    if "x-semantic-type" in schema:
        return True
    return False


def _extract_constraints(schema: Dict[str, Any]) -> Dict[str, Any]:
    constraints: Dict[str, Any] = {}
    for key in [
        "pattern",
        "minLength",
        "maxLength",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "format",
        "enum",
    ]:
        if key in schema:
            constraints[key] = schema[key]
    return constraints


def _emit_semantic_types_py(out_dir: Path, aliases: Dict[str, Dict[str, Any]]) -> None:
    pkg_dir = out_dir / "camunda_orchestration_sdk"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    target = pkg_dir / "semantic_types.py"

    lines = []
    lines.append("from __future__ import annotations\n")
    lines.append("from typing import NewType, Any, Tuple\n")
    lines.append("import re\n\n")

    for alias_name, info in sorted(aliases.items()):
        base = info.get("type", "string")
        py_base = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
        }.get(base, "str")
        constraints = info.get("constraints", {})

        lines.append(f"{alias_name} = NewType('{alias_name}', {py_base})\n")

        # lifter with validation
        func = []
        func_name = _snake(f"lift_{alias_name}")
        func.append(f"def {func_name}(value: Any) -> {alias_name}:\n")
        func.append(f"\tif not isinstance(value, {py_base}):\n")
        func.append(f"\t\traise TypeError(\"{alias_name} must be {py_base}\")\n")
        pattern = constraints.get("pattern")
        if pattern and isinstance(pattern, str):
            # Use fullmatch to validate the whole value
            func.append(f"\tif re.fullmatch(r{pattern!r}, value) is None:\n")
            func.append(f"\t\traise ValueError(\"{alias_name} does not match pattern {pattern}\")\n")
        if "minLength" in constraints:
            func.append(f"\tif len(value) < {int(constraints['minLength'])}:\n")
            func.append(f"\t\traise ValueError(\"{alias_name} shorter than minLength {int(constraints['minLength'])}\")\n")
        if "maxLength" in constraints:
            func.append(f"\tif len(value) > {int(constraints['maxLength'])}:\n")
            func.append(f"\t\traise ValueError(\"{alias_name} longer than maxLength {int(constraints['maxLength'])}\")\n")
        if base in {"integer", "number"}:
            if "minimum" in constraints:
                func.append(f"\tif value < {constraints['minimum']}:\n")
                func.append(f"\t\traise ValueError(\"{alias_name} smaller than minimum {constraints['minimum']}\")\n")
            if "maximum" in constraints:
                func.append(f"\tif value > {constraints['maximum']}:\n")
                func.append(f"\t\traise ValueError(\"{alias_name} larger than maximum {constraints['maximum']}\")\n")
        if "enum" in constraints and isinstance(constraints["enum"], list):
            enum_vals = constraints["enum"]
            func.append(f"\tif value not in {enum_vals!r}:\n")
            func.append(f"\t\traise ValueError(\"{alias_name} must be one of {enum_vals}\")\n")
        func.append(f"\treturn {alias_name}(value)\n\n")

        # try_lift variant returning (ok, value_or_error)
        try_func_name = _snake(f"try_lift_{alias_name}")
        func.append(f"def {try_func_name}(value: Any) -> Tuple[bool, {alias_name} | Exception]:\n")
        func.append(f"\ttry:\n")
        func.append(f"\t\treturn True, {func_name}(value)\n")
        func.append(f"\texcept Exception as e:\n")
        func.append(f"\t\treturn False, e\n\n")

        lines.extend(func)

    target.write_text("".join(lines), encoding="utf-8")

    # Update package __init__ to export these aliases and lifters
    init_file = pkg_dir / "__init__.py"
    if init_file.exists():
        init_txt = init_file.read_text(encoding="utf-8")
        export_line = "from camunda_orchestration_sdk.semantic_types import *\n"
        if export_line not in init_txt:
            init_txt += "\n" + export_line
            init_file.write_text(init_txt, encoding="utf-8")


def run(context: Dict[str, Any]) -> None:
    spec_path = Path(context["spec_path"]).resolve()
    out_dir = Path(context["out_dir"]).resolve()

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    components = (spec or {}).get("components", {})
    schemas = components.get("schemas", {})
    aliases: Dict[str, Dict[str, Any]] = {}

    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            continue
        if _is_primitive_alias(name, schema):
            alias_info = {
                "type": schema.get("type", "string"),
                "constraints": _extract_constraints(schema),
            }
            aliases[name] = alias_info

    if aliases:
        _emit_semantic_types_py(out_dir, aliases)


