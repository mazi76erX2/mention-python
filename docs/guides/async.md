# Error Handling

Mention-python provides a comprehensive exception hierarchy for handling API errors gracefully.

## Exception Hierarchy

```
MentionError (base)
├── MentionAPIError
│   ├── MentionAuthError (401, 403)
│   ├── MentionNotFoundError (404)
│   └── MentionRateLimitError (429)
├── MentionConnectionError
└── MentionValidationError
```

## Importing Exceptions

```python
from mention.exceptions import (
    MentionError,
    MentionAPIError,
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
    MentionConnectionError,
    MentionValidationError,
)
```

## Basic Error Handling

```python
from mention import MentionClient
from mention.exceptions import MentionError

with MentionClient(access_token="token") as client:
    try:
        alert = client.get_alert("account-id", "alert-id")
    except MentionError as e:
        print(f"Error: {e.message}")
```

## Specific Exceptions

### MentionAuthError (401, 403)

Raised when authentication fails or access is denied.

```python
from mention.exceptions import MentionAuthError

try:
    client = MentionClient(access_token="invalid-token")
    client.get_alerts("account-id")
except MentionAuthError as e:
    print(f"Authentication failed: {e.message}")
    print(f"Status code: {e.status_code}")
```

**Common causes:**

- Invalid access token
- Expired access token
- Insufficient permissions for the requested resource
- Wrong account ID

**How to fix:**

```python
# Check your token is valid
import os

token = os.environ.get("MENTION_ACCESS_TOKEN")
if not token:
    raise ValueError("MENTION_ACCESS_TOKEN environment variable not set")

# Ensure token has correct permissions
# Regenerate token in Mention dashboard if expired
```

### MentionNotFoundError (404)

Raised when a requested resource doesn't exist.

```python
from mention.exceptions import MentionNotFoundError

try:
    alert = client.get_alert("account-id", "nonexistent-alert-id")
except MentionNotFoundError as e:
    print(f"Not found: {e.message}")
    print(f"Status code: {e.status_code}")
```

**Common causes:**

- Invalid alert ID
- Invalid mention ID
- Invalid account ID
- Resource was deleted

**How to handle:**

```python
def get_alert_safely(client, account_id, alert_id):
    """Get an alert, returning None if not found."""
    try:
        return client.get_alert(account_id, alert_id)
    except MentionNotFoundError:
        return None

# Usage
alert = get_alert_safely(client, "account-id", "alert-id")
if alert is None:
    print("Alert not found")
else:
    print(f"Found alert: {alert.name}")
```

### MentionRateLimitError (429)

Raised when you've exceeded the API rate limit.

```python
from mention.exceptions import MentionRateLimitError
import time

try:
    for i in range(10000):
        client.get_mentions("account-id", "alert-id")
except MentionRateLimitError as e:
    print(f"Rate limited: {e.message}")
    print(f"Status code: {e.status_code}")
    
    if e.retry_after:
        print(f"Retry after: {e.retry_after} seconds")
        time.sleep(e.retry_after)
```

**Handling rate limits:**

```python
import time
from mention.exceptions import MentionRateLimitError

def fetch_with_rate_limit_handling(client, account_id, alert_id, max_retries=3):
    """Fetch mentions with automatic rate limit handling."""
    
    for attempt in range(max_retries):
        try:
            return client.get_mentions(account_id, alert_id)
        except MentionRateLimitError as e:
            if attempt == max_retries - 1:
                raise  # Give up after max retries
            
            wait_time = e.retry_after or 60
            print(f"Rate limited. Waiting {wait_time}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
    
    return None
```

### MentionConnectionError

Raised for network-related errors.

```python
from mention.exceptions import MentionConnectionError

try:
    client.get_alerts("account-id")
except MentionConnectionError as e:
    print(f"Connection failed: {e.message}")
```

**Common causes:**

- Network is unavailable
- DNS resolution failed
- Connection timeout
- SSL/TLS errors
- Firewall blocking requests

**How to handle:**

