"""
This hook patches the bundled OpenAPI spec to fix issues that cause openapi-python-client to skip endpoints.
Specifically, it injects an empty schema into request bodies that define 'application/json' content but provide no schema.
It also flattens allOf compositions to help the generator produce better models.
"""
import yaml
import json
import hashlib
from pathlib import Path

class InlineSchemaExtractor:
    def __init__(self, spec):
        self.spec = spec
        if 'components' not in self.spec:
            self.spec['components'] = {}
        if 'schemas' not in self.spec['components']:
            self.spec['components']['schemas'] = {}
        self.schemas = self.spec['components']['schemas']
        self.new_schemas = {} # Store new schemas here to avoid runtime modification errors
        self.schema_fingerprints = {} # hash -> name

    def get_fingerprint(self, schema):
        return hashlib.md5(json.dumps(schema, sort_keys=True).encode('utf-8')).hexdigest()

    def extract(self):
        self.traverse(self.spec)
        self.schemas.update(self.new_schemas)
        return self.spec

    def traverse(self, node, name_hint=""):
        if not isinstance(node, dict):
            return
            
        if 'oneOf' in node:
            self.process_composition(node, 'oneOf', name_hint)
        if 'anyOf' in node:
            self.process_composition(node, 'anyOf', name_hint)
            
        for k, v in node.items():
            if k == 'properties':
                for prop_name, prop_schema in v.items():
                    # Capitalize for class name style
                    clean_name = ''.join(x.capitalize() or '_' for x in prop_name.split('_'))
                    self.traverse(prop_schema, clean_name)
            elif k in ['allOf', 'oneOf', 'anyOf']:
                # These are lists
                for item in v:
                    self.traverse(item, name_hint)
            elif k == 'items':
                self.traverse(v, name_hint + "Item")
            else:
                self.traverse(v, name_hint)

    def process_composition(self, node, key, name_hint):
        new_options = []
        for option in node[key]:
            if isinstance(option, dict) and 'properties' in option and '$ref' not in option:
                # Found inline object - Extract it
                title = option.get('title', 'Object').replace(' ', '')
                base_name = f"{name_hint}{title}"
                print(f"Extracting inline object: {base_name}")
                
                # Deduplicate
                fingerprint = self.get_fingerprint(option)
                if fingerprint in self.schema_fingerprints:
                    schema_name = self.schema_fingerprints[fingerprint]
                else:
                    schema_name = base_name
                    # Ensure unique name
                    counter = 1
                    while schema_name in self.schemas or schema_name in self.new_schemas:
                        schema_name = f"{base_name}{counter}"
                        counter += 1
                    
                    self.new_schemas[schema_name] = option
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
    def __init__(self, spec):
        self.spec = spec
        self._cache = {}

    def resolve_ref(self, ref):
        if not ref.startswith('#/'):
            return None
        parts = ref.split('/')
        current = self.spec
        try:
            for part in parts[1:]:
                current = current[part]
            return current
        except (KeyError, TypeError):
            return None

    def flatten_schema(self, schema):
        if not isinstance(schema, dict):
            return schema

        # We construct a new schema dict
        new_schema = {}
        
        # Copy non-allOf properties first, recursively flattening them
        for k, v in schema.items():
            if k == 'allOf':
                continue
            if isinstance(v, dict):
                new_schema[k] = self.flatten_schema(v)
            elif isinstance(v, list):
                new_schema[k] = [self.flatten_schema(i) if isinstance(i, dict) else i for i in v]
            else:
                new_schema[k] = v

        if 'allOf' in schema:
            all_of_list = schema['allOf']
            
            # Collect all items to merge
            items_to_merge = []
            can_merge = True
            
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
                flattened_all_of = []
                for item in all_of_list:
                     flattened_all_of.append(self.flatten_schema(item))
                new_schema['allOf'] = flattened_all_of
                return new_schema

            # Analyze types to decide if we should merge
            types = set()
            if 'type' in new_schema:
                types.add(new_schema['type'])
            
            has_properties = 'properties' in new_schema
            
            for item in items_to_merge:
                if 'type' in item:
                    types.add(item['type'])
                if 'properties' in item:
                    has_properties = True

            primitive_types = {'string', 'integer', 'number', 'boolean'}
            is_primitive = bool(types.intersection(primitive_types))
            is_object = 'object' in types or has_properties

            if is_primitive:
                # Merge primitives
                for item in items_to_merge:
                    for k, v in item.items():
                        if k not in new_schema:
                            new_schema[k] = v
                        # We could merge descriptions etc here
            
            elif is_object:
                # Merge objects
                if 'type' not in new_schema:
                    new_schema['type'] = 'object'
                
                merged_props = new_schema.get('properties', {})
                merged_required = set(new_schema.get('required', []))
                
                for item in items_to_merge:
                    if 'properties' in item:
                        for pk, pv in item['properties'].items():
                            if pk not in merged_props:
                                merged_props[pk] = pv
                            # If property exists, we assume the parent/first one wins or they are compatible
                    
                    if 'required' in item:
                        merged_required.update(item['required'])
                        
                    # Merge other fields
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

    # Flatten allOf schemas
    print("Flattening allOf schemas...")
    flattener = SpecFlattener(spec)
    spec = flattener.flatten_schema(spec)

    # Extract inline objects from oneOf/anyOf
    print("Extracting inline objects from compositions...")
    extractor = InlineSchemaExtractor(spec)
    spec = extractor.extract()

    with open(spec_path, 'w') as f:
        yaml.safe_dump(spec, f, sort_keys=False)
