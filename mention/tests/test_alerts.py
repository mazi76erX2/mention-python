"""Test suite for the alerts module."""

from typing import Any, Dict
from unittest.mock import MagicMock

import pytest
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session

from ..api.alerts import CreateAnAlertAPI


@pytest.fixture
def mock_oauth_session() -> OAuth2Session:
    """
    Creates a mocked OAuth2Session for testing API interactions.

    Returns:
        OAuth2Session: A mock object simulating an OAuth2Session.
    """
    mock_session = MagicMock(spec=OAuth2Session)
    mock_response = MagicMock()
    mock_response.json.return_value = {"alert_id": "12345"}
    mock_session.post.return_value = mock_response
    return mock_session


@pytest.fixture
def basic_alert_data() -> Dict[str, Any]:
    """
    Provides sample data for creating a basic alert.

    Returns:
        Dict[str, Any]: A dictionary containing data for a basic alert.
    """
    return {
        "type": "basic",
        "included_keywords": ["Python"],
        "required_keywords": ["pytest"],
        "excluded_keywords": ["unittest"],
        "monitored_website": [{"domain": "www.python.org", "block_self": True}],
    }


@pytest.fixture
def advanced_alert_data() -> Dict[str, Any]:
    """
    Provides sample data for creating an advanced alert.

    Returns:
        Dict[str, Any]: A dictionary containing data for an advanced alert.
    """
    return {
        "type": "advanced",
        "query_string": "(Python AND Django) OR (Flask AND REST)",
    }


class TestCreateAnAlertAPI:
    """Test suite for the CreateAnAlertAPI class."""

    def test_create_basic_alert_success(
        self, mock_oauth_session: OAuth2Session, basic_alert_data: Dict[str, Any]
    ) -> None:
        """Tests the successful creation of a basic alert."""
        api = CreateAnAlertAPI(
            mock_oauth_session,
            "account123",
            "Test Basic Alert",
            basic_alert_data,
            ["en"],
            noise_detection=True,
        )
        response = api.query()

        mock_oauth_session.post.assert_called_once_with(
            f"{api._base_url}/accounts/account123/alerts",
            json={
                "name": "Test Basic Alert",
                "query": basic_alert_data,
                "languages": ["en"],
                "noise_detection": "true",
            },
        )

        assert response == {"alert_id": "12345"}


    def test_create_advanced_alert_success(
        self, mock_oauth_session: OAuth2Session, advanced_alert_data: Dict[str, Any]
    ) -> None:
        """Tests the successful creation of an advanced alert."""
        api = CreateAnAlertAPI(
            mock_oauth_session,
            "account123",
            "Test Advanced Alert",
            advanced_alert_data,
            ["en", "fr"],
            countries=["US", "FR"],
        )
        response = api.query()

        mock_oauth_session.post.assert_called_once_with(
            f"{api._base_url}/accounts/account123/alerts",
            json={
                "name": "Test Advanced Alert",
                "query": advanced_alert_data,
                "languages": ["en", "fr"],
                "countries": ["US", "FR"],
            },
        )

        assert response == {"alert_id": "12345"}


    def test_create_alert_with_optional_params(
        self, mock_oauth_session: OAuth2Session, basic_alert_data: Dict[str, Any]
    ) -> None:
        """Tests alert creation with all optional parameters."""
        api = CreateAnAlertAPI(
            mock_oauth_session,
            "account123",
            "Alert with Options",
            basic_alert_data,
            ["en"],
            sources=["web", "twitter"],
            blocked_sites=["example.com"],
            noise_detection=False,
            reviews_pages=["amazon.com"],
        )
        response = api.query()

        mock_oauth_session.post.assert_called_once_with(
            f"{api._base_url}/accounts/account123/alerts",
            json={
                "name": "Alert with Options",
                "query": basic_alert_data,
                "languages": ["en"],
                "sources": ["web", "twitter"],
                "blocked_sites": ["example.com"],
                "noise_detection": "false",
                "reviews_pages": ["amazon.com"],
            },
        )
        assert response == {"alert_id": "12345"}


    def test_create_alert_http_error(
        self, mock_oauth_session: OAuth2Session, basic_alert_data: Dict[str, Any]
    ) -> None:
        """Tests handling of HTTP errors during alert creation."""
        mock_oauth_session.post.side_effect = HTTPError("Simulated HTTP Error")
        api = CreateAnAlertAPI(
            mock_oauth_session, "account123", "Error Alert", {}, ["en"]
        )  # Empty query
        response = api.query()
        assert response == {}  # Expect an empty dictionary on error

    def test_create_alert_empty_query(
        self, mock_oauth_session: OAuth2Session, basic_alert_data: Dict[str, Any]
    ) -> None:
        """Tests behavior when creating an alert with an empty query."""
        api = CreateAnAlertAPI(
            mock_oauth_session,
            "account123",
            "Error Alert",
            {},  # Empty query data
            ["en"],
        )

        response = api.query()

        assert response == {}  # Expect an empty dictionary on error


    def test_create_alert_invalid_language(
        self, mock_oauth_session: OAuth2Session, basic_alert_data: Dict[str, Any]
    ) -> None:
        """Tests behavior when creating an alert with an invalid language code."""
        with pytest.raises(ValueError):
            CreateAnAlertAPI(
                mock_oauth_session,
                "account123",
                "Error Alert",
                basic_alert_data,
                ["invalid_lang_code"],  # Invalid language code
                noise_detection=True,
            )
