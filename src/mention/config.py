"""Configuration management for Mention API client."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from dotenv import load_dotenv

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True, slots=True)
class MentionConfig:
    """
    Configuration for the Mention API client.
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
            msg = f"Missing required environment variable: {prefix}ACCESS_TOKEN or ACCESS_TOKEN"
            raise ValueError(msg)

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
