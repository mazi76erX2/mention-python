"""
Mention Python Client - A modern Python wrapper for the Mention API.

Example usage:
    >>> from mention import MentionClient
    >>> client = MentionClient(access_token="your-token")
    >>> alerts = client.get_alerts(account_id="your-account-id")
    >>> for alert in alerts:
    ...     print(alert.name)
"""

from __future__ import annotations

from mention.client import AsyncMentionClient, MentionClient
from mention.config import MentionConfig
from mention.exceptions import (
    MentionAPIError,
    MentionAuthError,
    MentionConnectionError,
    MentionError,
    MentionNotFoundError,
    MentionRateLimitError,
    MentionValidationError,
)
from mention.models import (
    Account,
    Alert,
    AlertPreferences,
    AlertQuery,
    AlertsResponse,
    AppData,
    Author,
    AuthorsResponse,
    CreateAlertRequest,
    CreateShareRequest,
    CreateTagRequest,
    CreateTaskRequest,
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    NotificationChannel,
    Share,
    SharesResponse,
    SourceStats,
    StatsData,
    StatsPeriod,
    StatsRequest,
    StatsResponse,
    Tag,
    TagsResponse,
    Task,
    TaskStatus,
    TasksResponse,
    UpdateAlertRequest,
    UpdatePreferencesRequest,
    UpdateShareRequest,
    UpdateTagRequest,
    UpdateTaskRequest,
)

__version__ = "2.0.0"
__author__ = "Xolani Mazibuko"
__email__ = "mazi76erx@gmail.com"

__all__ = [
    "Account",
    "Alert",
    "AlertPreferences",
    "AlertQuery",
    "AlertsResponse",
    "AppData",
    "AsyncMentionClient",
    "Author",
    "AuthorsResponse",
    "CreateAlertRequest",
    "CreateShareRequest",
    "CreateTagRequest",
    "CreateTaskRequest",
    "CurateMentionRequest",
    "Mention",
    "MentionAPIError",
    "MentionAuthError",
    "MentionClient",
    "MentionConfig",
    "MentionConnectionError",
    "MentionError",
    "MentionNotFoundError",
    "MentionRateLimitError",
    "MentionsResponse",
    "MentionValidationError",
    "NotificationChannel",
    "Share",
    "SharesResponse",
    "SourceStats",
    "StatsData",
    "StatsPeriod",
    "StatsRequest",
    "StatsResponse",
    "Tag",
    "TagsResponse",
    "Task",
    "TaskStatus",
    "TasksResponse",
    "UpdateAlertRequest",
    "UpdatePreferencesRequest",
    "UpdateShareRequest",
    "UpdateTagRequest",
    "UpdateTaskRequest",
]
