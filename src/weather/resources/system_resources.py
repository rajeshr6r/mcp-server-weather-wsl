"""System resources for the MCP server."""

import logging
from typing import List

from ..services.system_service import get_top_processes

# Configure logging
logger = logging.getLogger(__name__)


def register_resources(server):
    """
    Register all system resources with the server.

    Args:
        server: MCP server instance
    """

    @server.resource("processes://top")
    def get_top_processes_resource() -> List[str]:
        """
        Get the top 10 processes currently running on the workstation.

        Returns:
            List of formatted process strings
        """
        processes = get_top_processes(limit=10)

        if not processes:
            return ["Error getting process information"]

        return [
            f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']:.1f}%"
            for proc in processes
        ]
