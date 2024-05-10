SHELL:=/usr/bin/env bash


build:
	flit build

install:
	flit install

extract_messages:
	@echo 'extract messages'

compile_messages:
	@echo "compile messages"

.PHONY: lint_python
lint_python:
	flake8 .
	mypy . || true
	pydocstyle src/x6tools
	find . -type f -name '*.py' | xargs pyupgrade --py37-plus

.PHONY: lint_formatting
lint_formatting:
	black --check .
	isort --check-only .

.PHONY: lint_spelling
lint_spelling:
	codespell || true

.PHONY: lint_deps
lint_deps:
	pip check
	safety check --full-report

.PHONY: lint
lint: lint_python lint_formatting lint_spelling lint_deps

.PHONY: test
test:
	pytest

.PHONY: ci
ci: lint test
