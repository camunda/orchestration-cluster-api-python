.PHONY: install generate clean test itest

install:
	mkdir -p generated
	uv sync

generate: install
	uv run generate.py 

generate-v2: install
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests

clean:
	rm -rf generated .openapi-cache .venv

test: generate-v2
	uv run pytest -q tests/acceptance

itest: generate-v2
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

