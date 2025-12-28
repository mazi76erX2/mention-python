# Working with Mentions

Mentions are individual pieces of content that match your alert keywords.

## Fetching Mentions

### Basic Fetch

```python
from mention import MentionClient

with MentionClient(access_token="token") as client:
    response = client.get_mentions(
        account_id="account-id",
        alert_id="alert-id",
        limit=100,
    )

    print(f"Found {len(response.mentions)} mentions")

    for mention in response.mentions:
        print(f"{mention.title}")
        print(f"  Source: {mention.source_name}")
        print(f"  URL: {mention.original_url}")
        print()
```

### Mention Properties

```python
mention = client.get_mention("account-id", "alert-id", "mention-id")

# Basic information
print(f"ID: {mention.id}")
print(f"Title: {mention.title}")
print(f"Description: {mention.description}")
print(f"Short description: {mention.description_short}")

# Source information
print(f"Source name: {mention.source_name}")
print(f"Source type: {mention.source_type}")
print(f"Original URL: {mention.original_url}")

# Metadata
print(f"Language: {mention.language}")
print(f"Country: {mention.country}")
print(f"Published at: {mention.published_at}")
print(f"Created at: {mention.created_at}")

# Sentiment and reach
print(f"Tone: {mention.tone}")
print(f"Reach: {mention.reach}")

# Status flags
print(f"Favorite: {mention.favorite}")
print(f"Read: {mention.read}")
print(f"Trashed: {mention.trashed}")

# Media
print(f"Image URL: {mention.image_url}")
print(f"Video URL: {mention.video_url}")
```

## Filtering Mentions

### By Source

```python
# Twitter mentions only
mentions = client.get_mentions(
    "account-id", "alert-id",
    source="twitter",
)

# Web mentions only
mentions = client.get_mentions(
    "account-id", "alert-id",
    source="web",
)

# News mentions only
mentions = client.get_mentions(
    "account-id", "alert-id",
    source="news",
)
```

### By Sentiment

```python
from mention import Tone

# Positive mentions
mentions = client.get_mentions(
    "account-id", "alert-id",
    tone="positive",
)

# Negative mentions
mentions = client.get_mentions(
    "account-id", "alert-id",
    tone="negative",
)

# Neutral mentions
mentions = client.get_mentions(
    "account-id", "alert-id",
    tone="neutral",
)
```

### By Read Status

```python
# Unread mentions only
mentions = client.get_mentions(
    "account-id", "alert-id",
    read=False,
)

# Already read mentions
mentions = client.get_mentions(
    "account-id", "alert-id",
    read=True,
)
```

### By Favorite Status

```python
# Favorited mentions only
mentions = client.get_mentions(
    "account-id", "alert-id",
    favorite=True,
)

# Non-favorited mentions
mentions = client.get_mentions(
    "account-id", "alert-id",
    favorite=False,
)
```

### By Date Range

```python
from datetime import datetime, timedelta

# Mentions from the last 7 days
week_ago = datetime.now() - timedelta(days=7)

mentions = client.get_mentions(
    "account-id", "alert-id",
    not_before_date=week_ago,
)

# Mentions from a specific date range
mentions = client.get_mentions(
    "account-id", "alert-id",
    before_date=datetime(2025, 1, 31),
    not_before_date=datetime(2025, 1, 1),
)

# Using string format
mentions = client.get_mentions(
    "account-id", "alert-id",
    before_date="2025-01-31",
    not_before_date="2025-01-01",
)
```

### Combined Filters

```python
# Unread negative Twitter mentions from the last week
mentions = client.get_mentions(
    "account-id", "alert-id",
    limit=100,
    source="twitter",
    tone="negative",
    read=False,
    not_before_date=datetime.now() - timedelta(days=7),
)
```

## Pagination

### Understanding Limits

- Maximum `limit` per request is 1000
- Default `limit` is 100
- Use pagination to fetch more mentions

### Manual Pagination

```python
response = client.get_mentions("account-id", "alert-id", limit=100)

all_mentions = []

while True:
    all_mentions.extend(response.mentions)
    print(f"Fetched {len(all_mentions)} mentions so far...")

    if not response.has_more:
        break

    # Get next page using cursor
    response = client.get_mentions(
        "account-id", "alert-id",
        limit=100,
        cursor=response.links.more,
    )

print(f"Total mentions: {len(all_mentions)}")
```

### Automatic Pagination (Recommended)

