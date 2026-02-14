"""
This hook patches the bundled OpenAPI spec to fix issues that cause openapi-python-client to skip endpoints.
Specifically, it injects an empty schema into request bodies that define 'application/json' content but provide no schema.
It also flattens allOf compositions to help the generator produce better models.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, cast

import yaml

SpecNode = dict[str, Any] | list[Any] | str | int | float | bool | None


def to_pascal_case(name: str) -> str:
    """Convert a camelCase, snake_case, space-separated, or mixed name to PascalCase.

    Examples:
        customHeaders       -> CustomHeaders
        batch_operation     -> BatchOperation
        elementInstanceState -> ElementInstanceState
        scopeKey            -> ScopeKey
        $like               -> Like
        Process creation by id -> ProcessCreationById
        Advanced filter     -> AdvancedFilter
    """
    # Strip leading non-alphanumeric chars (e.g. '$like' -> 'like')
    cleaned = re.sub(r'^[^a-zA-Z0-9]+', '', name)
    # Normalize spaces to underscores, then split on underscores
    words: list[str] = []
    for segment in cleaned.replace(' ', '_').split('_'):
        # Insert boundary before each uppercase letter that follows a lowercase letter or digit
        parts = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', segment).split('_')
        words.extend(parts)
    return ''.join(w.capitalize() for w in words if w)

class InlineSchemaExtractor:
    def __init__(self, spec: dict[str, Any]) -> None:
        self.spec: dict[str, Any] = spec
        if 'components' not in self.spec:
            self.spec['components'] = {}
        if 'schemas' not in self.spec['components']:
            self.spec['components']['schemas'] = {}
        self.schemas: dict[str, Any] = self.spec['components']['schemas']
        self.new_schemas: dict[str, Any] = {}  # Store new schemas here to avoid runtime modification errors
        self.schema_fingerprints: dict[str, str] = {}  # hash -> name

    def get_fingerprint(self, schema: dict[str, Any]) -> str:
        return hashlib.md5(json.dumps(schema, sort_keys=True).encode('utf-8')).hexdigest()

    def extract(self) -> dict[str, Any]:
        self.traverse(self.spec)
        self.schemas.update(self.new_schemas)
        return self.spec

    def traverse(self, node: SpecNode, name_hint: str = "") -> None:
        if not isinstance(node, dict):
            return
            
        if 'oneOf' in node:
            self.process_composition(node, 'oneOf', name_hint)
        if 'anyOf' in node:
            self.process_composition(node, 'anyOf', name_hint)
            
        for k, v in node.items():
            if k == 'properties':
                if isinstance(v, dict):
                    properties = cast(dict[str, Any], v)
                    for prop_name, prop_schema in properties.items():
                        clean_name = to_pascal_case(str(prop_name))
                        self.traverse(prop_schema, clean_name)
            elif k in ['allOf', 'oneOf', 'anyOf']:
                # These are lists
                if isinstance(v, list):
                    items_list = cast(list[Any], v)
                    for item in items_list:
                        self.traverse(item, name_hint)
            elif k == 'items':
                self.traverse(v, name_hint + "Item")
            else:
                self.traverse(v, name_hint)

    def process_composition(self, node: dict[str, Any], key: str, name_hint: str) -> None:
        new_options: list[dict[str, Any]] = []
        options_list: list[Any] = node[key]
        for option_raw in options_list:
            option: dict[str, Any] | Any = option_raw
            # Extract inline schemas that have metadata properties or are complex
            # We want to extract schemas with: properties, enum, title, description, etc.
            # But skip simple type-only schemas and existing refs
            should_extract: bool = False
            if isinstance(option_raw, dict):
                option = cast(dict[str, Any], option_raw)
                should_extract = (
                    '$ref' not in option and
                    (
                        'properties' in option or  # inline object
                        ('enum' in option and ('title' in option or 'description' in option)) or  # enum with metadata
                        ('type' in option and len(option) > 2)  # complex type with multiple constraints
                    )
                )

            if should_extract:
                assert isinstance(option, dict)
                opt = cast(dict[str, Any], option)
                # Found inline schema - Extract it
                title: str = to_pascal_case(str(opt.get('title', 'Object')))
                base_name: str = f"{name_hint}{title}"
                print(f"Extracting inline schema: {base_name}")
                
                # Deduplicate
                fingerprint: str = self.get_fingerprint(opt)
                if fingerprint in self.schema_fingerprints:
                    schema_name: str = self.schema_fingerprints[fingerprint]
                else:
                    schema_name = base_name
                    # Ensure unique name
                    counter: int = 1
                    while schema_name in self.schemas or schema_name in self.new_schemas:
                        schema_name = f"{base_name}{counter}"
                        counter += 1
                    
                    self.new_schemas[schema_name] = opt
                    # Remove title to avoid duplicate model names in the generator.
                    # The generator uses the component schema key for naming.
                    if 'title' in self.new_schemas[schema_name]:
                        del self.new_schemas[schema_name]['title']
                    self.schema_fingerprints[fingerprint] = schema_name
                
                new_options.append({'$ref': f"#/components/schemas/{schema_name}"})
            else:
                self.traverse(option, name_hint)
                new_options.append(option)
        node[key] = new_options

class SpecFlattener:
    def __init__(self, spec: dict[str, Any]) -> None:
        self.spec: dict[str, Any] = spec
        self._cache: dict[str, SpecNode] = {}

    def resolve_ref(self, ref: str) -> SpecNode:
        if not ref.startswith('#/'):
            return None
        parts = ref.split('/')
        current: Any = self.spec
        try:
            for part in parts[1:]:
                current = current[part]
            return current  # type: ignore[no-any-return]
        except (KeyError, TypeError):
            return None

    def flatten_schema(self, schema: SpecNode) -> SpecNode:
        if not isinstance(schema, dict):
            return schema

        # We construct a new schema dict
        new_schema: dict[str, Any] = {}
        
        # Copy non-allOf properties first, recursively flattening them
        for k, v in schema.items():
            if k == 'allOf':
                continue
            if isinstance(v, dict):
                new_schema[k] = self.flatten_schema(cast(dict[str, Any], v))
            elif isinstance(v, list):
                items_list = cast(list[Any], v)
                new_schema[k] = [self.flatten_schema(cast(dict[str, Any], i)) if isinstance(i, dict) else i for i in items_list]
            else:
                new_schema[k] = v

        if 'allOf' in schema:
            all_of_list: list[Any] = schema['allOf']
            
            # Collect all items to merge
            items_to_merge: list[SpecNode] = []
            can_merge: bool = True
            
            for item in all_of_list:
                if '$ref' in item:
                    resolved = self.resolve_ref(item['$ref'])
                    if resolved:
                        # Recursively flatten the resolved schema
                        flattened_resolved = self.flatten_schema(resolved)
                        
                        # Don't inline Unions or Enums - keep them as refs/allOf
                        # if 'oneOf' in flattened_resolved or 'anyOf' in flattened_resolved or 'enum' in flattened_resolved:
                        #    can_merge = False
                        #    break
                            
                        items_to_merge.append(flattened_resolved)
                    else:
                        can_merge = False
                        break
                else:
                    flattened_item = self.flatten_schema(item)
                    # Don't inline Unions or Enums
                    # if 'oneOf' in flattened_item or 'anyOf' in flattened_item or 'enum' in flattened_item:
                    #    can_merge = False
                    #    break
                    items_to_merge.append(flattened_item)
            
            if not can_merge:
                # If we couldn't resolve a ref, we keep the original allOf (but with flattened children where possible)
                flattened_all_of: list[SpecNode] = []
                for item in all_of_list:
                     flattened_all_of.append(self.flatten_schema(item))
                new_schema['allOf'] = flattened_all_of
                return new_schema

            # Analyze types to decide if we should merge
            types: set[Any] = set()
            if 'type' in new_schema:
                types.add(new_schema['type'])
            
            has_properties: bool = 'properties' in new_schema
            
            for item in items_to_merge:
                if isinstance(item, dict) and 'type' in item:
                    types.add(item['type'])
                if isinstance(item, dict) and 'properties' in item:
                    has_properties = True

            primitive_types: set[str] = {'string', 'integer', 'number', 'boolean'}
            is_primitive: bool = bool(types.intersection(primitive_types))
            is_object: bool = 'object' in types or has_properties

            if is_primitive:
                # Merge primitives
                for item in items_to_merge:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if k not in new_schema:
                                new_schema[k] = v
                        # We could merge descriptions etc here
            
            elif is_object:
                # Merge objects
                if 'type' not in new_schema:
                    new_schema['type'] = 'object'
                
                merged_props: dict[str, Any] = new_schema.get('properties', {})
                merged_required: set[Any] = set(new_schema.get('required', []))
                
                for item in items_to_merge:
                    if isinstance(item, dict) and 'properties' in item:
                        for pk, pv in item['properties'].items():
                            if pk not in merged_props:
                                merged_props[pk] = pv
                            # If property exists, we assume the parent/first one wins or they are compatible
                    
                    if isinstance(item, dict) and 'required' in item:
                        merged_required.update(item['required'])
                        
                    # Merge other fields
                    if isinstance(item, dict):
                        for k, v in item.items():
                            if k not in ['properties', 'required', 'type', 'description', 'allOf', '$ref']:
                                if k not in new_schema:
                                    new_schema[k] = v

                if merged_props:
                    new_schema['properties'] = merged_props
                if merged_required:
                    new_schema['required'] = list(merged_required)
                
                # If we have a oneOf, removing the explicit type: object allows the union to work
                # even if some options are primitives (like string vs object filter)
                if 'oneOf' in new_schema:
                    if 'type' in new_schema:
                        del new_schema['type']
                    # Also remove description as it might confuse the generator into making a class
                    if 'description' in new_schema:
                        del new_schema['description']
            
            else:
                # Fallback: keep allOf if we don't know how to merge
                new_schema['allOf'] = items_to_merge

        return new_schema

def extract_nested_properties(spec: dict[str, Any]) -> dict[str, Any]:
    """
    Extract nested object properties that have their own 'properties' defined
    into separate schemas. This fixes issues with openapi-python-client
    when nested objects appear in schemas used in unions.
    """
    schemas: dict[str, Any] = spec.get('components', {}).get('schemas', {})
    new_schemas: dict[str, Any] = {}
    schema_fingerprints: dict[str, str] = {}

    def get_fingerprint(schema: dict[str, Any]) -> str:
        return hashlib.md5(json.dumps(schema, sort_keys=True).encode('utf-8')).hexdigest()

    # Precompute fingerprints for existing component schemas so we can
    # deduplicate inline schemas against them (replacing with $ref).
    existing_fingerprints: dict[str, str] = {}
    for sname, sval in schemas.items():
        if isinstance(sval, dict):
            existing_fingerprints[get_fingerprint(cast(dict[str, Any], sval))] = sname

    def extract_object_schema(obj_schema: dict[str, Any], base_name: str) -> dict[str, str]:
        """Extract a nested object schema and return a ref to it."""
        fingerprint: str = get_fingerprint(obj_schema)
        # Check against already-extracted schemas
        if fingerprint in schema_fingerprints:
            return {'$ref': f"#/components/schemas/{schema_fingerprints[fingerprint]}"}
        # Check against existing component schemas (handles inlined-by-flattener cases)
        if fingerprint in existing_fingerprints:
            schema_fingerprints[fingerprint] = existing_fingerprints[fingerprint]
            return {'$ref': f"#/components/schemas/{existing_fingerprints[fingerprint]}"}

        schema_name: str = base_name
        counter: int = 1
        while schema_name in schemas or schema_name in new_schemas:
            schema_name = f"{base_name}{counter}"
            counter += 1

        # Recursively process sub-properties before storing
        processed = process_schema(obj_schema.copy(), schema_name)
        processed['title'] = schema_name
        new_schemas[schema_name] = processed
        schema_fingerprints[fingerprint] = schema_name
        print(f"Extracting nested property: {schema_name}")

        return {'$ref': f"#/components/schemas/{schema_name}"}

    def process_schema(schema: dict[str, Any], parent_name: str) -> dict[str, Any]:
        """Recursively process a schema to extract nested objects."""

        # Handle array items
        if 'items' in schema and isinstance(schema['items'], dict):
            items = cast(dict[str, Any], schema['items'])
            if (items.get('type') == 'object' and
                ('properties' in items or
                 ('additionalProperties' in items and items['additionalProperties'] is not False))):
                # Extract the item schema
                clean_name: str = f"{parent_name}Item"
                schema['items'] = extract_object_schema(items, clean_name)
            else:
                # Recursively process items
                schema['items'] = process_schema(items, f"{parent_name}Item")

        # Handle properties
        if 'properties' in schema:
            schema['properties'] = process_properties(schema['properties'], parent_name)

        return schema

    def process_properties(props: dict[str, Any], parent_name: str) -> dict[str, Any]:
        new_props: dict[str, Any] = {}
        for prop_name, prop_schema in props.items():
            prop_name_str: str = str(prop_name)
            # Extract nested objects that are complex enough to warrant their own schema
            is_dict: bool = isinstance(prop_schema, dict)
            should_extract: bool = False
            if is_dict:
                prop_dict = cast(dict[str, Any], prop_schema)
                should_extract = (
                    'type' in prop_dict and
                    prop_dict.get('type') == 'object' and
                    ('properties' in prop_dict or
                     ('additionalProperties' in prop_dict and prop_dict['additionalProperties'] is not False))
                )

            if should_extract:
                assert isinstance(prop_schema, dict)
                # This is a nested object - extract it
                clean_prop_name: str = to_pascal_case(prop_name_str)
                base_name: str = f"{parent_name}{clean_prop_name}"
                new_props[prop_name] = extract_object_schema(cast(dict[str, Any], prop_schema), base_name)
            elif isinstance(prop_schema, dict):
                # Recursively process the property
                clean_prop_name = to_pascal_case(prop_name_str)
                new_props[prop_name] = process_schema(cast(dict[str, Any], prop_schema), f"{parent_name}{clean_prop_name}")
            else:
                new_props[prop_name] = prop_schema

        return new_props

    # Process all component schemas
    for schema_name, schema_val in list(schemas.items()):
        if isinstance(schema_val, dict):
            typed_schema = cast(dict[str, Any], schema_val)
            process_schema(typed_schema, str(schema_name))

    # Also process inline request/response body schemas in paths
    paths = cast(dict[str, Any], spec.get('paths', {}))
    for _path_str, path_obj in paths.items():
        if not isinstance(path_obj, dict):
            continue
        typed_path = cast(dict[str, Any], path_obj)
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            op = typed_path.get(method)
            if not isinstance(op, dict):
                continue
            typed_op = cast(dict[str, Any], op)
            op_id = str(typed_op.get('operationId', ''))
            parent_name = to_pascal_case(op_id) if op_id else ''

            # Process request body
            rb_raw = typed_op.get('requestBody', {})
            if isinstance(rb_raw, dict):
                rb = cast(dict[str, Any], rb_raw)
                rb_content = cast(dict[str, Any], rb.get('content', {}))
                for _ct_key, ct_val in rb_content.items():
                    if isinstance(ct_val, dict) and 'schema' in ct_val:
                        s = cast(dict[str, Any], ct_val['schema'])
                        if '$ref' not in s:
                            ct_val['schema'] = process_schema(s, parent_name)

            # Process response bodies
            responses = cast(dict[str, Any], typed_op.get('responses', {}))
            for _status, resp in responses.items():
                if not isinstance(resp, dict):
                    continue
                typed_resp = cast(dict[str, Any], resp)
                resp_content = cast(dict[str, Any], typed_resp.get('content', {}))
                for _ct_key, ct_val in resp_content.items():
                    if isinstance(ct_val, dict) and 'schema' in ct_val:
                        s = cast(dict[str, Any], ct_val['schema'])
                        if '$ref' not in s:
                            ct_val['schema'] = process_schema(s, parent_name)

    # Add new schemas
    schemas.update(new_schemas)
    return spec


def fix_generator_compatibility(spec: dict[str, Any]) -> dict[str, Any]:
    """
    Fix patterns that openapi-python-client cannot handle:
    1. Duplicate titles (e.g. 'Advanced filter' on 39 different schemas) cause
       the generator to emit duplicate model names. Fix by setting titles to the
       component schema key name.
    2. Schemas with both 'type: object' and 'oneOf' where variants include
       non-object types cause 'Invalid property in union'. Fix by removing 'type'.
    3. Properties with allOf wrapping a single oneOf (e.g. pagination) should be
       unwrapped so the generator sees a clean oneOf.
    """
    schemas: dict[str, Any] = spec.get('components', {}).get('schemas', {})

    # Track title usage to detect collisions
    title_counts: dict[str, int] = {}
    for schema_any in schemas.values():
        if isinstance(schema_any, dict):
            s = cast(dict[str, Any], schema_any)
            title = s.get('title')
            if isinstance(title, str):
                title_counts[title] = title_counts.get(title, 0) + 1

    for name, schema_val in schemas.items():
        if not isinstance(schema_val, dict):
            continue
        schema = cast(dict[str, Any], schema_val)
        # Fix 1: Replace duplicate titles with the unique schema name
        title = schema.get('title')
        if isinstance(title, str) and title_counts.get(title, 0) > 1:
            print(f"Fixing duplicate title '{title}' on {name}")
            schema['title'] = name

        # Fix 2: Remove type: object from schemas with oneOf
        if 'oneOf' in schema and schema.get('type') == 'object':
            print(f"Removing type:object from oneOf schema {name}")
            del schema['type']
            # Also remove description that could confuse the generator
            if 'description' in schema:
                del schema['description']

    # Fix 3: Unwrap allOf-wrapped oneOf throughout the spec
    _unwrap_allof_oneof(spec)

    return spec


def _unwrap_allof_oneof(node: dict[str, Any] | list[Any]) -> None:
    """Recursively find allOf with a single oneOf item and unwrap it."""
    if isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                _unwrap_allof_oneof(cast(dict[str, Any], item))
            elif isinstance(item, list):
                _unwrap_allof_oneof(cast(list[Any], item))
        return
    for key, value in list(node.items()):
        if key == 'allOf' and isinstance(value, list):
            all_of_list = cast(list[Any], value)
            if len(all_of_list) == 1:
                inner_val = all_of_list[0]
                if isinstance(inner_val, dict):
                    inner = cast(dict[str, Any], inner_val)
                    if 'oneOf' in inner:
                        # Unwrap: promote oneOf and other inner fields here
                        del node['allOf']
                        for ik, iv in inner.items():
                            if ik not in node:
                                node[ik] = iv
                        print(f"Unwrapped allOf->oneOf in schema property")
        if isinstance(value, dict):
            _unwrap_allof_oneof(cast(dict[str, Any], value))
        elif isinstance(value, list):
            _unwrap_allof_oneof(cast(list[Any], value))


def patch_bundled_spec(spec_path: Path) -> None:
    with open(spec_path, 'r') as f:
        spec: dict[str, Any] = yaml.safe_load(f)

    # Fix empty request bodies
    paths: dict[str, Any] = spec.get('paths', {})
    for path, methods_val in paths.items():
        if not isinstance(methods_val, dict):
            continue
        methods_dict = cast(dict[str, Any], methods_val)
        for method, operation_val in methods_dict.items():
            if not isinstance(operation_val, dict):
                continue
            operation = cast(dict[str, Any], operation_val)
            if 'requestBody' in operation:
                req_body: dict[str, Any] = cast(dict[str, Any], operation['requestBody']) if isinstance(operation['requestBody'], dict) else {}
                content = cast(dict[str, Any], req_body.get('content', {}))
                if 'application/json' in content:
                    if content['application/json'] == {}:
                        print(f"Patching empty request body for {str(method).upper()} {path}")
                        content['application/json'] = {'schema': {}}

    # Flatten allOf schemas
    print("Flattening allOf schemas...")
    flattener = SpecFlattener(spec)
    spec_result: SpecNode = flattener.flatten_schema(spec)
    assert isinstance(spec_result, dict)
    spec = spec_result

    # Fix generator compatibility issues (duplicate titles, type+oneOf, allOf wrap)
    print("Fixing generator compatibility...")
    spec = fix_generator_compatibility(spec)

    # Extract inline objects from oneOf/anyOf
    print("Extracting inline objects from compositions...")
    extractor = InlineSchemaExtractor(spec)
    spec = extractor.extract()

    # Fix title/key collisions: a schema's title might normalize to a name
    # that collides with another schema's key (e.g. title "Process creation by id"
    # normalizes to "ProcessCreationById" which is now also a schema key).
    schemas_dict: dict[str, Any] = spec.get('components', {}).get('schemas', {})
    schema_keys: set[str] = set(schemas_dict.keys())
    for sname, sval in schemas_dict.items():
        if not isinstance(sval, dict):
            continue
        s = cast(dict[str, Any], sval)
        title = s.get('title')
        if isinstance(title, str):
            normalized = to_pascal_case(title)
            if normalized != sname and normalized in schema_keys:
                print(f"Fixing title/key collision: '{title}' on {sname} → {sname}")
                s['title'] = sname

    # Extract nested properties to fix union issues
    print("Extracting nested object properties...")
    spec = extract_nested_properties(spec)

    with open(spec_path, 'w') as f:
        yaml.safe_dump(spec, f, sort_keys=False)


def run(context: dict[str, str]) -> None:
    bundled_spec_path = context.get("bundled_spec_path", "")
    if not bundled_spec_path:
        print("Warning: No bundled_spec_path in context, skipping patch_bundled_spec")
        return
    path = Path(bundled_spec_path)
    if not path.exists():
        print(f"Warning: Bundled spec not found at {path}, skipping")
        return
    print("Patching bundled spec...")
    patch_bundled_spec(path)
