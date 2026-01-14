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

docs-api-old:
	uv pip install pdoc --system
	# install root project (and all its dependencies)
	uv pip install -e . --system
	PYTHONPATH=./generated pdoc camunda_orchestration_sdk -o ./public --docformat google

clean-docs:
	rm -rf ./public

preview-docs: clean-docs docs-api
	@echo "Starting pdoc server at http://localhost:8080..."
	PYTHONPATH=./generated pdoc camunda_orchestration_sdk --docformat google

docs-api:
	# 1. Install Sphinx and SDK dependencies
	uv pip install sphinx sphinx-markdown-builder --system
	uv pip install -e . --system

	# 2. Clean previous Sphinx build cache
	rm -rf public

	# 3. Build HTML for GitHub Pages preview
	PYTHONPATH=./generated sphinx-build -M html docs-sphinx public

	# 4. Add .nojekyll to prevent GitHub Pages from ignoring _static folder
	touch ./public/html/.nojekyll

	# 5. Build Markdown for Docusaurus integration
	PYTHONPATH=./generated sphinx-build -M markdown docs-sphinx public

	# 6. Copy markdown into HTML folder for GitHub Pages access at /markdown/
	cp -R ./public/markdown ./public/html/markdown

	# 7. Copy markdown to Docusaurus folder and add frontmatter
	mkdir -p ./website/docs/api
	cp -R ./public/markdown/* ./website/docs/api/
	@# Add Docusaurus frontmatter to index.md
	@echo '---\nid: api-reference\ntitle: Python SDK API Reference\nsidebar_label: API Reference\n---\n' | cat - ./website/docs/api/index.md > ./website/docs/api/index.md.tmp && mv ./website/docs/api/index.md.tmp ./website/docs/api/index.md

	@echo "HTML docs: ./public/html (GitHub Pages root)"
	@echo "Markdown: ./public/html/markdown (GitHub Pages /markdown/)"
	@echo "Docusaurus: ./website/docs/api"