.PHONY: lint format install test clean dev outdated upgrade-deps run inspector hooks
SHELL := /bin/bash

hooks:	.git/hooks/pre-commit

.git/hooks/pre-commit: hooks/pre-commit
	@echo "Installing hooks..."
	@cp $? $@

install:
	@echo "Installing dependencies with uv..."
	@uv pip install --upgrade pip
	@uv pip install -e .

dev:
	@echo "Installing development dependencies with uv..."
	@uv pip install -e ".[dev]"
	@uv pip install pre-commit

lint:
	@echo "Running linter with uv..."
	@uv run ruff check --fix .

format:
	@echo "Running formatter with uv..."
	@uv run black .

format-check:
	@echo "Checking formatting with uv..."
	@uv run black --check .

lint-format: lint format
	@echo "Completed linting and formatting."

test:
	@echo "Running tests with uv..."
	@uv run pytest

test-cov:
	@echo "Running tests with coverage..."
	@uv run pytest --cov=src --cov-report=term --cov-report=html

test-verbose:
	@echo "Running tests in verbose mode..."
	@uv run pytest -v

test-watch:
	@echo "Running tests in watch mode..."
	@uv run python -m pytest_watch -- -v

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .ruff_cache/ __pycache__/ 
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

outdated:
	@echo "Checking for outdated dependencies..."
	@uv pip list --outdated --format columns

upgrade-deps:
	@echo "Upgrading all outdated dependencies..."
	@OUTDATED=$$(uv pip list --outdated | grep -v "^Package" | grep -v "^-------" | awk '{print $$1}'); \
	if [ -n "$$OUTDATED" ]; then \
		echo "Upgrading: $$OUTDATED"; \
		uv pip install --upgrade $$OUTDATED; \
	else \
		echo "No outdated packages found."; \
	fi
	@echo "Dependencies upgraded successfully!"

run:
	@echo "Starting MCP server with uv..."
	@uv run python -m main

inspector:
	@echo "Starting MCP Inspector for testing..."
	@npx @modelcontextprotocol/inspector uv run python -m main

hook-install:
	@echo "Installing git hooks..."
	@mkdir -p .git/hooks
	@cp -f hooks/pre-commit .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "Git hooks installed successfully!"

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  install      - Install project dependencies using uv"
	@echo "  dev          - Install development dependencies using uv"
	@echo "  lint         - Run ruff linter with auto-fix using uv"
	@echo "  format       - Run black formatter using uv"
	@echo "  format-check - Check if files would be reformatted by black"
	@echo "  lint-format  - Run both linter and formatter"
	@echo "  test         - Run tests using pytest with uv"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  test-verbose - Run tests in verbose mode"
	@echo "  test-watch   - Run tests in watch mode (auto-rerun on file changes)"
	@echo "  clean        - Remove build artifacts and cache files"
	@echo "  outdated     - Check for outdated dependencies using uv"
	@echo "  upgrade-deps - Upgrade all outdated dependencies using uv"
	@echo "  run          - Start the MCP server"
	@echo "  inspector    - Start the MCP Inspector for testing"
	@echo "  hooks         - Install git hooks"
