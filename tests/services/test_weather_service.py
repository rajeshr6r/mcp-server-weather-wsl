"""Tests for the weather service module."""

import pytest
from unittest.mock import patch, AsyncMock
from src.weather.services.weather_service import get_weather_alerts, get_weather_point, get_weather_forecast


@pytest.mark.asyncio
async def test_get_weather_alerts_success():
    """Test successful weather alerts retrieval."""
    mock_data = {
        "features": [
            {
                "properties": {
                    "event": "Flood Warning",
                    "areaDesc": "Test County",
                    "severity": "Moderate",
                    "description": "Test description",
                    "instruction": "Test instructions"
                }
            }
        ]
    }
    
    with patch("src.weather.services.weather_service.make_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_data
        result = await get_weather_alerts("CA")
        
        assert result == mock_data
        mock_request.assert_called_once_with(
            "https://api.weather.gov/alerts/active/area/CA",
            headers={"Accept": "application/geo+json"}
        )


@pytest.mark.asyncio
async def test_get_weather_alerts_failure():
    """Test weather alerts retrieval failure."""
    with patch("src.weather.services.weather_service.make_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = Exception("API Error")
        result = await get_weather_alerts("CA")
        
        assert result is None


@pytest.mark.asyncio
async def test_get_weather_point_success():
    """Test successful weather point data retrieval."""
    mock_data = {
        "properties": {
            "forecast": "https://api.weather.gov/gridpoints/ABC/1,2/forecast"
        }
    }
    
    with patch("src.weather.services.weather_service.make_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_data
        result = await get_weather_point(37.7749, -122.4194)
        
        assert result == mock_data
        mock_request.assert_called_once_with(
            "https://api.weather.gov/points/37.7749,-122.4194",
            headers={"Accept": "application/geo+json"}
        )


@pytest.mark.asyncio
async def test_get_weather_point_failure():
    """Test weather point data retrieval failure."""
    with patch("src.weather.services.weather_service.make_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = Exception("API Error")
        result = await get_weather_point(37.7749, -122.4194)
        
        assert result is None


@pytest.mark.asyncio
async def test_get_weather_forecast_success():
    """Test successful weather forecast retrieval."""
    mock_data = {
        "properties": {
            "periods": [
                {
                    "name": "Tonight",
                    "temperature": 65,
                    "temperatureUnit": "F",
                    "windSpeed": "10 mph",
                    "windDirection": "NE",
                    "detailedForecast": "Partly cloudy with a chance of rain"
                }
            ]
        }
    }
    
    forecast_url = "https://api.weather.gov/gridpoints/ABC/1,2/forecast"
    
    with patch("src.weather.services.weather_service.make_request", new_callable=AsyncMock) as mock_request:
        mock_request.return_value = mock_data
        result = await get_weather_forecast(forecast_url)
        
        assert result == mock_data
        mock_request.assert_called_once_with(
            forecast_url,
            headers={"Accept": "application/geo+json"}
        )


@pytest.mark.asyncio
async def test_get_weather_forecast_failure():
    """Test weather forecast retrieval failure."""
    forecast_url = "https://api.weather.gov/gridpoints/ABC/1,2/forecast"
    
    with patch("src.weather.services.weather_service.make_request", new_callable=AsyncMock) as mock_request:
        mock_request.side_effect = Exception("API Error")
        result = await get_weather_forecast(forecast_url)
        
        assert result is None
