import re
from pathlib import Path
from typing import Any, Dict, cast

import yaml

from _identifier_guard import safe_py_identifier


def _snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace("__", "_").lower()


def _extract_semantic_mappings(data: Any, mappings: Dict[str, str]) -> None:
    """
    Recursively traverse the spec to find all properties with x-semantic-type.
    Populates mappings dict with {json_property_name: semantic_type_name}.

    NOTE: This function collects *all* annotated properties. Ambiguous names
    (like "name", which is annotated in some schemas but not others) are
    removed from the global dict later in run(), so they don't get applied
    to every model file.
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
                            safe_py_identifier(semantic_type, "x-semantic-type")
                            mappings[prop_name] = semantic_type
                    # Recurse into properties
                    _extract_semantic_mappings(prop_schema, mappings)
            elif isinstance(value, (dict, list)):
                _extract_semantic_mappings(value, mappings)
    elif isinstance(data, list):
        data_list = cast(list[Any], data)
        for item in data_list:
            _extract_semantic_mappings(item, mappings)


def _resolve_ref(ref: str, schemas: dict[str, Any]) -> Any:
    """Resolve a local ``#/components/schemas/<Name>`` ref to its schema def.

    Returns ``None`` for non-local or unresolvable refs.
    """
    prefix = "#/components/schemas/"
    if not isinstance(ref, str) or not ref.startswith(prefix):
        return None
    return schemas.get(ref[len(prefix) :])


def _semantic_type_of_prop(
    prop_schema: Any,
    schemas: dict[str, Any],
    _seen: set[str] | None = None,
) -> str | None:
    """Return the ``x-semantic-type`` carried (directly or indirectly) by a property.

    Handles three shapes:

    * inline ``x-semantic-type`` on the property itself;
    * a ``$ref`` to a schema that carries ``x-semantic-type``;
    * a single-element ``allOf`` whose only member is such a ``$ref`` (or inline).

    The ``$ref``/``allOf`` cases are what regressed: a property declared as
    ``$ref: '#/components/schemas/TenantId'`` is ignored by a naive inline-only
    scan even though the referenced schema is annotated.
    """
    if not isinstance(prop_schema, dict):
        return None
    prop_dict = cast(dict[str, Any], prop_schema)

    semantic_type = prop_dict.get("x-semantic-type")
    if isinstance(semantic_type, str):
        return semantic_type

    if _seen is None:
        _seen = set()

    ref = prop_dict.get("$ref")
    if isinstance(ref, str):
        if ref in _seen:
            return None
        _seen.add(ref)
        target = _resolve_ref(ref, schemas)
        if target is not None:
            return _semantic_type_of_prop(target, schemas, _seen)
        return None

    all_of = prop_dict.get("allOf")
    if isinstance(all_of, list) and len(all_of) == 1:
        return _semantic_type_of_prop(all_of[0], schemas, _seen)

    return None


def _collect_schema_properties(
    schema_def: Any,
    schemas: dict[str, Any],
    _seen: set[int] | None = None,
) -> dict[str, Any]:
    """Collect a schema's effective properties, following ``allOf`` parents.

    Spec ``main`` defines the process-creation variants' shared fields through
    ``allOf`` (camunda/camunda@cd1294e5); without following those parents the
    inherited ``tenantId``/``businessId`` annotations are lost. Direct
    properties win over inherited ones on name collision.
    """
    if not isinstance(schema_def, dict):
        return {}
    schema_dict = cast(dict[str, Any], schema_def)

    if _seen is None:
        _seen = set()
    marker = id(schema_dict)
    if marker in _seen:
        return {}
    _seen.add(marker)

    collected: dict[str, Any] = {}

    all_of = schema_dict.get("allOf")
    if isinstance(all_of, list):
        for member in all_of:
            member_schema: Any = member
            if isinstance(member, dict) and "$ref" in member:
                member_schema = _resolve_ref(
                    cast(str, cast(dict[str, Any], member)["$ref"]), schemas
                )
            collected.update(_collect_schema_properties(member_schema, schemas, _seen))

    props = schema_dict.get("properties")
    if isinstance(props, dict):
        collected.update(cast(dict[str, Any], props))

    return collected


def _model_name_for_schema(schema_name: str, schema_def: Any) -> str:
    """Return the model name openapi-python-client generates for a schema.

    openapi-python-client names a model from the schema ``title`` when one is
    set, otherwise from the schema name. Keying the per-schema map by this value
    is what lets the lookup in ``run()`` (which derives a name from the model
    *file* name) find title-named schemas such as
    ``ProcessInstanceCreationInstructionById`` (title "Process creation by id",
    file ``process_creation_by_id.py``).

    The returned key is normalised to match exactly how ``run()`` derives a name
    from a model file stem: the generated module name (which is what the file is
    called) run through the same per-word ``capitalize`` join. This matters for
    titles carrying acronyms, e.g. "Decision evaluation by ID" generates
    ``decision_evaluation_by_id.py`` → key ``DecisionEvaluationById`` (not
    ``...ByID``).
    """
    source = schema_name
    if isinstance(schema_def, dict):
        title = cast(dict[str, Any], schema_def).get("title")
        if isinstance(title, str) and title.strip():
            source = title
    module = _module_name(source)
    return "".join(word.capitalize() for word in module.split("_"))


def _module_name(name: str) -> str:
    """Derive the generated module (file) name for a schema name/title.

    Prefers openapi-python-client's own ``snake_case(pascal_case(...))`` naming
    so the result matches the actual generated file name; falls back to a local
    conversion if the generator package is unavailable (e.g. isolated tests).
    """
    try:
        from openapi_python_client import utils as _oac_utils

        return _oac_utils.snake_case(_oac_utils.pascal_case(name))
    except Exception:
        return _snake(_pascal(name))


def _pascal(name: str) -> str:
    """PascalCase a name, matching how model file stems are converted in run()."""
    words = re.split(r"[^0-9a-zA-Z]+", name)
    return "".join(word[:1].upper() + word[1:] for word in words if word)


def _extract_per_schema_semantic_mappings(spec: dict[str, Any]) -> dict[str, dict[str, str]]:
    """
    Walk components/schemas and return {model_name: {property_name: semantic_type}}.
    This is the schema-aware version used to apply context-sensitive mappings.

    ``model_name`` is the name openapi-python-client generates for the schema
    (its ``title`` when set, else its schema name), so it matches the key the
    caller derives from each model file name. A property's semantic type is
    resolved through ``$ref``/``allOf`` indirection and inherited ``allOf``
    parents, not only from an inline ``x-semantic-type``.
    """
    result: dict[str, dict[str, str]] = {}
    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})
    for schema_name, schema_def in schemas.items():
        if not isinstance(schema_def, dict):
            continue
        model_name = _model_name_for_schema(schema_name, schema_def)
        props = _collect_schema_properties(schema_def, schemas)
        for prop_name, prop_schema in props.items():
            semantic_type = _semantic_type_of_prop(prop_schema, schemas)
            if isinstance(semantic_type, str):
                safe_py_identifier(semantic_type, "x-semantic-type")
                result.setdefault(model_name, {})[prop_name] = semantic_type
    return result


def _patch_model_file(file_path: Path, semantic_mappings: Dict[str, str], union_type_names: set[str] | None = None) -> None:
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

    # 2. Build explicit import for only the semantic types used in this file.
    # Union types are not callable classes -- use lift_<name> for those.
    _union_names = union_type_names or set()
    types_needed: set[str] = set()
    for _json_prop, _py_prop, semantic_type in fields_to_patch:
        types_needed.add(semantic_type)
        if semantic_type in _union_names:
            types_needed.add(_snake(f"lift_{semantic_type}"))
    all_names = sorted(types_needed)
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
        # Union types are not callable; use the lift_* function for them.
        constructor = _snake(f"lift_{semantic_type}") if semantic_type in _union_names else semantic_type

        # Patch type hint
        type_hint_pattern = re.compile(
            rf"^(\s+){py_prop}: ((?:None \| )?(?:str|int|float|bool))(.*)$",
            re.MULTILINE,
        )

        def type_hint_replacer(
            match: re.Match[str],
            _py_prop: str = py_prop,
            _semantic_type: str = semantic_type,
        ) -> str:
            indent = match.group(1)
            old_type = match.group(2)
            rest = match.group(3)
            if old_type.startswith("None | "):
                return f"{indent}{_py_prop}: None | {_semantic_type}{rest}"
            return f"{indent}{_py_prop}: {_semantic_type}{rest}"

        content = type_hint_pattern.sub(type_hint_replacer, content)

        # Patch from_dict
        # Pattern: indentation, py_prop, =, d.pop("json_prop")
        # We capture the d.pop(...) part to wrap it.

        # Note: json_prop in the regex needs to be escaped if it contains special chars, but usually it doesn't.
        pop_pattern = re.compile(rf'(\s+){py_prop} = (d\.pop\("{json_prop}"[^)]*\))')

        def pop_replacer(
            match: re.Match[str], _ctor: str = constructor, _py_prop: str = py_prop
        ) -> str:
            indent = match.group(1)
            pop_call = match.group(2)

            # Check for default value in d.pop
            # We look for ", default_value)" at the end of the pop call
            default_match = re.search(r", ([^)]+)\)$", pop_call)

            if default_match:
                default_val = default_match.group(1)
                # Use walrus operator to capture value and check against default
                return f"{indent}{_py_prop} = {_ctor}(_val) if (_val := {pop_call}) is not {default_val} else {default_val}"

            return f"{indent}{_py_prop} = {_ctor}({pop_call})"

        # Check if already patched to avoid double patching
        if (
            f"{constructor}(d.pop" not in content
            and f"{constructor}(_val)" not in content
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
        if parse_match and f"{constructor}(_raw_{py_prop}" not in content:
            indent = parse_match.group(1)
            parse_call = parse_match.group(2)
            raw_var = f"_raw_{py_prop}"
            replacement = (
                f"{indent}{raw_var} = {parse_call}\n"
                f"{indent}{py_prop} = {constructor}({raw_var}) if isinstance({raw_var}, str) else {raw_var}"
            )
            content = content.replace(parse_match.group(0), replacement, 1)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        print(f"Patched {file_path.name}")


def run(context: dict[str, str]) -> None:
    import json as _json

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

    # Build per-schema mappings to identify ambiguous property names.
    # A property name is "ambiguous" if it appears in some schemas WITH
    # x-semantic-type and in other schemas WITHOUT it (e.g. "name" is
    # ClusterVariableName in ClusterVariable* schemas but plain str in
    # Group, Role, Tenant, User, etc.).
    per_schema_mappings: dict[str, dict[str, str]] = {}
    if spec:
        per_schema_mappings = _extract_per_schema_semantic_mappings(spec)

    # Determine which property names are schema-specific (ambiguous).
    # A name is ambiguous if it exists as a plain property (no x-semantic-type)
    # in schemas other than where it is annotated.
    all_schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {}) if spec else {}
    ambiguous_props: set[str] = set()
    for prop_name in semantic_mappings:
        # Count schemas that have this property WITHOUT x-semantic-type
        for _schema_name, schema_def in all_schemas.items():
            if not isinstance(schema_def, dict):
                continue
            schema_dict = cast(dict[str, Any], schema_def)
            props = cast(dict[str, Any], schema_dict.get("properties", {}))
            if prop_name in props:
                prop_schema: Any = props[prop_name]
                if isinstance(prop_schema, dict) and "x-semantic-type" not in prop_schema:
                    ambiguous_props.add(prop_name)
                    break

    # Remove ambiguous properties from the global mapping
    for prop_name in ambiguous_props:
        del semantic_mappings[prop_name]

    if ambiguous_props:
        print(f"Excluded {len(ambiguous_props)} ambiguous property name(s) from global mapping: {sorted(ambiguous_props)}")

    print(f"Found {len(semantic_mappings)} semantic property mappings (global).")

    # Load union type names from spec-metadata so we know which semantic types
    # are Union aliases (not callable classes) and need a lift_* function instead.
    union_type_names: set[str] = set()
    generated_semantic_types: set[str] = set()
    metadata_path_str = context.get("metadata_path", "")
    if metadata_path_str:
        metadata_path = Path(metadata_path_str)
        if metadata_path.exists():
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    meta = _json.load(f)
                for entry in meta.get("unions", []):
                    union_type_names.add(entry["name"])
                # The set of semantic types actually emitted by hook 0700:
                # the string-typed semanticKeys plus the union aliases. Keys the
                # bundler dropped from metadata (e.g. integer-backed IterationId)
                # are absent here, so branding a field to them would import a
                # name semantic_types.py never defines.
                for entry in meta.get("semanticKeys", []):
                    generated_semantic_types.add(entry["name"])
                generated_semantic_types |= union_type_names
            except Exception as e:
                print(f"Warning: Failed to load metadata for union type detection: {e}")

    # Drop mappings whose semantic type was not emitted by the semantic-types
    # generator, leaving those fields at their native type. Only enforced when
    # metadata is available; the spec-scan fallback emits every annotated type.
    if generated_semantic_types:
        dropped = sorted(
            {
                st
                for st in semantic_mappings.values()
                if st not in generated_semantic_types
            }
        )
        semantic_mappings = {
            prop: st
            for prop, st in semantic_mappings.items()
            if st in generated_semantic_types
        }
        for schema_name in list(per_schema_mappings):
            per_schema_mappings[schema_name] = {
                prop: st
                for prop, st in per_schema_mappings[schema_name].items()
                if st in generated_semantic_types
            }
        if dropped:
            print(
                f"Excluded {len(dropped)} ungenerated semantic type(s) from "
                f"model branding: {dropped}"
            )

    # 2. Iterate over ALL model files
    for model_file in models_dir.glob("*.py"):
        if model_file.name == "__init__.py":
            continue
        # Build per-file mapping: global mappings + schema-specific mappings
        # for any schema that maps to this model file.
        file_mappings = dict(semantic_mappings)

        # Derive potential schema names from file name.
        # Model file "cluster_variable_create_request.py" → schema "ClusterVariableCreateRequest"
        stem = model_file.stem  # e.g. "cluster_variable_create_request"
        # Convert snake_case to PascalCase for schema matching
        pascal_name = "".join(word.capitalize() for word in stem.split("_"))

        # Apply per-schema mappings for this model's schema
        if pascal_name in per_schema_mappings:
            for prop_name, semantic_type in per_schema_mappings[pascal_name].items():
                file_mappings[prop_name] = semantic_type

        _patch_model_file(model_file, file_mappings, union_type_names)
