"""Custom exceptions for the Mention API client."""

from __future__ import annotations

from typing import Any


class MentionError(Exception):
    """Base exception for all Mention API errors."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class MentionAPIError(MentionError):
    """Exception raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        response_body: dict[str, Any] | str | None = None,
    ) -> None:
        super().__init__(message, details={"status_code": status_code, "response": response_body})
        self.status_code = status_code
        self.response_body = response_body


class MentionAuthError(MentionAPIError):
    """Exception raised for authentication/authorization errors (401, 403)."""

    pass


class MentionNotFoundError(MentionAPIError):
    """Exception raised when a resource is not found (404)."""

    pass


class MentionRateLimitError(MentionAPIError):
    """Exception raised when rate limit is exceeded (429)."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 429,
        response_body: dict[str, Any] | str | None = None,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)
        self.retry_after = retry_after


class MentionValidationError(MentionError):
    """Exception raised for request validation errors."""

    pass


class MentionConnectionError(MentionError):
    """Exception raised for network/connection errors."""

    pass
