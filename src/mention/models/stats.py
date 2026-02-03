"""Statistics-related models for the Mention API."""

from __future__ import annotations

from enum import Enum

from pydantic import Field

from mention.models.base import MentionBaseModel


class StatsPeriod(str, Enum):
    """Time period for statistics."""

    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


class SourceStats(MentionBaseModel):
    """Statistics for a specific source."""

    source: str
    mentions_count: int = 0
    reach: int = 0
    sentiment_positive: int = 0
    sentiment_negative: int = 0
    sentiment_neutral: int = 0


class StatsData(MentionBaseModel):
    """Statistics data for a specific time period."""

    period: str | None = None
    mentions_count: int = 0
    reach: int = 0
    sentiment_positive: int = 0
    sentiment_negative: int = 0
    sentiment_neutral: int = 0
    sources: list[SourceStats] = Field(default_factory=list)


class StatsResponse(MentionBaseModel):
    """Response containing statistics."""

    account_id: str | None = None
    alert_id: str | None = None
    period: str | None = None
    from_date: str | None = None
    to_date: str | None = None
    data: list[StatsData] = Field(default_factory=list)
    total_mentions: int = 0
    total_reach: int = 0
    sentiment_distribution: dict[str, int] = Field(default_factory=dict)
    sources_distribution: dict[str, int] = Field(default_factory=dict)


class StatsRequest(MentionBaseModel):
    """Request parameters for fetching statistics."""

    from_date: str | None = None
    to_date: str | None = None
    period: StatsPeriod = StatsPeriod.DAY
    group_by: str | None = None
