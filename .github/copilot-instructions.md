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

**Always Green**: The `main` branch must have **0 errors** from `uv run pyright`. Any change that introduces pyright errors must be fixed before merging. Do not dismiss new errors as "pre-existing" without verifying by checking the baseline. If a change produces errors, fix them — do not leave regressions.

**After pipeline changes**: When modifying hooks, runtime code, or any part of the generation pipeline, always run `make lint` and `make typecheck` and fix any errors before considering the change complete.

### 6. Clean
To remove generated artifacts:
```bash
make clean
```

## Project Layout

### Key Directories
- **`generate.py`**: The main entry point script for the generation process.
- **`generated/`**: The output directory for the generated Python package. **Do not edit files here directly**; they will be overwritten.
- **`stubs/`**: Generated `.pyi` stub files for downstream tooling (e.g., API changelog generation). Mirrors the `generated/` package structure. These stubs are type-checked by pyright alongside the rest of the project — they must remain error-free.
- **`runtime/`**: Contains the manually written runtime logic (e.g., `JobWorker`) that is injected into the generated SDK. **Edit files here** if you need to modify the runtime behavior.
- **`hooks/`**: Contains Python scripts that run during the generation process to modify the spec or the generated code (e.g., renaming classes, fixing imports).
- **`tests/acceptance/`**: Tests that validate the generated code's structure and logic without a server.
- **`tests/integration/`**: Tests that validate the SDK against a real Camunda instance.
- **`generator-config-python-client.yaml`**: Configuration file for the `openapi-python-client` generator.

### Architecture & Generation Flow
1.  **Spec Retrieval**: `generate.py` fetches the OpenAPI spec.
2.  **Pre-Gen Hooks**: Scripts in `hooks/pre_gen` modify the raw OpenAPI spec (e.g., renaming fields).
3.  **Core Generation**: `openapi-python-client` runs using `generator-config-python-client.yaml`.
4.  **Post-Gen Hooks**: Scripts in `hooks/post_gen` modify the generated Python files (e.g., flattening client structure, patching imports).
5.  **Runtime Injection**: The content of `runtime/` is copied into `generated/camunda_orchestration_sdk/runtime/`.

### Important Files
- `pyproject.toml`: Defines project dependencies and build settings. Use `uv` to manage this.
- `Makefile`: Defines the standard workflows.
- `docker/docker-compose.yaml`: Configuration for the local development server.

### Dependencies
- **Runtime**: `httpx`, `attrs`, `pydantic`, `python-dateutil`, `loguru`, `python-dotenv`, `typing-extensions`.
- **Development**: `pytest`, `pytest-asyncio`, `pyyaml`, `openapi-python-client`, `jsonref`, `ruff`, `pyright`, `python-semantic-release`, `sphinx`, `sphinx-markdown-builder`, `sphinx-book-theme`, `psutil`, `pydantic-settings`, `fastapi`, `uvicorn`.

## Bug fix process (red/green refactor)

Every bug fix **must** follow the red/green refactor discipline:

1. **Red** — Write a failing test **first**, before changing any production code. The test must fail for the reason you expect (the bug). Commit this separately or demonstrate the failure clearly in the PR.
2. **Green** — Apply the minimal production fix that makes the test pass.
3. **Refactor** (optional) — Clean up while keeping all tests green.

### Test scope: target the defect class, not just the instance

The regression test must be broad enough to detect the **class of defect**, not only the specific instance you are fixing. For example, if the bug is "generated model X has a wrong field type", the test should verify that **all** generated models have correct field types — not just model X.

A test that only covers the exact instance provides weaker protection: the same category of bug can recur in a different model without being caught.

### Why

- The failing test **proves** the test can detect this category of defect.
- The green step **proves** the fix resolves it.
- A class-scoped test acts as a durable regression guard against future reintroduction of the same pattern.

## Backporting generator fixes to `stable/*` branches

Generator fixes (changes to `hooks/pre_gen/`, `hooks/post_gen/`, `hooks_shared/`, `runtime/`, `generate.py`, `bundle.py`, `generator-config-python-client.yaml`, or the `camunda-schema-bundler` integration) are **safe and expected to backport** to `stable/N` branches via cherry-pick.

> **Definition (important):** "Generator code" includes everything that produces `generated/camunda_orchestration_sdk/*` and `stubs/*` from the bundled spec **plus the hand-written runtime under `runtime/`**. Hook `0300_copy_runtime.py` copies `runtime/` into the generated package on every regen, so a fix in `runtime/` is a generator-class change for backport purposes — it propagates through the next `make generate`.

**What is NOT a generator fix** (do not auto-backport without discussion):

