"""Pytest configuration and fixtures for mention-python tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import respx

from mention import MentionClient, MentionConfig

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def access_token() -> str:
    """Test access token."""
    return "test-access-token-12345"


@pytest.fixture
def account_id() -> str:
    """Test account ID."""
    return "test-account-id"


@pytest.fixture
def alert_id() -> str:
    """Test alert ID."""
    return "test-alert-id"


@pytest.fixture
def mention_id() -> str:
    """Test mention ID."""
    return "test-mention-id"


@pytest.fixture
def config(access_token: str, account_id: str) -> MentionConfig:
    """Test configuration."""
    return MentionConfig(
        access_token=access_token,
        account_id=account_id,
        timeout=10.0,
        max_retries=1,
    )


@pytest.fixture
def client(access_token: str) -> MentionClient:
    """Test client instance."""
    return MentionClient(
        access_token=access_token,
        timeout=10.0,
        max_retries=1,
    )


@pytest.fixture
def mock_api() -> respx.MockRouter:
    """Create a mock API router."""
    with respx.mock(base_url="https://api.mention.net/api") as router:
        yield router


def load_fixture(name: str) -> dict[str, Any]:
    """Load a JSON fixture file."""
    fixture_path = FIXTURES_DIR / f"{name}.json"
    with fixture_path.open() as f:
        return json.load(f)


@pytest.fixture
def alert_fixture() -> dict[str, Any]:
    """Load alert fixture."""
    return load_fixture("alert")


@pytest.fixture
def alerts_fixture() -> dict[str, Any]:
    """Load alerts list fixture."""
    return load_fixture("alerts")


@pytest.fixture
def mention_fixture() -> dict[str, Any]:
    """Load mention fixture."""
    return load_fixture("mention")


@pytest.fixture
def mentions_fixture() -> dict[str, Any]:
    """Load mentions list fixture."""
    return load_fixture("mentions")
