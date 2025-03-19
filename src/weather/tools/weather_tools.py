"""Weather tools for the MCP server."""

import logging

from ..services.weather_service import (
    get_weather_alerts,
    get_weather_point,
    get_weather_forecast,
)
from ..utils.formatting import format_alert, format_forecast

# Configure logging
logger = logging.getLogger(__name__)


def register_tools(server):
    """
    Register all weather tools with the server.

    Args:
        server: MCP server instance
    """

    @server.tool()
    async def get_alerts(state: str) -> str:
        """
        Get active weather alerts for a state.

        Args:
            state: Two-letter state code (e.g., 'CA', 'NY')

        Returns:
            Formatted alerts or error message
        """
        data = await get_weather_alerts(state)

        if not data or "features" not in data:
            return "Unable to fetch alerts or no alerts found."

        if not data["features"]:
            return "No active alerts for this state."

        alerts = [format_alert(feature) for feature in data["features"]]
        return "\n".join(alerts)

    @server.tool()
    async def get_forecast(latitude: float, longitude: float) -> str:
        """
        Get weather forecast for coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Formatted forecast or error message
        """
        points_data = await get_weather_point(latitude, longitude)

        if not points_data:
            return "Unable to fetch forecast data for the specified location."

        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await get_weather_forecast(forecast_url)

        if not forecast_data:
            return "Unable to fetch detailed forecast data."

        periods = forecast_data["properties"]["periods"]
        forecasts = [
            format_forecast(period) for period in periods[:5]
        ]  # Only show next 5 periods

        return "\n---\n".join(forecasts)
