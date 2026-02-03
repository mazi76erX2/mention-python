"""Task-related models for the Mention API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import Field

from mention.models.base import MentionBaseModel

if TYPE_CHECKING:
    from datetime import datetime


class TaskStatus(str, Enum):
    """Task status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(MentionBaseModel):
    """Represents a task associated with a mention."""

    id: str
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: str | None = None
    due_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    mention_id: str | None = None
    alert_id: str | None = None
    account_id: str | None = None


class TasksResponse(MentionBaseModel):
    """Response containing a list of tasks."""

    tasks: list[Task] = Field(default_factory=list)


class CreateTaskRequest(MentionBaseModel):
    """Request body for creating a new task."""

    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: str | None = None
    due_at: datetime | str | None = None


class UpdateTaskRequest(MentionBaseModel):
    """Request body for updating an existing task."""

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assigned_to: str | None = None
    due_at: datetime | str | None = None
