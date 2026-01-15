.PHONY: install sync start build clean

# Install npm dependencies
install:
	npm install

# Sync markdown from parent project's generated docs
sync:
	@if [ ! -f ../../public/markdown/index.md ]; then \
		echo "Error: Run 'make docs-api' from project root first"; \
		exit 1; \
	fi
	mkdir -p docs/api
	cp ../../public/markdown/index.md docs/api/python-sdk-api.md
	@echo "Synced docs/api/python-sdk-api.md"

# Start dev server (runs sync first)
start: sync
	npm start

# Build static site
build: sync
	npm run build

# Clean generated files
clean:
	rm -rf docs/api build .docusaurus
