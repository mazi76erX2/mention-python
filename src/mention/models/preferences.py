"""Alert preferences-related models for the Mention API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import Field

from mention.models.base import MentionBaseModel

if TYPE_CHECKING:
    from datetime import datetime


class NotificationChannel(str, Enum):
    """Notification channel types."""

    EMAIL = "email"
    PUSH = "push"
    SLACK = "slack"
    WEBHOOK = "webhook"


class AlertPreferences(MentionBaseModel):
    """Represents alert preferences/settings."""

    alert_id: str
    account_id: str | None = None
    email_notifications: bool = True
    push_notifications: bool = False
    daily_digest: bool = False
    weekly_digest: bool = False
    mention_limit: int | None = None
    notification_channels: list[NotificationChannel] = Field(default_factory=list)
    language: str | None = None
    timezone: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UpdatePreferencesRequest(MentionBaseModel):
    """Request body for updating alert preferences."""

    email_notifications: bool | None = None
    push_notifications: bool | None = None
    daily_digest: bool | None = None
    weekly_digest: bool | None = None
    mention_limit: int | None = None
    notification_channels: list[NotificationChannel] | None = None
    language: str | None = None
    timezone: str | None = None
