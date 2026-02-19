import re
from pathlib import Path
from typing import Any, Dict, cast

import yaml


def _snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace("__", "_").lower()


def _extract_semantic_mappings(data: Any, mappings: Dict[str, str]) -> None:
    """
    Recursively traverse the spec to find all properties with x-semantic-type.
    Populates mappings dict with {json_property_name: semantic_type_name}.
    """
    if isinstance(data, dict):
        data_dict = cast(dict[str, Any], data)
        for key, value in data_dict.items():
            if key == "properties" and isinstance(value, dict):
                props_dict = cast(dict[str, Any], value)
                for prop_name, prop_schema in props_dict.items():
                    if (
                        isinstance(prop_schema, dict)
                        and "x-semantic-type" in prop_schema
                    ):
                        prop_schema_dict = cast(dict[str, Any], prop_schema)
                        semantic_type = prop_schema_dict.get("x-semantic-type")
                        if isinstance(semantic_type, str):
                            mappings[prop_name] = semantic_type
                    # Recurse into properties
                    _extract_semantic_mappings(prop_schema, mappings)
            elif isinstance(value, (dict, list)):
                _extract_semantic_mappings(value, mappings)
    elif isinstance(data, list):
        data_list = cast(list[Any], data)
        for item in data_list:
            _extract_semantic_mappings(item, mappings)


def _patch_model_file(file_path: Path, semantic_mappings: Dict[str, str]) -> None:
    if not file_path.exists():
        return

    content = file_path.read_text(encoding="utf-8")
    original_content = content

    # We need to find which properties in this file match our semantic mappings.
    # We can scan the content for "    prop_name: type" patterns.

    # 1. Identify fields to patch in this file
    # We look for lines like: "    process_definition_key: str"
    # We convert the python property name back to potential json names?
    # Or better: we iterate over our known semantic mappings, convert them to snake_case,
    # and check if they exist in the file as a field definition.

    fields_to_patch: list[tuple[str, str, str]] = []

    for json_prop, semantic_type in semantic_mappings.items():
        py_prop = _snake(json_prop)

        # Check if this property is defined in the file as a simple type
        # Regex: indentation, py_prop, colon, type (str/int/etc), newline
        # We want to be careful not to match things that are already patched or complex types

        # We'll use a regex that we'll use for replacement anyway.
        pattern = re.compile(
            rf"^(\s+){py_prop}: ((?:None \| )?(?:str|int|float|bool))(.*)$",
            re.MULTILINE,
        )
        if pattern.search(content):
            fields_to_patch.append((json_prop, py_prop, semantic_type))

    if not fields_to_patch:
        return

    # 2. Build explicit import for only the semantic types used in this file
    types_needed: set[str] = set()
    lifters_needed: set[str] = set()
    for _json_prop, _py_prop, semantic_type in fields_to_patch:
        types_needed.add(semantic_type)
        lifters_needed.add(_snake(f"lift_{semantic_type}"))
    all_names = sorted(types_needed | lifters_needed)
    import_line = (
        f"from camunda_orchestration_sdk.semantic_types import {', '.join(all_names)}"
    )

    # Remove any existing wildcard import first
    content = content.replace(
        "from camunda_orchestration_sdk.semantic_types import *\n", ""
    )

    if import_line not in content:
        if "from __future__ import annotations" in content:
            content = content.replace(
                "from __future__ import annotations\n",
                "from __future__ import annotations\n" + import_line + "\n",
            )
        else:
            content = import_line + "\n" + content

    # 3. Apply patches
    for json_prop, py_prop, semantic_type in fields_to_patch:
        lifter_name = _snake(f"lift_{semantic_type}")

        # Patch type hint
        type_hint_pattern = re.compile(
            rf"^(\s+){py_prop}: ((?:None \| )?(?:str|int|float|bool))(.*)$",
            re.MULTILINE,
        )

        def type_hint_replacer(match: re.Match[str]) -> str:
            indent = match.group(1)
            old_type = match.group(2)
            rest = match.group(3)
            if old_type.startswith("None | "):
                return f"{indent}{py_prop}: None | {semantic_type}{rest}"
            return f"{indent}{py_prop}: {semantic_type}{rest}"

        content = type_hint_pattern.sub(type_hint_replacer, content)

        # Patch from_dict
        # Pattern: indentation, py_prop, =, d.pop("json_prop")
        # We capture the d.pop(...) part to wrap it.

        # Note: json_prop in the regex needs to be escaped if it contains special chars, but usually it doesn't.
        pop_pattern = re.compile(rf'(\s+){py_prop} = (d\.pop\("{json_prop}"[^)]*\))')

        def pop_replacer(match: re.Match[str]) -> str:
            indent = match.group(1)
            pop_call = match.group(2)

            # Check for default value in d.pop
            # We look for ", default_value)" at the end of the pop call
            default_match = re.search(r", ([^)]+)\)$", pop_call)

            if default_match:
                default_val = default_match.group(1)
                # Use walrus operator to capture value and check against default
                return f"{indent}{py_prop} = {lifter_name}(_val) if (_val := {pop_call}) is not {default_val} else {default_val}"

            return f"{indent}{py_prop} = {lifter_name}({pop_call})"

        # Check if already lifted to avoid double patching
        if (
            f"{lifter_name}(d.pop" not in content
            and f"{lifter_name}(_val)" not in content
        ):
            content = pop_pattern.sub(pop_replacer, content)

        # Also handle _parse_* function pattern:
        #   py_prop = _parse_py_prop(d.pop("jsonProp", UNSET))
        # or multi-line:
        #   py_prop = _parse_py_prop(
        #       d.pop("jsonProp", UNSET)
        #   )
        # The _parse_* returns str | ... | Unset, but the field expects SemanticType | ...
        # Wrap with lifter only when the value is a str.
        parse_call_pattern = re.compile(
            rf'(\s+){re.escape(py_prop)} = (_parse_{re.escape(py_prop)}\(.*?d\.pop\("[^"]*".*?\)[\s)]*\))',
            re.DOTALL,
        )
        parse_match = parse_call_pattern.search(content)
        if parse_match and f"{lifter_name}(_raw_" not in content:
            indent = parse_match.group(1)
            parse_call = parse_match.group(2)
            raw_var = f"_raw_{py_prop}"
            replacement = (
                f"{indent}{raw_var} = {parse_call}\n"
                f"{indent}{py_prop} = {lifter_name}({raw_var}) if isinstance({raw_var}, str) else {raw_var}"
            )
            content = content.replace(parse_match.group(0), replacement, 1)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        print(f"Patched {file_path.name}")


def run(context: dict[str, str]) -> None:
    # spec_path = Path(context["spec_path"]).resolve()
    out_dir = Path(context["out_dir"]).resolve()

    # Use the bundled spec which has resolved refs and x-semantic-type annotations
    spec_path = out_dir / "bundled_spec.yaml"

    models_dir = out_dir / "camunda_orchestration_sdk" / "models"

    # 1. Build global registry of {json_property: semantic_type}
    semantic_mappings: Dict[str, str] = {}

    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
            if spec:
                _extract_semantic_mappings(spec, semantic_mappings)
    except Exception as e:
        print(f"Warning: Failed to load spec for semantic mapping extraction: {e}")
        return

    if not semantic_mappings:
        print("No semantic types found in spec.")
        return

    print(f"Found {len(semantic_mappings)} semantic property mappings.")

    # 2. Iterate over ALL model files
    for model_file in models_dir.glob("*.py"):
        if model_file.name == "__init__.py":
            continue
        _patch_model_file(model_file, semantic_mappings)
