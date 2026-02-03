"""Share-related models for the Mention API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import Field

from mention.models.base import MentionBaseModel

if TYPE_CHECKING:
    from datetime import datetime


class SharePermission(str, Enum):
    """Share permission levels."""

    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


class Share(MentionBaseModel):
    """Represents a share of an alert with another user."""

    id: str
    alert_id: str
    user_id: str | None = None
    email: str | None = None
    permission: SharePermission = SharePermission.READ
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SharesResponse(MentionBaseModel):
    """Response containing a list of shares."""

    shares: list[Share] = Field(default_factory=list)


class CreateShareRequest(MentionBaseModel):
    """Request body for creating a new share."""

    email: str
    permission: SharePermission = SharePermission.READ


class UpdateShareRequest(MentionBaseModel):
    """Request body for updating an existing share."""

    permission: SharePermission | None = None