```python
import time
from mention.exceptions import MentionConnectionError

def fetch_with_retry(client, account_id, max_retries=3, delay=2):
    """Fetch alerts with connection retry logic."""
    
    for attempt in range(max_retries):
        try:
            return client.get_alerts(account_id)
        except MentionConnectionError as e:
            if attempt == max_retries - 1:
                raise
            
            wait = delay * (2 ** attempt)  # Exponential backoff
            print(f"Connection error: {e.message}")
            print(f"Retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(wait)
    
    return None
```

### MentionValidationError

Raised for request validation errors (client-side).

```python
from mention.exceptions import MentionValidationError
from mention import CreateAlertRequest, AlertQuery

try:
    # This will raise a validation error
    request = CreateAlertRequest(
        name="",  # Empty name is invalid
        query=AlertQuery(included_keywords=[]),
    )
except MentionValidationError as e:
    print(f"Validation error: {e.message}")
```

### MentionAPIError (Generic)

Base class for all API errors. Catches any API error.

```python
from mention.exceptions import MentionAPIError

try:
    client.get_alerts("account-id")
except MentionAPIError as e:
    print(f"API error: {e.message}")
    print(f"Status code: {e.status_code}")
    print(f"Response body: {e.response_body}")
```

## Exception Attributes

### MentionError (Base)

```python
exception.message    # str: Error message
exception.details    # dict: Additional error details
```

### MentionAPIError

```python
exception.message        # str: Error message
exception.status_code    # int: HTTP status code
exception.response_body  # dict | str | None: Raw API response
```

### MentionRateLimitError

```python
exception.message        # str: Error message
exception.status_code    # int: HTTP status code (429)
exception.response_body  # dict | str | None: Raw API response
exception.retry_after    # int | None: Seconds to wait before retrying
```

## Complete Error Handling Example

```python
import time
from mention import MentionClient
from mention.exceptions import (
    MentionError,
    MentionAPIError,
    MentionAuthError,
    MentionNotFoundError,
    MentionRateLimitError,
    MentionConnectionError,
)

def fetch_alert_safely(
    client: MentionClient,
    account_id: str,
    alert_id: str,
    max_retries: int = 3,
):
    """Fetch an alert with comprehensive error handling."""
    
    for attempt in range(max_retries):
        try:
            return client.get_alert(account_id, alert_id)
        
        except MentionAuthError as e:
            # Don't retry authentication errors
            print(f"Authentication failed: {e.message}")
            print("Please check your access token.")
            raise
        
        except MentionNotFoundError:
            # Don't retry not found errors
            print(f"Alert '{alert_id}' not found")
            return None
        
        except MentionRateLimitError as e:
            wait_time = e.retry_after or 60
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            continue
        
        except MentionConnectionError as e:
            print(f"Connection error: {e.message}")
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise
        
        except MentionAPIError as e:
            print(f"API error {e.status_code}: {e.message}")
            if e.status_code >= 500:
                # Retry server errors
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"Server error. Retrying in {wait}s...")
                    time.sleep(wait)
                    continue
            raise
    
    return None


# Usage
with MentionClient(access_token="token") as client:
    alert = fetch_alert_safely(client, "account-id", "alert-id")
    if alert:
        print(f"Found alert: {alert.name}")
```

## Automatic Retries

The client has built-in retry logic for transient errors.

### Default Retry Behavior

```python
client = MentionClient(
    access_token="token",
    max_retries=3,      # Default: 3 retries
    retry_delay=1.0,    # Default: 1 second initial delay
)
```

### Retry Schedule

With default settings, retries use exponential backoff:

| Attempt | Delay |
|---------|-------|
| 1 | 1 second |
| 2 | 2 seconds |
| 3 | 4 seconds |

### What Gets Retried

| Error Type | Retried? |
|------------|----------|
| Connection timeout | ✅ Yes |
| Network errors | ✅ Yes |
| Rate limits (429) | ✅ Yes (uses Retry-After) |
| Server errors (5xx) | ✅ Yes |
| Auth errors (401, 403) | ❌ No |
| Not found (404) | ❌ No |
| Bad request (400) | ❌ No |

### Customizing Retries