- Changes under `generated/camunda_orchestration_sdk/` directly (regenerated; never hand-edit).
- Changes under `stubs/` directly (regenerated by hook `1400_generate_stubs.py`).
- Changes that alter the public API surface, runtime behavior of generated clients, or anything that changes the published SDK semantics.

### Why backporting generator fixes is safe

The publish workflow (`.github/workflows/publish.yml`) runs `make generate SPEC_REF=…` on every release of `stable/*`, regenerating `generated/` and `stubs/` from the pinned spec and hooks before publishing. So a hooks-only or `runtime/`-only change cherry-picked onto `stable/N`:

1. Doesn't change `generated/*` under the **currently pinned** generator version (verify locally — see checklist below).
2. Lets the next Dependabot bump of `openapi-python-client` (or other generator deps) succeed where it would otherwise fail.
3. Auto-publishes a clean N.x patch with no behavioral change to the SDK.

### Backport workflow

1. Land the fix on `main` first via a normal PR. Get it reviewed and merged.
2. For each `stable/N` branch that needs the fix:
   ```bash
   git fetch origin stable/N
   git checkout -b backport/stable-N/<short-name> origin/stable/N
   git cherry-pick <commit-sha-from-main>
   ```
3. If the cherry-pick is clean (no conflicts), push and open a PR targeting `stable/N`. If conflicts arise, resolve them — but be conservative; if a conflict suggests the fix doesn't apply cleanly to that branch's generator pipeline, ask before forcing it.
4. PR title convention: `<original-title> (backport #<main-pr> to stable/N)`.
5. PR body: link the original PR, summarize the cherry-pick, and explicitly state the verification (see below).

### Verification before opening the backport PR

- Cherry-pick applied cleanly (or document any conflict resolution).
- The change is generator-class (hooks, `runtime/`, `generate.py`, `bundle.py`, generator config) — not generated output and not behavioral.
- Where feasible, locally run `make generate` under that branch's pinned generator version and confirm `git diff --stat generated/ stubs/` is empty (byte-identical output).
- `make lint` and `make typecheck` still pass.

### Anti-patterns

- **Don't** cherry-pick changes that touch `generated/` or `stubs/` directly — those will be overwritten on the next regen.
- **Don't** cherry-pick generator fixes alongside unrelated runtime/behavioral changes in the same commit. Split them on `main` first so the backport is surgical.
- **Don't** backport without first landing on `main`, unless the `main` branch itself cannot reproduce the issue (rare; flag explicitly in the PR).

## README Code Examples

### API spec examples: prefer ergonomic helpers

The `examples/operation-map.json` file maps OpenAPI `operationId`s to example regions that are displayed in the Camunda docs API reference (via `docusaurus-plugin-openapi-docs`).

When an ergonomic helper method exists for a generated operation, the operation-map entry **must** point to the helper — not to the raw generated method. Users should see the best developer experience by default.

Example: `create_deployment` maps to `DeployResources` (`deploy_resources_from_files` helper) instead of the raw `create_deployment` (requires manual multipart form construction). This preference is consistent across all three SDK repos (C#, TypeScript, Python).

Code blocks in `README.md` are **injected from compilable example files** — do not edit them inline.

- **Source of truth**: `examples/readme.py` (type-checked by pyright during build)
- **Sync script**: `scripts/sync-readme-snippets.py`
- **CI gate**: `python3 scripts/sync-readme-snippets.py --check` (fails if README is out of sync)

### How it works

1. Wrap code in `examples/readme.py` with `# region RegionName` / `# endregion RegionName` tags.
2. In `README.md`, place `<!-- snippet-source: examples/readme.py | regions: RegionName -->` immediately before the fenced code block.
3. Run `python3 scripts/sync-readme-snippets.py` to update README (or the build does it automatically).
4. Composite regions: `<!-- snippet-source: examples/readme.py | regions: A+B -->` concatenates regions A and B separated by a blank line.
5. Exempt blocks: use `<!-- snippet-exempt: reason -->` above a code block to exclude it from injection enforcement (e.g. pseudo-code).

The script auto-upgrades legacy `<!-- snippet:Name -->` markers to the new descriptive format.

### Adding or updating a README example

1. Add/edit the region-tagged code in `examples/readme.py`.
2. Add/verify the `<!-- snippet-source: examples/readme.py | regions: RegionName -->` marker in `README.md`.
3. Run `python3 scripts/sync-readme-snippets.py` to sync.
4. Run `uv run pyright` to confirm the example type-checks.

**Never edit a snippet-marked code block directly in README.md** — it will be overwritten on the next sync.
