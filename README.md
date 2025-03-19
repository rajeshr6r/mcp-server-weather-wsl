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
python -m main
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

2. Restart Claude Desktop
3. Connect to the weather server from Claude

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
| `dev`        | Install development dependencies using uv    |
| `lint`       | Run ruff linter with auto-fix using uv       |
| `format`     | Run black formatter using uv                 |
| `format-check` | Check if files would be reformatted by black |
| `lint-format`| Run both linter and formatter                |
| `test`       | Run tests using pytest with uv               |
| `clean`      | Remove build artifacts and cache files       |

Run `make help` to see all available targets.

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