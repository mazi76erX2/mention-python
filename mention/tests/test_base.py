from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError # mypy: ignore
from requests_oauthlib import OAuth2Session

from ..api.base import Mention, create_oauth_session


class ConcreteMention(Mention):
    """A concrete implementation of the Mention abstract base class for testing purposes."""

    def params(self):
        """Return a sample parameter dictionary."""
        return {"key": "value"}

    def url(self):
        """Return a sample URL."""
        return f"{self._base_url}/test"


def test_mention_base_url():
    """Test that the base URL property returns the correct value."""
    oauth_mock = Mock(spec=OAuth2Session)
    mention = ConcreteMention(oauth_mock)
    assert mention._base_url == "https://api.mention.net/api"


def test_mention_params():
    """Test that the params method returns the correct dictionary."""
    oauth_mock = Mock(spec=OAuth2Session)
    mention = ConcreteMention(oauth_mock)
    assert mention.params() == {"key": "value"}


def test_mention_url():
    """Test that the url method returns the correct URL."""
    oauth_mock = Mock(spec=OAuth2Session)
    mention = ConcreteMention(oauth_mock)
    assert mention.url() == "https://api.mention.net/api/test"


def test_mention_query_success():
    """Test that the query method returns the correct data on successful API call."""
    oauth_mock = Mock(spec=OAuth2Session)
    oauth_mock.get.return_value.json.return_value = {"data": "test"}
    mention = ConcreteMention(oauth_mock)
    result = mention.query()
    assert result == {"data": "test"}
    oauth_mock.get.assert_called_once_with(mention.url())


def test_mention_query_http_error():
    """Test that the query method handles HTTP errors correctly."""
    oauth_mock = Mock(spec=OAuth2Session)
    oauth_mock.get.side_effect = HTTPError("HTTP Error")
    mention = ConcreteMention(oauth_mock)
    result = mention.query()
    assert result == {}


def test_create_oauth_session():
    """Test that create_oauth_session creates an OAuth2Session correctly."""
    with patch("oauthlib.oauth2.BackendApplicationClient") as mock_client:
        with patch("requests_oauthlib.OAuth2Session") as mock_session:
            access_token = "test_token"
            session = create_oauth_session(access_token)
            mock_client.assert_called_once_with(client_id=access_token)
            mock_session.assert_called_once_with(client=mock_client.return_value)
            assert isinstance(session, OAuth2Session)


@pytest.mark.integration
def test_mention_integration():
    """
    Integration test for the Mention base class.

    This test creates a real OAuth session and makes an actual API call.
    It requires a valid access token to run successfully.
    """
    access_token = "your_actual_access_token"  # Replace with a valid access token
    oauth_session = create_oauth_session(access_token)
    mention = ConcreteMention(oauth_session)
    result = mention.query()
    assert isinstance(result, dict)
