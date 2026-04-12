from __future__ import annotations
import re
from pathlib import Path
from typing import Any, Dict, List, cast

import yaml

# Unicode property escapes (ECMAScript) -> Python re equivalents
_UNICODE_PROPERTY_MAP: Dict[str, str] = {
    r"\p{L}": r"\w",
    r"\p{N}": r"0-9",
}


def _convert_unicode_regex(pattern: str) -> str:
    """Convert Unicode property escapes to Python-compatible regex."""
    result = pattern
    for esc, replacement in _UNICODE_PROPERTY_MAP.items():
        result = result.replace(esc, replacement)
    return result


def _snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace("__", "_").lower()


def _is_primitive_alias(name: str, schema: Dict[str, Any]) -> bool:
    if not isinstance(schema, dict):  # type: ignore
        return False
    t = schema.get("type")
    if t in {"string", "integer", "number", "boolean"}:
        return True
    # Some aliases use allOf: [$ref: LongKey] without repeating type
    # Treat anything with x-semantic-type as an alias
    if "x-semantic-type" in schema:
        return True
    return False


def _extract_constraints(
    schema: Dict[str, Any], schemas: Dict[str, Any]
) -> Dict[str, Any]:
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
    if "pattern" in constraints and isinstance(constraints["pattern"], str):
        constraints["pattern"] = _convert_unicode_regex(constraints["pattern"])
    return constraints


def _emit_semantic_types_py(
    out_dir: Path,
    aliases: Dict[str, Dict[str, Any]],
    union_aliases: Dict[str, List[str]] | None = None,
) -> None:
    pkg_dir = out_dir / "camunda_orchestration_sdk"
    pkg_dir.mkdir(parents=True, exist_ok=True)
    target = pkg_dir / "semantic_types.py"

    lines: List[str] = []
    lines.append("from __future__ import annotations\n")
    lines.append("from typing import Any, Tuple, Union\n")
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

        # Class definition with __new__ containing validation
        class_def: List[str] = []
        class_def.append(f"class {alias_name}({py_base}):\n")
        class_def.append(f'\tdef __new__(cls, value: {py_base}) -> "{alias_name}":\n')
        
        # Type check (always first)
        class_def.append(f'\t\tif not isinstance(value, {py_base}):  # pyright: ignore[reportUnnecessaryIsInstance]\n')
        class_def.append(
            f'\t\t\traise TypeError(f"{alias_name} must be {py_base}, got {{type(value).__name__}}: {{value!r}}")\n'
        )
        
        # Pattern validation
        pattern = constraints.get("pattern")
        if pattern and isinstance(pattern, str):
            class_def.append(f'\t\tif re.fullmatch({pattern!r}, value) is None:\n')
            class_def.append(f'\t\t\tpat = {pattern!r}\n')
            class_def.append(
                f'\t\t\traise ValueError(f"{alias_name} does not match pattern {{pat!r}}, got {{value!r}}")\n'
            )
        
        # Length constraints (for string-like types)
        if py_base == "str":
            if "minLength" in constraints:
                min_len = int(constraints["minLength"])
                class_def.append(f'\t\tif len(value) < {min_len}:\n')
                class_def.append(
                    f'\t\t\traise ValueError(f"{alias_name} shorter than minLength {min_len}, got {{value!r}}")\n'
                )
            if "maxLength" in constraints:
                max_len = int(constraints["maxLength"])
                class_def.append(f'\t\tif len(value) > {max_len}:\n')
                class_def.append(
                    f'\t\t\traise ValueError(f"{alias_name} longer than maxLength {max_len}, got {{value!r}}")\n'
                )
        
        # Numeric constraints
        if py_base in {"int", "float"}:
            if "minimum" in constraints:
                class_def.append(f'\t\tif value < {constraints["minimum"]}:\n')
                class_def.append(
                    f'\t\t\traise ValueError(f"{alias_name} smaller than minimum {constraints["minimum"]}, got {{value!r}}")\n'
                )
            if "maximum" in constraints:
                class_def.append(f'\t\tif value > {constraints["maximum"]}:\n')
                class_def.append(
                    f'\t\t\traise ValueError(f"{alias_name} larger than maximum {constraints["maximum"]}, got {{value!r}}")\n'
                )
        
        # Enum constraints
        if "enum" in constraints and isinstance(constraints["enum"], list):
            enum_vals = constraints["enum"]
            class_def.append(f'\t\tif value not in {enum_vals!r}:\n')
            class_def.append(
                f'\t\t\traise ValueError(f"{alias_name} must be one of {enum_vals}, got {{value!r}}")\n'
            )
        
        # Call parent class constructor
        class_def.append('\t\treturn super().__new__(cls, value)\n\n')
        
        lines.extend(class_def)

        # Track exported names (class only; no lifter functions for concrete types)
        all_exported_names.append(alias_name)

    # Emit union type aliases (e.g. ScopeKey = ProcessInstanceKey | ElementInstanceKey)
    if union_aliases:
        for union_name, branch_names in sorted(union_aliases.items()):
            func_name = _snake(f"lift_{union_name}")
            try_func_name = _snake(f"try_lift_{union_name}")
            all_exported_names.extend([union_name, func_name, try_func_name])

            lines.append(f"{union_name} = Union[{', '.join(branch_names)}]\n\n")

            lines.append(f"def {func_name}(value: Any) -> {union_name}:\n")
            for branch in branch_names:
                lines.append("\ttry:\n")
                lines.append(f"\t\treturn {branch}(value)\n")
                lines.append("\texcept Exception:\n")
                lines.append("\t\tpass\n")
            lines.append(
                f'\traise ValueError(f"{union_name}: value {{value!r}} does not match any branch ({", ".join(branch_names)})")\n\n'
            )

            lines.append(
                f"def {try_func_name}(value: Any) -> Tuple[bool, {union_name} | Exception]:\n"
            )
            lines.append("\ttry:\n")
            lines.append(f"\t\treturn True, {func_name}(value)\n")
            lines.append("\texcept Exception as e:\n")
            lines.append("\t\treturn False, e\n\n")

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
        explicit_line = (
            f"from camunda_orchestration_sdk.semantic_types import {export_names}\n"
        )
        if explicit_line not in init_txt:
            init_txt += "\n" + explicit_line

        # Extend __all__ to include the semantic type names so pyright
        # considers them intentional re-exports.
        import re as _re

        # Support both tuple (__all__ = (...)) and list (__all__: list[str] = [...]) formats
        all_match = _re.search(
            r"__all__(?::\s*list\[str\])?\s*=\s*[\(\[]([^\)\]]*)[\)\]]",
            init_txt,
            _re.DOTALL,
        )
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
        if "pattern" in constraints and isinstance(constraints["pattern"], str):
            constraints["pattern"] = _convert_unicode_regex(constraints["pattern"])
        # Infer base type from constraints or default to string
        base_type = "string"
        if "minimum" in constraints or "maximum" in constraints:
            base_type = "integer"
        aliases[name] = {
            "type": base_type,
            "constraints": constraints,
        }
    return aliases


