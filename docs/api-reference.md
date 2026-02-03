# API Reference

Complete reference for all classes, methods, and models in mention-python.

## Client Classes

### MentionClient

The main synchronous client for the Mention API.

```python
from mention import MentionClient

client = MentionClient(
    access_token="your-token",
    base_url="https://api.mention.net/api",  # optional
    timeout=30.0,                             # optional
    max_retries=3,                            # optional
    retry_delay=1.0,                          # optional
)
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `access_token` | `str` | Yes | - | OAuth2 access token |
| `base_url` | `str` | No | `https://api.mention.net/api` | API base URL |
| `timeout` | `float` | No | `30.0` | Request timeout in seconds |
| `max_retries` | `int` | No | `3` | Maximum retry attempts |
| `retry_delay` | `float` | No | `1.0` | Base delay between retries |

#### Class Methods

##### `from_config`

Create a client from a `MentionConfig` object.

```python
@classmethod
def from_config(cls, config: MentionConfig) -> MentionClient
```

**Example:**

```python
config = MentionConfig.from_env()
client = MentionClient.from_config(config)
```

#### Instance Methods

##### App Data

| Method | Returns | Description |
|--------|---------|-------------|
| `get_app_data()` | `AppData` | Get application configuration |

##### Alerts

| Method | Returns | Description |
|--------|---------|-------------|
| `get_alerts(account_id)` | `AlertsResponse` | List all alerts |
| `get_alert(account_id, alert_id)` | `Alert` | Get single alert |
| `create_alert(account_id, request)` | `Alert` | Create new alert |
| `update_alert(account_id, alert_id, request)` | `Alert` | Update alert |
| `delete_alert(account_id, alert_id)` | `bool` | Delete alert |

##### Mentions

| Method | Returns | Description |
|--------|---------|-------------|
| `get_mentions(account_id, alert_id, **filters)` | `MentionsResponse` | List mentions |
| `get_mention(account_id, alert_id, mention_id)` | `Mention` | Get single mention |
| `iter_mentions(account_id, alert_id, **filters)` | `Iterator[Mention]` | Iterate all mentions |
| `curate_mention(account_id, alert_id, mention_id, request)` | `Mention` | Update mention |
| `mark_all_mentions_read(account_id, alert_id)` | `bool` | Mark all as read |

##### Lifecycle

| Method | Returns | Description |
|--------|---------|-------------|
| `close()` | `None` | Close the HTTP client |

#### Context Manager

```python
with MentionClient(access_token="token") as client:
    alerts = client.get_alerts("account-id")
# Client automatically closed
```

---

### AsyncMentionClient

Asynchronous version of the client with identical API.

```python
from mention import AsyncMentionClient

client = AsyncMentionClient(
    access_token="your-token",
    base_url="https://api.mention.net/api",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0,
)
```

**Parameters:** Same as `MentionClient`

#### Class Methods

##### `from_config`

```python
@classmethod
def from_config(cls, config: MentionConfig) -> AsyncMentionClient
```

#### Instance Methods

All methods are async versions of `MentionClient` methods:

```python
async with AsyncMentionClient(access_token="token") as client:
    alerts = await client.get_alerts("account-id")
    alert = await client.get_alert("account-id", "alert-id")
    mentions = await client.get_mentions("account-id", "alert-id")
```

#### Async Context Manager

```python
async with AsyncMentionClient(access_token="token") as client:
    alerts = await client.get_alerts("account-id")
# Client automatically closed
```

---

## Configuration

### MentionConfig

Configuration container for client settings.

```python
from mention import MentionConfig

config = MentionConfig(
    access_token="your-token",
    account_id="default-account-id",  # optional
    base_url="https://api.mention.net/api",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0,
)
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `access_token` | `str` | Yes | - | OAuth2 access token |
| `account_id` | `str \| None` | No | `None` | Default account ID |
| `base_url` | `str` | No | `https://api.mention.net/api` | API base URL |
| `timeout` | `float` | No | `30.0` | Request timeout |
| `max_retries` | `int` | No | `3` | Maximum retries |
| `retry_delay` | `float` | No | `1.0` | Base retry delay |

#### Class Methods

