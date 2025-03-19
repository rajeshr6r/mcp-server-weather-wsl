.PHONY: lint format install test clean dev outdated upgrade-deps run inspector
SHELL := /bin/bash

install:
	@echo "Installing dependencies with uv..."
	@uv pip install --upgrade pip
	@uv pip install -e .

dev:
	@echo "Installing development dependencies with uv..."
	@uv pip install -e ".[dev]"

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
	@echo "  clean        - Remove build artifacts and cache files"
	@echo "  outdated     - Check for outdated dependencies using uv"
	@echo "  upgrade-deps - Upgrade all outdated dependencies using uv"
	@echo "  run          - Start the MCP server"
	@echo "  inspector    - Start the MCP Inspector for testing"
	@echo "  inspector-dev - Start the MCP Inspector with hot reloading"
