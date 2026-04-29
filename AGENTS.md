# AGENTS.md

> **Note:** This file delegates to a central AGENTS.md. Read and apply it before proceeding.

**URL:**
https://raw.githubusercontent.com/camunda/.github/refs/heads/main/AGENTS.md

Treat the central file's contents as if they were written directly in this file.
Instructions below extend those guidelines and take precedence if there is any conflict.

## Repo-specific instructions

### Role & boundary

This repo is the Python SDK Generator for the Camunda 8 Orchestration Cluster API. It produces the `camunda_orchestration_sdk` package in `generated/` from an OpenAPI spec, layering custom runtime logic and post-processing hooks on top of `openapi-python-client`.

- **Project type**: Python SDK generator + client library
- **Source language**: Python 3.10+
- **Build/dependency**: `uv` (primary), `make` (orchestration)
- **Generation**: `openapi-python-client` with custom Python hooks
- **Runtime**: `httpx`, `pydantic`, `asyncio`
- **Testing**: `pytest`, `pytest-asyncio`

Upstream dependencies — when they misbehave, fix them at the source rather than working around them here:

- [`camunda-schema-bundler`](https://github.com/camunda/camunda-schema-bundler) — fetches and bundles the upstream OpenAPI spec.
- [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client) — generates `generated/camunda_orchestration_sdk/`.
- [`camunda/camunda`](https://github.com/camunda/camunda) — source of the OpenAPI spec.

**Path map:**

| Path                 | Ownership and intent                                                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `generate.py`        | Main entry point for generation.                                                                                                                      |
| `runtime/`           | Hand-written runtime logic (e.g. `JobWorker`) **injected** into the generated SDK. Primary edit surface for runtime behavior.                         |
| `hooks/pre_gen/`     | Hooks that modify the raw OpenAPI spec before generation.                                                                                             |
| `hooks/post_gen/`    | Hooks that modify the generated Python files (flatten client, patch imports, etc.). Primary edit surface for fixing generator output.                |
| `generated/`         | **Generated.** Produced by `make generate`. Never hand-edit. The published `camunda_orchestration_sdk` package lives under `generated/`.              |
| `stubs/`             | Generated `.pyi` stub files mirroring the `generated/` package, used by downstream tooling (e.g. API changelog generation). Type-checked by pyright. |
| `tests/acceptance/`  | Fast unit tests that validate the generated code's structure and logic. No live Camunda required.                                                     |
| `tests/integration/` | Integration tests against a real Camunda instance.                                                                                                    |
| `examples/readme.py` | Source of truth for `README.md` code examples — type-checked by pyright.                                                                              |
| `docker/`            | Local Camunda compose stack for integration tests.                                                                                                    |
| `scripts/`           | Build, bundle, and sync helpers.                                                                                                                      |

## Documentation (Audiences)

This repo serves two audiences. When updating documentation, choose the correct file:

- **End users of the published SDK**: document in `README.md` (installation, configuration, and how to use `CamundaClient` / `CamundaAsyncClient`). Keep generator internals out of the README.
- **Contributors / SDK generator maintainers**: document in `CONTRIBUTING.md` (generation workflow, hooks, runtime injection, testing, release/build details).
- **Deep technical reference**: use `docs/*.md` for focused design notes and longer-form explanations.

If the user request is ambiguous (e.g. "update the docs"), clarify which audience they mean before editing.

## Build instructions

Always use `uv` for package management and running scripts. The `Makefile` provides convenient shortcuts, but understanding the underlying `uv` commands is helpful depending on the task.

> Contributor workflows (generation, hooks, testing) are documented in `CONTRIBUTING.md`. Prefer keeping this file focused on execution conventions for the coding agent.

### 1. Bootstrap & install

Ensure `uv` is installed. Then install dependencies:

```bash
uv sync
```

### 2. Generate SDK (critical step)

Before running tests, type checks, or using the SDK, you **must** generate it. This script fetches the OpenAPI spec, runs the generator, and executes post-processing hooks (including copying runtime code).

```bash
make generate
# OR manually:
# uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests
```

**Validation**: Check that `generated/camunda_orchestration_sdk` exists and contains `client.py` and `models/`.

### 3. Run tests

The repository has two types of tests:

- **Acceptance tests**: fast, no live Camunda required. Run after every generation.

  ```bash
  make test
  # OR: uv run pytest -q tests/acceptance
  ```

- **Integration tests**: require a local Camunda server.

  1. Start server: `cd docker && docker compose up -d`
  2. Run tests:

     ```bash
     make itest
     # OR: CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration
     ```

### 4. Linting & formatting

```bash
make lint
# OR: uv run ruff check .
```

To fix auto-fixable issues:

```bash
uv run ruff check . --fix
```

### 5. Type checking

Type checking runs `pyright` on the generated code and test files.

```bash
make typecheck
# OR: uv run pyright
```

*Precondition*: The SDK must be generated first (`make generate`).

**Always green**: The `main` branch must have **0 errors** from `uv run pyright`. Any change that introduces pyright errors must be fixed before merging. Do not dismiss new errors as "pre-existing" without verifying by checking the baseline. If a change produces errors, fix them — do not leave regressions.

**After pipeline changes**: When modifying hooks, runtime code, or any part of the generation pipeline, always run `make lint` and `make typecheck` and fix any errors before considering the change complete.

### 6. Clean

To remove generated artifacts:

```bash
make clean
```

## Project layout

### Architecture & generation flow

1. **Spec retrieval**: `generate.py` fetches the OpenAPI spec.
2. **Pre-gen hooks**: scripts in `hooks/pre_gen/` modify the raw OpenAPI spec (e.g. renaming fields).
3. **Core generation**: `openapi-python-client` runs using `generator-config-python-client.yaml`.
4. **Post-gen hooks**: scripts in `hooks/post_gen/` modify the generated Python files (e.g. flattening client structure, patching imports).
5. **Runtime injection**: the content of `runtime/` is copied into `generated/camunda_orchestration_sdk/runtime/`.

### Important files

- `pyproject.toml`: project dependencies and build settings. Use `uv` to manage this.
- `Makefile`: standard workflows.
- `generator-config-python-client.yaml`: configuration for the `openapi-python-client` generator.
- `docker/docker-compose.yaml`: local development server.

### Dependencies

- **Runtime**: `httpx`, `attrs`, `pydantic`, `python-dateutil`, `loguru`, `python-dotenv`, `typing-extensions`.
- **Development**: `pytest`, `pytest-asyncio`, `pyyaml`, `openapi-python-client`, `jsonref`, `ruff`, `pyright`, `python-semantic-release`, `sphinx`, `sphinx-markdown-builder`, `sphinx-book-theme`, `psutil`, `pydantic-settings`, `fastapi`, `uvicorn`.

## Commit message guidelines

We use Conventional Commits (enforced by `python-semantic-release`).

Format:

```
<type>(optional scope): <subject>

<body>

BREAKING CHANGE: <explanation>
```

Allowed type values (common set):

```
feat
fix
chore
docs
style
refactor
test
ci
build
perf
```

Rules:

- Subject length: 5–100 characters.
- Use imperative mood ("add support", not "added support").
- Lowercase subject (except proper nouns). No PascalCase subjects.
- Keep subject concise; body can include details, rationale, links.
- Prefix breaking changes with `BREAKING CHANGE:` either in body or footer.

### Review-comment fix-ups

Commits that address PR review comments must use the `chore` type (e.g. `chore:` or `chore(<scope>):`), **not** the `fix` type.
`fix` commits trigger a patch release and a CHANGELOG entry — review iterations are not user-facing bug fixes.

```
# Correct
chore: address review comments — clarify dry-run output

# Wrong — will pollute the CHANGELOG
fix: address review comments — clarify dry-run output
```

### Separate generator changes from regenerated output

When a change modifies the generator (hooks under `hooks/`, `generate.py`, generator config, `runtime/` files that get copied verbatim, build scripts) **and** that change causes `generated/*` (and/or `stubs/*`) to differ, **split the work into two commits**:

1. **First commit** — generator change only: hook / `runtime/` / config / script / test edits. No `generated/*` or `stubs/*` changes.
2. **Second commit** — regenerated output: `generated/*` and `stubs/*` produced by running the pipeline against the first commit.

Why:

- **Cherry-picks stay clean.** Backports to `stable/*` only need the generator commit; the target branch's release CI regenerates `generated/*` itself. Mixing the two means the cherry-pick drags generated diff through, which conflicts with whatever generated state the target branch has.
- **Reviewers can read the change.** Generator commits are small and meaningful; regenerated commits are large and mechanical. Mixing them makes the review effectively unreadable.
- **`git blame` stays useful** for both surfaces.

Naming convention for the second commit (mirrors the existing release-pipeline convention `chore(generation): update generated SDK [skip ci]`):

```
chore(generation): regenerate SDK for <short summary of generator change>
```

If `make generate` modifies `generated/*` or `stubs/*` after the generator commit, `git add` those directories and commit them separately — do **not** amend them back into the generator commit.

The pre-push checklist below still applies: always run `make generate && make lint && make typecheck && make test` before pushing, and commit any regenerated drift before the push.

## Pre-push checklist

Before pushing any commits, **always** run:

1. `make generate` — regenerates `generated/` from the bundled spec.
2. `make lint` — ruff lint.
3. `make typecheck` — `pyright` on generated + tests + stubs.
4. `make test` — acceptance tests.

If any step modifies tracked files (e.g. `generated/*` drift, README snippet drift, stub drift), commit those changes before pushing — and respect the **separate-commits rule** above when the modified files are under `generated/` or `stubs/`.

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

### There are no flaky tests

We do not acknowledge the existence of "flaky tests". A test that passes sometimes and fails other times is reporting one of two things:

1. **A test defect** — the test contains a race, an unbounded timeout, an order-of-operation assumption, an unsynchronised readiness signal, or a dependency on wall-clock timing. Fix the test so its outcome is deterministic for the behaviour it claims to assert.
2. **A product defect** — the production code has a race, a missed signal, an unhandled error path, or a resource it leaks under load. Fix the product.

Either way, an intermittent failure is a real defect that must be diagnosed and fixed before the change merges. Do not retry the CI job, mark the test `@pytest.mark.skip`, or describe the failure as "flaky" or "unrelated" in the PR description. "Re-run and hope" is a coping strategy, not engineering.

When triaging an intermittent CI failure:

- Reproduce locally if possible (loops, resource pressure, timeout reduction). If you cannot reproduce, reason from first principles about what *could* differ between local and CI (load, filesystem semantics, signal delivery latency, parallel test interaction).
- Identify the specific race or assumption. Common shapes: polling for an output line that is printed *before* the relevant handler is registered; timeouts that double as correctness assertions; tests that share a temp directory across runs; tests that depend on event ordering across two processes.
- Pick category 1 vs category 2 explicitly in the fix commit message, and explain which signal the test was previously relying on and which deterministic signal it now relies on.
- If timeouts must be generous to absorb runner load, the timeout is a safety net — not a correctness signal. State this in a comment so future maintainers don't tighten it back into a race.

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
