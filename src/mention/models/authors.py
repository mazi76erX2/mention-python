"""Author/Influencer-related models for the Mention API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from mention.models.base import MentionBaseModel

if TYPE_CHECKING:
    from datetime import datetime


class Author(MentionBaseModel):
    """Represents an author/influencer."""

    id: str | None = None
    name: str | None = None
    username: str | None = None
    profile_url: str | None = None
    avatar_url: str | None = None
    followers_count: int | None = None
    following_count: int | None = None
    influence_score: float | None = None
    mentions_count: int | None = None
    source: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AuthorsResponse(MentionBaseModel):
    """Response containing a list of authors."""

    authors: list[Author] = Field(default_factory=list)
    total: int | None = None


class AuthorStats(MentionBaseModel):
    """Statistics for a specific author."""

    author_id: str
    mentions_count: int = 0
    reach: int = 0
    engagement: int = 0
    sentiment_positive: int = 0
    sentiment_negative: int = 0
    sentiment_neutral: int = 0


class AuthorStatsResponse(MentionBaseModel):
    """Response containing author statistics."""

    author: Author | None = None
    stats: AuthorStats | None = None
