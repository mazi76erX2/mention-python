# Working with Alerts

Alerts are the core of Mention - they define what keywords and sources to monitor.

## Listing Alerts

```python
from mention import MentionClient

with MentionClient(access_token="token") as client:
    response = client.get_alerts("account-id")

    print(f"Total alerts: {len(response.alerts)}")

    for alert in response.alerts:
        print(f"\n{alert.name}")
        print(f"  ID: {alert.id}")
        print(f"  Keywords: {alert.query.included_keywords}")
        print(f"  Sources: {alert.sources}")
        print(f"  Total mentions: {alert.mentions_count}")
        print(f"  Unread: {alert.unread_mentions_count}")
```

## Getting a Single Alert

```python
alert = client.get_alert("account-id", "alert-id")

print(f"Name: {alert.name}")
print(f"Query type: {alert.query.type}")
print(f"Included keywords: {alert.query.included_keywords}")
print(f"Excluded keywords: {alert.query.excluded_keywords}")
print(f"Languages: {alert.languages}")
print(f"Countries: {alert.countries}")
print(f"Sources: {alert.sources}")
print(f"Created: {alert.created_at}")
print(f"Last mention: {alert.last_mention_at}")
```

## Creating an Alert

### Basic Alert

```python
from mention import CreateAlertRequest, AlertQuery, QueryType

request = CreateAlertRequest(
    name="My Brand",
    query=AlertQuery(
        type=QueryType.BASIC,
        included_keywords=["my brand", "mybrand"],
    ),
)

alert = client.create_alert("account-id", request)
print(f"Created alert: {alert.id}")
```

### Advanced Alert

```python
request = CreateAlertRequest(
    name="Competitor Monitor",
    query=AlertQuery(
        type=QueryType.BASIC,
        included_keywords=["competitor1", "competitor2", "competitor3"],
        excluded_keywords=["jobs", "careers", "hiring"],
        required_keywords=["review", "opinion"],
    ),
    languages=["en", "es", "fr"],
    countries=["US", "GB", "CA"],
    sources=["web", "twitter", "news", "blog"],
    noise_detection=True,
    sentiment_analysis=True,
)

alert = client.create_alert("account-id", request)
```

### Available Sources

| Source | Description |
|--------|-------------|
| `web` | Websites |
| `twitter` | Twitter/X |
| `facebook` | Facebook |
| `instagram` | Instagram |
| `youtube` | YouTube |
| `reddit` | Reddit |
| `news` | News sites |
| `blog` | Blogs |
| `forum` | Forums |
| `review` | Review sites |

### Available Languages

Languages are specified using ISO 639-1 codes:

```python
# Common language codes
languages = [
    "en",  # English
    "es",  # Spanish
    "fr",  # French
    "de",  # German
    "pt",  # Portuguese
    "it",  # Italian
    "nl",  # Dutch
    "ja",  # Japanese
    "zh",  # Chinese
    "ko",  # Korean
]
```

### Available Countries

Countries are specified using ISO 3166-1 alpha-2 codes:

```python
# Common country codes
countries = [
    "US",  # United States
    "GB",  # United Kingdom
    "CA",  # Canada
    "AU",  # Australia
    "DE",  # Germany
    "FR",  # France
    "ES",  # Spain
    "BR",  # Brazil
    "JP",  # Japan
    "IN",  # India
]
```

## Updating an Alert

### Full Update

```python
from mention import UpdateAlertRequest, AlertQuery, QueryType

request = UpdateAlertRequest(
    name="Updated Alert Name",
    query=AlertQuery(
        type=QueryType.BASIC,
        included_keywords=["new", "keywords", "list"],
        excluded_keywords=["spam"],
    ),
    languages=["en", "de"],
    sources=["web", "twitter"],
)

updated = client.update_alert("account-id", "alert-id", request)
print(f"Updated: {updated.name}")
```

### Partial Updates

Only include fields you want to change:

```python
from mention import UpdateAlertRequest

# Just update the name
request = UpdateAlertRequest(name="New Name Only")
client.update_alert("account-id", "alert-id", request)

# Just update languages
request = UpdateAlertRequest(languages=["en", "de", "fr"])
client.update_alert("account-id", "alert-id", request)

# Just update sources
request = UpdateAlertRequest(sources=["web", "twitter", "news"])
client.update_alert("account-id", "alert-id", request)

# Disable noise detection
request = UpdateAlertRequest(noise_detection=False)
client.update_alert("account-id", "alert-id", request)
```

### Adding Keywords

