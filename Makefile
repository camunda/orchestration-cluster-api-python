.PHONY: install generate clean test itest

install:
	mkdir -p generated
	uv sync

generate: install
	uv run generate.py 

clean:
	rm -rf generated .openapi-cache .venv

test: generate
	uv run pytest -q tests/acceptance

itest: generate
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

