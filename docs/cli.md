# CLI Reference

Mention-python includes a command-line interface for common operations without writing code.

## Installation

The CLI is automatically installed with the package:

```bash
pip install mention-python
```

Verify installation:

```bash
mention --version
```

## Configuration

### Environment Variables

Set your credentials before using the CLI:

```bash
export MENTION_ACCESS_TOKEN="your-access-token"
export MENTION_ACCOUNT_ID="your-account-id"  # Optional default
```

### Using .env File

Create a `.env` file in your working directory:

```bash
# .env
MENTION_ACCESS_TOKEN=your-access-token
MENTION_ACCOUNT_ID=your-account-id
```

The CLI automatically loads `.env` files.

## Global Options

```bash
mention [OPTIONS] COMMAND [ARGS]

Options:
  --version                Show version and exit
  --help                   Show help message and exit
  --account-id, -a TEXT    Account ID (overrides env var)
  --output, -o [json]      Output format (default: json)
```

## Commands Overview

| Command | Description |
|---------|-------------|
| `mention app-data` | Get application data |
| `mention alerts list` | List all alerts |
| `mention alerts get` | Get a single alert |
| `mention alerts create` | Create a new alert |
| `mention alerts delete` | Delete an alert |
| `mention mentions list` | List mentions |
| `mention mentions get` | Get a single mention |
| `mention mentions stream` | Stream all mentions |
| `mention mentions curate` | Update a mention |
| `mention mentions mark-read` | Mark all mentions as read |

---

## App Data

Get application configuration data including available sources, languages, and countries.

```bash
mention app-data
```

**Example output:**

```json
{
  "sources": [
    {"id": "web", "name": "Web", "type": "web"},
    {"id": "twitter", "name": "Twitter", "type": "social"}
  ],
  "languages": [
    {"code": "en", "name": "English"},
    {"code": "es", "name": "Spanish"}
  ]
}
```

---

## Alerts

### List Alerts

List all alerts for an account.

```bash
mention alerts list
mention alerts list --account-id=abc123
```

**Example output:**

```json
{
  "alerts": [
    {
      "id": "alert-123",
      "name": "Brand Monitor",
      "mentions_count": 1500,
      "unread_mentions_count": 45
    },
    {
      "id": "alert-456",
      "name": "Competitor Watch",
      "mentions_count": 800,
      "unread_mentions_count": 12
    }
  ]
}
```

### Get Alert

Get details for a single alert.

```bash
mention alerts get --alert-id=xyz789
mention alerts get -i xyz789  # Short form
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID |

**Example output:**

```json
{
  "id": "alert-123",
  "name": "Brand Monitor",
  "query": {
    "type": "basic",
    "included_keywords": ["my brand", "mybrand"],
    "excluded_keywords": ["jobs", "careers"]
  },
  "languages": ["en", "es"],
  "sources": ["web", "twitter"],
  "mentions_count": 1500,
  "unread_mentions_count": 45
}
```

### Create Alert

Create a new alert.

```bash
mention alerts create \
    --name="Brand Monitor" \
    --keywords="my brand,mybrand,my-brand" \
    --languages="en,es" \
    --sources="web,twitter,news"
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--name` | `-n` | Yes | Alert name |
| `--keywords` | `-k` | Yes | Comma-separated keywords to monitor |
| `--excluded` | `-e` | No | Comma-separated keywords to exclude |
| `--languages` | `-l` | No | Comma-separated language codes (default: en) |
| `--sources` | `-s` | No | Comma-separated sources (default: web) |

**Examples:**

```bash
# Basic alert
mention alerts create \
    --name="Python News" \
    --keywords="python,programming"

# Alert with exclusions
mention alerts create \
    --name="Company Monitor" \
    --keywords="acme corp,acme inc" \
    --excluded="jobs,careers,hiring,salary"

# Multi-language alert
mention alerts create \
    --name="Global Brand" \
    --keywords="brand name" \
    --languages="en,es,fr,de" \
    --sources="web,twitter,news,blog"
