"""Alert-related models for the Mention API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from pydantic import Field, field_validator

from mention.models.base import MentionBaseModel, PaginatedResponse, TimestampMixin

if TYPE_CHECKING:
    from datetime import datetime


class QueryType(str, Enum):
    """Alert query types."""

    BASIC = "basic"
    ADVANCED = "advanced"
    BOOLEAN = "boolean"


class AlertQuery(MentionBaseModel):
    """Alert query configuration."""

    type: QueryType = QueryType.BASIC
    included_keywords: list[str] = Field(default_factory=list)
    excluded_keywords: list[str] = Field(default_factory=list)
    required_keywords: list[str] = Field(default_factory=list)
    should_belong_to_owner: bool | None = None


class AlertSource(str, Enum):
    """Available alert sources."""

    WEB = "web"
    TWITTER = "twitter"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    REDDIT = "reddit"
    NEWS = "news"
    BLOG = "blog"
    FORUM = "forum"
    REVIEW = "review"


class Alert(TimestampMixin, MentionBaseModel):
    """Represents a Mention alert."""

    id: str
    name: str
    query: AlertQuery
    languages: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    noise_detection: bool = True
    sentiment_analysis: bool = True
    mentions_count: int = 0
    unread_mentions_count: int = 0
    shares_count: int = 0
    followers_count: int = 0
    reach: int = 0
    last_mention_at: datetime | None = None

    @field_validator("sources", mode="before")
    @classmethod
    def parse_sources(cls, v: Any) -> list[str]:
        """Parse sources from various formats."""
        if isinstance(v, str):
            return [v]
        if isinstance(v, list):
            return [str(s) for s in v]
        return []


class AlertsResponse(PaginatedResponse[Alert]):
    """Response containing a list of alerts."""

    alerts: list[Alert] = Field(default_factory=list)

    @property
    def items(self) -> list[Alert]:
        """Alias for alerts to support generic pagination."""
        return self.alerts


class CreateAlertRequest(MentionBaseModel):
    """Request body for creating a new alert."""

    name: str
    query: AlertQuery
    languages: list[str] = Field(default_factory=lambda: ["en"])
    countries: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=lambda: ["web"])
    noise_detection: bool = True
    sentiment_analysis: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate alert name is not empty."""
        if not v or not v.strip():
            msg = "Alert name cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("languages")
    @classmethod
    def validate_languages(cls, v: list[str]) -> list[str]:
        """Ensure at least one language is specified."""
        if not v:
            return ["en"]
        return v


class UpdateAlertRequest(MentionBaseModel):
    """Request body for updating an existing alert."""

    name: str | None = None
    query: AlertQuery | None = None
    languages: list[str] | None = None
    countries: list[str] | None = None
    sources: list[str] | None = None
    noise_detection: bool | None = None
    sentiment_analysis: bool | None = None
