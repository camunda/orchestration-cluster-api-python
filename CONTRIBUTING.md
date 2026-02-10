## Camunda Orchestration Cluster API – Python SDK Generator

This project generates a Python SDK for the Camunda 8 Orchestration Cluster REST API from the OpenAPI specification.

### Overview

- Fetches the OpenAPI spec via shallow clone from the public repository (fallback to local checked-out repo if offline).
- Generates the SDK using OpenAPI Generator (prefers `npx`, falls back to Docker).
- Provides an extensible hooks system for post-processing tasks.

### Requirements

- Python 3.9+
- One of:
  - Node.js with `npx` available; or
  - Docker (for `openapitools/openapi-generator-cli`)

### Quick start

```bash
cd orchestration-cluster-api-python
# Install deps and run generation (defaults to output in ./generated)
make generate
```

Generated SDK will be placed in `generated/` by default. You can change this with `--out-dir`.

### Local fallback of the spec

If the network is not available or the remote repository cannot be reached, the generator will use the locally cloned spec at:

- `../camunda-orchestration-cluster-api/specification/rest-api.yaml`

Ensure that repository is present in the workspace if you need offline generation.

### Configuration

`generator-config.yaml` holds OpenAPI Generator options such as package name. You may add or tweak options there.

You can also pass CLI arguments:

```bash
python3 generate.py \
  --out-dir ./generated \
  --generator python \
  --spec-ref main \
  --package-name camunda_orchestration_sdk
```

Run `python3 generate.py --help` for all options.

To temporarily generate against a different spec branch/tag/SHA from the upstream Camunda repo, set `--spec-ref` (default is `main`).

For the default v2 generator flow (used by `make generate`):

```bash
uv run generate.py \
  --generator openapi-python-client \
  --config generator-config-python-client.yaml \
  --spec-ref 45369-fix-spec \
  --skip-tests
```

Or via Make:

```bash
make generate SPEC_REF=45369-fix-spec
```

### CI: temporary spec ref override

GitHub Actions defaults to generating against the upstream spec `main`. If the upstream spec `main` is temporarily broken and you need CI to use a different ref, workflows support a guarded override via **repo variables**:

- `SPEC_REF_OVERRIDE`: the upstream spec ref to use (branch/tag/SHA)
- `SPEC_REF_OVERRIDE_ACK`: must be set to `true`
- `SPEC_REF_OVERRIDE_EXPIRES`: must be set to a date in `YYYY-MM-DD` format

The guard will fail CI after the expiry date to prevent accidentally leaving a non-`main` spec pinned indefinitely.

### Hooks (post-processing)

Add Python files under `hooks/` exporting a `run(context)` function. Hooks are executed in sorted order after generation.

`context` includes:

- `out_dir`: path to the generated SDK directory
- `spec_path`: path to the spec used for generation
- `config_path`: path to the generator config file
- `generator`: the generator type used (default `python`)

Example hook: see `hooks/postprocess_example.py`.

### Acceptance tests (post-generation)

After generation and post-processing, acceptance tests run automatically unless `--skip-tests` is provided. Tests live under `tests/acceptance/` and run against the generated package by injecting `PYTHONPATH`.

Run tests manually:

```bash
make test
```

### Integration tests (opt-in)

Integration tests live in `tests/integration` and require a running server. They are skipped unless `CAMUNDA_INTEGRATION=1` is set. By default, the client points to `http://localhost:8080/v2`; override with `CAMUNDA_REST_ADDRESS`.

Run manually:

```bash
make itest
```

### Make targets

- `make generate` – run the generator (uses Python script)
- `make clean` – remove the `generated/` directory and cache
