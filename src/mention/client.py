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
    Account,
    Alert,
    AlertPreferences,
    AlertsResponse,
    AppData,
    AuthorsResponse,
    CreateAlertRequest,
    CreateShareRequest,
    CreateTagRequest,
    CreateTaskRequest,
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    Share,
    SharesResponse,
    StatsPeriod,
    StatsResponse,
    Tag,
    TagsResponse,
    Task,
    TasksResponse,
    UpdateAlertRequest,
    UpdatePreferencesRequest,
    UpdateShareRequest,
    UpdateTagRequest,
    UpdateTaskRequest,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

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

        error_message = body.get("error", body.get("message", f"HTTP {response.status_code}"))

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

    def _get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
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

    def create_account(
        self,
        name: str,
        email: str,
        password: str,
        company: str | None = None,
        language: str = "en",
        timezone: str = "UTC",
    ) -> Account:
        """
        Create a new account.

        Args:
            name: Account name.
            email: Account email address.
            password: Account password.
            company: Company name (optional).
            language: Language code (default: en).
            timezone: Timezone (default: UTC).

        Returns:
            Created Account object.
        """
        data = self._post(
            "/accounts",
            json={
                "name": name,
                "email": email,
                "password": password,
                "company": company,
                "language": language,
                "timezone": timezone,
            },
        )
        return Account.model_validate(data.get("account", data))

    def get_account(self, account_id: str) -> Account:
        """
        Retrieve account information.

        Args:
            account_id: The account ID.

        Returns:
            Account object.
        """
        data = self._get(f"/accounts/{account_id}")
        return Account.model_validate(data.get("account", data))

    def get_account_me(self) -> Account:
        """
        Retrieve current user's account information.

        Returns:
            Account object for the authenticated user.
        """
        data = self._get("/accounts/me")
        return Account.model_validate(data.get("account", data))

    def update_account(
        self,
        account_id: str,
        name: str | None = None,
        email: str | None = None,
        company: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ) -> Account:
        """
        Update account information.

        Args:
            account_id: The account ID.
            name: New account name (optional).
            email: New email address (optional).
            company: New company name (optional).
            language: New language code (optional).
            timezone: New timezone (optional).

        Returns:
            Updated Account object.
        """
        json_data = {}
        if name is not None:
            json_data["name"] = name
        if email is not None:
            json_data["email"] = email
        if company is not None:
            json_data["company"] = company
        if language is not None:
            json_data["language"] = language
        if timezone is not None:
            json_data["timezone"] = timezone

        data = self._put(f"/accounts/{account_id}", json=json_data)
        return Account.model_validate(data.get("account", data))

    def delete_account(self, account_id: str) -> bool:
        """
        Delete an account.

        Args:
            account_id: The account ID.

        Returns:
            True if deletion was successful.
        """
        self._delete(f"/accounts/{account_id}")
        return True

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

    def pause_alert(self, account_id: str, alert_id: str) -> bool:
        """
        Pause an alert (stop monitoring).

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            True if pause was successful.
        """
        self._post(f"/accounts/{account_id}/alerts/{alert_id}/pause")
        return True

    def unpause_alert(self, account_id: str, alert_id: str) -> bool:
        """
        Unpause an alert (resume monitoring).

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            True if unpause was successful.
        """
        self._post(f"/accounts/{account_id}/alerts/{alert_id}/unpause")
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
                before_date.isoformat() if isinstance(before_date, datetime) else before_date
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

        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/mentions", params=params)
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
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}")
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

    def get_mention_children(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> MentionsResponse:
        """
        Fetch child mentions (replies, comments) of a mention.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.

        Returns:
            MentionsResponse containing child mentions.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/children")
        return MentionsResponse.model_validate(data)

    def stream_mentions(
        self,
        account_id: str,
        alert_id: str,
        *,
        since: datetime | str | None = None,
    ) -> Iterator[Mention]:
        """
        Stream mentions in real-time.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            since: Start streaming from this timestamp.

        Yields:
            Mention objects as they arrive.
        """
        params: dict[str, Any] = {}
        if since:
            params["since"] = since.isoformat() if isinstance(since, datetime) else since

        # This is a long-polling endpoint that returns mentions as they arrive
        while True:
            data = self._get(
                f"/accounts/{account_id}/alerts/{alert_id}/mentions/stream",
                params=params,
            )
            response = MentionsResponse.model_validate(data)

            for mention in response.mentions:
                yield mention
                # Update the since parameter for next request
                if mention.published_at:
                    params["since"] = mention.published_at.isoformat()

    # --- Tasks ---

    def get_tasks(self, account_id: str, alert_id: str) -> TasksResponse:
        """
        Fetch all tasks for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            TasksResponse containing list of tasks.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/tasks")
        return TasksResponse.model_validate(data)

    def get_mention_tasks(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> TasksResponse:
        """
        Fetch all tasks for a specific mention.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.

        Returns:
            TasksResponse containing list of tasks.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks")
        return TasksResponse.model_validate(data)

    def get_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        task_id: str,
    ) -> Task:
        """
        Fetch a single task by ID.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.
            task_id: The task ID.

        Returns:
            Task object.
        """
        data = self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks/{task_id}"
        )
        return Task.model_validate(data.get("task", data))

    def create_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        request: CreateTaskRequest,
    ) -> Task:
        """
        Create a new task for a mention.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.
            request: Task creation request.

        Returns:
            Created Task object.
        """
        data = self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks",
            json=request.model_dump(exclude_none=True),
        )
        return Task.model_validate(data.get("task", data))

    def update_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        task_id: str,
        request: UpdateTaskRequest,
    ) -> Task:
        """
        Update an existing task.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.
            task_id: The task ID.
            request: Task update request.

        Returns:
            Updated Task object.
        """
        data = self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks/{task_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Task.model_validate(data.get("task", data))

    def delete_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        task_id: str,
    ) -> bool:
        """
        Delete a task.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            mention_id: The mention ID.
            task_id: The task ID.

        Returns:
            True if deletion was successful.
        """
        self._delete(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks/{task_id}"
        )
        return True

    # --- Tags ---

    def get_tags(self, account_id: str, alert_id: str) -> TagsResponse:
        """
        Fetch all tags for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            TagsResponse containing list of tags.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/tags")
        return TagsResponse.model_validate(data)

    def create_tag(
        self,
        account_id: str,
        alert_id: str,
        request: CreateTagRequest,
    ) -> Tag:
        """
        Create a new tag for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            request: Tag creation request.

        Returns:
            Created Tag object.
        """
        data = self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/tags",
            json=request.model_dump(exclude_none=True),
        )
        return Tag.model_validate(data.get("tag", data))

    def update_tag(
        self,
        account_id: str,
        alert_id: str,
        tag_id: str,
        request: UpdateTagRequest,
    ) -> Tag:
        """
        Update an existing tag.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            tag_id: The tag ID.
            request: Tag update request.

        Returns:
            Updated Tag object.
        """
        data = self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/tags/{tag_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Tag.model_validate(data.get("tag", data))

    def delete_tag(self, account_id: str, alert_id: str, tag_id: str) -> bool:
        """
        Delete a tag.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            tag_id: The tag ID.

        Returns:
            True if deletion was successful.
        """
        self._delete(f"/accounts/{account_id}/alerts/{alert_id}/tags/{tag_id}")
        return True

    # --- Shares ---

    def get_shares(self, account_id: str, alert_id: str) -> SharesResponse:
        """
        Fetch all shares for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            SharesResponse containing list of shares.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/shares")
        return SharesResponse.model_validate(data)

    def get_share(self, account_id: str, alert_id: str, share_id: str) -> Share:
        """
        Fetch a single share by ID.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            share_id: The share ID.

        Returns:
            Share object.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/shares/{share_id}")
        return Share.model_validate(data.get("share", data))

    def create_share(
        self,
        account_id: str,
        alert_id: str,
        request: CreateShareRequest,
    ) -> Share:
        """
        Create a new share for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            request: Share creation request.

        Returns:
            Created Share object.
        """
        data = self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/shares",
            json=request.model_dump(exclude_none=True),
        )
        return Share.model_validate(data.get("share", data))

    def update_share(
        self,
        account_id: str,
        alert_id: str,
        share_id: str,
        request: UpdateShareRequest,
    ) -> Share:
        """
        Update an existing share.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            share_id: The share ID.
            request: Share update request.

        Returns:
            Updated Share object.
        """
        data = self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/shares/{share_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Share.model_validate(data.get("share", data))

    def delete_share(self, account_id: str, alert_id: str, share_id: str) -> bool:
        """
        Delete a share.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            share_id: The share ID.

        Returns:
            True if deletion was successful.
        """
        self._delete(f"/accounts/{account_id}/alerts/{alert_id}/shares/{share_id}")
        return True

    # --- Preferences ---

    def get_preferences(self, account_id: str, alert_id: str) -> AlertPreferences:
        """
        Fetch preferences for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.

        Returns:
            AlertPreferences object.
        """
        data = self._get(f"/accounts/{account_id}/alerts/{alert_id}/preferences")
        return AlertPreferences.model_validate(data.get("preferences", data))

    def update_preferences(
        self,
        account_id: str,
        alert_id: str,
        request: UpdatePreferencesRequest,
    ) -> AlertPreferences:
        """
        Update preferences for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            request: Preferences update request.

        Returns:
            Updated AlertPreferences object.
        """
        data = self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/preferences",
            json=request.model_dump(exclude_none=True),
        )
        return AlertPreferences.model_validate(data.get("preferences", data))

    # --- Authors ---

    def get_authors(
        self,
        account_id: str,
        alert_id: str,
        *,
        limit: int = 100,
        sort_by: str | None = None,
    ) -> AuthorsResponse:
        """
        Fetch authors/influencers for an alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            limit: Maximum number of authors to return.
            sort_by: Sort field (mentions, reach, influence, etc.).

        Returns:
            AuthorsResponse containing list of authors.
        """
        params: dict[str, Any] = {"limit": limit}
        if sort_by:
            params["sort_by"] = sort_by

        data = self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/authors",
            params=params,
        )
        return AuthorsResponse.model_validate(data)

    # --- Statistics ---

    def get_stats(
        self,
        account_id: str,
        alert_id: str | None = None,
        *,
        from_date: datetime | str | None = None,
        to_date: datetime | str | None = None,
        period: StatsPeriod = StatsPeriod.DAY,
    ) -> StatsResponse:
        """
        Fetch statistics for an account or alert.

        Args:
            account_id: The account ID.
            alert_id: The alert ID (optional, if None gets account-level stats).
            from_date: Start date for statistics period.
            to_date: End date for statistics period.
            period: Time grouping period (hour, day, week, month).

        Returns:
            StatsResponse containing statistics data.
        """
        params: dict[str, Any] = {"period": period.value}

        if from_date:
            params["from"] = from_date.isoformat() if isinstance(from_date, datetime) else from_date
        if to_date:
            params["to"] = to_date.isoformat() if isinstance(to_date, datetime) else to_date

        path = f"/accounts/{account_id}/stats"
        if alert_id:
            path = f"/accounts/{account_id}/alerts/{alert_id}/stats"

        data = self._get(path, params=params)
        return StatsResponse.model_validate(data)

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

        error_message = body.get("error", body.get("message", f"HTTP {response.status_code}"))

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

    async def _get(self, path: str, *, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make an async GET request."""
        return await self._request("GET", path, params=params)

    async def _post(self, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make an async POST request."""
        return await self._request("POST", path, json=json)

    async def _put(self, path: str, *, json: dict[str, Any] | None = None) -> dict[str, Any]:
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
                before_date.isoformat() if isinstance(before_date, datetime) else before_date
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

        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/mentions", params=params)
        return MentionsResponse.model_validate(data)

    async def get_mention(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> Mention:
        """Fetch a single mention by ID."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}")
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
        await self._post(f"/accounts/{account_id}/alerts/{alert_id}/mentions/markallread")
        return True

    async def get_mention_children(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> MentionsResponse:
        """Fetch child mentions (replies, comments) of a mention."""
        data = await self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/children"
        )
        return MentionsResponse.model_validate(data)

    async def stream_mentions(
        self,
        account_id: str,
        alert_id: str,
        *,
        since: datetime | str | None = None,
    ) -> AsyncIterator[Mention]:
        """
        Stream mentions in real-time.

        Args:
            account_id: The account ID.
            alert_id: The alert ID.
            since: Start streaming from this timestamp.

        Yields:
            Mention objects as they arrive.
        """
        params: dict[str, Any] = {}
        if since:
            params["since"] = since.isoformat() if isinstance(since, datetime) else since

        # This is a long-polling endpoint that returns mentions as they arrive
        while True:
            data = await self._get(
                f"/accounts/{account_id}/alerts/{alert_id}/mentions/stream",
                params=params,
            )
            response = MentionsResponse.model_validate(data)

            for mention in response.mentions:
                yield mention
                # Update the since parameter for next request
                if mention.published_at:
                    params["since"] = mention.published_at.isoformat()

    # --- Account ---

    async def create_account(
        self,
        name: str,
        email: str,
        password: str,
        company: str | None = None,
        language: str = "en",
        timezone: str = "UTC",
    ) -> Account:
        """Create a new account."""
        data = await self._post(
            "/accounts",
            json={
                "name": name,
                "email": email,
                "password": password,
                "company": company,
                "language": language,
                "timezone": timezone,
            },
        )
        return Account.model_validate(data.get("account", data))

    async def get_account(self, account_id: str) -> Account:
        """Fetch a single account by ID."""
        data = await self._get(f"/accounts/{account_id}")
        return Account.model_validate(data.get("account", data))

    async def get_account_me(self) -> Account:
        """Fetch the current user's account."""
        data = await self._get("/accounts/me")
        return Account.model_validate(data.get("account", data))

    async def update_account(
        self,
        account_id: str,
        name: str | None = None,
        email: str | None = None,
        company: str | None = None,
        language: str | None = None,
        timezone: str | None = None,
    ) -> Account:
        """Update an existing account."""
        json_data = {}
        if name is not None:
            json_data["name"] = name
        if email is not None:
            json_data["email"] = email
        if company is not None:
            json_data["company"] = company
        if language is not None:
            json_data["language"] = language
        if timezone is not None:
            json_data["timezone"] = timezone

        data = await self._put(f"/accounts/{account_id}", json=json_data)
        return Account.model_validate(data.get("account", data))

    async def delete_account(self, account_id: str) -> bool:
        """Delete an account."""
        await self._delete(f"/accounts/{account_id}")
        return True

    # --- Alert Pause/Unpause ---

    async def pause_alert(self, account_id: str, alert_id: str) -> bool:
        """Pause an alert (stop monitoring)."""
        await self._post(f"/accounts/{account_id}/alerts/{alert_id}/pause")
        return True

    async def unpause_alert(self, account_id: str, alert_id: str) -> bool:
        """Unpause an alert (resume monitoring)."""
        await self._post(f"/accounts/{account_id}/alerts/{alert_id}/unpause")
        return True

    # --- Tasks ---

    async def get_tasks(self, account_id: str, alert_id: str) -> TasksResponse:
        """Fetch all tasks for an alert."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/tasks")
        return TasksResponse.model_validate(data)

    async def get_mention_tasks(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
    ) -> TasksResponse:
        """Fetch all tasks for a specific mention."""
        data = await self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks"
        )
        return TasksResponse.model_validate(data)

    async def get_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        task_id: str,
    ) -> Task:
        """Fetch a single task by ID."""
        data = await self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks/{task_id}"
        )
        return Task.model_validate(data.get("task", data))

    async def create_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        request: CreateTaskRequest,
    ) -> Task:
        """Create a new task for a mention."""
        data = await self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks",
            json=request.model_dump(exclude_none=True),
        )
        return Task.model_validate(data.get("task", data))

    async def update_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        task_id: str,
        request: UpdateTaskRequest,
    ) -> Task:
        """Update an existing task."""
        data = await self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks/{task_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Task.model_validate(data.get("task", data))

    async def delete_task(
        self,
        account_id: str,
        alert_id: str,
        mention_id: str,
        task_id: str,
    ) -> bool:
        """Delete a task."""
        await self._delete(
            f"/accounts/{account_id}/alerts/{alert_id}/mentions/{mention_id}/tasks/{task_id}"
        )
        return True

    # --- Tags ---

    async def get_tags(self, account_id: str, alert_id: str) -> TagsResponse:
        """Fetch all tags for an alert."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/tags")
        return TagsResponse.model_validate(data)

    async def create_tag(
        self,
        account_id: str,
        alert_id: str,
        request: CreateTagRequest,
    ) -> Tag:
        """Create a new tag for an alert."""
        data = await self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/tags",
            json=request.model_dump(exclude_none=True),
        )
        return Tag.model_validate(data.get("tag", data))

    async def update_tag(
        self,
        account_id: str,
        alert_id: str,
        tag_id: str,
        request: UpdateTagRequest,
    ) -> Tag:
        """Update an existing tag."""
        data = await self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/tags/{tag_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Tag.model_validate(data.get("tag", data))

    async def delete_tag(self, account_id: str, alert_id: str, tag_id: str) -> bool:
        """Delete a tag."""
        await self._delete(f"/accounts/{account_id}/alerts/{alert_id}/tags/{tag_id}")
        return True

    # --- Shares ---

    async def get_shares(self, account_id: str, alert_id: str) -> SharesResponse:
        """Fetch all shares for an alert."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/shares")
        return SharesResponse.model_validate(data)

    async def get_share(self, account_id: str, alert_id: str, share_id: str) -> Share:
        """Fetch a single share by ID."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/shares/{share_id}")
        return Share.model_validate(data.get("share", data))

    async def create_share(
        self,
        account_id: str,
        alert_id: str,
        request: CreateShareRequest,
    ) -> Share:
        """Create a new share for an alert."""
        data = await self._post(
            f"/accounts/{account_id}/alerts/{alert_id}/shares",
            json=request.model_dump(exclude_none=True),
        )
        return Share.model_validate(data.get("share", data))

    async def update_share(
        self,
        account_id: str,
        alert_id: str,
        share_id: str,
        request: UpdateShareRequest,
    ) -> Share:
        """Update an existing share."""
        data = await self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/shares/{share_id}",
            json=request.model_dump(exclude_none=True),
        )
        return Share.model_validate(data.get("share", data))

    async def delete_share(self, account_id: str, alert_id: str, share_id: str) -> bool:
        """Delete a share."""
        await self._delete(f"/accounts/{account_id}/alerts/{alert_id}/shares/{share_id}")
        return True

    # --- Preferences ---

    async def get_preferences(self, account_id: str, alert_id: str) -> AlertPreferences:
        """Fetch preferences for an alert."""
        data = await self._get(f"/accounts/{account_id}/alerts/{alert_id}/preferences")
        return AlertPreferences.model_validate(data.get("preferences", data))

    async def update_preferences(
        self,
        account_id: str,
        alert_id: str,
        request: UpdatePreferencesRequest,
    ) -> AlertPreferences:
        """Update preferences for an alert."""
        data = await self._put(
            f"/accounts/{account_id}/alerts/{alert_id}/preferences",
            json=request.model_dump(exclude_none=True),
        )
        return AlertPreferences.model_validate(data.get("preferences", data))

    # --- Authors ---

    async def get_authors(
        self,
        account_id: str,
        alert_id: str,
        *,
        limit: int = 100,
        sort_by: str | None = None,
    ) -> AuthorsResponse:
        """Fetch authors/influencers for an alert."""
        params: dict[str, Any] = {"limit": limit}
        if sort_by:
            params["sort_by"] = sort_by

        data = await self._get(
            f"/accounts/{account_id}/alerts/{alert_id}/authors",
            params=params,
        )
        return AuthorsResponse.model_validate(data)

    # --- Statistics ---

    async def get_stats(
        self,
        account_id: str,
        alert_id: str | None = None,
        *,
        from_date: datetime | str | None = None,
        to_date: datetime | str | None = None,
        period: StatsPeriod = StatsPeriod.DAY,
    ) -> StatsResponse:
        """Fetch statistics for an account or alert."""
        params: dict[str, Any] = {"period": period.value}

        if from_date:
            params["from"] = from_date.isoformat() if isinstance(from_date, datetime) else from_date
        if to_date:
            params["to"] = to_date.isoformat() if isinstance(to_date, datetime) else to_date

        path = f"/accounts/{account_id}/stats"
        if alert_id:
            path = f"/accounts/{account_id}/alerts/{alert_id}/stats"

        data = await self._get(path, params=params)
        return StatsResponse.model_validate(data)

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
