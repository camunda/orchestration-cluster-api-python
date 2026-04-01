---
mode: agent
description: Generate missing SDK code examples for new API operations
tools:
  - run_in_terminal
  - file_search
  - read_file
  - replace_string_in_file
  - create_file
  - grep_search
---

# Add Missing SDK Examples

You are generating Python code examples for the Camunda Orchestration Cluster API Python SDK.

## Step 1: Identify missing operations

Run the coverage check:
```
python scripts/check_example_coverage.py
```

This compares every `operationId` in `external-spec/bundled/rest-api.bundle.json` against `examples/operation-map.json` and prints the missing operations.

If the spec hasn't been fetched yet, run `make bundle-spec` first.

## Step 2: Study the spec and generated client for each missing operation

For each missing operationId, check:
- The bundled spec entry for HTTP method, path, params, request/response schemas
- `generated/camunda_orchestration_sdk/client.py` for the exact method name and signature (the Python SDK uses `snake_case` method names)
- `generated/camunda_orchestration_sdk/models/` for the exact model class names

## Step 3: Find the right example file

Examples are organized by domain in `examples/`. Find the existing file that matches the operation's tag. If no suitable file exists, create a new one following the naming convention (`snake_case.py`) with:
```python
from __future__ import annotations

from camunda_orchestration_sdk import (
    CamundaClient,
    # model imports
)
```

## Step 4: Write the example

Follow these exact patterns:

### Imports
```python
from __future__ import annotations

from camunda_orchestration_sdk import (
    CamundaClient,
    ModelType,
    TypedKey,
)
```
Add imports to the existing import block if the file already exists.

### Region tags
```python
# region RegionName
def operation_name_example() -> None:
    # ...code...
# endregion RegionName
```
Use PascalCase region names derived from the operationId (e.g., `createProcessInstance` → `CreateProcessInstance`).

### Function patterns
```python
# Simple GET with typed key param:
# region GetSomething
def get_something_example(something_key: SomethingKey) -> None:
    client = CamundaClient()

    result = client.get_something(something_key=something_key)

    print(f"Name: {result.name}")
# endregion GetSomething

# POST with request body:
# region CreateSomething
def create_something_example() -> None:
    client = CamundaClient()

    client.create_something(
        data=SomethingCreationRequest(
            name="example",
            description="example description",
        )
    )
# endregion CreateSomething

# Search:
# region SearchSomethings
def search_somethings_example() -> None:
    client = CamundaClient()

    result = client.search_somethings(
        data=SomethingSearchQuery(
            filter_=SomethingSearchQueryFilter(
                name="example",
            ),
        )
    )

    if not isinstance(result.items, Unset):
        for item in result.items:
            print(f"Found: {item.name}")
# endregion SearchSomethings

# DELETE with typed key param:
# region DeleteSomething
def delete_something_example(something_key: SomethingKey) -> None:
    client = CamundaClient()

    client.delete_something(something_key=something_key)
# endregion DeleteSomething
```

### Conventions
- Functions are module-level (no class wrapper)
- Return type is always `-> None:`
- Use `snake_case` for function names and method calls
- Accept typed keys (e.g. `ProcessInstanceKey`, `JobKey`) as **function parameters** rather than using branded type constructors like `ProcessInstanceKey("...")` inline
- Use `data=ModelType(...)` for request bodies
- Use `filter_=` (trailing underscore) for the filter keyword
- Import `Unset` from `camunda_orchestration_sdk` when checking optional fields
- Use `CamundaClient()` for client init (no arguments)

## Step 5: Update operation-map.json

Add an entry for each new example:
```json
"operationId": [
  { "file": "domain_file.py", "region": "RegionName", "label": "Short description" }
]
```

The `operationId` key must match the spec's operationId exactly (camelCase).

## Step 6: Verify

Run `uv run pyright` to verify type checking and `python scripts/check_example_coverage.py` to verify coverage.
