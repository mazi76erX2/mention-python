# Configuration

## Environment Variables

Mention-python can be configured entirely through environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MENTION_ACCESS_TOKEN` | Yes | - | Your Mention API access token |
| `MENTION_ACCOUNT_ID` | No | - | Default account ID |
| `MENTION_BASE_URL` | No | `https://api.mention.net/api` | API base URL |
| `MENTION_TIMEOUT` | No | `30.0` | Request timeout in seconds |
| `MENTION_MAX_RETRIES` | No | `3` | Maximum retry attempts |
| `MENTION_RETRY_DELAY` | No | `1.0` | Base delay between retries (seconds) |

## Using .env Files

Create a `.env` file in your project root:

```bash
# .env
MENTION_ACCESS_TOKEN=your-access-token-here
MENTION_ACCOUNT_ID=your-default-account-id

# Optional overrides
MENTION_TIMEOUT=60.0
MENTION_MAX_RETRIES=5
```

Load configuration from environment:

```python
from mention import MentionClient, MentionConfig

# Automatically loads .env file
config = MentionConfig.from_env()
client = MentionClient.from_config(config)
```

!!! warning "Security"
    Never commit `.env` files to version control. Add `.env` to your `.gitignore`.

## Programmatic Configuration

### Basic Configuration

```python
from mention import MentionClient

client = MentionClient(
    access_token="your-token",
    timeout=60.0,
    max_retries=5,
)
```

### Full Configuration

```python
from mention import MentionConfig, MentionClient

config = MentionConfig(
    access_token="your-token",
    account_id="default-account-id",
    base_url="https://api.mention.net/api",
    timeout=60.0,
    max_retries=5,
    retry_delay=2.0,
)

client = MentionClient.from_config(config)
```

### Using Config with Different Accounts

```python
from mention import MentionConfig, MentionClient

# Base configuration
base_config = MentionConfig.from_env()

# Create config for a different account
other_config = base_config.with_account("other-account-id")
other_client = MentionClient.from_config(other_config)
```

## Configuration Precedence

Configuration values are resolved in this order (highest to lowest priority):

1. Explicitly passed arguments
2. Environment variables with `MENTION_` prefix
3. Environment variables without prefix (legacy support)
4. Default values

```python
# This explicit value takes precedence over environment variables
client = MentionClient(
    access_token="explicit-token",  # Used even if MENTION_ACCESS_TOKEN is set
)
```

## Retry Configuration

The client automatically retries failed requests with exponential backoff:

```python
config = MentionConfig(
    access_token="token",
    max_retries=3,      # Retry up to 3 times
    retry_delay=1.0,    # Start with 1 second delay
)

# Retry delays: 1s, 2s, 4s (exponential backoff)
```

Retries occur for:

- Connection errors
- Timeout errors
- Rate limit errors (429) - uses `Retry-After` header if provided
- Server errors (5xx)

Retries do **not** occur for:

- Authentication errors (401, 403)
- Not found errors (404)
- Validation errors (400)

## Timeout Configuration

```python
# Set timeout for all requests
client = MentionClient(
    access_token="token",
    timeout=60.0,  # 60 seconds
)
```

The timeout applies to the entire request (connect + read).

## Example: Production Configuration

```python
import os
from mention import MentionConfig, MentionClient

def get_mention_client() -> MentionClient:
    """Create a configured Mention client for production."""
    config = MentionConfig(
        access_token=os.environ["MENTION_ACCESS_TOKEN"],
        account_id=os.environ.get("MENTION_ACCOUNT_ID"),
        timeout=30.0,
        max_retries=3,
        retry_delay=1.0,
    )
    return MentionClient.from_config(config)

# Usage
with get_mention_client() as client:
    alerts = client.get_alerts("account-id")
```

## Example: Development Configuration

```python
from mention import MentionConfig, MentionClient

def get_dev_client() -> MentionClient:
    """Create a client for development with verbose settings."""
    config = MentionConfig.from_env(env_file=".env.development")
    return MentionClient.from_config(config)
```

## Example: Testing Configuration

```python
from mention import MentionConfig, MentionClient

def get_test_client() -> MentionClient:
    """Create a client for testing with minimal retries."""
    config = MentionConfig(
        access_token="test-token",
        base_url="https://api.mention.net/api",  # Or mock server URL
        timeout=5.0,
        max_retries=0,  # No retries in tests
    )
    return MentionClient.from_config(config)
```
```