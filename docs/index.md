# Mention-Python

A modern, typed Python client for the [Mention API](https://dev.mention.com/).

![PyPI version](https://img.shields.io/pypi/v/mention-python.svg)
![Python versions](https://img.shields.io/pypi/pyversions/mention-python.svg)
![License](https://img.shields.io/github/license/mazi76erX2/mention-python.svg)

## Features

- **Modern Python** - Built for Python 3.10+ with full type hints
- **Pydantic Models** - Validated request/response models
- **Sync & Async** - Both synchronous and asynchronous clients
- **CLI Included** - Command-line interface for common operations
- **Auto-Retry** - Built-in retry logic with exponential backoff
- **Pagination** - Easy iteration over paginated results

## Quick Example
```python
from mention import MentionClient

with MentionClient(access_token="your-token") as client:
    # Get all alerts
    alerts = client.get_alerts("account-id")

    for alert in alerts.alerts:
        print(f"{alert.name}: {alert.mentions_count} mentions")

        # Get mentions for each alert
        mentions = client.get_mentions("account-id", alert.id, limit=10)
        for mention in mentions.mentions:
            print(f"  - {mention.title}")
```

## Installation

### pip
```bash
pip install mention-python
```

### uv
```bash
uv add mention-python
```

### poetry
```bash
poetry add mention-python
```

## What's New in v2.0

> **Warning: Breaking Changes**  
> Version 2.0 is a complete rewrite. See the Changelog for migration instructions.

Version 2.0 is a complete rewrite using modern Python practices:

| Before (v0.x) | After (v2.0) |
|---------------|--------------|
| `mention.FetchAlertsAPI(token, id).query()` | `client.get_alerts(id)` |
| Dict responses | Typed Pydantic models |
| No async support | Full async client |
| No CLI | Complete CLI tool |

### Why the Rewrite?

The original library was built in 2018. The Python ecosystem has evolved significantly since then:

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

This rewrite brings mention-python up to 2025 standards while maintaining the same core functionality.

## Quick Links

* 📥 **Installation** - Get started with mention-python
* 🚀 **Quick Start** - Learn the basics in 5 minutes
* ⚙️ **Configuration** - Environment variables and options
* 🔌 **API Reference** - Complete API documentation

## Basic Usage

### Sync Client
```python
from mention import MentionClient

client = MentionClient(access_token="your-token")

# Get alerts
alerts = client.get_alerts("account-id")

# Get mentions
mentions = client.get_mentions("account-id", "alert-id", limit=100)

# Clean up
client.close()
```

### Async Client
```python
import asyncio
from mention import AsyncMentionClient

async def main():
    async with AsyncMentionClient(access_token="your-token") as client:
        alerts = await client.get_alerts("account-id")
        print(f"Found {len(alerts.alerts)} alerts")

asyncio.run(main())
```

### Command Line
```bash
# Set credentials
export MENTION_ACCESS_TOKEN="your-token"

# List alerts
mention alerts list --account-id=abc123

# Get mentions
mention mentions list --account-id=abc123 --alert-id=xyz789 --limit=50
```

## License

MIT License - see LICENSE for details.