from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
import respx
from httpx import Response

from mention.exceptions import (
    MentionAPIError,
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
)
from mention.models import (
    AlertQuery,
    CreateAlertRequest,
    CurateMentionRequest,
    QueryType,
    Tone,
)

if TYPE_CHECKING:
    from mention.client import MentionClient

# Base URL for API
BASE_URL = "https://api.mention.net/api"


class TestAlerts:
    """Tests for alert operations."""

    @respx.mock
    def test_get_alerts(
        self,
        client: MentionClient,
        account_id: str,
        alerts_fixture: dict[str, Any],
    ) -> None:
        """Test fetching all alerts."""
        respx.get(f"{BASE_URL}/accounts/{account_id}/alerts").mock(
            return_value=Response(200, json=alerts_fixture)
        )

        response = client.get_alerts(account_id)

        assert len(response.alerts) > 0
        assert response.alerts[0].id is not None
        assert response.alerts[0].name is not None

    @respx.mock
    def test_get_alert(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        alert_fixture: dict[str, Any],
    ) -> None:
        """Test fetching a single alert."""
        respx.get(f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}").mock(
            return_value=Response(200, json=alert_fixture)
        )

        alert = client.get_alert(account_id, alert_id)

        assert alert.id == alert_id
        assert alert.name == "Test Alert"
        assert alert.query is not None

    @respx.mock
    def test_create_alert(
        self,
        client: MentionClient,
        account_id: str,
        alert_fixture: dict[str, Any],
    ) -> None:
        """Test creating a new alert."""
        respx.post(f"{BASE_URL}/accounts/{account_id}/alerts").mock(
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

        assert alert.id is not None
        assert alert.name == "Test Alert"

    @respx.mock
    def test_delete_alert(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
    ) -> None:
        """Test deleting an alert."""
        respx.delete(f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}").mock(
            return_value=Response(204)
        )

        result = client.delete_alert(account_id, alert_id)

        assert result is True


class TestMentions:
    """Tests for mention operations."""

    @respx.mock
    def test_get_mentions(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        mentions_fixture: dict[str, Any],
    ) -> None:
        """Test fetching mentions."""
        respx.get(
            f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}/mentions",
            params={"limit": 50},
        ).mock(return_value=Response(200, json=mentions_fixture))

        response = client.get_mentions(account_id, alert_id, limit=50)

        assert len(response.mentions) == 2
        assert response.mentions[0].id == "mention-1"

    @respx.mock
    def test_get_mentions_with_filters(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
        mentions_fixture: dict[str, Any],
    ) -> None:
        """Test fetching mentions with filters."""
        respx.get(
            f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}/mentions",
            params={
                "limit": 100,
                "source": "twitter",
                "read": "true",
                "favorite": "false",
                "tone": "positive",
            },
        ).mock(return_value=Response(200, json=mentions_fixture))

        response = client.get_mentions(
            account_id,
            alert_id,
            limit=100,
            source="twitter",
            read=True,
            favorite=False,
            tone="positive",
        )

        assert len(response.mentions) > 0

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
            f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}"
        ).mock(return_value=Response(200, json=mention_fixture))

        mention = client.get_mention(account_id, alert_id, mention_id)

        assert mention.id == "mention-1"
        assert mention.title is not None
        assert mention.author is not None

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
            f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}"
        ).mock(return_value=Response(200, json=mention_fixture))

        request = CurateMentionRequest(
            favorite=True,
            read=True,
            tone=Tone.POSITIVE,
        )

        mention = client.curate_mention(account_id, alert_id, mention_id, request)

        assert mention.id is not None

    @respx.mock
    def test_mark_all_mentions_read(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
    ) -> None:
        """Test marking all mentions as read."""
        respx.post(
            f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}/mentions/markallread"
        ).mock(return_value=Response(200, json={"ok": True}))

        result = client.mark_all_mentions_read(account_id, alert_id)

        assert result is True


class TestErrorHandling:
    """Tests for error handling."""

    @respx.mock
    def test_auth_error(self, client: MentionClient, account_id: str) -> None:
        """Test authentication error handling."""
        respx.get(f"{BASE_URL}/accounts/{account_id}/alerts").mock(
            return_value=Response(401, json={"error": "Unauthorized"})
        )

        with pytest.raises(MentionAuthError) as exc_info:
            client.get_alerts(account_id)

        assert "401" in str(exc_info.value)

    @respx.mock
    def test_not_found_error(
        self,
        client: MentionClient,
        account_id: str,
        alert_id: str,
    ) -> None:
        """Test not found error handling."""
        respx.get(f"{BASE_URL}/accounts/{account_id}/alerts/{alert_id}").mock(
            return_value=Response(404, json={"error": "Alert not found"})
        )

        with pytest.raises(MentionNotFoundError) as exc_info:
            client.get_alert(account_id, alert_id)

        assert "404" in str(exc_info.value)

    @respx.mock
    def test_rate_limit_error(self, client: MentionClient, account_id: str) -> None:
        """Test rate limit error handling."""
        respx.get(f"{BASE_URL}/accounts/{account_id}/alerts").mock(
            return_value=Response(
                429,
                json={"error": "Rate limit exceeded"},
                headers={"Retry-After": "60"},
            )
        )

        with pytest.raises(MentionRateLimitError) as exc_info:
            client.get_alerts(account_id)

        assert exc_info.value.retry_after == 60

    @respx.mock
    def test_generic_api_error(self, client: MentionClient, account_id: str) -> None:
        """Test generic API error handling."""
        respx.get(f"{BASE_URL}/accounts/{account_id}/alerts").mock(
            return_value=Response(500, json={"error": "Internal server error"})
        )

        with pytest.raises(MentionAPIError) as exc_info:
            client.get_alerts(account_id)

        assert "500" in str(exc_info.value)
