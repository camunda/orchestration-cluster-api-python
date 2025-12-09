"""
This hook patches the bundled OpenAPI spec to fix issues that cause openapi-python-client to skip endpoints.
Specifically, it injects an empty schema into request bodies that define 'application/json' content but provide no schema.
"""
import yaml
from pathlib import Path

def flatten_all_of(schema):
    if not isinstance(schema, dict):
        return schema

    # Process children first
    new_schema = {}
    for k, v in schema.items():
        if k == 'allOf':
            continue  # Handle allOf later
        if isinstance(v, dict):
            new_schema[k] = flatten_all_of(v)
        elif isinstance(v, list):
            new_schema[k] = [flatten_all_of(i) if isinstance(i, dict) else i for i in v]
        else:
            new_schema[k] = v

    if 'allOf' in schema:
        all_of_list = schema['allOf']
        
        # Recursively flatten items in allOf
        flattened_all_of = [flatten_all_of(item) for item in all_of_list]
        
        # Check if we should merge
        # We merge if the resulting type is primitive
        types = set()
        if 'type' in new_schema:
            types.add(new_schema['type'])
        for item in flattened_all_of:
            if 'type' in item:
                types.add(item['type'])
        
        primitive_types = {'string', 'integer', 'number', 'boolean'}
        if types.intersection(primitive_types):
            # Merge!
            for item in flattened_all_of:
                for k, v in item.items():
                    if k not in new_schema:
                        new_schema[k] = v
                    elif k == 'description':
                        # Keep existing description (usually from parent)
                        pass
                    elif k == 'type':
                        # Verify consistency?
                        pass
                    # Add other merge strategies if needed
            
            # If we merged, we don't include 'allOf' in the result
            # print(f"Flattened allOf for primitive type: {types}")
        else:
            # If not primitive, keep allOf
            new_schema['allOf'] = flattened_all_of

    return new_schema

def make_optional(schema, property_name):
    if not isinstance(schema, dict):
        return

    if 'required' in schema and isinstance(schema['required'], list):
        if property_name in schema['required']:
            print(f"Removing {property_name} from required list in schema")
            schema['required'].remove(property_name)
            if not schema['required']:
                del schema['required']

    for k, v in schema.items():
        if isinstance(v, dict):
            make_optional(v, property_name)
        elif isinstance(v, list):
            for item in v:
                make_optional(item, property_name)

def patch_bundled_spec(spec_path: Path):
    with open(spec_path, 'r') as f:
        spec = yaml.safe_load(f)

    # Fix empty request bodies
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        for method, operation in methods.items():
            if 'requestBody' in operation:
                content = operation['requestBody'].get('content', {})
                if 'application/json' in content:
                    if content['application/json'] == {}:
                        print(f"Patching empty request body for {method.upper()} {path}")
                        content['application/json'] = {'schema': {}}

    # Flatten allOf for primitives
    print("Flattening allOf schemas...")
    spec = flatten_all_of(spec)

    with open(spec_path, 'w') as f:
        yaml.safe_dump(spec, f, sort_keys=False)