def _semantic_key_unions_from_metadata(
    metadata_path: Path, semantic_key_names: set[str]
) -> Dict[str, List[str]]:
    """Build union aliases dict from spec-metadata.json unions where all branches are semantic keys."""
    import json as _json

    with open(metadata_path, "r", encoding="utf-8") as f:
        meta: Dict[str, Any] = _json.load(f)
    union_aliases: Dict[str, List[str]] = {}
    for entry in meta.get("unions", []):
        branches = entry.get("branches", [])
        if branches and all(
            b.get("branchType") == "ref" and b.get("ref") in semantic_key_names
            for b in branches
        ):
            union_aliases[entry["name"]] = [b["ref"] for b in branches]
    return union_aliases


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
    union_aliases: Dict[str, List[str]] = {}
    if metadata_path and metadata_path.exists():
        print("Using spec-metadata.json for semantic types")
        aliases = _aliases_from_metadata(metadata_path)
        union_aliases = _semantic_key_unions_from_metadata(
            metadata_path, set(aliases.keys())
        )
    else:
        # Fallback: scan spec
        spec_path = Path(context["spec_path"]).resolve()
        bundled_spec_path = context.get("bundled_spec_path", "")
        bp = Path(bundled_spec_path).resolve() if bundled_spec_path else spec_path
        aliases = _aliases_from_spec(bp)

    if aliases:
        _emit_semantic_types_py(out_dir, aliases, union_aliases or None)
