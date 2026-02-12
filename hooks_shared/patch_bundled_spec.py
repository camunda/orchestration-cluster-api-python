"""
This hook patches the bundled OpenAPI spec to fix issues that cause openapi-python-client to skip endpoints.
Specifically, it injects an empty schema into request bodies that define 'application/json' content but provide no schema.
It also flattens allOf compositions to help the generator produce better models.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, cast

import yaml

SpecNode = dict[str, Any] | list[Any] | str | int | float | bool | None

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
                        # Capitalize for class name style
                        clean_name = ''.join(str(x).capitalize() or '_' for x in str(prop_name).split('_'))
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
                title: str = str(opt.get('title', 'Object')).replace(' ', '')
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
                    # Update the title of the extracted schema to match the name
                    # This helps generators that use title for naming and avoids collisions
                    self.new_schemas[schema_name]['title'] = schema_name
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

    def extract_object_schema(obj_schema: dict[str, Any], base_name: str) -> dict[str, str]:
        """Extract a nested object schema and return a ref to it."""
        fingerprint: str = get_fingerprint(obj_schema)
        if fingerprint in schema_fingerprints:
            return {'$ref': f"#/components/schemas/{schema_fingerprints[fingerprint]}"}

        schema_name: str = base_name
        counter: int = 1
        while schema_name in schemas or schema_name in new_schemas:
            schema_name = f"{base_name}{counter}"
            counter += 1

        new_schemas[schema_name] = obj_schema.copy()
        new_schemas[schema_name]['title'] = schema_name
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
                clean_prop_name: str = ''.join(str(x).capitalize() or '_' for x in prop_name_str.split('_'))
                base_name: str = f"{parent_name}{clean_prop_name}"
                new_props[prop_name] = extract_object_schema(cast(dict[str, Any], prop_schema), base_name)
            elif isinstance(prop_schema, dict):
                # Recursively process the property
                clean_prop_name = ''.join(str(x).capitalize() or '_' for x in prop_name_str.split('_'))
                new_props[prop_name] = process_schema(cast(dict[str, Any], prop_schema), f"{parent_name}{clean_prop_name}")
            else:
                new_props[prop_name] = prop_schema

        return new_props

    # Process all schemas
    for schema_name, schema_val in list(schemas.items()):
        if isinstance(schema_val, dict):
            typed_schema = cast(dict[str, Any], schema_val)
            process_schema(typed_schema, str(schema_name))

    # Add new schemas
    schemas.update(new_schemas)
    return spec


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

    # Extract inline objects from oneOf/anyOf
    print("Extracting inline objects from compositions...")
    extractor = InlineSchemaExtractor(spec)
    spec = extractor.extract()

    # Extract nested properties to fix union issues
    print("Extracting nested object properties...")
    spec = extract_nested_properties(spec)

    with open(spec_path, 'w') as f:
        yaml.safe_dump(spec, f, sort_keys=False)
