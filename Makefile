.PHONY: install generate clean test itest

install:
	mkdir -p generated
	uv sync

generate: clean install
	uv run generate.py 

generate-v2: clean install
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests

clean:
	rm -rf generated

clean_spec:
	rm -rf .openapi-cache
	
test: generate-v2
	uv run pytest -q tests/acceptance

itest: generate-v2
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

