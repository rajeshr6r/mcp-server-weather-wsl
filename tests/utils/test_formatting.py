"""Tests for the formatting utilities module."""

import pytest
from src.weather.utils.formatting import format_alert, format_forecast


def test_format_alert_complete():
    """Test alert formatting with complete data."""
    feature = {
        "properties": {
            "event": "Severe Thunderstorm",
            "areaDesc": "Central County",
            "severity": "Severe",
            "description": "Strong thunderstorms expected",
            "instruction": "Seek shelter immediately"
        }
    }
    
    formatted = format_alert(feature)
    
    assert "Event: Severe Thunderstorm" in formatted
    assert "Area: Central County" in formatted
    assert "Severity: Severe" in formatted
    assert "Description: Strong thunderstorms expected" in formatted
    assert "Instructions: Seek shelter immediately" in formatted


def test_format_alert_missing_fields():
    """Test alert formatting with missing fields."""
    feature = {
        "properties": {
            "event": "Flood Warning",
            "areaDesc": "River Valley"
        }
    }
    
    formatted = format_alert(feature)
    
    assert "Event: Flood Warning" in formatted
    assert "Area: River Valley" in formatted
    assert "Severity: Unknown" in formatted
    assert "Description: No description available" in formatted
    assert "Instructions: No specific instructions provided" in formatted


def test_format_alert_empty_properties():
    """Test alert formatting with empty properties."""
    feature = {
        "properties": {}
    }
    
    formatted = format_alert(feature)
    
    assert "Event: Unknown" in formatted
    assert "Area: Unknown" in formatted
    assert "Severity: Unknown" in formatted
    assert "Description: No description available" in formatted
    assert "Instructions: No specific instructions provided" in formatted


def test_format_forecast_complete():
    """Test forecast formatting with complete data."""
    period = {
        "name": "Tonight",
        "temperature": 65,
        "temperatureUnit": "F",
        "windSpeed": "10 mph",
        "windDirection": "NE",
        "detailedForecast": "Partly cloudy with a chance of rain"
    }
    
    formatted = format_forecast(period)
    
    assert "Tonight:" in formatted
    assert "Temperature: 65°F" in formatted
    assert "Wind: 10 mph NE" in formatted
    assert "Forecast: Partly cloudy with a chance of rain" in formatted


def test_format_forecast_integer_temperature():
    """Test forecast formatting with integer temperature."""
    period = {
        "name": "Tomorrow",
        "temperature": 72,
        "temperatureUnit": "F",
        "windSpeed": "5 mph",
        "windDirection": "SW",
        "detailedForecast": "Sunny and clear"
    }
    
    formatted = format_forecast(period)
    
    assert "Tomorrow:" in formatted
    assert "Temperature: 72°F" in formatted
    assert "Wind: 5 mph SW" in formatted
    assert "Forecast: Sunny and clear" in formatted
