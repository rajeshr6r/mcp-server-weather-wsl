.PHONY: lint format install
SHELL := /bin/bash

install:
	@echo "Installing dependencies..."
	@uv pip install --upgrade pip
	@uv pip install -e .

lint:
	@echo "Running linter..."
	@uv run ruff check . --fix

format:
	@echo "Running formatter..."
	@uv run black .

format-check:
	@echo "Checking formatting..."
	@uv run black --check .

lint-format: lint format
	@echo "Completed linting and formatting."

.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo "  install      - Install project dependencies"
	@echo "  lint         - Run ruff linter with auto-fix"
	@echo "  format       - Run black formatter"
	@echo "  format-check - Check if files would be reformatted by black"
	@echo "  lint-format  - Run both linter and formatter"
