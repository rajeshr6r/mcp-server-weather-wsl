"""HTTP utilities for making API requests."""

import httpx
from typing import Any, Dict, Optional

# Constants
USER_AGENT = "weather-app/1.0"


async def make_request(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any] | None:
    """
    Make an HTTP request to the specified URL.

    Args:
        url: The URL to make the request to
        headers: Optional headers to include in the request
        params: Optional query parameters
        timeout: Request timeout in seconds

    Returns:
        JSON response as a dictionary or None if the request fails
    """
    default_headers = {
        "User-Agent": USER_AGENT,
    }

    if headers:
        default_headers.update(headers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url, headers=default_headers, params=params, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError):
            # In a production app, you'd want to log this error
            return None
