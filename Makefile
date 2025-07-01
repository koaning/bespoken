.PHONY: docs

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf *.egg
	rm -rf *.whl
	rm -rf *.tar.gz

docs:
	marimo --yes export html-wasm demo.py -o docs --mode edit

pypi: clean
	uv build
	uv publish
