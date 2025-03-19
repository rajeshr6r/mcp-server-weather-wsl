"""Tools package for the MCP server."""

from .weather_tools import register_tools as register_weather_tools
from .system_tools import register_tools as register_system_tools


def register_all_tools(server):
    """
    Register all tools with the server.

    Args:
        server: MCP server instance
    """
    register_weather_tools(server)
    register_system_tools(server)
