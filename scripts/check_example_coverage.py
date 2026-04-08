#!/usr/bin/env python3
"""Check example coverage: compare operationIds in the bundled OpenAPI spec
against entries in examples/operation-map.json.

Exits with code 1 if any operations are missing examples.
Writes missing-examples.json for CI consumption.
"""

import json
import re
import sys
from pathlib import Path


def _to_snake_case(name: str) -> str:
    """Convert camelCase operationId to snake_case method name."""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


root_dir = Path(__file__).resolve().parent.parent
spec_path = root_dir / "external-spec" / "bundled" / "rest-api.bundle.json"
map_path = root_dir / "examples" / "operation-map.json"

if not spec_path.exists():
    print(f"Spec not found at {spec_path}", file=sys.stderr)
    print("Run 'make bundle-spec' first to fetch the spec.", file=sys.stderr)
    sys.exit(2)

with open(spec_path) as f:
    spec = json.load(f)

if not map_path.exists():
    print(f"Operation map not found at {map_path}", file=sys.stderr)
    print(
        "Ensure examples/operation-map.json exists and is committed.",
        file=sys.stderr,
    )
    sys.exit(2)

with open(map_path) as f:
    operation_map = json.load(f)

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}

spec_ops = []
for path_str, path_item in (spec.get("paths") or {}).items():
    for method, operation in path_item.items():
        if (
            method in HTTP_METHODS
            and isinstance(operation, dict)
            and operation.get("operationId")
        ):
            spec_ops.append(
                {
                    "operationId": operation["operationId"],
                    "method": method.upper(),
                    "path": path_str,
                    "summary": operation.get("summary", ""),
                }
            )

map_keys = set(operation_map.keys())
covered = [op for op in spec_ops if _to_snake_case(op["operationId"]) in map_keys]
missing = [op for op in spec_ops if _to_snake_case(op["operationId"]) not in map_keys]

print(f"Spec operations: {len(spec_ops)}")
print(f"Covered:         {len(covered)}")
print(f"Missing:         {len(missing)}")
print(f"Coverage:        {round(len(covered) / len(spec_ops) * 100)}%")

if missing:
    missing.sort(key=lambda op: op["operationId"])
    print("\nMissing operations:")
    for op in missing:
        print(f"  - {op['operationId']} ({op['method']} {op['path']})")

    print("\nTo fix this:")
    print("  1. Add an example for each missing operation in examples/")
    print("     Wrap code in # region <OperationId> ... # endregion <OperationId> tags")
    print("  2. Add an entry to examples/operation-map.json for each operation")
    print("  3. Or use the Copilot prompt: .github/prompts/add-missing-examples.prompt.md")

    with open(root_dir / "missing-examples.json", "w") as f:
        json.dump(missing, f, indent=2)

    sys.exit(1)
else:
    print("\nFull coverage!")
    missing_path = root_dir / "missing-examples.json"
    if missing_path.exists():
        missing_path.unlink()

# --- Integrity check: every operation-map entry must resolve ---

REGION_START_PATTERNS = [
    re.compile(r"^\s*//\s*#region\s+(.+?)\s*$"),
    re.compile(r"^\s*#region\s+(.+?)\s*$"),
    re.compile(r"^\s*//\s*<([A-Za-z]\w*)>\s*$"),
    re.compile(r"^\s*#\s*region\s+(.+?)\s*$"),
]


def extract_regions(content: str) -> set[str]:
    regions: set[str] = set()
    for line in content.splitlines():
        for pattern in REGION_START_PATTERNS:
            m = pattern.match(line)
            if m:
                regions.add(m.group(1).strip())
    return regions


examples_dir = root_dir / "examples"
integrity_errors: list[str] = []
file_region_cache: dict[Path, set[str]] = {}

for op_id, entries in operation_map.items():
    if not isinstance(entries, list):
        integrity_errors.append(f"{op_id}: value is not a list")
        continue
    for entry in entries:
        if not isinstance(entry.get("file"), str) or not entry["file"]:
            integrity_errors.append(f"{op_id}: entry missing 'file' field")
            continue
        if not isinstance(entry.get("region"), str) or not entry["region"]:
            integrity_errors.append(f"{op_id}: entry missing 'region' field")
            continue
        file_path = examples_dir / entry["file"]
        if not file_path.exists():
            integrity_errors.append(f"{op_id}: file not found: {entry['file']}")
            continue
        if file_path not in file_region_cache:
            file_region_cache[file_path] = extract_regions(
                file_path.read_text(encoding="utf-8")
            )
        if entry["region"] not in file_region_cache[file_path]:
            integrity_errors.append(
                f"{op_id}: region \"{entry['region']}\" not found in {entry['file']}"
            )

if integrity_errors:
    print(f"\nIntegrity errors ({len(integrity_errors)}):", file=sys.stderr)
    for err in integrity_errors:
        print(f"  - {err}", file=sys.stderr)
    sys.exit(1)
else:
    print("Integrity check passed: all files and regions resolve.")
