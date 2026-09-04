.PHONY: install test lint site preview build

install:
	python -m pip install -e ".[dev]"

test:
	behave

lint:
	ruff check src features

site:
	markus site site --out _site

preview:
	markus site site --out _site --serve --port 43147

build:
	python -m build
