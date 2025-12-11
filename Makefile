.PHONY: install generate clean test itest

install:
	mkdir -p generated
	uv sync

generate-v1: clean install
	uv run generate.py 

generate: clean install
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests
	uv run pytest -q tests/acceptance

clean:
	rm -rf generated

clean_spec:
	rm -rf .openapi-cache

itest: generate
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

lint:
	uv run ruff

typecheck:
	uv run pyright