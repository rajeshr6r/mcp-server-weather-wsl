import subprocess
import psutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Shell Command Server")


@mcp.tool()
async def run_shell_command(command: str) -> str:
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"


@mcp.resource("processes://top")
def get_top_processes() -> list[str]:
    """Get the top 10 processes currently running on the workstation."""
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

        # Sort by CPU percentage and get top 10
        top_processes = sorted(processes, key=lambda p: p["cpu_percent"], reverse=True)[
            :10
        ]

        # Format the output
        return [
            f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']:.1f}%"
            for proc in top_processes
        ]
    except Exception as e:
        return [f"Error getting process information: {str(e)}"]


if __name__ == "__main__":
    mcp.run()
