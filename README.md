# Weather MCP Server

## Overview

This project implements a Model Context Protocol (MCP) server that provides weather information services. It leverages the National Weather Service (NWS) API to fetch weather alerts and forecasts, and exposes them as tools that can be used by MCP clients like Claude.

The server is built with a modular architecture following best practices for Python projects, making it easy to maintain and extend.

### Features

- **Weather Tools**: Get weather alerts for states and forecasts for specific coordinates
- **System Tools**: Run shell commands and view system process information
- **MCP Integration**: Seamlessly integrates with MCP clients like Claude Desktop

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/weather.git
   cd weather
   ```

2. Install dependencies using uv:
   ```bash
   make install
   ```

3. For development, install additional dependencies:
   ```bash
   make dev
   ```

## Usage

### Running the Server

To start the MCP server:

```bash
make run
```

Or directly with uv:

```bash
uv run python -m main
```

### Connecting to Claude Desktop

1. Update your Claude Desktop configuration to include the weather server:

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/path/to/weather"
    }
  }
}
```
2. Restart Claude Desktop to apply the changes

3. In Claude Desktop, you can now select the "weather" MCP server from the MCP server dropdown menu

The weather MCP server will be available to Claude Desktop, allowing you to interact with weather data directly in your conversations.

### Example Queries

Once connected, you can ask Claude:

- "What are the current weather alerts in CA?"
- "What's the forecast for latitude 37.7749, longitude -122.4194?"
- "What processes are using the most CPU on my system?"

## Project Structure

```
weather/
├── src/
│   └── weather/
│       ├── __init__.py          # Package initialization
│       ├── server.py            # Main server setup
│       ├── tools/               # Tool implementations
│       │   ├── __init__.py
│       │   ├── weather_tools.py
│       │   └── system_tools.py
│       ├── resources/           # Resource implementations
│       │   ├── __init__.py
│       │   └── system_resources.py
│       ├── services/            # External service integrations
│       │   ├── __init__.py
│       │   ├── weather_service.py
│       │   └── system_service.py
│       └── utils/               # Helper functions
│           ├── __init__.py
│           ├── http.py
│           └── formatting.py
├── tests/                       # Test suite
├── main.py                      # Entry point
├── pyproject.toml               # Dependencies and metadata
├── Makefile                     # Build commands
└── README.md                    # This file
```

## Make Targets

The project includes several make targets to simplify development:

| Target       | Description                                  |
|--------------|----------------------------------------------|
| `install`    | Install project dependencies using uv        |
| `lint`       | Run ruff linter with auto-fix using uv       |
| `format`     | Run black formatter using uv                 |
| `format-check` | Check if files would be reformatted by black |
| `lint-format`| Run both linter and formatter                |
| `test`       | Run tests using pytest with uv               |
| `clean`      | Remove build artifacts and cache files       |
| `outdated`   | Check for outdated dependencies using uv     |
| `upgrade-deps` | Upgrade all outdated dependencies using uv   |
| `run`        | Start the MCP server using uv                |
| `inspector`  | Start the MCP Inspector for testing          |
| `hooks`      | Install git hooks                            |
| `dev-server` | Start the MCP server in development mode     |
| `stop-server`| Stop the MCP server and Inspector            |
| `claude-install` | Install the server in Claude Desktop     |
| `claude-uninstall` | Uninstall the server from Claude Desktop |

Run `make help` to see all available targets.

### Using with Claude Desktop

To use the weather MCP server with Claude Desktop:

1. Install the server in Claude Desktop:

```bash
make claude-install
```

This will:
- Use the MCP CLI to install the server in Claude Desktop
- Install the project in editable mode (`-e .`)
- Register the server with the name "weather"
- Configure the server to run from your project directory

2. Restart Claude Desktop to apply the changes

3. In Claude Desktop, you can now select the "weather" MCP server from the MCP server dropdown menu

The weather MCP server will be available to Claude Desktop, allowing you to interact with weather data directly in your conversations.

To uninstall the server from Claude Desktop:

```bash
make claude-uninstall
```

This will remove the weather MCP server configuration from Claude Desktop. You'll need to restart Claude to apply the changes.

### Development Mode

For active development with automatic reloading when code changes:

```bash
# Start the server in development mode with the MCP Inspector
make dev-server
```

This will:
1. Start the MCP server using the `mcp dev` command
2. Install the project in editable mode (`-e .`)
3. Launch the MCP Inspector automatically
4. Enable automatic reloading when your code changes

The MCP Inspector will be available at http://localhost:5173 in your web browser.

To stop the server and Inspector:

```bash
make stop-server
```

This setup is ideal for iterative development as the server will automatically reload when you make changes to your code.

### Inspector Features

The MCP Inspector allows you to:

1. **Explore Tools**: View all available tools, their parameters, and documentation.
2. **Call Tools**: Execute tools with custom parameters and see the results.
3. **Browse Resources**: View all available resources and their current values.
4. **Test Prompts**: If your server provides prompt templates, you can test them with different inputs.
5. **View Logs**: See detailed logs of all interactions between the Inspector and your server.

### Testing Weather Tools

With the Inspector, you can easily test the weather tools:

1. Find the `get_weather_alerts` tool in the Inspector interface
2. Enter a state code (e.g., "CA", "NY", "FL") in the parameters field
3. Execute the tool and view the results

Similarly, you can test the `get_forecast` tool by providing latitude and longitude coordinates.

### Testing System Tools

The Inspector also makes it easy to test system tools:

1. Find the `run_shell_command` tool
2. Enter a safe command (e.g., "ls -la", "echo hello") in the parameters field
3. Execute the tool and view the results

### Debugging with the Inspector

The Inspector is particularly useful for debugging:

1. It shows detailed error messages if a tool call fails
2. You can see the exact request and response payloads
3. It helps identify issues with parameter validation or tool implementation

For more information about the MCP Inspector, visit the [Model Context Protocol documentation](https://modelcontextprotocol.io/).

## Testing Locally

You can test your MCP server locally using the MCP CLI tool that comes with the `mcp[cli]` package:

1. Start your server:
   ```bash
   make run
   ```

2. In a separate terminal, use the MCP CLI to interact with your server:

   ```bash
   # List all available tools
   make inspector
   
   # Call a specific weather tool
   mcp call-tool http://localhost:8000 get_weather_alerts --args '{"state": "CA"}'
   
   # Get a weather forecast
   mcp call-tool http://localhost:8000 get_forecast --args '{"latitude": 37.7749, "longitude": -122.4194}'
   
   # List system resources
   mcp list-resources http://localhost:8000
   
   # Get system processes
   mcp get-resource http://localhost:8000 top_processes
   ```

If you're using uv directly, you can run the MCP CLI with:

```bash
uv run mcp list-tools http://localhost:8000
```

## Development

### Adding New Tools

To add a new tool to the server:

1. Create a function in the appropriate tools module
2. Register it with the `@server.tool()` decorator
3. Update the tool registration in `tools/__init__.py`

Example:

```python
@server.tool()
async def my_new_tool(param1: str, param2: int) -> str:
    """
    Tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    # Implementation
    return result
```

### Adding New Resources

To add a new resource:

1. Create a function in the appropriate resources module
2. Register it with the `@server.resource()` decorator
3. Update the resource registration in `resources/__init__.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [National Weather Service API](https://www.weather.gov/documentation/services-web-api) for weather data
