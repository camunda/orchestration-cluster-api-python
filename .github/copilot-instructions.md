# Copilot Instructions

## High Level Details

This repository contains the Python SDK Generator for the Camunda 8 Orchestration Cluster API. It automates the creation of a Python client library from an OpenAPI specification, incorporating custom runtime logic and post-processing hooks to improve usability.

- **Project Type**: Python SDK Generator & Client Library
- **Source Language**: Python 3.10+
- **Key Frameworks**:
    - **Build/Dependency**: `uv` (primary), `make` (orchestration)
    - **Generation**: `openapi-python-client` with custom python hooks
    - **Runtime**: `httpx` (HTTP client), `pydantic` (data validation), `asyncio` (async support)
    - **Testing**: `pytest`, `pytest-asyncio`
- **Output**: Generates the `camunda_orchestration_sdk` package in the `generated/` directory.

## Documentation (Audiences)

This repo serves two audiences. When updating documentation, choose the correct file:

- **End users of the published SDK**: document in `README.md` (installation, configuration, and how to use `CamundaClient` / `CamundaAsyncClient`). Keep generator internals out of the README.
- **Contributors / SDK generator maintainers**: document in `CONTRIBUTING.md` (generation workflow, hooks, runtime injection, testing, release/build details).
- **Deep technical reference**: use `docs/*.md` for focused design notes and longer-form explanations.

If the user request is ambiguous (e.g., "update the docs"), clarify which audience they mean before editing.

## Build Instructions

Always use `uv` for package management and running scripts. The `Makefile` provides convenient shortcuts, but understanding the underlying `uv` commands is helpful depending on the task.

Note: Contributor workflows (generation, hooks, testing) are documented in `CONTRIBUTING.md`. Prefer keeping this file focused on execution conventions for the coding agent.

### 1. Bootstrap & Install
Ensure `uv` is installed. Then install dependencies:
```bash
uv sync
```

### 2. Generate SDK (Critical Step)
Before running tests, type checks, or using the SDK, you **must** generate it. This script fetches the OpenAPI spec, runs the generator, and executes post-processing hooks (including copying runtime code).

```bash
make generate
# OR manually:
# uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests
```
**Validation**: Check that `generated/camunda_orchestration_sdk` exists and contains `client.py` and `models/`.

### 3. Run Tests
The repository has two types of tests:
- **Acceptance Tests**: Run fast, do not require a running Camunda server. Run these after every generation.
    ```bash
    make test
    # OR: uv run pytest -q tests/acceptance
    ```
- **Integration Tests**: Require a local Camunda server.
    1.  Start server: `cd docker && docker compose up -d`
    2.  Run tests:
        ```bash
        make itest
        # OR: CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration
        ```

### 4. Linting & Formatting
```bash
make lint
# OR: uv run ruff check .
```
To fix auto-fixable issues:
```bash
uv run ruff check . --fix
```

### 5. Type Checking
Type checking runs `pyright` on the generated code and test files.
```bash
make typecheck
# OR: uv run pyright
```
*Precondition*: The SDK must be generated first (`make generate`).

### 6. Clean
To remove generated artifacts:
```bash
make clean
```

## Project Layout

### Key Directories
- **`generate.py`**: The main entry point script for the generation process.
- **`generated/`**: The output directory for the generated Python package. **Do not edit files here directly**; they will be overwritten.
- **`runtime/`**: Contains the manually written runtime logic (e.g., `JobWorker`) that is injected into the generated SDK. **Edit files here** if you need to modify the runtime behavior.
- **`hooks/`**: Contains Python scripts that run during the generation process to modify the spec or the generated code (e.g., renaming classes, fixing imports).
- **`tests/acceptance/`**: Tests that validate the generated code's structure and logic without a server.
- **`tests/integration/`**: Tests that validate the SDK against a real Camunda instance.
- **`generator-config-python-client.yaml`**: Configuration file for the `openapi-python-client` generator.

### Architecture & Generation Flow
1.  **Spec Retrieval**: `generate.py` fetches the OpenAPI spec.
2.  **Pre-Gen Hooks**: Scripts in `hooks_v2/pre_gen` modify the raw OpenAPI spec (e.g., renaming fields).
3.  **Core Generation**: `openapi-python-client` runs using `generator-config-python-client.yaml`.
4.  **Post-Gen Hooks**: Scripts in `hooks_v2/post_gen` and `hooks_shared` modify the generated Python files (e.g., flattening client structure, patching imports).
5.  **Runtime Injection**: The content of `runtime/` is copied into `generated/camunda_orchestration_sdk/runtime/`.

### Important Files
- `pyproject.toml`: Defines project dependencies and build settings. Use `uv` to manage this.
- `Makefile`: Defines the standard workflows.
- `docker/docker-compose.yaml`: Configuration for the local development server.

### Dependencies
- **Runtime**: `httpx`, `attrs`, `pydantic`, `python-dateutil`, `loguru`, `python-dotenv`, `typing-extensions`.
- **Development**: `pytest`, `pytest-asyncio`, `pyyaml`, `openapi-python-client`, `jsonref`, `ruff`, `pyright`, `python-semantic-release`, `pdoc`, `psutil`, `pydantic-settings`, `fastapi`, `uvicorn`.
