"""Base models and shared types for the Mention API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class MentionBaseModel(BaseModel):
    """Base model with common configuration for all Mention API models."""

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        extra="allow",
    )


T = TypeVar("T")


class APIResponse(MentionBaseModel, Generic[T]):
    """Generic API response wrapper."""

    ok: bool = True
    data: T | None = None
    error: str | None = None
    error_code: str | None = None


class PaginationLinks(MentionBaseModel):
    """Pagination links for paginated responses."""

    more: str | None = None
    pull: str | None = None
    next: str | None = None
    previous: str | None = None


class PaginatedResponse(MentionBaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    items: list[T] = Field(default_factory=list)
    links: PaginationLinks | None = Field(default=None, alias="_links")
    total: int | None = None
    page: int | None = None
    per_page: int | None = None

    @property
    def has_more(self) -> bool:
        """Check if there are more pages available."""
        return bool(self.links and self.links.more)


# Note: No inheritance - just defines fields
class TimestampMixin:
    """Mixin for models with timestamp fields."""

    created_at: datetime | None = None
    updated_at: datetime | None = None


def parse_datetime(value: Any) -> datetime | None:
    """Parse various datetime formats from the API."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
    return None
