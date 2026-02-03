# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-XX-XX

### Why This Rewrite?

The original library was built in 2018 using patterns common at that time. Seven years later, the Python ecosystem has evolved significantly. This rewrite modernizes the library to follow current best practices:

| Aspect | v0.x (2018) | v2.0 (2025) |
|--------|-------------|-------------|
| Python | 3.6+ | 3.10+ |
| HTTP Client | requests | httpx |
| Validation | Manual dicts | Pydantic v2 |
| Type Hints | Minimal | Full strict typing |
| Async | Not supported | Full support |
| CLI | None | Complete CLI |
| Build | setuptools | hatchling |
| Linting | pylint/black/isort | ruff |
| Docs | Sphinx/RST | MkDocs/Markdown |
| Package Manager | pip/Pipfile | uv |

### Added

- **Modern Client Architecture**
    - `MentionClient` - Single client class for all API operations
    - `AsyncMentionClient` - Full async/await support
    - Context manager support (`with` statement)
    - Automatic retry logic with exponential backoff
    - Rate limit handling with `Retry-After` support

- **Type Safety**
    - Full type hints for all public APIs
    - Pydantic v2 models for request/response validation
    - IDE autocomplete and static analysis support

- **Configuration**
    - `MentionConfig` class for managing settings
    - Environment variable support with `MENTION_` prefix
    - Automatic `.env` file loading via python-dotenv

- **Pagination**
    - `iter_mentions()` method for automatic pagination
    - `has_more` property on response objects

- **Command Line Interface**
    - `mention alerts list` - List all alerts
    - `mention alerts get` - Get single alert
    - `mention alerts create` - Create new alert
    - `mention alerts delete` - Delete alert
    - `mention mentions list` - List mentions with filters
    - `mention mentions get` - Get single mention
    - `mention mentions stream` - Stream all mentions
    - `mention mentions curate` - Update mention
    - `mention mentions mark-read` - Mark all as read
    - `mention app-data` - Get application data

- **Exception Hierarchy**
    - `MentionError` - Base exception
    - `MentionAPIError` - API errors with status code
    - `MentionAuthError` - Authentication failures (401, 403)
    - `MentionNotFoundError` - Resource not found (404)
    - `MentionRateLimitError` - Rate limit exceeded (429)
    - `MentionConnectionError` - Network errors
    - `MentionValidationError` - Request validation errors

- **Models**
    - `Alert`, `AlertQuery`, `AlertsResponse`
    - `CreateAlertRequest`, `UpdateAlertRequest`
    - `Mention`, `MentionsResponse`, `Author`, `Tag`
    - `CurateMentionRequest`
    - `AppData`, `Source`
    - `Account`, `AccountQuota`, `AccountStats`
    - `QueryType`, `Tone` enums

- **Documentation**
    - MkDocs with Material theme
    - Complete API reference
    - User guides for common tasks
    - CLI reference

- **Testing**
    - pytest test suite
    - respx for HTTP mocking
    - Full test coverage

### Changed

- **BREAKING**: Complete API redesign
    - Single `MentionClient` instead of one class per endpoint
    - Method calls instead of `.query()` pattern
    - Typed model responses instead of raw dicts

- **BREAKING**: Minimum Python version is now 3.10
    - Required for modern type hint syntax (`X | None`)
    - Required for `match` statements (internal use)

- **BREAKING**: Import paths changed
    - Old: `from mention import FetchAlertsAPI`
    - New: `from mention import MentionClient`

- Switched HTTP client from `requests` to `httpx`
    - Better async support
    - HTTP/2 support
    - Improved performance

- Switched from manual dict handling to Pydantic models
    - Automatic validation
    - Type coercion
    - Serialization/deserialization

- Switched build system from setuptools to hatchling
    - Modern PEP 517/518 compliant
    - Faster builds

- Switched linting from pylint/black/isort to ruff
    - Single tool for linting and formatting
    - Much faster execution

- Switched documentation from Sphinx/RST to MkDocs/Markdown
    - Easier to write and maintain
    - Better default theme

- Project structure changed to `src/` layout
    - Industry standard
    - Better isolation during testing

### Removed

- **BREAKING**: All legacy API classes removed:
    - `FetchAlertsAPI` → Use `client.get_alerts()`
    - `FetchAnAlertAPI` → Use `client.get_alert()`
    - `CreateAnAlertAPI` → Use `client.create_alert()`
    - `UpdateAnAlertAPI` → Use `client.update_alert()`
    - `FetchAllMentionsAPI` → Use `client.get_mentions()`
    - `FetchAMentionAPI` → Use `client.get_mention()`
    - `CurateAMentionAPI` → Use `client.curate_mention()`
    - `MarkAllMentionsReadAPI` → Use `client.mark_all_mentions_read()`
    - `AppDataAPI` → Use `client.get_app_data()`

- Removed `requests` dependency (replaced with `httpx`)
- Removed `requests-oauthlib` dependency
- Removed `oauthlib` dependency
- Removed `Pipfile` (using `pyproject.toml` with uv)
- Removed Sphinx documentation files

