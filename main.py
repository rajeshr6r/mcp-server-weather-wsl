"""Main entry point for the weather MCP server."""

from src.weather import main as server_main


def main():
    """Run the weather MCP server."""
    server_main()


if __name__ == "__main__":
    main()