```python
# Iterate over ALL mentions automatically
count = 0
for mention in client.iter_mentions("account-id", "alert-id"):
    print(f"{mention.title}")
    count += 1

print(f"Total: {count} mentions")
```

### Pagination with Filters

```python
# Iterate over filtered mentions
for mention in client.iter_mentions(
    "account-id", "alert-id",
    source="twitter",
    tone="positive",
):
    process_positive_tweet(mention)
```

### Limiting Total Results

```python
# Stop after 500 mentions
count = 0
max_mentions = 500

for mention in client.iter_mentions("account-id", "alert-id"):
    process(mention)
    count += 1
    if count >= max_mentions:
        break
```

## Getting a Single Mention

```python
mention = client.get_mention(
    account_id="account-id",
    alert_id="alert-id",
    mention_id="mention-id",
)

print(f"Title: {mention.title}")
print(f"Description: {mention.description}")
print(f"URL: {mention.original_url}")
```

## Working with Authors

```python
mention = client.get_mention("account-id", "alert-id", "mention-id")

if mention.author:
    author = mention.author
    print(f"Name: {author.name}")
    print(f"Username: {author.username}")
    print(f"Profile URL: {author.profile_url}")
    print(f"Avatar URL: {author.avatar_url}")
    print(f"Followers: {author.followers_count}")
    print(f"Following: {author.following_count}")
    print(f"Influence score: {author.influence_score}")
else:
    print("No author information available")
```

## Working with Tags

```python
mention = client.get_mention("account-id", "alert-id", "mention-id")

if mention.tags:
    print("Tags:")
    for tag in mention.tags:
        print(f"  - {tag.name} (ID: {tag.id}, Color: {tag.color})")
else:
    print("No tags")
```

## Working with Engagement

```python
mention = client.get_mention("account-id", "alert-id", "mention-id")

if mention.engagement:
    print("Engagement:")
    print(f"  Likes: {mention.engagement.get('likes', 0)}")
    print(f"  Shares: {mention.engagement.get('shares', 0)}")
    print(f"  Comments: {mention.engagement.get('comments', 0)}")
    print(f"  Retweets: {mention.engagement.get('retweets', 0)}")
else:
    print("No engagement data")
```

## Curating Mentions

### Mark as Favorite

```python
from mention import CurateMentionRequest

request = CurateMentionRequest(favorite=True)
updated = client.curate_mention("account-id", "alert-id", "mention-id", request)
print(f"Favorited: {updated.favorite}")
```

### Mark as Read

```python
request = CurateMentionRequest(read=True)
client.curate_mention("account-id", "alert-id", "mention-id", request)
```

### Update Sentiment

```python
from mention import CurateMentionRequest, Tone

# Mark as positive
request = CurateMentionRequest(tone=Tone.POSITIVE)
client.curate_mention("account-id", "alert-id", "mention-id", request)

# Mark as negative
request = CurateMentionRequest(tone=Tone.NEGATIVE)
client.curate_mention("account-id", "alert-id", "mention-id", request)

# Mark as neutral
request = CurateMentionRequest(tone=Tone.NEUTRAL)
client.curate_mention("account-id", "alert-id", "mention-id", request)
```

### Move to Trash

```python
request = CurateMentionRequest(trashed=True)
client.curate_mention("account-id", "alert-id", "mention-id", request)
```

### Restore from Trash

```python
request = CurateMentionRequest(trashed=False)
client.curate_mention("account-id", "alert-id", "mention-id", request)
```

### Multiple Updates at Once

```python
request = CurateMentionRequest(
    favorite=True,
    read=True,
    tone=Tone.POSITIVE,
)
client.curate_mention("account-id", "alert-id", "mention-id", request)
```

### Add Tags

```python
# Tags must already exist - use tag IDs
request = CurateMentionRequest(tags=["tag-id-1", "tag-id-2"])
client.curate_mention("account-id", "alert-id", "mention-id", request)
```

## Mark All as Read

```python
client.mark_all_mentions_read("account-id", "alert-id")
print("All mentions marked as read")
```

## Example: Process Unread Mentions

