<h1 align="center">Maintainer Guide – Orchestration Cluster Python SDK</h1>

Architecture and pipeline documentation for the `camunda-orchestration-sdk` Python SDK generator. End-user consumption docs live in `README.md`; contributor setup is in `CONTRIBUTING.md`.

---

## 1. High-Level Flow

`make generate` runs a deterministic pipeline:

1. **Clean** – purge `generated/`.
2. **Install** – `uv sync` to install dependencies.
3. **Bundle spec** – `camunda-schema-bundler` fetches the upstream multi-file OpenAPI spec (sparse clone of `camunda/camunda`) and bundles it into:
   - `external-spec/bundled/rest-api.bundle.json` (single-file spec consumed by the generator)
   - `external-spec/bundled/spec-metadata.json` (operation metadata: keys, unions, consistency info)
4. **Pre-generation hooks** (`hooks/pre_gen/`) – transform the bundled spec (fix naming, flatten allOf, rename body → data).
5. **Core generation** – `openapi-python-client` generates the SDK package in `generated/camunda_orchestration_sdk/`.
6. **Post-generation hooks** (`hooks/post_gen/`) – transform generated code (exceptions, runtime injection, client flattening, typing fixes).
7. **Lint & format** – `ruff format` + `ruff check --fix`.
8. **Type-check** – `pyright` in strict mode.
9. **Acceptance tests** – `pytest tests/acceptance/`.

Each step is idempotent given identical upstream spec + environment.

### Build Variants

| Command | Description |
| --- | --- |
| `make generate` | Full build: fetch upstream spec, generate, lint, type-check, test |
| `make generate-local` | Fast local iteration: use already-fetched spec |
| `make bundle-spec` | Only fetch & bundle the upstream spec |
| `make test` | Run acceptance tests only |
| `make itest` | Full build + integration tests |
| `make lint` | Lint with ruff |
| `make typecheck` | Type-check with pyright |
| `make clean` | Remove `generated/` |
| `make clean_spec` | Remove cached spec and bundled output |

Pin a spec branch/tag: `SPEC_REF=my-branch make generate`.

---

## 2. Generator Script

`generate.py` is the pipeline orchestrator. It:

1. Discovers hook files in `hooks/pre_gen/` and `hooks/post_gen/`, sorted lexicographically by filename.
2. Copies the bundled spec into the output directory.
3. Runs pre-gen hooks (spec transforms).
4. Invokes `openapi-python-client generate` with the configured options.
5. Runs post-gen hooks (code transforms).
6. Optionally runs acceptance tests (skippable with `--skip-tests`).

### Hook Numbering Convention

Hooks are numbered in increments of 100 (0100, 0200, …). To insert a new step between existing hooks, use an intermediate number (e.g., 0150 between 0100 and 0200). The lexicographic sort on filenames determines execution order. Use zero-padded four-digit prefixes.

Each hook must export a `run(context: dict[str, str])` function.

---

## 3. Spec Acquisition

Spec fetching and bundling is handled by the `camunda-schema-bundler` npm package (separate repo), invoked via `scripts/bundle-spec.sh`. It performs:

- Sparse clone of `camunda/camunda` (configurable branch via `SPEC_REF`)
- `SwaggerParser.bundle()` to merge multi-file YAML into a single JSON
- Schema augmentation from all upstream YAML files
- Path-local `$ref` normalization (signature matching + manual overrides)
- Emission of `spec-metadata.json` (operation IDs, key types, union types, consistency annotations)

The bundled spec lands at `external-spec/bundled/rest-api.bundle.json`.

---

## 4. Hook Reference

### Pre-generation hooks (`hooks/pre_gen/`)

| Hook | Purpose |
| --- | --- |
| `0100_patch_bundled_spec.py` | Patches the bundled OpenAPI spec: flattens `allOf` compositions, extracts inline schemas into named components, fixes generator compatibility issues (duplicate titles, `type`+`oneOf` conflicts), and applies PascalCase naming normalization |
| `0200_rename_body_to_data.py` | Renames inline request-body schema names from `*Body` to `*Data` for ergonomic method signatures |

### Post-generation hooks (`hooks/post_gen/`)

| Hook | Purpose |
| --- | --- |
| `0100_generate_typed_exceptions.py` | Generates per-operation, per-status-code typed exception classes from OpenAPI error responses |
| `0200_raise_exceptions.py` | Rewrites generated API methods to raise typed exceptions instead of returning raw error responses |
| `0300_copy_runtime.py` | Copies the hand-written `runtime/` directory into the generated SDK package |
| `0400_fix_element_instance_key.py` | Creates a minimal `ElementInstanceKey` Pydantic model and ensures referencing models import it |
| `0500_fix_str_model_import.py` | Creates a `models/str.py` shim so generated `from ...models.str import str` imports resolve correctly |
| `0600_patch_invalid_imports.py` | Fixes invalid generated imports (`models.str`, `models.null<…>`) by redirecting to builtins |
| `0700_generate_semantic_types.py` | Generates `NewType`-based semantic type aliases (e.g., `ProcessDefinitionKey`) from `x-semantic-type` annotations |
| `0800_generate_composite_alias_models.py` | Generates Pydantic `RootModel` wrappers for composite/array-type schema aliases |
| `0900_flatten_client.py` | Flattens per-tag API classes into unified `CamundaClient` / `CamundaAsyncClient` with all methods, `ExtendedDeploymentResult`, job worker support, and configuration-based auth |
| `1000_patch_semantic_types_in_models.py` | Replaces primitive `int`/`str` annotations in generated models with semantic type aliases where `x-semantic-type` is present |
| `1100_fix_attrs_typing.py` | Replaces untyped `factory=dict` attrs fields with typed factory functions for pyright strict mode |
| `1200_fix_model_typing.py` | Fixes pyright-strict typing issues in generated code (casts after `isinstance`, annotates list accumulators, fixes `__all__` tuples) |
| `1300_create_py_typed.py` | Creates `py.typed` marker file (PEP 561) so the package advertises type-checking support |

