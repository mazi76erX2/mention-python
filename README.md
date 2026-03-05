# Mention-Python

[![PyPI version](https://img.shields.io/pypi/v/mention.svg)](https://pypi.org/project/mention)
[![CI](https://github.com/mazi76erX2/mention-python/actions/workflows/format-and-lint.yml/badge.svg)](https://github.com/mazi76erX2/mention-python/actions/workflows/format-and-lint.yml)
[![codecov](https://codecov.io/gh/mazi76erX2/mention-python/branch/main/graph/badge.svg)](https://codecov.io/gh/mazi76erX2/mention-python)
[![Documentation Status](https://readthedocs.org/projects/mention-python/badge/?version=latest)](https://mention-python.readthedocs.io/en/latest)

**A modern Python client for the Mention API.**

## Installation

```console
$ python3 -m pip install mention
```

## Quick Start

```python
from mention import MentionClient

client = MentionClient(access_token="your-token")

# Or load credentials from environment variables
# MENTION_ACCESS_TOKEN, MENTION_ACCOUNT_ID
from mention import MentionConfig
client = MentionClient.from_config(MentionConfig.from_env())
```

## Examples

**Fetch all alerts of an account**

```python
from mention import MentionClient

client = MentionClient(access_token="your-token")
response = client.get_alerts("your-account-id")

for alert in response.alerts:
    print(alert.name)
    print(alert.query.included_keywords)
```

**Fetch a single mention**

```python
mention = client.get_mention(account_id, alert_id, mention_id)
print(mention.title)
print(mention.description)
print(mention.original_url)
```

**Create an alert**

```python
from mention import MentionClient
from mention.models import AlertQuery, CreateAlertRequest

client = MentionClient(access_token="your-token")
request = CreateAlertRequest(
    name="My Brand",
    query=AlertQuery(included_keywords=["MyBrand", "my brand"]),
    languages=["en"],
    sources=["web", "twitter"],
)
alert = client.create_alert("your-account-id", request)
```

**Async usage**

```python
import asyncio
from mention import AsyncMentionClient

async def main():
    async with AsyncMentionClient(access_token="your-token") as client:
        response = await client.get_alerts("your-account-id")
        for alert in response.alerts:
            print(alert.name)

asyncio.run(main())
```

## Read More

- [Full Documentation](https://mention-python.readthedocs.io/en/latest/)
  - [Installation](https://mention-python.readthedocs.io/en/latest/pages/installation.html)
  - [Basic Usage](https://mention-python.readthedocs.io/en/latest/pages/quickstart.html)
  - [Contributing](https://mention-python.readthedocs.io/en/latest/pages/contributing.html)
```