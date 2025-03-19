.PHONY: lint format install test clean outdated upgrade-deps run inspector hooks dev-server stop-server claude-install claude-uninstall claude-uninstall-manual
SHELL := /bin/bash

hooks:	.git/hooks/pre-commit

.git/hooks/pre-commit: hooks/pre-commit
	@echo "Installing hooks..."
	@cp $? $@

install:
	@echo "Installing dependencies with uv..."
	@uv sync

dev-server:
	@echo "Starting MCP server in development mode..."
	@uv run mcp dev mcp_server.py:server -e .

stop-server:
	@echo "Stopping MCP server and Inspector..."
	@-pkill -f "mcp dev" 2>/dev/null || true
	@-pkill -f "node.*modelcontextprotocol/inspector" 2>/dev/null || true
	@echo "Server stopped."

claude-install:
	@echo "Installing weather MCP server in Claude Desktop..."
	@uv run mcp install mcp_server.py:server --name weather -e .
	@echo "Weather MCP server installed in Claude Desktop. Please restart Claude to apply changes."

claude-uninstall:
	@echo "Uninstalling weather MCP server from Claude Desktop..."
	@CONFIG_DIR="$$HOME/Library/Application Support/Claude/claude_desktop_config.json" && \
	if [ -f "$$CONFIG_DIR" ]; then \
		echo "Updating Claude Desktop configuration..."; \
		TMP_FILE=$$(mktemp) && \
		jq 'if .mcpServers.weather then del(.mcpServers.weather) else . end' "$$CONFIG_DIR" > "$$TMP_FILE" && \
		mv "$$TMP_FILE" "$$CONFIG_DIR" && \
		echo "Weather MCP server removed from Claude Desktop. Please restart Claude to apply changes."; \
	else \
		echo "Claude Desktop configuration not found. Nothing to uninstall."; \
	fi

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
	@uv lock --upgrade
	@uv sync
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
	@echo "  dev-server   - Start the MCP server in development mode"
	@echo "  stop-server  - Stop the MCP server and Inspector"
	@echo "  claude-install - Install the server in Claude Desktop"
	@echo "  claude-uninstall - Uninstall the server from Claude Desktop"
