#!/usr/bin/env python3
"""CI Guard: Verify every public CamundaClient / CamundaAsyncClient method
has a matching example region in the examples/ directory.

Extracts public methods from the generated client.py, then checks that each
has either:
  1. A PascalCase example region in examples/*.py, OR
  2. An entry in examples/operation-map.json

Addresses: https://github.com/camunda/orchestration-cluster-api-python/issues/86

Exits with code 1 if any public method lacks an example region.
"""

import re
import json
import sys
from pathlib import Path


root_dir = Path(__file__).resolve().parent.parent
client_path = root_dir / "generated" / "camunda_orchestration_sdk" / "client.py"
examples_dir = root_dir / "examples"
operation_map_path = examples_dir / "operation-map.json"

# Methods that are infrastructure / inherited utilities, not user-facing API
EXCLUDED_METHODS = {
    # httpx client internals (inherited from generated base)
    "get_httpx_client",
    "set_httpx_client",
    "get_async_httpx_client",
    "set_async_httpx_client",
    "with_cookies",
    "with_headers",
    "with_timeout",
}


def _to_pascal_case(snake: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in snake.split("_"))


# ── Step 1: Extract public methods from client classes ───────────────────────

if not client_path.exists():
    print(f"Client source not found at {client_path}", file=sys.stderr)
    print("Run 'make generate' first to generate the SDK.", file=sys.stderr)
    sys.exit(2)

client_source = client_path.read_text(encoding="utf-8")
lines = client_source.splitlines()

# Find class boundaries
sync_class_line = None
async_class_line = None
for i, line in enumerate(lines):
    if re.match(r"^class CamundaClient\b", line):
        sync_class_line = i
    elif re.match(r"^class CamundaAsyncClient\b", line):
        async_class_line = i

if sync_class_line is None or async_class_line is None:
    print("Could not find CamundaClient or CamundaAsyncClient in client.py", file=sys.stderr)
    sys.exit(2)


def extract_public_methods(start_line: int, end_line: int) -> set[str]:
    """Extract method names from a class body region."""
    methods: set[str] = set()
    method_re = re.compile(r"^\s{4}(?:async\s+)?def\s+([a-z]\w*)\s*\(")
    for i in range(start_line, end_line):
        m = method_re.match(lines[i])
        if m:
            name = m.group(1)
            if not name.startswith("_"):
                methods.add(name)
    return methods


sync_methods = extract_public_methods(sync_class_line, async_class_line)
async_methods = extract_public_methods(async_class_line, len(lines))

# Combine — we check coverage for the union of both clients
all_methods = sync_methods | async_methods

# Remove excluded infrastructure methods
all_methods -= EXCLUDED_METHODS

# ── Step 2: Collect all example regions from examples/*.py ───────────────────

REGION_PATTERN = re.compile(r"^\s*#\s*region\s+(.+?)\s*$")


def extract_regions(file_path: Path) -> set[str]:
    regions: set[str] = set()
    for line in file_path.read_text(encoding="utf-8").splitlines():
        m = REGION_PATTERN.match(line)
        if m:
            regions.add(m.group(1).strip())
    return regions


all_regions: set[str] = set()
for py_file in sorted(examples_dir.glob("*.py")):
    all_regions |= extract_regions(py_file)

# ── Step 3: Check operation-map.json for spec-method coverage ────────────────

operation_map: dict = {}
if operation_map_path.exists():
    with open(operation_map_path) as f:
        operation_map = json.load(f)

# Build per-file region caches for operation-map validation
_file_region_cache: dict[str, set[str]] = {}


def _get_file_regions(filename: str) -> set[str]:
    if filename not in _file_region_cache:
        fp = examples_dir / filename
        _file_region_cache[filename] = extract_regions(fp) if fp.exists() else set()
    return _file_region_cache[filename]


# ── Step 4: Match methods to example regions ─────────────────────────────────

methods_with_examples: set[str] = set()
broken_map_refs: list[str] = []

for method in all_methods:
    pascal = _to_pascal_case(method)

    # Check 1: Region exists matching PascalCase convention
    if pascal in all_regions:
        methods_with_examples.add(method)
        continue

    # Check 2: operationId entry in operation-map.json with valid file+region
    if method in operation_map:
        entries = operation_map[method]
        has_valid = False
        for entry in entries:
            file = entry.get("file", "")
            region = entry.get("region", "")
            if region in _get_file_regions(file):
                has_valid = True
            else:
                broken_map_refs.append(
                    f"{method}: file={file!r} region={region!r}"
                )
        if has_valid:
            methods_with_examples.add(method)
        continue

# ── Step 5: Report ───────────────────────────────────────────────────────────

missing = sorted(all_methods - methods_with_examples)

print(f"Sync CamundaClient methods:    {len(sync_methods - EXCLUDED_METHODS)}")
print(f"Async CamundaAsyncClient methods: {len(async_methods - EXCLUDED_METHODS)}")
print(f"Total unique public methods:   {len(all_methods)}")
print(f"Methods with example regions:  {len(methods_with_examples)}")

exit_code = 0

if missing:
    print(
        f"\n✗ {len(missing)} public method(s) missing example regions:",
        file=sys.stderr,
    )
    for m in missing:
        print(f"  - {m} (expected region: {_to_pascal_case(m)})", file=sys.stderr)
    print(
        "\nTo fix: add example regions in examples/*.py for each missing method.",
        file=sys.stderr,
    )
    exit_code = 1

if broken_map_refs:
    print(
        f"\n✗ {len(broken_map_refs)} broken operation-map reference(s):",
        file=sys.stderr,
    )
    for ref in broken_map_refs:
        print(f"  - {ref}", file=sys.stderr)
    exit_code = 1

if exit_code == 0:
    print("\n✓ All public methods have example regions.")
    print("✓ All operation-map references resolve.")

sys.exit(exit_code)
