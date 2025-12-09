.PHONY: install generate clean test itest

install:
	mkdir -p generated
	uv sync

generate-v1: clean install
	uv run generate.py 

generate: clean install
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests

clean:
	rm -rf generated

clean_spec:
	rm -rf .openapi-cache
	
test: generate
	uv run pytest -q tests/acceptance

itest: generate
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

