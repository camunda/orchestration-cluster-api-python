.PHONY: install generate clean test itest docs-api docs-sphinx-md clean-docs preview-docs generate-v1

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

test:
	uv run pytest -q tests/acceptance

lint:
	uv run ruff

typecheck:
	uv run pyright

docs-api:
	PYTHONPATH=./generated uv run pdoc camunda_orchestration_sdk -o ./public --docformat google

clean-docs:
	rm -rf ./public

preview-docs: clean-docs docs-api
	@echo "Starting pdoc server at http://localhost:8080..."
	PYTHONPATH=./generated pdoc camunda_orchestration_sdk --docformat google

docs-sphinx-md:
	# 1. Install dependencies
	uv pip install sphinx sphinx-markdown-builder --system
	
	# 2. Run Sphinx build
	# -M markdown: use the markdown builder
	# docs-sphinx: the directory with your conf.py and index.rst
	# public: the output directory
	PYTHONPATH=./generated sphinx-build -M markdown docs-sphinx public
	
	# 3. Clean up: Sphinx-markdown-builder puts files in public/markdown
	# We move them to our Docusaurus folder
	mkdir -p ./website/docs/api
	cp -R ./public/markdown/* ./website/docs/api/
	@echo "Sphinx Markdown docs are now in ./website/docs/api"