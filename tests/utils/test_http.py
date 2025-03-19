"""Tests for the HTTP utilities module."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from src.weather.utils.http import make_request


@pytest.mark.asyncio
async def test_make_request_success():
    """Test successful HTTP request."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await make_request("https://test.com/api")

        assert result == {"data": "test_data"}
        mock_client_instance.get.assert_called_once_with(
            "https://test.com/api",
            headers={"User-Agent": "weather-app/1.0"},
            params=None,
            timeout=30,
        )


@pytest.mark.asyncio
async def test_make_request_with_headers_and_params():
    """Test HTTP request with custom headers and parameters."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        headers = {"Accept": "application/json", "X-Custom": "Value"}
        params = {"param1": "value1"}

        result = await make_request(
            "https://test.com/api", headers=headers, params=params
        )

        assert result == {"data": "test_data"}
        mock_client_instance.get.assert_called_once_with(
            "https://test.com/api",
            headers={
                "User-Agent": "weather-app/1.0",
                "Accept": "application/json",
                "X-Custom": "Value",
            },
            params=params,
            timeout=30,
        )


@pytest.mark.asyncio
async def test_make_request_failure_request_error():
    """Test HTTP request failure handling for request errors."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.RequestError("Connection error")
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await make_request("https://test.com/api")

        assert result is None


@pytest.mark.asyncio
async def test_make_request_failure_http_error():
    """Test HTTP request failure handling for HTTP status errors."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=MagicMock(), response=MagicMock()
    )

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        # The make_request function should catch the exception and return None
        result = await make_request("https://test.com/api")
        assert result is None


@pytest.mark.asyncio
async def test_make_request_custom_timeout():
    """Test HTTP request with custom timeout."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = await make_request("https://test.com/api", timeout=60)

        assert result == {"data": "test_data"}
        mock_client_instance.get.assert_called_once_with(
            "https://test.com/api",
            headers={"User-Agent": "weather-app/1.0"},
            params=None,
            timeout=60,
        )
