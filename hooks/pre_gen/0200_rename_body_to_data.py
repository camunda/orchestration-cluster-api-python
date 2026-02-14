from __future__ import annotations

from typing import Any, cast

import yaml
from pathlib import Path


def run(context: dict[str, str]) -> None:
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
        spec: dict[str, Any] = yaml.safe_load(f)

    schemas: dict[str, Any] = spec.get("components", {}).get("schemas", {})
    paths: dict[str, Any] = spec.get("paths", {})
    
    # Track renamed schemas to update refs later
    renamed_schemas: dict[str, str] = {}

    # 1. Rename existing schemas ending in 'Body'
    for name, schema in list(schemas.items()):
        if name.endswith("Body"):
            new_name = name[:-4] + "Data"
            print(f"Renaming schema {name} -> {new_name}")
            schemas[new_name] = schema
            del schemas[name]
            renamed_schemas[f"#/components/schemas/{name}"] = f"#/components/schemas/{new_name}"

    # 2. Extract and name inline request bodies
    for _path, methods in paths.items():
        for _method, raw_operation in methods.items():
            if not isinstance(raw_operation, dict):
                continue

            operation = cast(dict[str, Any], raw_operation)
            request_body: dict[str, Any] = operation.get("requestBody", {})
            content: dict[str, Any] = request_body.get("content", {})
            # Check for both application/json and multipart/form-data
            target_content: dict[str, Any] | None = content.get("application/json") or content.get("multipart/form-data")
            
            if not target_content:
                continue

            schema: dict[str, Any] = target_content.get("schema", {})
            
            # If it's an inline schema (no $ref)
            if schema and "$ref" not in schema:
                op_id: str | None = operation.get("operationId")
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
    spec_str: str = yaml.safe_dump(spec, sort_keys=False)
    
    # Replace old refs with new refs
    for old_ref, new_ref in renamed_schemas.items():
        spec_str = spec_str.replace(old_ref, new_ref)
        
    # Write back
    with open(spec_path, "w") as f:
        f.write(spec_str)

    print("Spec patching complete.")