```python
# More aggressive retries
client = MentionClient(
    access_token="token",
    max_retries=5,
    retry_delay=2.0,
)

# No retries (for testing)
client = MentionClient(
    access_token="token",
    max_retries=0,
)

# Longer initial delay
client = MentionClient(
    access_token="token",
    max_retries=3,
    retry_delay=5.0,
)
```

## Logging Errors

### Basic Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    alert = client.get_alert("account-id", "alert-id")
except MentionAPIError as e:
    logger.error(f"API error: {e.status_code} - {e.message}")
    raise
```

### Detailed Logging

```python
import logging
from mention.exceptions import MentionAPIError

logger = logging.getLogger(__name__)

try:
    alert = client.get_alert("account-id", "alert-id")
except MentionAPIError as e:
    logger.error(
        "API request failed",
        extra={
            "status_code": e.status_code,
            "message": e.message,
            "response_body": e.response_body,
            "account_id": "account-id",
            "alert_id": "alert-id",
        }
    )
    raise
```

### Structured Logging (JSON)

```python
import json
import logging
from mention.exceptions import MentionAPIError

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record),
        }
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "response_body"):
            log_data["response_body"] = record.response_body
        return json.dumps(log_data)

# Setup
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage
try:
    alert = client.get_alert("account-id", "alert-id")
except MentionAPIError as e:
    logger.error(
        f"API error: {e.message}",
        extra={"status_code": e.status_code, "response_body": e.response_body},
    )
```

## Error Handling Patterns

### Fail Fast

Stop immediately on any error:

```python
from mention.exceptions import MentionError

try:
    alerts = client.get_alerts("account-id")
    for alert in alerts.alerts:
        mentions = client.get_mentions("account-id", alert.id)
        process(mentions)
except MentionError as e:
    print(f"Error: {e.message}")
    sys.exit(1)
```

### Fail Safe

Continue processing despite errors:

```python
from mention.exceptions import MentionError

alerts = client.get_alerts("account-id")
errors = []

for alert in alerts.alerts:
    try:
        mentions = client.get_mentions("account-id", alert.id)
        process(mentions)
    except MentionError as e:
        errors.append({"alert_id": alert.id, "error": str(e)})
        continue

if errors:
    print(f"Completed with {len(errors)} errors:")
    for error in errors:
        print(f"  - Alert {error['alert_id']}: {error['error']}")
```

### Circuit Breaker

Stop after too many consecutive errors:

```python
from mention.exceptions import MentionError

class CircuitBreaker:
    def __init__(self, max_failures=5):
        self.max_failures = max_failures
        self.failures = 0
    
    def record_success(self):
        self.failures = 0
    
    def record_failure(self):
        self.failures += 1
    
    @property
    def is_open(self):
        return self.failures >= self.max_failures

# Usage
breaker = CircuitBreaker(max_failures=5)

for alert in alerts.alerts:
    if breaker.is_open:
        print("Too many failures. Stopping.")
        break
    
    try:
        mentions = client.get_mentions("account-id", alert.id)
        process(mentions)
        breaker.record_success()
    except MentionError as e:
        print(f"Error: {e.message}")
        breaker.record_failure()
```

## Testing Error Handling

```python
import pytest
from unittest.mock import patch, MagicMock
from mention import MentionClient
from mention.exceptions import MentionNotFoundError, MentionAuthError

def test_handles_not_found():
    """Test that not found errors are handled gracefully."""
    client = MentionClient(access_token="test-token")
    
    with patch.object(client, "_get") as mock_get:
        mock_get.side_effect = MentionNotFoundError(
            "Alert not found",
            status_code=404,
        )
        
        result = get_alert_safely(client, "account", "invalid-id")
        assert result is None

def test_raises_auth_error():
    """Test that auth errors are not caught."""
    client = MentionClient(access_token="invalid-token")
    
    with patch.object(client, "_get") as mock_get:
        mock_get.side_effect = MentionAuthError(
            "Unauthorized",
            status_code=401,
        )
        
        with pytest.raises(MentionAuthError):
            get_alert_safely(client, "account", "alert-id")
```