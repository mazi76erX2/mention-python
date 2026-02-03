"""Tag-related models for the Mention API."""

from __future__ import annotations

from pydantic import Field

from mention.models.base import MentionBaseModel


class Tag(MentionBaseModel):
    """Represents a tag associated with an alert."""

    id: str
    name: str
    color: str | None = None


class TagsResponse(MentionBaseModel):
    """Response containing a list of tags."""

    tags: list[Tag] = Field(default_factory=list)


class CreateTagRequest(MentionBaseModel):
    """Request body for creating a new tag."""

    name: str
    color: str | None = None


class UpdateTagRequest(MentionBaseModel):
    """Request body for updating an existing tag."""

    name: str | None = None
    color: str | None = None
