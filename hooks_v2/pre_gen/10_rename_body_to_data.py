import yaml
from pathlib import Path

def run(context):
    """
    Pre-generation hook to patch the bundled spec.
    Renames inline request bodies to end with 'Data' instead of 'Body'.
    """
    spec_path = Path(context["bundled_spec_path"])
    if not spec_path.exists():
        print(f"Spec file not found at {spec_path}")
        return

    print(f"Patching spec at {spec_path} to rename Body to Data...")
    
    with open(spec_path, "r") as f:
        spec = yaml.safe_load(f)

    schemas = spec.get("components", {}).get("schemas", {})
    paths = spec.get("paths", {})
    
    # Track renamed schemas to update refs later
    renamed_schemas = {}
    new_schemas = {}

    # 1. Rename existing schemas ending in 'Body'
    for name, schema in list(schemas.items()):
        if name.endswith("Body"):
            new_name = name[:-4] + "Data"
            print(f"Renaming schema {name} -> {new_name}")
            schemas[new_name] = schema
            del schemas[name]
            renamed_schemas[f"#/components/schemas/{name}"] = f"#/components/schemas/{new_name}"

    # 2. Extract and name inline request bodies
    for path, methods in paths.items():
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
                
            request_body = operation.get("requestBody", {})
            content = request_body.get("content", {})
            # Check for both application/json and multipart/form-data
            target_content = content.get("application/json") or content.get("multipart/form-data")
            
            if not target_content:
                continue

            schema = target_content.get("schema", {})
            
            # If it's an inline schema (no $ref)
            if schema and "$ref" not in schema:
                op_id = operation.get("operationId")
                if not op_id:
                    continue
                    
                # Create a name: {OperationId}Data
                # Capitalize first letter of op_id
                model_name = op_id[0].upper() + op_id[1:] + "Data"
                
                print(f"Extracting inline body for {op_id} -> {model_name}")
                
                # Move schema to components
                schemas[model_name] = schema
                
                # Replace with ref
                target_content["schema"] = {"$ref": f"#/components/schemas/{model_name}"}

    # 3. Update all references
    # This is a simple string replacement on the dumped YAML. 
    # It's safer than traversing the dict for deep refs.
    
    # First dump to string
    spec_str = yaml.safe_dump(spec, sort_keys=False)
    
    # Replace old refs with new refs
    for old_ref, new_ref in renamed_schemas.items():
        spec_str = spec_str.replace(old_ref, new_ref)
        
    # Write back
    with open(spec_path, "w") as f:
        f.write(spec_str)

    print("Spec patching complete.")