### Migration Guide

#### Quick Reference

| Old (v0.x) | New (v2.0) |
|------------|------------|
| `FetchAlertsAPI(token, account_id).query()` | `client.get_alerts(account_id)` |
| `FetchAnAlertAPI(token, account_id, alert_id).query()` | `client.get_alert(account_id, alert_id)` |
| `CreateAnAlertAPI(token, account_id, name, query, langs).query()` | `client.create_alert(account_id, request)` |
| `UpdateAnAlertAPI(token, account_id, alert_id, ...).query()` | `client.update_alert(account_id, alert_id, request)` |
| `FetchAllMentionsAPI(token, account_id, alert_id).query()` | `client.get_mentions(account_id, alert_id)` |
| `FetchAMentionAPI(token, account_id, alert_id, mention_id).query()` | `client.get_mention(account_id, alert_id, mention_id)` |
| `CurateAMentionAPI(token, account_id, alert_id, mention_id, ...).query()` | `client.curate_mention(account_id, alert_id, mention_id, request)` |
| `MarkAllMentionsReadAPI(token, account_id, alert_id).query()` | `client.mark_all_mentions_read(account_id, alert_id)` |
| `AppDataAPI(token).query()` | `client.get_app_data()` |

#### Before (v0.x)

```python
import mention

# Create API instance for each call
alerts_api = mention.FetchAlertsAPI(access_token, account_id)
data = alerts_api.query()

# Access data via dict keys
for alert_data in data['alerts']:
    alert_name = alert_data['alert']['name']
    print(alert_name)

# Fetch a mention
mention_api = mention.FetchAMentionAPI(
    access_token, account_id, alert_id, mention_id
)
data = mention_api.query()
title = data['title']
description = data['description']
```

#### After (v2.0)

```python
from mention import MentionClient

# Create client once, use for all calls
with MentionClient(access_token=access_token) as client:
    # Get typed response
    response = client.get_alerts(account_id)
    
    # Access data via typed attributes (IDE autocomplete works!)
    for alert in response.alerts:
        print(alert.name)
    
    # Fetch a mention
    mention = client.get_mention(account_id, alert_id, mention_id)
    title = mention.title
    description = mention.description
```

#### Creating Alerts

**Before:**

```python
name = "My Alert"
queryd = {
    "type": "basic",
    "included_keywords": ["python", "programming"]
}
languages = ["en"]

api = mention.CreateAnAlertAPI(
    access_token, account_id, name, queryd, languages
)
data = api.query()
alert_id = data['alert']['id']
```

**After:**

```python
from mention import MentionClient, CreateAlertRequest, AlertQuery, QueryType

with MentionClient(access_token=access_token) as client:
    request = CreateAlertRequest(
        name="My Alert",
        query=AlertQuery(
            type=QueryType.BASIC,
            included_keywords=["python", "programming"],
        ),
        languages=["en"],
    )
    
    alert = client.create_alert(account_id, request)
    alert_id = alert.id
```

#### Error Handling

**Before:**

```python
try:
    api = mention.FetchAnAlertAPI(access_token, account_id, alert_id)
    data = api.query()
except Exception as e:
    print(f"Error: {e}")
```

**After:**

```python
from mention import MentionClient
from mention.exceptions import MentionNotFoundError, MentionAuthError

with MentionClient(access_token=access_token) as client:
    try:
        alert = client.get_alert(account_id, alert_id)
    except MentionAuthError:
        print("Invalid token")
    except MentionNotFoundError:
        print("Alert not found")
```

#### Environment Setup

**Before:**

```python
import os

access_token = os.environ.get('MENTION_ACCESS_TOKEN')
account_id = os.environ.get('MENTION_ACCOUNT_ID')

api = mention.FetchAlertsAPI(access_token, account_id)
```

**After:**

```python
from mention import MentionClient, MentionConfig

# Automatically loads from environment
config = MentionConfig.from_env()
client = MentionClient.from_config(config)

# Or use .env file
config = MentionConfig.from_env(env_file=".env")
```

---

## [0.2.0] - 2018-12-21

### Added

- Initial public release
- Support for Mention API v1
- Alert management
    - `FetchAlertsAPI` - List all alerts
    - `FetchAnAlertAPI` - Get single alert
    - `CreateAnAlertAPI` - Create alert
    - `UpdateAnAlertAPI` - Update alert
- Mention management
    - `FetchAllMentionsAPI` - List mentions
    - `FetchAMentionAPI` - Get single mention
    - `CurateAMentionAPI` - Update mention
    - `MarkAllMentionsReadAPI` - Mark all as read
- Application data
    - `AppDataAPI` - Get app configuration
- OAuth2 authentication via requests-oauthlib
- Sphinx documentation

---

## [0.1.0] - 2018-12-01

### Added

- Initial development release
- Basic API structure
- Alert fetching functionality

---