```python
# Get current alert
alert = client.get_alert("account-id", "alert-id")

# Add new keywords to existing ones
new_keywords = alert.query.included_keywords + ["new keyword"]

request = UpdateAlertRequest(
    query=AlertQuery(
        type=alert.query.type,
        included_keywords=new_keywords,
        excluded_keywords=alert.query.excluded_keywords,
    ),
)

client.update_alert("account-id", "alert-id", request)
```

## Deleting an Alert

```python
success = client.delete_alert("account-id", "alert-id")
if success:
    print("Alert deleted")
```

!!! warning "Permanent Action"
    Deleting an alert also deletes all associated mentions. This action cannot be undone.

## Alert Statistics

```python
alert = client.get_alert("account-id", "alert-id")

print(f"Total mentions: {alert.mentions_count}")
print(f"Unread mentions: {alert.unread_mentions_count}")
print(f"Shares: {alert.shares_count}")
print(f"Followers: {alert.followers_count}")
print(f"Reach: {alert.reach}")
print(f"Last mention: {alert.last_mention_at}")
```

## Query Types

### Basic Query

The most common query type. Uses simple keyword matching:

```python
query = AlertQuery(
    type=QueryType.BASIC,
    included_keywords=["python", "programming"],
    excluded_keywords=["snake"],
)
```

### Advanced Query

For more complex matching requirements:

```python
query = AlertQuery(
    type=QueryType.ADVANCED,
    included_keywords=["python programming"],
    required_keywords=["tutorial", "guide"],
    excluded_keywords=["snake", "monty"],
)
```

### Boolean Query

For precise control with boolean operators:

```python
query = AlertQuery(
    type=QueryType.BOOLEAN,
    included_keywords=["(python OR django) AND (tutorial OR guide)"],
)
```

## Best Practices

### Use Specific Keywords

```python
# Too broad - will get many irrelevant mentions
query = AlertQuery(
    type=QueryType.BASIC,
    included_keywords=["apple"],
)

# Better - more specific
query = AlertQuery(
    type=QueryType.BASIC,
    included_keywords=["apple iphone", "apple macbook", "apple watch"],
    excluded_keywords=["fruit", "recipe", "cider"],
)
```

### Exclude Noise

```python
query = AlertQuery(
    type=QueryType.BASIC,
    included_keywords=["your brand"],
    excluded_keywords=[
        "jobs",
        "careers",
        "hiring",
        "salary",
        "glassdoor",
        "linkedin job",
    ],
)
```

### Monitor Competitors

```python
from mention import CreateAlertRequest, AlertQuery, QueryType

competitors = ["competitor1", "competitor2", "competitor3"]

for competitor in competitors:
    request = CreateAlertRequest(
        name=f"Competitor: {competitor}",
        query=AlertQuery(
            type=QueryType.BASIC,
            included_keywords=[competitor],
            excluded_keywords=["your brand"],  # Exclude your own mentions
        ),
        languages=["en"],
        sources=["web", "twitter", "news"],
    )
    alert = client.create_alert("account-id", request)
    print(f"Created alert for {competitor}: {alert.id}")
```

### Monitor Product Launches

```python
request = CreateAlertRequest(
    name="Product Launch Monitor",
    query=AlertQuery(
        type=QueryType.BASIC,
        included_keywords=["your product name", "product launch"],
        required_keywords=["review", "first look", "hands-on"],
    ),
    languages=["en"],
    sources=["news", "blog", "youtube"],
    sentiment_analysis=True,
)

alert = client.create_alert("account-id", request)
```

## Example: Alert Management Script

```python
from mention import MentionClient, CreateAlertRequest, AlertQuery, QueryType

def manage_alerts(client: MentionClient, account_id: str):
    """Example alert management workflow."""
    
    # List all alerts
    response = client.get_alerts(account_id)
    print(f"Current alerts: {len(response.alerts)}")
    
    # Find alerts with no recent mentions
    inactive_alerts = [
        alert for alert in response.alerts
        if alert.mentions_count == 0
    ]
    
    if inactive_alerts:
        print(f"\nInactive alerts ({len(inactive_alerts)}):")
        for alert in inactive_alerts:
            print(f"  - {alert.name} (ID: {alert.id})")
    
    # Find alerts with many unread mentions
    busy_alerts = [
        alert for alert in response.alerts
        if alert.unread_mentions_count > 100
    ]
    
    if busy_alerts:
        print(f"\nAlerts needing attention ({len(busy_alerts)}):")
        for alert in busy_alerts:
            print(f"  - {alert.name}: {alert.unread_mentions_count} unread")

if __name__ == "__main__":
    with MentionClient(access_token="token") as client:
        manage_alerts(client, "account-id")
```