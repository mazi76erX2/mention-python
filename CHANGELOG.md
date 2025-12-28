# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-01-XX

### Added

- Modern `MentionClient` class with full type hints
- Async support via `AsyncMentionClient`
- Pydantic v2 models for request/response validation
- Command-line interface (`mention` command)
- Automatic retry logic with exponential backoff
- Rate limit handling with `Retry-After` support
- `iter_mentions()` method for automatic pagination
- Configuration management via `MentionConfig` class
- Environment variable support with python-dotenv
- Comprehensive exception hierarchy:
  - `MentionError` (base)
  - `MentionAPIError`
  - `MentionAuthError`
  - `MentionNotFoundError`
  - `MentionRateLimitError`
  - `MentionConnectionError`
- Context manager support for clients
- Full test suite with pytest and respx

### Changed

- **BREAKING**: Complete API redesign - see Migration Guide below
- **BREAKING**: Minimum Python version is now 3.10
- Switched from `requests` to `httpx` for HTTP client
- Switched from manual dict handling to Pydantic models
- Switched from Sphinx/RST to MkDocs/Markdown for documentation
- Switched from setuptools to hatchling for builds
- Switched to `uv` for dependency management
- Switched to `ruff` for linting and formatting (replaces black, isort, pylint)
- Project structure changed to `src/` layout

### Removed

- **BREAKING**: Removed all legacy API classes:
  - `FetchAMentionAPI` → Use `client.get_mention()`
  - `FetchAllMentionsAPI` → Use `client.get_mentions()`
  - `FetchAnAlertAPI` → Use `client.get_alert()`
  - `FetchAlertsAPI` → Use `client.get_alerts()`
  - `CreateAnAlertAPI` → Use `client.create_alert()`
  - `UpdateAnAlertAPI` → Use `client.update_alert()`
  - `CurateAMentionAPI` → Use `client.curate_mention()`
  - `MarkAllMentionsReadAPI` → Use `client.mark_all_mentions_read()`
  - `AppDataAPI` → Use `client.get_app_data()`
- Removed `requests` and `requests-oauthlib` dependencies
- Removed Pipfile (using pyproject.toml with uv)

## [0.2.0] - 2018-12-21

### Added

- Initial public release
- Support for Mention API v1
- Alert management (create, read, update, delete)
- Mention fetching and curation

---

## Migration Guide: v0.x → v2.0

### Before (v0.x)

```python
import mention

# Fetch alerts
alerts_api = mention.FetchAlertsAPI(access_token, account_id)
data = alerts_api.query()
alerts = data['alerts']

# Fetch a mention
mention_api = mention.FetchAMentionAPI(access_token, account_id, alert_id, mention_id)
data = mention_api.query()
title = data['title']

# Create an alert
create_api = mention.CreateAnAlertAPI(
    access_token, account_id, name, queryd, languages
)
data = create_api.query()