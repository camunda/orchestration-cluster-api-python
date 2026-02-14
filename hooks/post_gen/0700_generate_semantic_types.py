from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, cast

import yaml


def _snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.replace("__", "_").lower()


def _is_primitive_alias(name: str, schema: Dict[str, Any]) -> bool:
    if not isinstance(schema, dict): # type: ignore
        return False
    t = schema.get("type")
    if t in {"string", "integer", "number", "boolean"}:
        return True
    # Some aliases use allOf: [$ref: LongKey] without repeating type
    # Treat anything with x-semantic-type as an alias
    if "x-semantic-type" in schema:
        return True
    return False


def _extract_constraints(schema: Dict[str, Any], schemas: Dict[str, Any]) -> Dict[str, Any]:
    constraints: Dict[str, Any] = {}

    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/components/schemas/"):
            ref_name = ref.split("/")[-1]
            if ref_name in schemas:
                constraints.update(_extract_constraints(schemas[ref_name], schemas))

    if "allOf" in schema:
        for sub_schema in schema["allOf"]:
            constraints.update(_extract_constraints(sub_schema, schemas))

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

    lines: List[str] = []
    lines.append("from __future__ import annotations\n")
    lines.append("from typing import NewType, Any, Tuple\n")
    lines.append("import re\n\n")

    # Track all exported names for __all__ and explicit import
    all_exported_names: List[str] = []

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

        # Track exported names
        func_name = _snake(f"lift_{alias_name}")
        try_func_name = _snake(f"try_lift_{alias_name}")
        all_exported_names.extend([alias_name, func_name, try_func_name])

        # lifter with validation
        func: List[str] = []
        func_name = _snake(f"lift_{alias_name}")
        func.append(f"def {func_name}(value: Any) -> {alias_name}:\n")
        func.append(f"\tif not isinstance(value, {py_base}):\n")
        func.append(f"\t\traise TypeError(f\"{alias_name} must be {py_base}, got {{type(value).__name__}}: {{value!r}}\")\n")
        pattern = constraints.get("pattern")
        if pattern and isinstance(pattern, str):
            # Use fullmatch to validate the whole value
            func.append(f"\tif re.fullmatch(r{pattern!r}, value) is None:\n")
            func.append(f"\t\traise ValueError(f\"{alias_name} does not match pattern {pattern!r}, got {{value!r}}\")\n")
        if "minLength" in constraints:
            func.append(f"\tif len(value) < {int(constraints['minLength'])}:\n")
            func.append(f"\t\traise ValueError(f\"{alias_name} shorter than minLength {int(constraints['minLength'])}, got {{value!r}}\")\n")
        if "maxLength" in constraints:
            func.append(f"\tif len(value) > {int(constraints['maxLength'])}:\n")
            func.append(f"\t\traise ValueError(f\"{alias_name} longer than maxLength {int(constraints['maxLength'])}, got {{value!r}}\")\n")
        if base in {"integer", "number"}:
            if "minimum" in constraints:
                func.append(f"\tif value < {constraints['minimum']}:\n")
                func.append(f"\t\traise ValueError(f\"{alias_name} smaller than minimum {constraints['minimum']}, got {{value!r}}\")\n")
            if "maximum" in constraints:
                func.append(f"\tif value > {constraints['maximum']}:\n")
                func.append(f"\t\traise ValueError(f\"{alias_name} larger than maximum {constraints['maximum']}, got {{value!r}}\")\n")
        if "enum" in constraints and isinstance(constraints["enum"], list):
            enum_vals = constraints["enum"]
            func.append(f"\tif value not in {enum_vals!r}:\n")
            func.append(f"\t\traise ValueError(f\"{alias_name} must be one of {enum_vals}, got {{value!r}}\")\n")
        func.append(f"\treturn {alias_name}(value)\n\n")

        # try_lift variant returning (ok, value_or_error)
        try_func_name = _snake(f"try_lift_{alias_name}")
        func.append(f"def {try_func_name}(value: Any) -> Tuple[bool, {alias_name} | Exception]:\n")
        func.append("\ttry:\n")
        func.append(f"\t\treturn True, {func_name}(value)\n")
        func.append("\texcept Exception as e:\n")
        func.append("\t\treturn False, e\n\n")

        lines.extend(func)

    # Add __all__ for explicit export control
    lines.append(f"__all__ = {sorted(all_exported_names)!r}\n")

    target.write_text("".join(lines), encoding="utf-8")

    # Update package __init__ to export these aliases and lifters with explicit import
    init_file = pkg_dir / "__init__.py"
    if init_file.exists():
        init_txt = init_file.read_text(encoding="utf-8")
        # Remove any existing wildcard import
        wildcard_line = "from camunda_orchestration_sdk.semantic_types import *\n"
        init_txt = init_txt.replace(wildcard_line, "")
        # Add explicit import
        export_names = ", ".join(sorted(all_exported_names))
        explicit_line = f"from camunda_orchestration_sdk.semantic_types import {export_names}\n"
        if explicit_line not in init_txt:
            init_txt += "\n" + explicit_line

        # Extend __all__ to include the semantic type names so pyright
        # considers them intentional re-exports.
        import re as _re
        # Support both tuple (__all__ = (...)) and list (__all__: list[str] = [...]) formats
        all_match = _re.search(r'__all__(?::\s*list\[str\])?\s*=\s*[\(\[]([^\)\]]*)[\)\]]', init_txt, _re.DOTALL)
        if all_match:
            existing_all = all_match.group(0)
            is_list = existing_all.rstrip().endswith("]")
            close_char = "]" if is_list else ")"
            # Build new entries
            quoted_names = [f'    "{n}",' for n in sorted(all_exported_names)]
            new_entries = "\n".join(quoted_names)
            # Replace the closing bracket/paren with the new entries + close
            new_all = existing_all.rstrip(close_char)
            new_all += "\n" + new_entries + "\n" + close_char
            init_txt = init_txt.replace(existing_all, new_all, 1)

        init_file.write_text(init_txt, encoding="utf-8")


