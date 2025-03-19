"""Formatting utilities for weather data."""

from typing import Dict, Any


def format_alert(feature: Dict[str, Any]) -> str:
    """
    Format a weather alert into a readable string.

    Args:
        feature: Alert feature data from the NWS API

    Returns:
        Formatted alert string
    """
    props = feature["properties"]

    return f"""
    Event: {props.get('event', 'Unknown')}
    Area: {props.get('areaDesc', 'Unknown')}
    Severity: {props.get('severity', 'Unknown')}
    Description: {props.get('description', 'No description available')}
    Instructions: {props.get('instruction', 'No specific instructions provided')}
    """


def format_forecast(period: Dict[str, Any]) -> str:
    """
    Format a forecast period into a readable string.

    Args:
        period: Forecast period data from the NWS API

    Returns:
        Formatted forecast string
    """
    return f"""
    {period['name']}:
    Temperature: {period['temperature']}°{period['temperatureUnit']}
    Wind: {period['windSpeed']} {period['windDirection']}
    Forecast: {period['detailedForecast']}
    """