##### `from_env`

Load configuration from environment variables.

```python
@classmethod
def from_env(
    cls,
    env_file: str | Path | None = None,
    prefix: str = "MENTION_",
) -> MentionConfig
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `env_file` | `str \| Path \| None` | `None` | Path to .env file |
| `prefix` | `str` | `"MENTION_"` | Environment variable prefix |

**Example:**

```python
# Load from default .env
config = MentionConfig.from_env()

# Load from specific file
config = MentionConfig.from_env(env_file=".env.production")

# Custom prefix
config = MentionConfig.from_env(prefix="MYAPP_MENTION_")
```

#### Instance Methods

##### `with_account`

Create new config with different account ID.

```python
def with_account(self, account_id: str) -> MentionConfig
```

**Example:**

```python
base_config = MentionConfig.from_env()
other_config = base_config.with_account("other-account-id")
```

---

## Models

### Alert Models

#### Alert

Represents a Mention alert.

```python
class Alert:
    id: str
    name: str
    query: AlertQuery
    languages: list[str]
    countries: list[str]
    sources: list[str]
    noise_detection: bool
    sentiment_analysis: bool
    mentions_count: int
    unread_mentions_count: int
    shares_count: int
    followers_count: int
    reach: int
    created_at: datetime | None
    updated_at: datetime | None
    last_mention_at: datetime | None
```

**Example:**

```python
alert = client.get_alert("account-id", "alert-id")

print(alert.name)
print(alert.query.included_keywords)
print(alert.mentions_count)
```

#### AlertQuery

Query configuration for an alert.

```python
class AlertQuery:
    type: QueryType
    included_keywords: list[str]
    excluded_keywords: list[str]
    required_keywords: list[str]
    should_belong_to_owner: bool | None
```

**Example:**

```python
from mention import AlertQuery, QueryType

query = AlertQuery(
    type=QueryType.BASIC,
    included_keywords=["python", "programming"],
    excluded_keywords=["snake"],
)
```

#### QueryType

Enum for alert query types.

```python
class QueryType(str, Enum):
    BASIC = "basic"
    ADVANCED = "advanced"
    BOOLEAN = "boolean"
```

#### AlertsResponse

Response containing a list of alerts.

```python
class AlertsResponse:
    alerts: list[Alert]
    total: int | None
    
    @property
    def has_more(self) -> bool
```

**Example:**

```python
response = client.get_alerts("account-id")

for alert in response.alerts:
    print(alert.name)

print(f"Total: {response.total}")
```

#### CreateAlertRequest

Request body for creating an alert.

```python
class CreateAlertRequest:
    name: str
    query: AlertQuery
    languages: list[str] = ["en"]
    countries: list[str] = []
    sources: list[str] = ["web"]
    noise_detection: bool = True
    sentiment_analysis: bool = True
```

**Example:**

```python
from mention import CreateAlertRequest, AlertQuery, QueryType

request = CreateAlertRequest(
    name="My Alert",
    query=AlertQuery(
        type=QueryType.BASIC,
        included_keywords=["keyword1", "keyword2"],
    ),
    languages=["en", "es"],
    sources=["web", "twitter"],
)

alert = client.create_alert("account-id", request)
```

#### UpdateAlertRequest

Request body for updating an alert. All fields are optional.

```python
class UpdateAlertRequest:
    name: str | None = None
    query: AlertQuery | None = None
    languages: list[str] | None = None
    countries: list[str] | None = None
    sources: list[str] | None = None
    noise_detection: bool | None = None
    sentiment_analysis: bool | None = None
```

**Example:**

```python
from mention import UpdateAlertRequest

# Partial update - only change name
request = UpdateAlertRequest(name="New Name")
alert = client.update_alert("account-id", "alert-id", request)
```

---

### Mention Models

#### Mention

Represents a single mention.

```python
class Mention:
    id: str
    title: str | None
    description: str | None
    description_short: str | None
    original_url: str | None
    source_name: str | None
    source_type: str | None
    tone: Tone | None
    author: Author | None
    tags: list[Tag]
    favorite: bool
    read: bool
    trashed: bool
    published_at: datetime | None
    created_at: datetime | None
    reach: int | None
    engagement: dict[str, int] | None
    language: str | None
    country: str | None
    image_url: str | None
    video_url: str | None
