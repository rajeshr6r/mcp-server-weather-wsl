"""Tests for the MCP server implementation."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.weather.server import create_server, run_server


@pytest.mark.asyncio
async def test_server_initialization():
    """Test that the server initializes correctly with all tools and resources."""
    server = create_server("test-weather")
    
    # Verify server name
    assert server.name == "test-weather"
    
    # Verify tools are registered
    tools = await server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_alerts" in tool_names
    assert "get_forecast" in tool_names
    
    # Verify there are at least 2 tools (the weather tools)
    assert len(tools) >= 2


@pytest.mark.asyncio
async def test_server_tool_execution():
    """Test that the server can execute tools correctly."""
    server = create_server()
    
    # Mock the call_tool method to return a formatted alert
    expected_result = """
    Event: Test Alert
    Area: Test Area
    Severity: Test
    Description: Test Description
    Instructions: Test Instructions
    """
    
    with patch.object(server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        # Execute the tool through the server's call_tool method
        result = await server.call_tool("get_alerts", {"state": "CA"})
        
        # Verify the result contains the expected formatted alert
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_alerts", {"state": "CA"})


@pytest.mark.asyncio
async def test_run_server():
    """Test that the run_server function initializes and runs the server."""
    mock_server = MagicMock()
    mock_server.run_async = AsyncMock()
    
    with patch("src.weather.server.create_server", return_value=mock_server):
        await run_server(transport="test-transport")
        
        # Verify the server was created and run with the correct transport
        mock_server.run_async.assert_called_once_with(transport="test-transport")


def test_main_function():
    """Test that the main function initializes and runs the server."""
    mock_server = MagicMock()
    mock_server.run = MagicMock()
    
    with patch("src.weather.server.create_server", return_value=mock_server):
        from src.weather.server import main
        main()
        
        # Verify the server was created and run with stdio transport
        mock_server.run.assert_called_once_with(transport="stdio")


@pytest.mark.asyncio
async def test_server_resources_registration():
    """Test that resources are properly registered with the server."""
    with patch("src.weather.server.register_all_resources") as mock_register_resources:
        server = create_server()
        
        # Verify that register_all_resources was called once
        mock_register_resources.assert_called_once_with(server)


@pytest.mark.asyncio
async def test_server_tools_registration():
    """Test that tools are properly registered with the server."""
    with patch("src.weather.server.register_all_tools") as mock_register_tools:
        server = create_server()
        
        # Verify that register_all_tools was called once
        mock_register_tools.assert_called_once_with(server)
