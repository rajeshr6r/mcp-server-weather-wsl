"""Tests for the weather tools module."""

import pytest
from unittest.mock import patch, AsyncMock
from src.weather.server import create_server


@pytest.mark.asyncio
async def test_get_alerts_tool_success(weather_server):
    """Test the get_alerts MCP tool with successful data retrieval."""
    # Verify the get_alerts tool is registered
    tools = await weather_server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_alerts" in tool_names
    
    # Expected formatted alert
    expected_result = """
    Event: Winter Storm Warning
    Area: Mountain County
    Severity: Moderate
    Description: Heavy snow expected
    Instructions: Avoid unnecessary travel
    """
    
    # Mock the call_tool method
    with patch.object(weather_server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        result = await weather_server.call_tool("get_alerts", {"state": "NY"})
        
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_alerts", {"state": "NY"})


@pytest.mark.asyncio
async def test_get_alerts_tool_no_alerts(weather_server):
    """Test the get_alerts MCP tool with no alerts found."""
    # Verify the get_alerts tool is registered
    tools = await weather_server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_alerts" in tool_names
    
    # Expected result for no alerts
    expected_result = "No active alerts for this state."
    
    # Mock the call_tool method
    with patch.object(weather_server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        result = await weather_server.call_tool("get_alerts", {"state": "CA"})
        
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_alerts", {"state": "CA"})


@pytest.mark.asyncio
async def test_get_alerts_tool_failure(weather_server):
    """Test the get_alerts MCP tool with API failure."""
    # Verify the get_alerts tool is registered
    tools = await weather_server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_alerts" in tool_names
    
    # Expected result for API failure
    expected_result = "Unable to fetch alerts or no alerts found."
    
    # Mock the call_tool method
    with patch.object(weather_server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        result = await weather_server.call_tool("get_alerts", {"state": "TX"})
        
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_alerts", {"state": "TX"})


@pytest.mark.asyncio
async def test_get_forecast_tool_success(weather_server):
    """Test the get_forecast MCP tool with successful data retrieval."""
    # Verify the get_forecast tool is registered
    tools = await weather_server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_forecast" in tool_names
    
    # Expected formatted forecast
    expected_result = """
    Today:
    Temperature: 72°F
    Wind: 5 mph SW
    Forecast: Sunny and clear
    
    Tonight:
    Temperature: 58°F
    Wind: 10 mph NE
    Forecast: Partly cloudy
    """
    
    # Mock the call_tool method
    with patch.object(weather_server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        result = await weather_server.call_tool("get_forecast", {"latitude": 37.7749, "longitude": -122.4194})
        
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_forecast", {"latitude": 37.7749, "longitude": -122.4194})


@pytest.mark.asyncio
async def test_get_forecast_tool_point_failure(weather_server):
    """Test the get_forecast MCP tool with point data retrieval failure."""
    # Verify the get_forecast tool is registered
    tools = await weather_server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_forecast" in tool_names
    
    # Expected result for point data retrieval failure
    expected_result = "Unable to fetch forecast data for the specified location."
    
    # Mock the call_tool method
    with patch.object(weather_server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        result = await weather_server.call_tool("get_forecast", {"latitude": 37.7749, "longitude": -122.4194})
        
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_forecast", {"latitude": 37.7749, "longitude": -122.4194})


@pytest.mark.asyncio
async def test_get_forecast_tool_forecast_failure(weather_server):
    """Test the get_forecast MCP tool with forecast data retrieval failure."""
    # Verify the get_forecast tool is registered
    tools = await weather_server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "get_forecast" in tool_names
    
    # Expected result for forecast data retrieval failure
    expected_result = "Unable to fetch detailed forecast data."
    
    # Mock the call_tool method
    with patch.object(weather_server, "call_tool", new_callable=AsyncMock) as mock_call_tool:
        mock_call_tool.return_value = expected_result
        
        result = await weather_server.call_tool("get_forecast", {"latitude": 37.7749, "longitude": -122.4194})
        
        assert result == expected_result
        mock_call_tool.assert_called_once_with("get_forecast", {"latitude": 37.7749, "longitude": -122.4194})
