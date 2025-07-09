.PHONY: install install-dev test clean docs docs-serve docs-build docs-watch

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

# Setup the documentation environment
docs-setup:
	uv venv docs-venv
	source docs-venv/bin/activate && uv pip install mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-git-authors-plugin mkdocs-minify-plugin watchdog

# Build the documentation
docs-build:
	source docs-venv/bin/activate && mkdocs build --clean --strict

# Serve the documentation with live reload
docs-serve:
	source docs-venv/bin/activate && mkdocs serve --dirtyreload --livereload

# Watch for changes and rebuild automatically with custom template handling
docs-watch:
	source docs-venv/bin/activate && python3 watch_docs.py

test:
	pytest tests -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

pypi: clean
	uv build
	uv publish