```python
from mention import MentionClient, CurateMentionRequest, Tone

def process_unread_mentions(client: MentionClient, account_id: str, alert_id: str):
    """Process all unread mentions and categorize them."""
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for mention in client.iter_mentions(
        account_id, alert_id,
        read=False,
        limit=100,
    ):
        print(f"Processing: {mention.title[:50]}...")
        
        # Count by sentiment
        if mention.tone == Tone.POSITIVE:
            positive_count += 1
        elif mention.tone == Tone.NEGATIVE:
            negative_count += 1
            # Favorite negative mentions for review
            request = CurateMentionRequest(favorite=True, read=True)
            client.curate_mention(account_id, alert_id, mention.id, request)
        else:
            neutral_count += 1
            # Just mark neutral mentions as read
            request = CurateMentionRequest(read=True)
            client.curate_mention(account_id, alert_id, mention.id, request)
    
    print(f"\nSummary:")
    print(f"  Positive: {positive_count}")
    print(f"  Negative: {negative_count}")
    print(f"  Neutral: {neutral_count}")

if __name__ == "__main__":
    with MentionClient(access_token="token") as client:
        process_unread_mentions(client, "account-id", "alert-id")
```

## Example: Export Mentions to CSV

```python
import csv
from mention import MentionClient

def export_mentions_to_csv(
    client: MentionClient,
    account_id: str,
    alert_id: str,
    filename: str,
    max_mentions: int = 1000,
):
    """Export mentions to a CSV file."""
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Header row
        writer.writerow([
            "ID",
            "Title",
            "Source",
            "URL",
            "Tone",
            "Author",
            "Published At",
            "Reach",
        ])
        
        count = 0
        for mention in client.iter_mentions(account_id, alert_id):
            writer.writerow([
                mention.id,
                mention.title or "",
                mention.source_name or "",
                mention.original_url or "",
                mention.tone.value if mention.tone else "",
                mention.author.name if mention.author else "",
                mention.published_at.isoformat() if mention.published_at else "",
                mention.reach or 0,
            ])
            
            count += 1
            if count >= max_mentions:
                break
    
    print(f"Exported {count} mentions to {filename}")

if __name__ == "__main__":
    with MentionClient(access_token="token") as client:
        export_mentions_to_csv(
            client,
            "account-id",
            "alert-id",
            "mentions_export.csv",
            max_mentions=5000,
        )
```

## Example: Find Influential Mentions

```python
from mention import MentionClient

def find_influential_mentions(
    client: MentionClient,
    account_id: str,
    alert_id: str,
    min_followers: int = 10000,
):
    """Find mentions from influential authors."""
    
    influential = []
    
    for mention in client.iter_mentions(account_id, alert_id, limit=100):
        if mention.author and mention.author.followers_count:
            if mention.author.followers_count >= min_followers:
                influential.append(mention)
    
    # Sort by follower count
    influential.sort(
        key=lambda m: m.author.followers_count if m.author else 0,
        reverse=True,
    )
    
    print(f"Found {len(influential)} influential mentions:")
    for mention in influential[:10]:  # Top 10
        print(f"\n{mention.title[:60]}...")
        print(f"  Author: {mention.author.name}")
        print(f"  Followers: {mention.author.followers_count:,}")
        print(f"  URL: {mention.original_url}")

if __name__ == "__main__":
    with MentionClient(access_token="token") as client:
        find_influential_mentions(client, "account-id", "alert-id")
```

## Example: Sentiment Analysis Report

```python
from collections import defaultdict
from mention import MentionClient, Tone

def sentiment_report(
    client: MentionClient,
    account_id: str,
    alert_id: str,
):
    """Generate a sentiment analysis report."""
    
    by_tone = defaultdict(list)
    by_source = defaultdict(lambda: defaultdict(int))
    
    for mention in client.iter_mentions(account_id, alert_id, limit=100):
        tone = mention.tone or Tone.NEUTRAL
        source = mention.source_name or "unknown"
        
        by_tone[tone].append(mention)
        by_source[source][tone] += 1
    
    # Overall sentiment
    total = sum(len(mentions) for mentions in by_tone.values())
    print(f"Total mentions analyzed: {total}\n")
    
    print("Sentiment breakdown:")
    for tone in [Tone.POSITIVE, Tone.NEUTRAL, Tone.NEGATIVE]:
        count = len(by_tone[tone])
        percentage = (count / total * 100) if total > 0 else 0
        print(f"  {tone.value.capitalize()}: {count} ({percentage:.1f}%)")
    
    print("\nSentiment by source:")
    for source, tones in sorted(by_source.items()):
        total_source = sum(tones.values())
        print(f"\n  {source} ({total_source} mentions):")
        for tone in [Tone.POSITIVE, Tone.NEUTRAL, Tone.NEGATIVE]:
            count = tones[tone]
            if count > 0:
                print(f"    {tone.value}: {count}")

if __name__ == "__main__":
    with MentionClient(access_token="token") as client:
        sentiment_report(client, "account-id", "alert-id")
```