```

**Example:**

```python
mention = client.get_mention("account-id", "alert-id", "mention-id")

print(mention.title)
print(mention.tone)
print(mention.original_url)

if mention.author:
    print(mention.author.name)
```

#### Tone

Enum for mention sentiment.

```python
class Tone(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
```

**Example:**

```python
from mention import Tone

if mention.tone == Tone.POSITIVE:
    print("Positive mention!")
elif mention.tone == Tone.NEGATIVE:
    print("Negative mention!")
```

#### Author

Author information for a mention.

```python
class Author:
    id: str | None
    name: str | None
    username: str | None
    profile_url: str | None
    avatar_url: str | None
    followers_count: int | None
    following_count: int | None
    influence_score: float | None
```

**Example:**

```python
if mention.author:
    print(f"Author: {mention.author.name}")
    print(f"Followers: {mention.author.followers_count}")
```

#### Tag

Tag associated with a mention.

```python
class Tag:
    id: str
    name: str
    color: str | None
```

**Example:**

```python
for tag in mention.tags:
    print(f"Tag: {tag.name} ({tag.color})")
```

#### MentionsResponse

Response containing a list of mentions.

```python
class MentionsResponse:
    mentions: list[Mention]
    links: PaginationLinks | None
    total: int | None
    
    @property
    def has_more(self) -> bool
```

**Example:**

```python
response = client.get_mentions("account-id", "alert-id", limit=100)

for mention in response.mentions:
    print(mention.title)

if response.has_more:
    print("More mentions available")
```

#### PaginationLinks

Pagination links for navigating results.

```python
class PaginationLinks:
    more: str | None
    pull: str | None
    next: str | None
    previous: str | None
```

#### CurateMentionRequest

Request body for updating a mention.

```python
class CurateMentionRequest:
    favorite: bool | None = None
    read: bool | None = None
    trashed: bool | None = None
    tone: Tone | None = None
    tags: list[str] | None = None
    folder: str | None = None
```

**Example:**

```python
from mention import CurateMentionRequest, Tone

request = CurateMentionRequest(
    favorite=True,
    read=True,
    tone=Tone.POSITIVE,
)

mention = client.curate_mention(
    "account-id", "alert-id", "mention-id", request
)
```

---

### App Models

#### AppData

Application configuration data.

```python
class AppData:
    languages: list[dict[str, str]]
    countries: list[dict[str, str]]
    sources: list[Source]
    timezones: list[str]
    features: dict[str, bool]
    version: str | None
```

**Example:**

```python
app_data = client.get_app_data()

print(f"Available sources: {len(app_data.sources)}")
print(f"Available languages: {len(app_data.languages)}")
```

#### Source

Available source information.

```python
class Source:
    id: str
    name: str
    type: str
    available: bool
    description: str | None
```

---

### Account Models

#### Account

Account information.

```python
class Account:
    id: str
    name: str | None
    email: str | None
    company: str | None
    plan: str | None
    quota: AccountQuota | None
    stats: AccountStats | None
    timezone: str | None
    language: str | None
    features: list[str]
    is_admin: bool
    subscription_expires_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None
```

#### AccountQuota

Account quota and limits.

```python
class AccountQuota:
    alerts: int | None
    mentions: int | None
    mentions_without_archive: int | None
    api_calls: int | None
```

#### AccountStats

Account usage statistics.

```python
class AccountStats:
    alerts_count: int
    mentions_count: int
    unread_mentions_count: int
```

---

## Exceptions

### Exception Hierarchy

```
MentionError (base)
├── MentionAPIError
│   ├── MentionAuthError (401, 403)
│   ├── MentionNotFoundError (404)
│   └── MentionRateLimitError (429)
├── MentionConnectionError
└── MentionValidationError
```

### MentionError

Base exception for all Mention errors.

```python
class MentionError(Exception):
    message: str
    details: dict[str, Any]
```

### MentionAPIError

Exception for API errors.

```python
class MentionAPIError(MentionError):
    message: str
    status_code: int
    response_body: dict | str | None
```

### MentionAuthError

Exception for authentication errors (401, 403).

```python
class MentionAuthError(MentionAPIError):
    pass
```

### MentionNotFoundError

Exception for not found errors (404).

```python
class MentionNotFoundError(MentionAPIError):
    pass
```

### MentionRateLimitError

Exception for rate limit errors (429).

```python
class MentionRateLimitError(MentionAPIError):
    retry_after: int | None  # Seconds to wait
```

### MentionConnectionError

Exception for network errors.

```python
class MentionConnectionError(MentionError):
    pass
```

### MentionValidationError

Exception for validation errors.

```python
class MentionValidationError(MentionError):
    pass
```

### Usage Example

```python
from mention.exceptions import (
    MentionError,
    MentionAPIError,
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
    MentionConnectionError,
)

try:
    alert = client.get_alert("account-id", "alert-id")
except MentionAuthError as e:
    print(f"Auth failed: {e.message}")
    print(f"Status: {e.status_code}")
except MentionNotFoundError as e:
    print(f"Not found: {e.message}")
except MentionRateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after}s")
except MentionConnectionError as e:
    print(f"Connection error: {e.message}")
except MentionAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
except MentionError as e:
    print(f"Error: {e.message}")
```

---

## Method Details

### get_mentions

Fetch mentions for an alert with optional filters.

```python
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
) -> MentionsResponse
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `account_id` | `str` | - | Account ID |
| `alert_id` | `str` | - | Alert ID |
| `limit` | `int` | `100` | Max mentions (max: 1000) |
| `before_date` | `datetime \| str \| None` | `None` | Return mentions before date |
| `not_before_date` | `datetime \| str \| None` | `None` | Return mentions on/after date |
| `since_id` | `str \| None` | `None` | Return mentions since ID |
| `source` | `str \| None` | `None` | Filter by source |
| `read` | `bool \| None` | `None` | Filter by read status |
| `favorite` | `bool \| None` | `None` | Filter by favorite status |
| `tone` | `str \| None` | `None` | Filter by tone |
| `cursor` | `str \| None` | `None` | Pagination cursor |

**Example:**

```python
# Basic usage
mentions = client.get_mentions("account-id", "alert-id")

# With filters
mentions = client.get_mentions(
    "account-id",
    "alert-id",
    limit=50,
    source="twitter",
    tone="positive",
    read=False,
)

# With date range
from datetime import datetime, timedelta

mentions = client.get_mentions(
    "account-id",
    "alert-id",
    not_before_date=datetime.now() - timedelta(days=7),
    before_date=datetime.now(),
)
```

### iter_mentions

Iterate over all mentions with automatic pagination.

```python
def iter_mentions(
    self,
    account_id: str,
    alert_id: str,
    *,
    limit: int = 100,
    **kwargs: Any,
) -> Iterator[Mention]
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `account_id` | `str` | - | Account ID |
| `alert_id` | `str` | - | Alert ID |
| `limit` | `int` | `100` | Mentions per page |
| `**kwargs` | `Any` | - | Same filters as `get_mentions` |

**Example:**

```python
# Iterate all mentions
for mention in client.iter_mentions("account-id", "alert-id"):
    print(mention.title)

# With filters
for mention in client.iter_mentions(
    "account-id",
    "alert-id",
    source="twitter",
    tone="negative",
):
    handle_negative_tweet(mention)

# Limit total iterations
count = 0
for mention in client.iter_mentions("account-id", "alert-id"):
    process(mention)
    count += 1
    if count >= 1000:
        break
```

---

## Type Aliases

```python
from mention import (
    MentionClient,
    AsyncMentionClient,
    MentionConfig,
    
    # Models
    Alert,
    AlertQuery,
    AlertsResponse,
    CreateAlertRequest,
    UpdateAlertRequest,
    
    Mention,
    MentionsResponse,
    CurateMentionRequest,
    Author,
    Tag,
    
    AppData,
    Source,
    
    Account,
    AccountQuota,
    AccountStats,
    
    # Enums
    QueryType,
    Tone,
    
    # Exceptions
    MentionError,
    MentionAPIError,
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
    MentionConnectionError,
    MentionValidationError,
)
```