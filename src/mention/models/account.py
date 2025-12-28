"""Account-related models for the Mention API."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from mention.models.base import MentionBaseModel, TimestampMixin


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


class Account(MentionBaseModel, TimestampMixin):
    """
    Represents a Mention account.

    Attributes:
        id: Unique account identifier.
        name: Account name.
        email: Account email address.
        company: Company name.
        plan: Subscription plan name.
        quota: Account quotas and limits.
        stats: Account usage statistics.
    """

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
