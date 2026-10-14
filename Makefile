.PHONY: install generate generate-only generate-local clean test itest itest-deps itest-only itest-local docs-api docs-md docs-link-check bundle-spec typecheck-examples clean-docs preview-docs sync-readme sync-readme-check check escape-hatch-check escape-hatch-update

# Git ref/branch/tag/SHA in https://github.com/camunda/camunda.git to fetch the OpenAPI spec from.
# Override like: `make generate SPEC_REF=45369-fix-spec`
SPEC_REF ?= main

BUNDLED_SPEC = external-spec/bundled/rest-api.bundle.json

install:
	mkdir -p generated
	uv sync
	bash scripts/setup-hooks.sh

# Fetch & bundle the upstream OpenAPI spec using camunda-schema-bundler.
# Produces external-spec/bundled/rest-api.bundle.json + spec-metadata.json
bundle-spec:
	SPEC_REF=$(SPEC_REF) bash scripts/bundle-spec.sh

# Generate using the pre-bundled spec from camunda-schema-bundler
generate: clean install bundle-spec
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests --bundled-spec $(BUNDLED_SPEC)
	uv run ruff format generated/ stubs/
	uv run ruff check generated/ --fix
	uv run ty check
	uv run ty check examples/
	uv run pytest -q tests/acceptance
	uv run python scripts/sync-readme-snippets.py --check
	uv run scripts/generate_config_reference.py

# Generate using already-bundled spec (skip fetch, fast local iteration).
# Pure generation only — no validation and no dependency install. CI installs
# dependencies once in the workflow and calls this directly, so the SDK is
# generated once per matrix job without a redundant `uv sync`; the validation
# steps (ty, acceptance, readme, config) run as their own explicit, deduplicated
# steps. Local callers use `generate-local`, which installs first.
generate-only: clean
	mkdir -p generated
	uv run generate.py --generator openapi-python-client --config generator-config-python-client.yaml --skip-tests --bundled-spec $(BUNDLED_SPEC)
	uv run ruff format generated/ stubs/
	uv run ruff check generated/ --fix

# Full local generate: dependency install, generation, plus the validation suite
# (used by developers and by itest-local).
generate-local: install generate-only
	uv run ty check
	uv run ty check examples/
	uv run pytest -q tests/acceptance
	uv run python scripts/sync-readme-snippets.py --check
	uv run scripts/generate_config_reference.py

clean:
	rm -rf generated

clean_spec:
	rm -rf .openapi-cache external-spec

# Integration tests only — assumes dependencies (incl. the itest group) are
# already installed. CI installs once in the workflow; local callers go through
# `itest`/`itest-local`, which sync the itest group via `itest-deps` first.
itest-only:
	CAMUNDA_INTEGRATION=1 uv run pytest -q tests/integration

# Sync dependencies including the integration-test group (local convenience).
itest-deps:
	uv sync --group itest

itest: generate itest-deps itest-only

# Integration tests using already-bundled spec (for CI with pre-fetched artifact)
itest-local: generate-local itest-deps itest-only

test:
	uv run pytest -q tests/acceptance

lint:
	uv run ruff check .

typecheck:
	uv run ty check

# Ratcheting guard: fail if new # type: ignore / cast / Any are added to runtime/ or hooks/.
escape-hatch-check:
	uv run python scripts/check_escape_hatches.py

# Rewrite the escape-hatch baseline to the current counts.
escape-hatch-update:
	uv run python scripts/check_escape_hatches.py --update

check: lint typecheck escape-hatch-check

typecheck-examples:
	uv run ty check examples/

docs-api:
	rm -rf public
	# Build HTML for GitHub Pages preview
	PYTHONPATH=./generated uv run sphinx-build -M html docs-sphinx public
	touch ./public/html/.nojekyll
	# Build multi-page Markdown for Docusaurus integration
	PYTHONPATH=./generated uv run sphinx-build -M markdown docs-sphinx public
	# Post-process all markdown files for Docusaurus compatibility
	uv run python scripts/postprocess_markdown.py ./public/markdown/
	# Move API reference files into python-sdk/api-reference subdirectory
	mkdir -p public/markdown/python-sdk/api-reference
	mv public/markdown/*.md public/markdown/python-sdk/api-reference/
	# Generate landing page (sibling of python-sdk/) + section pages (inside python-sdk/)
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
	mkdir -p public/markdown/python-sdk/api-reference
	mv public/markdown/*.md public/markdown/python-sdk/api-reference/
	uv run python scripts/generate_landing_page.py --validate-links
	@echo "Markdown docs: ./public/markdown/"

# Validate that generated docs contain no broken links (fast, no Sphinx needed)
docs-link-check:
	uv run python scripts/generate_landing_page.py --output-dir public/markdown-check --validate-links
	rm -rf public/markdown-check


config-reference:
	uv run scripts/generate_config_reference.py

config-reference-check:
	uv run scripts/generate_config_reference.py --check

sync-readme:
	uv run python scripts/sync-readme-snippets.py

sync-readme-check:
	uv run python scripts/sync-readme-snippets.py --check

clean-docs:
	rm -rf ./public

preview-docs: clean-docs docs-api
	@echo "Serving HTML docs at http://localhost:8080..."
	python3 -m http.server 8080 --directory public/html
