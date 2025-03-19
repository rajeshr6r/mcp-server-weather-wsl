"""Resources package for the MCP server."""

from .system_resources import register_resources as register_system_resources


def register_all_resources(server):
    """
    Register all resources with the server.

    Args:
        server: MCP server instance
    """
    register_system_resources(server)
