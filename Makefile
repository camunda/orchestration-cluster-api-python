.PHONY: install generate clean test itest docs-api docs-md bundle-spec typecheck-examples clean-docs preview-docs

# Git ref/branch/tag/SHA in https://github.com/camunda/camunda.git to fetch the OpenAPI spec from.
# Override like: `make generate SPEC_REF=45369-fix-spec`
SPEC_REF ?= main

BUNDLED_SPEC = external-spec/bundled/rest-api.bundle.json

install:
	mkdir -p generated
	uv sync
	uv run pre-commit install

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
	rm -rf public
	# Build HTML for GitHub Pages preview
	PYTHONPATH=./generated uv run sphinx-build -M html docs-sphinx public
	touch ./public/html/.nojekyll
	# Build multi-page Markdown for Docusaurus integration
	PYTHONPATH=./generated uv run sphinx-build -M markdown docs-sphinx public
	# Post-process all markdown files for Docusaurus compatibility
	uv run python scripts/postprocess_markdown.py ./public/markdown/
	# Move API reference files into subdirectory
	mkdir -p public/markdown/api-reference
	mv public/markdown/*.md public/markdown/api-reference/
	# Generate pages from README + API Reference category metadata
	uv run python scripts/generate_landing_page.py
	# Copy markdown into HTML folder for GitHub Pages access at /markdown/
	cp -R ./public/markdown ./public/html/markdown
	@echo "HTML docs:  ./public/html  (GitHub Pages root)"
	@echo "Markdown:   ./public/html/markdown  (GitHub Pages /markdown/)"

# Generate only the Docusaurus-ready markdown (no HTML, used by CI sync)
docs-md:
	rm -rf public/markdown
	PYTHONPATH=./generated uv run sphinx-build -M markdown docs-sphinx public
	uv run python scripts/postprocess_markdown.py ./public/markdown/
	mkdir -p public/markdown/api-reference
	mv public/markdown/*.md public/markdown/api-reference/
	uv run python scripts/generate_landing_page.py
	@echo "Markdown docs: ./public/markdown/"


config-reference:
	uv run scripts/generate_config_reference.py

config-reference-check:
	uv run scripts/generate_config_reference.py --check

clean-docs:
	rm -rf ./public

preview-docs: clean-docs docs-api
	@echo "Serving HTML docs at http://localhost:8080..."
	python3 -m http.server 8080 --directory public/html
