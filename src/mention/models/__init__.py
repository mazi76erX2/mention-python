"""Pydantic models for the Mention API."""

from __future__ import annotations

from mention.models.account import Account, AccountQuota, AccountStats
from mention.models.alerts import (
    Alert,
    AlertQuery,
    AlertsResponse,
    CreateAlertRequest,
    QueryType,
    UpdateAlertRequest,
)
from mention.models.app import AppData, Source
from mention.models.authors import (
    Author,
    AuthorsResponse,
    AuthorStats,
    AuthorStatsResponse,
)
from mention.models.base import APIResponse, PaginatedResponse, PaginationLinks
from mention.models.mentions import (
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    Tone,
)
from mention.models.preferences import (
    AlertPreferences,
    NotificationChannel,
    UpdatePreferencesRequest,
)
from mention.models.shares import (
    CreateShareRequest,
    Share,
    SharePermission,
    SharesResponse,
    UpdateShareRequest,
)
from mention.models.stats import (
    SourceStats,
    StatsData,
    StatsPeriod,
    StatsRequest,
    StatsResponse,
)
from mention.models.tags import (
    CreateTagRequest,
    Tag,
    TagsResponse,
    UpdateTagRequest,
)
from mention.models.tasks import (
    CreateTaskRequest,
    Task,
    TasksResponse,
    TaskStatus,
    UpdateTaskRequest,
)

__all__ = [
    "APIResponse",
    "Account",
    "AccountQuota",
    "AccountStats",
    "Alert",
    "AlertPreferences",
    "AlertQuery",
    "AlertsResponse",
    "AppData",
    "Author",
    "AuthorStats",
    "AuthorStatsResponse",
    "AuthorsResponse",
    "CreateAlertRequest",
    "CreateShareRequest",
    "CreateTagRequest",
    "CreateTaskRequest",
    "CurateMentionRequest",
    "Mention",
    "MentionsResponse",
    "NotificationChannel",
    "PaginatedResponse",
    "PaginationLinks",
    "Share",
    "SharePermission",
    "SharesResponse",
    "Source",
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
    "Tone",
    "UpdateAlertRequest",
    "UpdatePreferencesRequest",
    "UpdateShareRequest",
    "UpdateTagRequest",
    "UpdateTaskRequest",
    "QueryType",
]
