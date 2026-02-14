.PHONY: install generate clean test itest docs-api bundle-spec typecheck-examples

# Git ref/branch/tag/SHA in https://github.com/camunda/camunda.git to fetch the OpenAPI spec from.
# Override like: `make generate SPEC_REF=45369-fix-spec`
SPEC_REF ?= main

BUNDLED_SPEC = external-spec/bundled/rest-api.bundle.json

install:
	mkdir -p generated
	uv sync

# Fetch & bundle the upstream OpenAPI spec using camunda-schema-bundler.
# Produces external-spec/bundled/rest-api.bundle.json + spec-metadata.json
bundle-spec:
	SPEC_REF=$(SPEC_REF) bash scripts/bundle-spec.sh

# Generate using the pre-bundled spec from camunda-schema-bundler
generate: clean install bundle-spec
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests --bundled-spec $(BUNDLED_SPEC)
	uv run ruff format generated/
	uv run ruff check generated/ --fix
	uv run pyright
	uv run pytest -q tests/acceptance

# Generate using already-bundled spec (skip fetch, fast local iteration)
generate-local: clean install
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests --bundled-spec $(BUNDLED_SPEC)
	uv run ruff format generated/
	uv run ruff check generated/ --fix
	uv run pyright
	uv run pytest -q tests/acceptance

clean:
	rm -rf generated

clean_spec:
	rm -rf .openapi-cache external-spec

itest: generate
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

test:
	uv run pytest -q tests/acceptance

lint:
	uv run ruff check .

typecheck:
	uv run pyright

typecheck-examples:
	uv run pyright examples/

docs-api:
	PYTHONPATH=./generated uv run pdoc camunda_orchestration_sdk -o ./public --docformat google

config-reference:
	uv run scripts/generate_config_reference.py

config-reference-check:
	uv run scripts/generate_config_reference.py --check

clean-docs:
	rm -rf ./public

preview-docs: clean-docs docs-api
	@echo "Starting pdoc server at http://localhost:8080..."
	PYTHONPATH=./generated uv run pdoc camunda_orchestration_sdk --docformat google