```

**Example output:**

```json
{
  "id": "new-alert-123",
  "name": "Brand Monitor",
  "query": {
    "type": "basic",
    "included_keywords": ["my brand", "mybrand", "my-brand"]
  }
}
```

### Delete Alert

Delete an alert.

```bash
mention alerts delete --alert-id=xyz789
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID to delete |

!!! warning "Permanent Action"
    Deleting an alert also deletes all associated mentions. This cannot be undone.

---

## Mentions

### List Mentions

List mentions for an alert.

```bash
mention mentions list --alert-id=xyz789
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID |
| `--limit` | `-l` | No | Max mentions to return (default: 100, max: 1000) |
| `--source` | `-s` | No | Filter by source (web, twitter, etc.) |
| `--tone` | `-t` | No | Filter by tone (positive, negative, neutral) |
| `--read` | | No | Filter by read status (true/false) |
| `--favorite` | | No | Filter by favorite status (true/false) |

**Examples:**

```bash
# Basic listing
mention mentions list --alert-id=xyz789

# Limit results
mention mentions list --alert-id=xyz789 --limit=50

# Filter by source
mention mentions list --alert-id=xyz789 --source=twitter

# Filter by sentiment
mention mentions list --alert-id=xyz789 --tone=negative

# Unread mentions only
mention mentions list --alert-id=xyz789 --read=false

# Favorited mentions
mention mentions list --alert-id=xyz789 --favorite=true

# Combined filters
mention mentions list \
    --alert-id=xyz789 \
    --limit=100 \
    --source=twitter \
    --tone=positive \
    --read=false
```

**Example output:**

```json
{
  "mentions": [
    {
      "id": "mention-001",
      "title": "Great product announcement",
      "source_name": "Twitter",
      "tone": "positive",
      "original_url": "https://twitter.com/user/status/123"
    },
    {
      "id": "mention-002",
      "title": "Customer feedback",
      "source_name": "Web",
      "tone": "neutral",
      "original_url": "https://example.com/blog/post"
    }
  ],
  "has_more": true
}
```

### Get Mention

Get details for a single mention.

```bash
mention mentions get --alert-id=xyz789 --mention-id=m123
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID |
| `--mention-id` | `-m` | Yes | Mention ID |

**Example output:**

```json
{
  "id": "mention-001",
  "title": "Great product announcement",
  "description": "Full text of the mention...",
  "source_name": "Twitter",
  "source_type": "twitter",
  "tone": "positive",
  "original_url": "https://twitter.com/user/status/123",
  "published_at": "2025-01-15T10:30:00Z",
  "reach": 15000,
  "favorite": false,
  "read": true,
  "author": {
    "name": "John Doe",
    "username": "johndoe",
    "followers_count": 5000
  }
}
```

### Stream Mentions

Stream all mentions with automatic pagination. Useful for exporting or bulk processing.

```bash
mention mentions stream --alert-id=xyz789
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID |
| `--source` | `-s` | No | Filter by source |
| `--limit` | `-l` | No | Mentions per page (default: 100) |
| `--max` | | No | Maximum total mentions to stream |

**Examples:**

```bash
# Stream all mentions
mention mentions stream --alert-id=xyz789

# Limit total mentions
mention mentions stream --alert-id=xyz789 --max=1000

# Filter while streaming
mention mentions stream --alert-id=xyz789 --source=twitter

# Stream to file
mention mentions stream --alert-id=xyz789 > mentions.json
```

**Output:**

Each mention is output as a separate JSON object:

```json
{"id": "m001", "title": "First mention", ...}
{"id": "m002", "title": "Second mention", ...}
{"id": "m003", "title": "Third mention", ...}
```

### Curate Mention

Update a mention's properties.

```bash
mention mentions curate \
    --alert-id=xyz789 \
    --mention-id=m123 \
    --favorite=true \
    --read=true
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID |
| `--mention-id` | `-m` | Yes | Mention ID |
| `--favorite` | | No | Set favorite status (true/false) |
| `--read` | | No | Set read status (true/false) |
| `--trashed` | | No | Set trashed status (true/false) |
| `--tone` | `-t` | No | Set tone (positive/negative/neutral) |

