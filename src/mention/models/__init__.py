"""Pydantic models for the Mention API."""

from __future__ import annotations

from mention.models.account import Account, AccountQuota, AccountStats
from mention.models.alerts import (
    Alert,
    AlertQuery,
    AlertsResponse,
    CreateAlertRequest,
    UpdateAlertRequest,
)
from mention.models.app import AppData, Source
from mention.models.base import APIResponse, PaginatedResponse, PaginationLinks
from mention.models.mentions import (
    Author,
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    Tag,
)

__all__ = [
    # Base
    "APIResponse",
    "PaginatedResponse",
    "PaginationLinks",
    # Account
    "Account",
    "AccountQuota",
    "AccountStats",
    # Alerts
    "Alert",
    "AlertQuery",
    "AlertsResponse",
    "CreateAlertRequest",
    "UpdateAlertRequest",
    # App
    "AppData",
    "Source",
    # Mentions
    "Author",
    "CurateMentionRequest",
    "Mention",
    "MentionsResponse",
    "Tag",
]
