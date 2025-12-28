"""
Main client for the Mention API.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import TYPE_CHECKING, Any, TypeVar

import httpx

from mention.exceptions import (
    MentionAPIError,
    MentionAuthError,
    MentionConnectionError,
    MentionNotFoundError,
    MentionRateLimitError,
)
from mention.models import (
    Alert,
    AlertsResponse,
    AppData,
    CreateAlertRequest,
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    UpdateAlertRequest,
)

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mention.config import MentionConfig

T = TypeVar("T")


class MentionClient:
    """
    A typed client for the Mention API.

    This client provides methods for interacting with all Mention API endpoints,
    with full type hints and automatic request/response validation.

    Example:
        >>> from mention import MentionClient
        >>> client = MentionClient(access_token="your-token")
        >>> alerts = client.get_alerts("account-id")
        >>> for alert in alerts.alerts:
        ...     print(alert.name)

    With configuration:
        >>> from mention import MentionClient, MentionConfig
        >>> config = MentionConfig.from_env()
        >>> client = MentionClient.from_config(config)

    As context manager:
        >>> with MentionClient(access_token="token") as client:
        ...     data = client.get_app_data()
    """

    DEFAULT_BASE_URL = "https://api.mention.net/api"

    def __init__(
        self,
        access_token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """
        Initialize the Mention API client.

        Args:
            access_token: OAuth2 access token for authentication.
            base_url: Base URL for the Mention API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retry attempts for failed requests.
            retry_delay: Base delay between retries in seconds.
        """
        if not access_token:
            raise ValueError("access_token is required")

        self._access_token = access_token
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._default_headers(),
        )

    @classmethod
    def from_config(cls, config: MentionConfig) -> MentionClient:
        """
        Create a client from a MentionConfig instance.

        Args:
            config: Configuration object.

        Returns:
            Configured MentionClient instance.
        """
        return cls(
            access_token=config.access_token,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
            retry_delay=config.retry_delay,
        )

    def _default_headers(self) -> dict[str, str]:
        """Get default headers for all requests."""
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "mention-python/1.0.0",
        }

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: The httpx response object.

        Returns:
            Parsed JSON response body.

        Raises:
            MentionAuthError: For 401/403 responses.
            MentionNotFoundError: For 404 responses.
            MentionRateLimitError: For 429 responses.
            MentionAPIError: For other error responses.
        """
        try:
            body = response.json() if response.content else {}
        except Exception:
            body = {"raw": response.text}

        if response.is_success:
            return body

        error_message = body.get(
            "error", body.get("message", f"HTTP {response.status_code}")
        )

        if response.status_code in (401, 403):
            raise MentionAuthError(
                f"Authentication failed: {error_message}",
                status_code=response.status_code,
                response_body=body,
            )

        if response.status_code == 404:
            raise MentionNotFoundError(
                f"Resource not found: {error_message}",
                status_code=response.status_code,
                response_body=body,
            )

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise MentionRateLimitError(
                f"Rate limit exceeded: {error_message}",
                status_code=response.status_code,
                response_body=body,
                retry_after=int(retry_after) if retry_after else None,
            )

        raise MentionAPIError(
            f"API error: {error_message}",
            status_code=response.status_code,
            response_body=body,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE).
            path: API endpoint path.
            params: Query parameters.
            json: JSON body for POST/PUT requests.

        Returns:
            Parsed JSON response.
        """
        last_exception: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json,
                )
                return self._handle_response(response)

            except httpx.TimeoutException as e:
                last_exception = MentionConnectionError(f"Request timed out: {e}")
            except httpx.ConnectError as e:
                last_exception = MentionConnectionError(f"Connection failed: {e}")
            except MentionRateLimitError as e:
                if attempt < self._max_retries:
                    delay = e.retry_after or (self._retry_delay * (2**attempt))
                    time.sleep(delay)
                    continue
                raise
            except MentionAPIError:
                raise
            except Exception as e:
                last_exception = MentionConnectionError(f"Unexpected error: {e}")

            if attempt < self._max_retries:
                time.sleep(self._retry_delay * (2**attempt))

        raise last_exception or MentionConnectionError("Request failed after retries")

    def _get(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a GET request."""
        return self._request("GET", path, params=params)

    def _post(self, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a POST request."""
        return self._request("POST", path, json=json)

    def _put(self, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a PUT request."""
        return self._request("PUT", path, json=json)

    def _delete(self, path: str) -> dict[str, Any]:
        """Make a DELETE request."""
        return self._request("DELETE", path)

    # --- App Data ---

    def get_app_data(self) -> AppData:
        """
        Retrieve application data including available sources, languages, etc.

        Returns:
            AppData object with application configuration.
        """
        data = self._get("/app/data")
        return AppData.model_validate(data)

    # --- Account ---

    def get_account(self, account_id: str) -> dict[str, Any]:
        """
        Retrieve account information.

        Args:
            account_id: The account ID.

        Returns:
            Account data dictionary.
        """
        return self._get(f"/accounts/{account_id}")

    # --- Alerts ---

    def get_alerts(self, account_id: str) -> AlertsResponse:
        """
        Fetch all alerts for an account.

        Args:
            account_id: The account ID.

        Returns:
            AlertsResponse containing list of alerts.
        """
        data = self._get(f"/accounts/{account_id}/alerts")
        return AlertsResponse.model_validate(data)

    def get_alert(self, account_id: str, alert_id: str) -> Alert:
        """
        Fetch a single alert by ID.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            Alert object.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}")
        alert_data = data.get("alert", data)
        return Alert.model_validate(alert_data)

    def create_alert(self, account_id: str, request: CreateAlertRequest) -> Alert:
        """
        Create a new alert.

        Args:
            account_id: The account ID.
            request: Alert creation request.

        Returns:
            Created Alert object.
        """
        data = self._post(
            f"/accounts/{account_id}/alerts",
            json=request.model_dump(exclude_none=True),
        )
        alert_data = data.get("alert", data)
        return Alert.model_validate(alert_data)

    def update_alert(
        self,
        account_id: str,
        alert_id: str,
        request: UpdateAlertRequest,
    ) -> Alert:
        """
        Update an existing alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            request: Alert update request.

        Returns:
            Updated Alert object.
        """
        data = self._put(
            f"/accounts/{account_id}/alerts/{alert_id}",
            json=request.model_dump(exclude_none=True),
        )
        alert_data = data.get("alert", data)
        return Alert.model_validate(alert_data)

    def delete_alert(self, account_id: str, alert_id: str) -> bool:
        """
        Delete an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            True if deletion was successful.
        """
        self._delete(f"/accounts/{account_id}/alerts/{alert_id}")
        return True

    # --- Mentions ---

    def get_mentions(
        self,
        account_id: str,
        alert_id: str,
        *,
        limit: int = 100,
        before_date: datetime | str | None = None,
        not_before_date: datetime | str | None = None,
        since_id: str | None = None,
        source: str | None = None,
        read: bool | None = None,
        favorite: bool | None = None,
        tone: str | None = None,
        cursor: str | None = None,
    ) -> MentionsResponse:
        """
        Fetch mentions for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            limit: Maximum number of mentions to return (max 1000).
            before_date: Return mentions before this date.
            not_before_date: Return mentions on or after this date.
            since_id: Return mentions since this mention ID.
            source: Filter by source type.
            read: Filter by read status.
            favorite: Filter by favorite status.
            tone: Filter by tone (positive, negative, neutral).
            cursor: Pagination cursor.

        Returns:
            MentionsResponse containing list of mentions.
        """
        params: dict[str, Any] = {"limit": min(limit, 1000)}

        if before_date:
            params["before_date"] = (
                before_date.isoformat()
                if isinstance(before_date, datetime)
                else before_date
            )
        if not_before_date:
            params["not_before_date"] = (
                not_before_date.isoformat()
                if isinstance(not_before_date, datetime)
                else not_before_date
            )
        if since_id:
            params["since_id"] = since_id
        if source:
            params["source"] = source
        if read is not None:
            params["read"] = str(read).lower()
        if favorite is not None:
            params["favorite"] = str(favorite).lower()
        if tone:
            params["tone"] = tone
        if cursor:
            params["cursor"] = cursor

        data = self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions", params=params
        )
        return MentionsResponse.model_validate(data)

    def iter_mentions(
        self,
        account_id: str,
        alert_id: str,
        *,
        limit: int = 100,
        **kwargs: Any,
    ) -> Iterator[Mention]:
        """
        Iterate over all mentions with automatic pagination.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            limit: Number of mentions per page.
            **kwargs: Additional filters (see get_mentions).

        Yields:
            Mention objects.
        """
        cursor: str | None = None

        while True:
            response = self.get_mentions(
                account_id,
                alert_id,
                limit=limit,
                cursor=cursor,
                **kwargs,
            )

            yield from response.mentions

            if not response.has_more or not response.links or not response.links.more:
                break

            # Extract cursor from the 'more' URL
            cursor = response.links.more

    def get_mention(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> Mention:
        """
        Fetch a single mention by ID.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.

        Returns:
            Mention object.
        """
        data = self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}"
        )
        return Mention.model_validate(data)

    def curate_mention(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        request: CurateMentionRequest,
    ) -> Mention:
        """
        Update/curate a mention.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.
            request: Curation request with updates.

        Returns:
            Updated Mention object.
        """
        data = self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Mention.model_validate(data)

    def mark_all_mentions_read(self, account_id: str, alert_id: str) -> bool:
        """
        Mark all mentions for an alert as read.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            True if successful.
        """
        self._post(f"/accounts/{account_id}/alerts/{alert_id}/mentions/markallread")
        return True

    # --- Context Manager ---

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> MentionClient:
        """Enter context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit context manager."""
        self.close()


class AsyncMentionClient:
    """
    Async version of the Mention API client.

    Example:
        >>> import asyncio
        >>> from mention import AsyncMentionClient
        >>>
        >>> async def main():
        ...     async with AsyncMentionClient(access_token="token") as client:
        ...         alerts = await client.get_alerts("account-id")
        ...         print(alerts)
        >>>
        >>> asyncio.run(main())
    """

    DEFAULT_BASE_URL = "https://api.mention.net/api"

    def __init__(
        self,
        access_token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """Initialize the async Mention API client."""
        if not access_token:
            raise ValueError("access_token is required")

        self._access_token = access_token
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay

        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=self._default_headers(),
        )

    def _default_headers(self) -> dict[str, str]:
        """Get default headers for all requests."""
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "mention-python/1.0.0",
        }

    @classmethod
    def from_config(cls, config: MentionConfig) -> AsyncMentionClient:
        """Create an async client from a MentionConfig instance."""
        return cls(
            access_token=config.access_token,
            base_url=config.base_url,
            timeout=config.timeout,
            max_retries=config.max_retries,
            retry_delay=config.retry_delay,
        )

    async def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        try:
            body = response.json() if response.content else {}
        except Exception:
            body = {"raw": response.text}

        if response.is_success:
            return body

        error_message = body.get(
            "error", body.get("message", f"HTTP {response.status_code}")
        )

        if response.status_code in (401, 403):
            raise MentionAuthError(
                f"Authentication failed: {error_message}",
                status_code=response.status_code,
                response_body=body,
            )

        if response.status_code == 404:
            raise MentionNotFoundError(
                f"Resource not found: {error_message}",
                status_code=response.status_code,
                response_body=body,
            )

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise MentionRateLimitError(
                f"Rate limit exceeded: {error_message}",
                status_code=response.status_code,
                response_body=body,
                retry_after=int(retry_after) if retry_after else None,
            )

        raise MentionAPIError(
            f"API error: {error_message}",
            status_code=response.status_code,
            response_body=body,
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an async HTTP request with retry logic."""
        import asyncio

        last_exception: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json,
                )
                return await self._handle_response(response)

            except httpx.TimeoutException as e:
                last_exception = MentionConnectionError(f"Request timed out: {e}")
            except httpx.ConnectError as e:
                last_exception = MentionConnectionError(f"Connection failed: {e}")
            except MentionRateLimitError as e:
                if attempt < self._max_retries:
                    delay = e.retry_after or (self._retry_delay * (2**attempt))
                    await asyncio.sleep(delay)
                    continue
                raise
            except MentionAPIError:
                raise
            except Exception as e:
                last_exception = MentionConnectionError(f"Unexpected error: {e}")

            if attempt < self._max_retries:
                await asyncio.sleep(self._retry_delay * (2**attempt))

        raise last_exception or MentionConnectionError("Request failed after retries")

    async def _get(
        self, path: str, *, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make an async GET request."""
        return await self._request("GET", path, params=params)

    async def _post(
        self, path: str, *, json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make an async POST request."""
        return await self._request("POST", path, json=json)

    async def _put(
        self, path: str, *, json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make an async PUT request."""
        return await self._request("PUT", path, json=json)

    async def _delete(self, path: str) -> dict[str, Any]:
        """Make an async DELETE request."""
        return await self._request("DELETE", path)

    # --- App Data ---

    async def get_app_data(self) -> AppData:
        """Retrieve application data."""
        data = await self._get("/app/data")
        return AppData.model_validate(data)

    # --- Alerts ---

    async def get_alerts(self, account_id: str) -> AlertsResponse:
        """Fetch all alerts for an account."""
        data = await self._get(f"/accounts/{account_id}/alerts")
        return AlertsResponse.model_validate(data)

    async def get_alert(self, account_id: str, alert_id: str) -> Alert:
        """Fetch a single alert by ID."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}")
        alert_data = data.get("alert", data)
        return Alert.model_validate(alert_data)

    async def create_alert(self, account_id: str, request: CreateAlertRequest) -> Alert:
        """Create a new alert."""
        data = await self._post(
            f"/accounts/{account_id}/alerts",
            json=request.model_dump(exclude_none=True),
        )
        alert_data = data.get("alert", data)
        return Alert.model_validate(alert_data)

    async def update_alert(
        self,
        account_id: str,
        alert_id: str,
        request: UpdateAlertRequest,
    ) -> Alert:
        """Update an existing alert."""
        data = await self._put(
            f"/accounts/{account_id}/alerts/{alert_id}",
            json=request.model_dump(exclude_none=True),
        )
        alert_data = data.get("alert", data)
        return Alert.model_validate(alert_data)

    async def delete_alert(self, account_id: str, alert_id: str) -> bool:
        """Delete an alert."""
        await self._delete(f"/accounts/{account_id}/alerts/{alert_id}")
        return True

    # --- Mentions ---

    async def get_mentions(
        self,
        account_id: str,
        alert_id: str,
        *,
        limit: int = 100,
        before_date: datetime | str | None = None,
        not_before_date: datetime | str | None = None,
        since_id: str | None = None,
        source: str | None = None,
        read: bool | None = None,
        favorite: bool | None = None,
        tone: str | None = None,
        cursor: str | None = None,
    ) -> MentionsResponse:
        """Fetch mentions for an alert."""
        params: dict[str, Any] = {"limit": min(limit, 1000)}

        if before_date:
            params["before_date"] = (
                before_date.isoformat()
                if isinstance(before_date, datetime)
                else before_date
            )
        if not_before_date:
            params["not_before_date"] = (
                not_before_date.isoformat()
                if isinstance(not_before_date, datetime)
                else not_before_date
            )
        if since_id:
            params["since_id"] = since_id
        if source:
            params["source"] = source
        if read is not None:
            params["read"] = str(read).lower()
        if favorite is not None:
            params["favorite"] = str(favorite).lower()
        if tone:
            params["tone"] = tone
        if cursor:
            params["cursor"] = cursor

        data = await self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions", params=params
        )
        return MentionsResponse.model_validate(data)

    async def get_mention(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> Mention:
        """Fetch a single mention by ID."""
        data = await self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}"
        )
        return Mention.model_validate(data)

    async def curate_mention(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        request: CurateMentionRequest,
    ) -> Mention:
        """Update/curate a mention."""
        data = await self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Mention.model_validate(data)

    async def mark_all_mentions_read(self, account_id: str, alert_id: str) -> bool:
        """Mark all mentions for an alert as read."""
        await self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/markallread"
        )
        return True

    # --- Context Manager ---

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncMentionClient:
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        """Exit async context manager."""
        await self.close()