---

## 5. Runtime Components

The `runtime/` directory contains hand-written infrastructure that is copied into the generated package by hook 0300:

| Module | Purpose |
| --- | --- |
| `configuration_resolver.py` | Resolves SDK configuration from environment variables, constructor args, and `.env` files (mirrors the JS SDK's config hydration) |
| `auth.py` | Pluggable authentication: OAuth client-credentials (with token caching/refresh), HTTP Basic auth, and null auth |
| `job_worker.py` | Long-poll job worker that activates, dispatches, and completes/fails Zeebe jobs using thread, process, or async execution strategies |

To modify runtime behavior, edit files in `runtime/` (not in `generated/`). They are copied into the generated package on every build.

---

## 6. Generated Artifacts

| Directory / File | Purpose |
| --- | --- |
| `generated/camunda_orchestration_sdk/` | Complete SDK package |
| `generated/camunda_orchestration_sdk/client.py` | `CamundaClient`, `CamundaAsyncClient`, `ExtendedDeploymentResult`, and underlying httpx client classes |
| `generated/camunda_orchestration_sdk/models/` | Pydantic/attrs model classes from OpenAPI schemas |
| `generated/camunda_orchestration_sdk/api/` | Per-tag API operation modules (each with `sync` and `asyncio` functions) |
| `generated/camunda_orchestration_sdk/errors.py` | Typed exception classes per operation/status-code |
| `generated/camunda_orchestration_sdk/semantic_types.py` | `NewType` semantic aliases for domain keys |
| `generated/camunda_orchestration_sdk/runtime/` | Copied from `runtime/` — auth, config, job worker |
| `generated/camunda_orchestration_sdk/py.typed` | PEP 561 marker |

Generated files are entirely disposable; never edit them manually—change inputs, templates, or hooks instead.

---

## 7. Client Flattening (Hook 0900)

The generator produces per-tag API modules under `api/`. Hook 0900 synthesizes two top-level client classes:

- **`CamundaClient`** — synchronous client with all API methods, `deploy_resources_from_files()` convenience method
- **`CamundaAsyncClient`** — async client with all API methods, `deploy_resources_from_files()`, `create_job_worker()`, and `run_workers()`

Both clients integrate:

- **Configuration resolution** — environment variables, `.env` files, explicit constructor args
- **Authentication** — auto-detected from `CAMUNDA_AUTH_STRATEGY` (NONE, BASIC, OAUTH)
- **Context manager support** — `with` / `async with` for proper resource cleanup

Method signatures are transformed: `body` → `data`, `client` is removed (bound to `self.client`). Type imports are placed under `TYPE_CHECKING` to minimize runtime import overhead.

---

## 8. Semantic Types

Signal: presence of `x-semantic-type` on OpenAPI schema properties.

Flow:

1. `camunda-schema-bundler` detects `x-semantic-type` markers during bundling and records them in `spec-metadata.json`.
2. Post-hook 0700 reads the metadata and generates `semantic_types.py` with `NewType` aliases (e.g., `ProcessDefinitionKey = NewType('ProcessDefinitionKey', int)`).
3. Post-hook 1000 patches generated model files to replace raw `int`/`str` annotations with the semantic type aliases.

---

## 9. Testing Strategy

### Acceptance Tests

Run as the final stage of every `make generate`. Fast, deterministic, no containers required.

```bash
make test
# or: uv run pytest -q tests/acceptance
```

These validate:
- Generated code structure and model correctness
- Client construction and configuration
- Job worker logic
- Exception types

### Unit Tests

```bash
uv run pytest -q tests/unit
```

### Integration Tests

Require a running Camunda cluster via Docker:

```bash
cd docker && docker compose up -d
make itest
# or: CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration
```

---

## 10. Code Quality Gates

The `make generate` pipeline enforces three gates after code generation:

1. **`ruff format`** — auto-format all generated code
2. **`ruff check --fix`** — lint and auto-fix; build fails if unfixable violations remain
3. **`pyright`** — strict type-checking; build fails on any error

Pyright is configured in `pyproject.toml` with `typeCheckingMode = "strict"`.

---

## 11. Documentation

### API Docs

Generated with `pdoc`:

```bash
make docs-api        # Generate to ./public/
make preview-docs    # Live preview at http://localhost:8080
```

### Configuration Reference

Auto-generated from the configuration resolver:

```bash
make config-reference        # Generate
make config-reference-check  # Verify up-to-date (CI gate)
```

---

## 12. Releasing

Uses [python-semantic-release](https://python-semantic-release.readthedocs.io/) (configured in `pyproject.toml`).

### Branch model

- **`main`** → dev prereleases (`8.9.0-dev.1`, `8.9.0-dev.2`, …)
- **`stable/*`** → stable releases

### Configuration

```toml
[tool.semantic_release]
version_toml = ["pyproject.toml:project.version"]
build_command = "uv build"
```

Version is stored in `pyproject.toml` under `project.version`.

---

## 13. Customizing Generation

To add a new pipeline step:

1. Create a `.py` file in `hooks/pre_gen/` or `hooks/post_gen/` with an appropriate four-digit number prefix.
2. Export a `run(context: dict[str, str])` function.
3. The pipeline orchestrator will discover and run it automatically in sort order.

Guidelines:

- **New spec transforms**: place in `hooks/pre_gen/` (before openapi-python-client runs).
- **Augment raw generated artifacts**: place in `hooks/post_gen/` with a number below 0900 (before client flattening).
- **Modify the flattened client**: place after 0900.
- **Add typing fixes**: place after 1000.

Context dictionary keys available to hooks:

| Key | Value |
| --- | --- |
| `out_dir` | Output directory path (`generated/`) |
| `spec_path` | Path to the raw or bundled spec source |
| `bundled_spec_path` | Path to the bundled spec in the output directory |
| `metadata_path` | Path to `spec-metadata.json` (empty string if absent) |
| `config_path` | Path to the generator config YAML |
| `generator` | Generator name (`openapi-python-client`) |

Never edit generated files in `generated/` manually—they are overwritten every build.

---

## 14. Where Things Live

| What | Path |
| --- | --- |
| Pipeline orchestrator | `generate.py` |
| Generator config | `generator-config-python-client.yaml` |
| Pre-generation hooks | `hooks/pre_gen/` |
| Post-generation hooks | `hooks/post_gen/` |
| Runtime infrastructure | `runtime/` |
| Bundled spec input | `external-spec/bundled/rest-api.bundle.json` |
| Spec metadata | `external-spec/bundled/spec-metadata.json` |
| Generated SDK package | `generated/camunda_orchestration_sdk/` |
| Acceptance tests | `tests/acceptance/` |
| Unit tests | `tests/unit/` |
| Integration tests | `tests/integration/` |
| Build orchestration | `Makefile` |
| Spec bundling script | `scripts/bundle-spec.sh` |
| Config reference generator | `scripts/generate_config_reference.py` |
| Docker compose | `docker/docker-compose.yaml` |
| CI workflows | `.github/workflows/` |

---

## 15. Troubleshooting

| Issue | Likely Cause | Action |
| --- | --- | --- |
| `ruff check` fails with unfixable error | Duplicate class/import in generated code | Check for duplicate hooks (e.g., two flatten hooks both injecting `ExtendedDeploymentResult`) |
| pyright errors in generated code | Generator emitted untyped patterns | Add a fix to hook 1200 (`fix_model_typing`) or 1100 (`fix_attrs_typing`) |
| Mangled model names (e.g., `Processcreationbyid`) | Missing PascalCase normalization in spec patching | Check `to_pascal_case()` in hook 0100 and the `InlineSchemaExtractor` |
| Import errors for model classes | Model was renamed by spec patching | Update imports in `runtime/`, tests, and post-gen hooks |
| Spec fetch fails | Network / repo moved | Use `make generate-local` with existing spec; check `SPEC_REF` |
| `openapi-python-client` crashes | Unsupported schema pattern in spec | Add a compatibility fix to hook 0100 (`fix_generator_compatibility()`) |
| Missing semantic type aliases | No `x-semantic-type` in upstream spec | Add vendor extension upstream & regenerate |
| `py.typed` missing | Hook 1300 didn't run | Verify hook exists and `run()` function is exported |
| Tests import wrong model name | Model renamed by spec change | Update test imports to match new generated model names |

---

## 16. Maintenance Quick Commands

| Task | Command |
| --- | --- |
| Full build (fetch + generate + lint + type-check + test) | `make generate` |
| Fast local build (no fetch) | `make generate-local` |
| Bundle spec only | `make bundle-spec` |
| Run acceptance tests | `make test` |
| Run integration tests | `make itest` |
| Lint | `make lint` |
| Type-check | `make typecheck` |
| Generate API docs | `make docs-api` |
| Preview API docs | `make preview-docs` |
| Generate config reference | `make config-reference` |
| Clean generated code | `make clean` |
| Clean everything (spec + generated) | `make clean_spec && make clean` |
| Pin spec to a branch | `SPEC_REF=my-branch make generate` |

---

Contributions: open a draft PR early when altering generator semantics (spec patching, client flattening, typing fixes) to surface design discussion before large diffs land.