**Examples:**

```bash
# Mark as favorite
mention mentions curate \
    --alert-id=xyz789 \
    --mention-id=m123 \
    --favorite=true

# Mark as read
mention mentions curate \
    --alert-id=xyz789 \
    --mention-id=m123 \
    --read=true

# Update sentiment
mention mentions curate \
    --alert-id=xyz789 \
    --mention-id=m123 \
    --tone=positive

# Move to trash
mention mentions curate \
    --alert-id=xyz789 \
    --mention-id=m123 \
    --trashed=true

# Multiple updates
mention mentions curate \
    --alert-id=xyz789 \
    --mention-id=m123 \
    --favorite=true \
    --read=true \
    --tone=positive
```

### Mark All Read

Mark all mentions for an alert as read.

```bash
mention mentions mark-read --alert-id=xyz789
```

**Options:**

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--alert-id` | `-i` | Yes | Alert ID |

---

## Output Processing

### JSON Output

All commands output JSON by default, making it easy to process with tools like `jq`.

### Count Results

```bash
# Count alerts
mention alerts list | jq '.alerts | length'

# Count mentions
mention mentions list --alert-id=xyz789 | jq '.mentions | length'
```

### Extract Fields

```bash
# Get alert names
mention alerts list | jq -r '.alerts[].name'

# Get mention URLs
mention mentions list --alert-id=xyz789 | jq -r '.mentions[].original_url'

# Get mention titles and sources
mention mentions list --alert-id=xyz789 | \
    jq -r '.mentions[] | "\(.title) - \(.source_name)"'
```

### Filter with jq

```bash
# Get alerts with more than 100 unread mentions
mention alerts list | \
    jq '.alerts[] | select(.unread_mentions_count > 100)'

# Get positive mentions only
mention mentions list --alert-id=xyz789 | \
    jq '.mentions[] | select(.tone == "positive")'
```

### Export to CSV

```bash
# Export mentions to CSV
mention mentions stream --alert-id=xyz789 | \
    jq -r '[.title, .source_name, .original_url] | @csv' > mentions.csv

# With headers
echo "title,source,url" > mentions.csv
mention mentions stream --alert-id=xyz789 | \
    jq -r '[.title, .source_name, .original_url] | @csv' >> mentions.csv
```

### Export to TSV

```bash
mention mentions list --alert-id=xyz789 | \
    jq -r '.mentions[] | [.title, .source_name, .original_url] | @tsv'
```

---

## Shell Scripts

### Daily Report

```bash
#!/bin/bash
# daily_report.sh - Generate a daily mention report

ACCOUNT_ID="${MENTION_ACCOUNT_ID}"
OUTPUT_DIR="./reports"
DATE=$(date +%Y-%m-%d)

mkdir -p "$OUTPUT_DIR"

echo "=== Mention Report: $DATE ===" | tee "$OUTPUT_DIR/report_$DATE.txt"
echo "" | tee -a "$OUTPUT_DIR/report_$DATE.txt"

# Get all alerts
ALERTS=$(mention alerts list)
ALERT_COUNT=$(echo "$ALERTS" | jq '.alerts | length')

echo "Total alerts: $ALERT_COUNT" | tee -a "$OUTPUT_DIR/report_$DATE.txt"
echo "" | tee -a "$OUTPUT_DIR/report_$DATE.txt"

# Process each alert
echo "$ALERTS" | jq -r '.alerts[] | "\(.id) \(.name)"' | while read -r ALERT_ID ALERT_NAME; do
    MENTIONS=$(mention mentions list --alert-id="$ALERT_ID" --limit=1)
    UNREAD=$(echo "$MENTIONS" | jq '.total // 0')
    
    echo "Alert: $ALERT_NAME" | tee -a "$OUTPUT_DIR/report_$DATE.txt"
    echo "  Unread: $UNREAD" | tee -a "$OUTPUT_DIR/report_$DATE.txt"
    echo "" | tee -a "$OUTPUT_DIR/report_$DATE.txt"
