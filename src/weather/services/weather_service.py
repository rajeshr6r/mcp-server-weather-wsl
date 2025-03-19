"""Weather service for interacting with the National Weather Service API."""

import logging
from typing import Dict, Any, Optional

from ..utils.http import make_request

# Configure logging
logger = logging.getLogger(__name__)

# Constants
NWS_API_BASE = "https://api.weather.gov"


async def get_weather_alerts(state: str) -> Optional[Dict[str, Any]]:
    """
    Get active weather alerts for a state.

    Args:
        state: State code (e.g., 'CA', 'NY')

    Returns:
        Weather alerts data or None if the request fails
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    headers = {"Accept": "application/geo+json"}

    try:
        return await make_request(url, headers=headers)
    except Exception as e:
        logger.error(f"Error fetching alerts for {state}: {str(e)}")
        return None


async def get_weather_point(
    latitude: float, longitude: float
) -> Optional[Dict[str, Any]]:
    """
    Get weather point data for coordinates.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        Weather point data or None if the request fails
    """
    url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    headers = {"Accept": "application/geo+json"}

    try:
        return await make_request(url, headers=headers)
    except Exception as e:
        logger.error(f"Error fetching point data for {latitude},{longitude}: {str(e)}")
        return None


async def get_weather_forecast(forecast_url: str) -> Optional[Dict[str, Any]]:
    """
    Get weather forecast data.

    Args:
        forecast_url: URL for the forecast endpoint

    Returns:
        Weather forecast data or None if the request fails
    """
    headers = {"Accept": "application/geo+json"}

    try:
        return await make_request(forecast_url, headers=headers)
    except Exception as e:
        logger.error(f"Error fetching forecast data: {str(e)}")
        return None
