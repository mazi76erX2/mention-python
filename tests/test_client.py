"""Tests for the MentionClient."""

from __future__ import annotations

from typing import Any

import pytest
import respx
from httpx import Response

from mention import MentionClient
from mention.exceptions import (
    MentionAPIError,
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
)
from mention.models import (
    Alert,
    AlertQuery,
    AlertsResponse,
    CreateAlertRequest,
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    QueryType,
    Tone,
)


class TestClientInitialization:
    """Tests for client initialization."""

    def test_init_with_token(self) -> None:
        """Test client initialization with access token."""
        client = MentionClient(access_token="test-token")
        assert client._access_token == "test-token"
        assert client._base_url == "https://api.mention.net/api"
        client.close()

    def test_init_without_token_raises(self) -> None:
        """Test that initialization without token raises ValueError."""
        with pytest.raises(ValueError, match="access_token is required"):
            MentionClient(access_token="")

    def test_init_with_custom_base_url(self) -> None:
        """Test client initialization with custom base URL."""
        client = MentionClient(
            access_token="test-token",
            base_url="https://custom.api.com/",
        )
        assert client._base_url == "https://custom.api.com"
        client.close()

    def test_context_manager(self) -> None:
        """Test client as context manager."""
        with MentionClient(access_token="test-token") as client:
            assert client._access_token == "test-token"


class TestAlerts:
    """Tests for alert-related methods."""

    @respx.mock
    def test_get_alerts(
        self,
        client: MentionClient,
        account_id: str,
        alerts_fixture: dict[str, Any],
    ) -> None:
        """Test fetching all alerts."""
        respx.get(f"/accounts/{account_id}/alerts").mock(
            return_value=Response(200, json=alerts_fixture)
        )

        response = client.get_alerts(account_id)

        assert isinstance(response, AlertsResponse)
        assert len(response.alerts) > 0
        assert all(isinstance(a, Alert) for a in response.alerts)

    @respx.mock
    def test_get_alert(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        alert_fixture: dict[str, Any],
    ) -> None:
        """Test fetching a single alert."""
        respx.get(f"/accounts/{account_id}/alerts/{alert_id}").mock(
            return_value=Response(200, json=alert_fixture)
        )

        alert = client.get_alert(account_id, alert_id)

        assert isinstance(alert, Alert)
        assert alert.id == alert_fixture.get("alert", alert_fixture).get("id")

    @respx.mock
    def test_create_alert(
        self,
        client: MentionClient,
        account_id: str,
        alert_fixture: dict[str, Any],
    ) -> None:
        """Test creating a new alert."""
        respx.post(f"/accounts/{account_id}/alerts").mock(
            return_value=Response(201, json=alert_fixture)
        )

        request = CreateAlertRequest(
            name="Test Alert",
            query=AlertQuery(
                type=QueryType.BASIC,
                included_keywords=["python", "api"],
            ),
            languages=["en"],
            sources=["web", "twitter"],
        )

        alert = client.create_alert(account_id, request)

        assert isinstance(alert, Alert)

    @respx.mock
    def test_delete_alert(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
    ) -> None:
        """Test deleting an alert."""
        respx.delete(f"/accounts/{account_id}/alerts/{alert_id}").mock(
            return_value=Response(204)
        )

        result = client.delete_alert(account_id, alert_id)

        assert result is True


class TestMentions:
    """Tests for mention-related methods."""

    @respx.mock
    def test_get_mentions(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        mentions_fixture: dict[str, Any],
    ) -> None:
        """Test fetching mentions."""
        respx.get(f"/accounts/{account_id}/alerts/{alert_id}/mentions").mock(
            return_value=Response(200, json=mentions_fixture)
        )

        response = client.get_mentions(account_id, alert_id, limit=50)

        assert isinstance(response, MentionsResponse)
        assert all(isinstance(m, Mention) for m in response.mentions)

    @respx.mock
    def test_get_mentions_with_filters(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        mentions_fixture: dict[str, Any],
    ) -> None:
        """Test fetching mentions with filters."""
        route = respx.get(f"/accounts/{account_id}/alerts/{alert_id}/mentions").mock(
            return_value=Response(200, json=mentions_fixture)
        )

        response = client.get_mentions(
            account_id,
            alert_id,
            limit=100,
            source="twitter",
            read=True,
            favorite=False,
            tone="positive",
        )

        assert isinstance(response, MentionsResponse)
        # Verify query params were sent
        assert route.called

    @respx.mock
    def test_get_mention(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        mention_id: str,
        mention_fixture: dict[str, Any],
    ) -> None:
        """Test fetching a single mention."""
        respx.get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}"
        ).mock(return_value=Response(200, json=mention_fixture))

        mention = client.get_mention(account_id, alert_id, mention_id)

        assert isinstance(mention, Mention)

    @respx.mock
    def test_curate_mention(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        mention_id: str,
        mention_fixture: dict[str, Any],
    ) -> None:
        """Test curating a mention."""
        respx.put(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}"
        ).mock(return_value=Response(200, json=mention_fixture))

        request = CurateMentionRequest(
            favorite=True,
            read=True,
            tone=Tone.POSITIVE,
        )

        mention = client.curate_mention(account_id, alert_id, mention_id, request)

        assert isinstance(mention, Mention)

    @respx.mock
    def test_mark_all_mentions_read(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
    ) -> None:
        """Test marking all mentions as read."""
        respx.post(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/markallread"
        ).mock(return_value=Response(200, json={"ok": True}))

        result = client.mark_all_mentions_read(account_id, alert_id)

        assert result is True


class TestErrorHandling:
    """Tests for error handling."""

    @respx.mock
    def test_auth_error(self, client: MentionClient, account_id: str) -> None:
        """Test authentication error handling."""
        respx.get(f"/accounts/{account_id}/alerts").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(MentionAuthError) as exc_info:
            client.get_alerts(account_id)

        assert exc_info.value.status_code == 401

    @respx.mock
    def test_not_found_error(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
    ) -> None:
        """Test not found error handling."""
        respx.get(f"/accounts/{account_id}/alerts/{alert_id}").mock(
            return_value=Response(404, json={"error": "Alert not found"})
        )

        with pytest.raises(MentionNotFoundError) as exc_info:
            client.get_alert(account_id, alert_id)

        assert exc_info.value.status_code == 404

    @respx.mock
    def test_rate_limit_error(self, client: MentionClient, account_id: str) -> None:
        """Test rate limit error handling."""
        respx.get(f"/accounts/{account_id}/alerts").mock(
            return_value=Response(
                429,
                json={"error": "Rate limit exceeded"},
                headers={"Retry-After": "60"},
            )
        )

        with pytest.raises(MentionRateLimitError) as exc_info:
            client.get_alerts(account_id)

        assert exc_info.value.status_code == 429
        assert exc_info.value.retry_after == 60

    @respx.mock
    def test_generic_api_error(self, client: MentionClient, account_id: str) -> None:
        """Test generic API error handling."""
        respx.get(f"/accounts/{account_id}/alerts").mock(
            return_value=Response(500, json={"error": "Internal server error"})
        )

        with pytest.raises(MentionAPIError) as exc_info:
            client.get_alerts(account_id)

        assert exc_info.value.status_code == 500