def _load_spec_file(path: Path) -> Dict[str, Any] | None:
    """Load a spec file (YAML or JSON)."""
    import json as _json
    try:
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix == ".json":
                return _json.load(f)
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Failed to load {path}: {e}")
        return None


def _aliases_from_metadata(metadata_path: Path) -> Dict[str, Dict[str, Any]]:
    """Build aliases dict from spec-metadata.json semanticKeys."""
    import json as _json
    with open(metadata_path, "r", encoding="utf-8") as f:
        meta: Dict[str, Any] = _json.load(f)
    aliases: Dict[str, Dict[str, Any]] = {}
    for entry in meta.get("semanticKeys", []):
        name = entry["name"]
        constraints = entry.get("constraints", {})
        # Infer base type from constraints or default to string
        base_type = "string"
        if "minimum" in constraints or "maximum" in constraints:
            base_type = "integer"
        aliases[name] = {
            "type": base_type,
            "constraints": constraints,
        }
    return aliases


def _aliases_from_spec(spec_path: Path) -> Dict[str, Dict[str, Any]]:
    """Fallback: derive aliases by scanning the spec for x-semantic-type."""
    schemas: Dict[str, Any] = {}
    if spec_path.suffix == ".json":
        loaded = _load_spec_file(spec_path)
        if loaded:
            schemas = loaded.get("components", {}).get("schemas", {})
    else:
        for yaml_file in spec_path.parent.glob("*.yaml"):
            loaded = _load_spec_file(yaml_file)
            if loaded:
                file_schemas = loaded.get("components", {}).get("schemas", {})
                if file_schemas:
                    schemas.update(file_schemas)

    aliases: Dict[str, Dict[str, Any]] = {}
    for name, schema_val in schemas.items():
        if not isinstance(schema_val, dict):
            continue
        schema = cast(Dict[str, Any], schema_val)
        if _is_primitive_alias(name, schema):
            aliases[name] = {
                "type": schema.get("type", "string"),
                "constraints": _extract_constraints(schema, schemas),
            }
    return aliases


def run(context: dict[str, str]) -> None:
    out_dir = Path(context["out_dir"]).resolve()

    # Try metadata first (pre-computed by camunda-schema-bundler)
    metadata_path_str = context.get("metadata_path", "")
    metadata_path = Path(metadata_path_str) if metadata_path_str else None

    aliases: Dict[str, Dict[str, Any]] = {}
    if metadata_path and metadata_path.exists():
        print(f"Using spec-metadata.json for semantic types")
        aliases = _aliases_from_metadata(metadata_path)
    else:
        # Fallback: scan spec
        spec_path = Path(context["spec_path"]).resolve()
        bundled_spec_path = context.get("bundled_spec_path", "")
        bp = Path(bundled_spec_path).resolve() if bundled_spec_path else spec_path
        aliases = _aliases_from_spec(bp)

    if aliases:
        _emit_semantic_types_py(out_dir, aliases)


