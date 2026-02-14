#!/usr/bin/env python3
"""Check which operations are in the spec but missing from generated output."""
import json
from pathlib import Path

spec = json.load(open("external-spec/bundled/rest-api.bundle.json"))

# All operationIds in the spec
spec_ops = {}
for path, methods in spec.get("paths", {}).items():
    for method, op in methods.items():
        if isinstance(op, dict) and "operationId" in op:
            spec_ops[op["operationId"]] = (method.upper(), path)

# All operation files in generated output  
gen_dir = Path("generated/camunda_orchestration_sdk/api")
gen_ops = set()
for py_file in gen_dir.rglob("*.py"):
    if py_file.name == "__init__.py":
        continue
    gen_ops.add(py_file.stem)

# Map operationId to expected filename
import re
def to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

missing = []
for op_id, (method, path) in sorted(spec_ops.items()):
    snake = to_snake(op_id)
    if snake not in gen_ops:
        # Check request body
        op = None
        methods_dict = spec["paths"][path]
        for m, o in methods_dict.items():
            if isinstance(o, dict) and o.get("operationId") == op_id:
                op = o
                break
        
        rb_info = ""
        if op and "requestBody" in op:
            content = op["requestBody"].get("content", {})
            for ct, si in content.items():
                schema = si.get("schema", {})
                if "$ref" in schema:
                    rb_info = f" body=$ref:{schema['$ref']}"
                else:
                    keys = list(schema.keys())
                    rb_info = f" body=inline({keys})"
        
        missing.append(f"  {method} {path} -> {op_id} (expected: {snake}){rb_info}")

print(f"Spec has {len(spec_ops)} operations")
print(f"Generated has {len(gen_ops)} operation files")
print(f"Missing {len(missing)} operations:")
for m in missing:
    print(m)