done

echo "Report saved to $OUTPUT_DIR/report_$DATE.txt"
```

### Export All Mentions

```bash
#!/bin/bash
# export_mentions.sh - Export all mentions to JSON files

ACCOUNT_ID="${MENTION_ACCOUNT_ID}"
OUTPUT_DIR="./exports"
DATE=$(date +%Y-%m-%d)

mkdir -p "$OUTPUT_DIR"

# Get all alerts
mention alerts list | jq -r '.alerts[].id' | while read -r ALERT_ID; do
    echo "Exporting mentions for alert: $ALERT_ID"
    
    mention mentions stream --alert-id="$ALERT_ID" \
        > "$OUTPUT_DIR/${ALERT_ID}_${DATE}.json"
    
    COUNT=$(wc -l < "$OUTPUT_DIR/${ALERT_ID}_${DATE}.json")
    echo "  Exported $COUNT mentions"
done

echo "Export complete. Files saved to $OUTPUT_DIR/"
```

### Monitor Negative Mentions

```bash
#!/bin/bash
# monitor_negative.sh - Alert on negative mentions

ALERT_ID="$1"

if [ -z "$ALERT_ID" ]; then
    echo "Usage: $0 <alert-id>"
    exit 1
fi

# Get negative unread mentions
NEGATIVE=$(mention mentions list \
    --alert-id="$ALERT_ID" \
    --tone=negative \
    --read=false \
    --limit=10)

COUNT=$(echo "$NEGATIVE" | jq '.mentions | length')

if [ "$COUNT" -gt 0 ]; then
    echo "⚠️  Found $COUNT negative mentions!"
    echo ""
    echo "$NEGATIVE" | jq -r '.mentions[] | "- \(.title)\n  \(.original_url)\n"'
else
    echo "✓ No new negative mentions"
fi
```

### Batch Mark as Read

```bash
#!/bin/bash
# mark_all_read.sh - Mark all mentions as read for all alerts

echo "Marking all mentions as read..."

mention alerts list | jq -r '.alerts[].id' | while read -r ALERT_ID; do
    echo "Processing alert: $ALERT_ID"
    mention mentions mark-read --alert-id="$ALERT_ID"
done

echo "Done!"
```

---

## Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| `Configuration error: Missing MENTION_ACCESS_TOKEN` | Access token not set | Set `MENTION_ACCESS_TOKEN` env var |
| `Error: --account-id is required` | No account ID provided | Set `MENTION_ACCOUNT_ID` or use `--account-id` |
| `Authentication failed` | Invalid or expired token | Check/regenerate your access token |
| `Resource not found` | Invalid ID | Verify the alert/mention ID exists |
| `Rate limit exceeded` | Too many requests | Wait and retry |

---

## Troubleshooting

### Check Configuration

```bash
# Verify environment variables are set
echo $MENTION_ACCESS_TOKEN
echo $MENTION_ACCOUNT_ID

# Test connection
mention app-data
```

### Debug Mode

```bash
# View full error details
mention alerts list 2>&1 | head -50
```

### Common Issues

**"Missing MENTION_ACCESS_TOKEN"**

```bash
# Set the environment variable
export MENTION_ACCESS_TOKEN="your-token"

# Or create a .env file
echo "MENTION_ACCESS_TOKEN=your-token" > .env
```

**"--account-id is required"**

```bash
# Set default account ID
export MENTION_ACCOUNT_ID="your-account-id"

# Or pass it explicitly
mention alerts list --account-id=your-account-id
```

**"Authentication failed"**

1. Verify your token is correct
2. Check if token has expired
3. Regenerate token in Mention dashboard

**"Rate limit exceeded"**

1. Wait before retrying
2. Reduce request frequency
3. Use `--limit` to fetch fewer items per request
