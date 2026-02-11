.PHONY: install generate clean test itest docs-api regenerate

# Git ref/branch/tag/SHA in https://github.com/camunda/camunda.git to fetch the OpenAPI spec from.
# Override like: `make generate SPEC_REF=45369-fix-spec`
SPEC_REF ?= main

install:
	mkdir -p generated
	uv sync

generate-v1: clean install
	uv run generate.py --spec-ref $(SPEC_REF)

generate: clean install
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests --spec-ref $(SPEC_REF)
	uv run ruff format generated/
	uv run ruff check generated/ --fix
	uv run pyright
	uv run pytest -q tests/acceptance

clean:
	rm -rf generated

clean_spec:
	rm -rf .openapi-cache

itest: generate
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

regenerate: generate
	@if git diff --quiet generated/; then \
		echo "No changes to generated code."; \
	else \
		git add generated/; \
		git commit -m "chore: regenerate SDK"; \
		echo "Committed regenerated SDK output."; \
	fi

test:
	uv run pytest -q tests/acceptance

lint:
	uv run ruff check .

typecheck:
	uv run pyright

docs-api:
	PYTHONPATH=./generated uv run pdoc camunda_orchestration_sdk -o ./public --docformat google

clean-docs:
	rm -rf ./public

preview-docs: clean-docs docs-api
	@echo "Starting pdoc server at http://localhost:8080..."
	PYTHONPATH=./generated uv run pdoc camunda_orchestration_sdk --docformat google