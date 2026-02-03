"""Mention-related models for the Mention API."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import Field, field_validator

from mention.models.base import MentionBaseModel, PaginatedResponse, TimestampMixin


class Tone(str, Enum):
    """Mention sentiment/tone values."""

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Author(MentionBaseModel):
    """Author of a mention."""

    id: str | None = None
    name: str | None = None
    username: str | None = None
    profile_url: str | None = None
    avatar_url: str | None = None
    followers_count: int | None = None
    following_count: int | None = None
    influence_score: float | None = None


class Tag(MentionBaseModel):
    """Tag associated with a mention."""

    id: str
    name: str
    color: str | None = None


class Mention(TimestampMixin, MentionBaseModel):
    """Represents a single mention from the Mention API."""

    id: str
    title: str | None = None
    description: str | None = None
    description_short: str | None = None
    original_url: str | None = None
    source_name: str | None = None
    source_type: str | None = None
    tone: Tone | None = None
    author: Author | None = None
    tags: list[Tag] = Field(default_factory=list)
    favorite: bool = False
    read: bool = False
    trashed: bool = False
    published_at: datetime | None = None
    reach: int | None = None
    engagement: dict[str, int] | None = None
    language: str | None = None
    country: str | None = None
    image_url: str | None = None
    video_url: str | None = None

    @field_validator("tone", mode="before")
    @classmethod
    def parse_tone(cls, v: Any) -> Tone | None:
        """Parse tone from string or int."""
        if v is None:
            return None
        if isinstance(v, Tone):
            return v
        if isinstance(v, str):
            try:
                return Tone(v.lower())
            except ValueError:
                return None
        if isinstance(v, int):
            mapping = {1: Tone.POSITIVE, 0: Tone.NEUTRAL, -1: Tone.NEGATIVE}
            return mapping.get(v)
        return None


class MentionsResponse(PaginatedResponse[Mention]):
    """Response containing a list of mentions."""

    mentions: list[Mention] = Field(default_factory=list)

    @property
    def items(self) -> list[Mention]:
        """Alias for mentions to support generic pagination."""
        return self.mentions


class CurateMentionRequest(MentionBaseModel):
    """Request body for curating (updating) a mention."""

    favorite: bool | None = None
    read: bool | None = None
    trashed: bool | None = None
    tone: Tone | None = None
    tags: list[str] | None = None
    folder: str | None = None
