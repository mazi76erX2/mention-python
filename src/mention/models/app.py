"""Application-related models for the Mention API."""

from __future__ import annotations

from pydantic import Field

from mention.models.base import MentionBaseModel


class Source(MentionBaseModel):
    """Available source information."""

    id: str
    name: str
    type: str
    available: bool = True
    description: str | None = None


class AppData(MentionBaseModel):
    """
    Application data from the Mention API.

    Contains information about available features, sources, and other
    application-level configuration.
    """

    languages: list[dict[str, str]] = Field(default_factory=list)
    countries: list[dict[str, str]] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    timezones: list[str] = Field(default_factory=list)
    features: dict[str, bool] = Field(default_factory=dict)
    version: str | None = None
