"""Pytest configuration and fixtures."""

import pytest
from src.weather.server import create_server


@pytest.fixture
def weather_server():
    """Create a weather server instance for testing."""
    return create_server("test-weather")
