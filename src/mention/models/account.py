"""Account-related models for the Mention API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from mention.models.base import MentionBaseModel, TimestampMixin

if TYPE_CHECKING:
    from datetime import datetime


class AccountQuota(MentionBaseModel):
    """Account quota and limits."""

    alerts: int | None = None
    mentions: int | None = None
    mentions_without_archive: int | None = None
    api_calls: int | None = None


class AccountStats(MentionBaseModel):
    """Account usage statistics."""

    alerts_count: int = 0
    mentions_count: int = 0
    unread_mentions_count: int = 0


class Account(TimestampMixin, MentionBaseModel):
    """Represents a Mention account."""

    id: str
    name: str | None = None
    email: str | None = None
    company: str | None = None
    plan: str | None = None
    quota: AccountQuota | None = None
    stats: AccountStats | None = None
    timezone: str | None = None
    language: str | None = None
    features: list[str] = Field(default_factory=list)
    is_admin: bool = False
    subscription_expires_at: datetime | None = None
