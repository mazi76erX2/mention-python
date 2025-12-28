# Quick Start

This guide will get you up and running with mention-python in minutes.

## Setup

First, set up your credentials:

=== "Environment Variables"

    ```bash
    export MENTION_ACCESS_TOKEN="your-access-token"
    export MENTION_ACCOUNT_ID="your-account-id"
    ```

=== ".env File"

    ```bash
    # .env
    MENTION_ACCESS_TOKEN=your-access-token
    MENTION_ACCOUNT_ID=your-account-id
    ```

Then create a client:

```python
from mention import MentionClient, MentionConfig

# Option 1: Direct initialization
client = MentionClient(access_token="your-token")

# Option 2: From environment variables
config = MentionConfig.from_env()
client = MentionClient.from_config(config)

# Option 3: Context manager (recommended)
with MentionClient(access_token="your-token") as client:
    # Your code here
    pass  # Client automatically closes
```

## Working with Alerts

### List All Alerts

```python
with MentionClient(access_token="token") as client:
    response = client.get_alerts(account_id="your-account-id")

    for alert in response.alerts:
        print(f"{alert.name}")
        print(f"  ID: {alert.id}")
        print(f"  Mentions: {alert.mentions_count}")
        print(f"  Unread: {alert.unread_mentions_count}")
```

### Get a Specific Alert

```python
alert = client.get_alert(
    account_id="your-account-id",
    alert_id="your-alert-id",
)

print(f"Alert: {alert.name}")
print(f"Keywords: {alert.query.included_keywords}")
print(f"Languages: {alert.languages}")
print(f"Sources: {alert.sources}")
```

### Create an Alert

```python
from mention import CreateAlertRequest, AlertQuery, QueryType

request = CreateAlertRequest(
    name="Python News",
    query=AlertQuery(
        type=QueryType.BASIC,
        included_keywords=["python", "programming", "django"],
        excluded_keywords=["snake"],
    ),
    languages=["en", "es"],
    sources=["web", "twitter", "news"],
)

alert = client.create_alert("your-account-id", request)
print(f"Created alert: {alert.id}")
```

## Working with Mentions

### Fetch Mentions

```python
mentions = client.get_mentions(
    account_id="your-account-id",
    alert_id="your-alert-id",
    limit=50,
)

for mention in mentions.mentions:
    print(f"{mention.title}")
    print(f"  Source: {mention.source_name}")
    print(f"  Tone: {mention.tone}")
    print(f"  URL: {mention.original_url}")
    print()
```

### Filter Mentions

```python
# Get only Twitter mentions with positive sentiment
mentions = client.get_mentions(
    account_id="your-account-id",
    alert_id="your-alert-id",
    limit=100,
    source="twitter",
    tone="positive",
    read=False,  # Only unread
)
```

### Iterate Over All Mentions

```python
# Automatically handles pagination
for mention in client.iter_mentions("account-id", "alert-id"):
    print(mention.title)

    # Stop after condition met
    if some_condition:
        break
```

### Update a Mention

```python
from mention import CurateMentionRequest, Tone

request = CurateMentionRequest(
    favorite=True,
    read=True,
    tone=Tone.POSITIVE,
)

updated = client.curate_mention(
    account_id="your-account-id",
    alert_id="your-alert-id",
    mention_id="mention-id",
    request=request,
)

print(f"Mention marked as favorite: {updated.favorite}")
```

## Using the CLI

The package includes a command-line interface:

```bash
# List alerts
mention alerts list

# Get mentions
mention mentions list --alert-id=abc123 --limit=50

# Stream all mentions
mention mentions stream --alert-id=abc123 --max=500
```

See [CLI Reference](cli.md) for all commands.

## Error Handling

```python
from mention.exceptions import (
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
    MentionAPIError,
)

try:
    alert = client.get_alert("account-id", "invalid-id")
except MentionAuthError:
    print("Check your access token")
except MentionNotFoundError:
    print("Alert not found")
except MentionRateLimitError as e:
    print(f"Rate limited. Retry in {e.retry_after} seconds")
except MentionAPIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

## Next Steps

- [Configuration](configuration.md) - Learn about all configuration options
- [Alerts Guide](guides/alerts.md) - Deep dive into alert management
- [Mentions Guide](guides/mentions.md) - Advanced mention handling
- [Async Usage](guides/async.md) - Using the async client
```