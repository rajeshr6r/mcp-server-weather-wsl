"""System tools for the MCP server."""

import logging


# Configure logging
logger = logging.getLogger(__name__)


def register_tools(server):
    """
    Register all system tools with the server.

    Args:
        server: MCP server instance
    """

    @server.tool()
    async def run_shell_command(command: str) -> str:
        """
        Run a shell command and return the output.

        Args:
            command: Shell command to execute

        Returns:
            Command output or error message
        """
        result = run_shell_command(command)

        if result["success"]:
            return result["stdout"]
        else:
            return f"Error: {result['stderr']}"
