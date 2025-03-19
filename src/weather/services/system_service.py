"""System service for interacting with the local system."""

import logging
import subprocess
import psutil
from typing import List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)


def run_shell_command(command: str) -> Dict[str, Any]:
    """
    Run a shell command and return the output.

    Args:
        command: Shell command to execute

    Returns:
        Dictionary with success status, stdout, and stderr
    """
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command '{command}': {str(e)}")
        return {"success": False, "stdout": "", "stderr": str(e.stderr)}


def get_top_processes(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the top processes by CPU usage.

    Args:
        limit: Maximum number of processes to return

    Returns:
        List of process information dictionaries
    """
    try:
        # Get all processes and filter out ones with None CPU percentage
        processes = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent"]):
            try:
                info = proc.info
                if info["cpu_percent"] is not None:
                    processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Sort by CPU percentage and get top N
        return sorted(processes, key=lambda p: p["cpu_percent"], reverse=True)[:limit]
    except Exception as e:
        logger.error(f"Error getting process information: {str(e)}")
        return []
