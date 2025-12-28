# Installation

## Requirements

- Python 3.10 or higher
- A [Mention.com](https://mention.com) account
- An API access token

## Install from PyPI

=== "pip"

    ```bash
    pip install mention-python
    ```

=== "uv (recommended)"

    ```bash
    uv add mention-python
    ```

=== "poetry"

    ```bash
    poetry add mention-python
    ```

=== "pipenv"

    ```bash
    pipenv install mention-python
    ```

## Install from Source

```bash
# Clone the repository
git clone https://github.com/mazi76erX2/mention-python.git
cd mention-python

# Install with uv
uv sync

# Or with pip
pip install -e .
```

## Getting Your Access Token

1. Log in to your [Mention dashboard](https://web.mention.com)
2. Navigate to **Settings** → **API**
3. Create a new application (or use an existing one)
4. Copy the **Access Token**

!!! tip "Keep your token secure"
    Never commit your access token to version control. Use environment variables or a `.env` file.

## Finding Your Account ID

Your account ID can be found in:

1. The URL when logged into Mention: `https://web.mention.com/accounts/{account_id}/...`
2. The API response when fetching account details

## Verify Installation

```python
from mention import MentionClient

# Create client
client = MentionClient(access_token="your-token")

# Test connection by fetching app data
app_data = client.get_app_data()
print(f"Connected! Available sources: {len(app_data.sources)}")

# Clean up
client.close()
```

## What's Installed

The package installs the following dependencies:

| Package | Purpose |
|---------|---------|
| `httpx` | HTTP client with async support |
| `pydantic` | Data validation and serialization |
| `python-dotenv` | Environment variable management |

## Next Steps

- [Quick Start](quickstart.md) - Learn how to use the client
- [Configuration](configuration.md) - Set up environment variables
```