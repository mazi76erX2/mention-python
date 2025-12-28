"""Configuration management for Mention API client."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class MentionConfig:
    """
    Configuration for the Mention API client.

    Attributes:
        access_token: OAuth2 access token for authentication.
        account_id: Default account ID to use for API calls.
        base_url: Base URL for the Mention API.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts for failed requests.
        retry_delay: Base delay between retries in seconds.
    """

    access_token: str
    account_id: str | None = None
    base_url: str = "https://api.mention.net/api"
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(
        cls,
        env_file: str | Path | None = None,
        *,
        prefix: str = "MENTION_",
    ) -> MentionConfig:
        """
        Create configuration from environment variables.

        Args:
            env_file: Path to .env file (optional).
            prefix: Prefix for environment variables (default: "MENTION_").

        Returns:
            MentionConfig instance.

        Raises:
            ValueError: If required environment variables are missing.

        Environment variables:
            - {prefix}ACCESS_TOKEN: OAuth2 access token (required)
            - {prefix}ACCOUNT_ID: Default account ID
            - {prefix}BASE_URL: API base URL
            - {prefix}TIMEOUT: Request timeout
            - {prefix}MAX_RETRIES: Maximum retry attempts
            - {prefix}RETRY_DELAY: Delay between retries
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        def get_var(name: str, default: str | None = None) -> str | None:
            """Get environment variable with prefix fallback."""
            return os.getenv(f"{prefix}{name}") or os.getenv(name) or default

        access_token = get_var("ACCESS_TOKEN")
        if not access_token:
            raise ValueError(
                f"Missing required environment variable: {prefix}ACCESS_TOKEN or ACCESS_TOKEN"
            )

        return cls(
            access_token=access_token,
            account_id=get_var("ACCOUNT_ID"),
            base_url=get_var("BASE_URL", "https://api.mention.net/api")
            or "https://api.mention.net/api",
            timeout=float(get_var("TIMEOUT", "30.0") or "30.0"),
            max_retries=int(get_var("MAX_RETRIES", "3") or "3"),
            retry_delay=float(get_var("RETRY_DELAY", "1.0") or "1.0"),
        )

    def with_account(self, account_id: str) -> MentionConfig:
        """Return a new config with a different account ID."""
        return MentionConfig(
            access_token=self.access_token,
            account_id=account_id,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            extra=self.extra,
        )
