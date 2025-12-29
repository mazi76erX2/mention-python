"""
Command-line interface for the Mention API client.

Usage:
    mention alerts list --account-id=<id>
    mention alerts get --account-id=<id> --alert-id=<id>
    mention mentions list --account-id=<id> --alert-id=<id>
    mention mentions get --account-id=<id> --alert-id=<id> --mention-id=<id>
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import NoReturn

from mention.client import MentionClient
from mention.config import MentionConfig
from mention.exceptions import MentionError
from mention.models import (
    AlertQuery,
    CreateAlertRequest,
    CurateMentionRequest,
    QueryType,
)


def get_client() -> MentionClient:
    """
    Create a MentionClient from environment variables.

    Required environment variables:
        - MENTION_ACCESS_TOKEN: OAuth2 access token

    Optional environment variables:
        - MENTION_ACCOUNT_ID: Default account ID
        - MENTION_BASE_URL: API base URL
        - MENTION_TIMEOUT: Request timeout
    """
    try:
        config = MentionConfig.from_env()
        return MentionClient.from_config(config)
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("\nRequired environment variables:", file=sys.stderr)
        print("  MENTION_ACCESS_TOKEN - Your Mention API access token", file=sys.stderr)
        print("\nOptional environment variables:", file=sys.stderr)
        print("  MENTION_ACCOUNT_ID  - Default account ID", file=sys.stderr)
        print("  MENTION_BASE_URL    - API base URL", file=sys.stderr)
        sys.exit(1)


def output_json(data: object) -> None:
    """Output data as formatted JSON."""
    if hasattr(data, "model_dump"):
        data = data.model_dump()  # type: ignore[union-attr]
    print(json.dumps(data, indent=2, default=str))


def get_account_id(args: argparse.Namespace) -> str:
    """Get account ID from args or environment."""
    if args.account_id:
        return args.account_id

    try:
        config = MentionConfig.from_env()
        if config.account_id:
            return config.account_id
    except ValueError:
        pass

    print("Error: --account-id is required", file=sys.stderr)
    sys.exit(1)


# --- Command handlers ---


def cmd_app_data(_args: argparse.Namespace) -> None:
    """Get application data."""
    with get_client() as client:
        data = client.get_app_data()
        output_json(data)


def cmd_alerts_list(args: argparse.Namespace) -> None:
    """List all alerts."""
    account_id = get_account_id(args)
    with get_client() as client:
        response = client.get_alerts(account_id)
        output_json(response)


def cmd_alerts_get(args: argparse.Namespace) -> None:
    """Get a single alert."""
    account_id = get_account_id(args)
    with get_client() as client:
        alert = client.get_alert(account_id, args.alert_id)
        output_json(alert)


def cmd_alerts_create(args: argparse.Namespace) -> None:
    """Create a new alert."""
    account_id = get_account_id(args)

    keywords = args.keywords.split(",") if args.keywords else []
    excluded = args.excluded.split(",") if args.excluded else []
    languages = args.languages.split(",") if args.languages else ["en"]
    sources = args.sources.split(",") if args.sources else ["web"]

    request = CreateAlertRequest(
        name=args.name,
        query=AlertQuery(
            type=QueryType.BASIC,
            included_keywords=keywords,
            excluded_keywords=excluded,
        ),
        languages=languages,
        sources=sources,
    )

    with get_client() as client:
        alert = client.create_alert(account_id, request)
        output_json(alert)
        print(f"\n✓ Alert created: {alert.id}", file=sys.stderr)


def cmd_alerts_delete(args: argparse.Namespace) -> None:
    """Delete an alert."""
    account_id = get_account_id(args)
    with get_client() as client:
        client.delete_alert(account_id, args.alert_id)
        print(f"✓ Alert {args.alert_id} deleted", file=sys.stderr)


def cmd_mentions_list(args: argparse.Namespace) -> None:
    """List mentions for an alert."""
    account_id = get_account_id(args)

    kwargs = {
        "limit": args.limit,
    }
    if args.source:
        kwargs["source"] = args.source
    if args.tone:
        kwargs["tone"] = args.tone
    if args.read is not None:
        kwargs["read"] = args.read
    if args.favorite is not None:
        kwargs["favorite"] = args.favorite

    with get_client() as client:
        response = client.get_mentions(account_id, args.alert_id, **kwargs)
        output_json(response)
        print(f"\n{len(response.mentions)} mentions returned", file=sys.stderr)


def cmd_mentions_get(args: argparse.Namespace) -> None:
    """Get a single mention."""
    account_id = get_account_id(args)
    with get_client() as client:
        mention = client.get_mention(account_id, args.alert_id, args.mention_id)
        output_json(mention)


def cmd_mentions_curate(args: argparse.Namespace) -> None:
    """Curate (update) a mention."""
    account_id = get_account_id(args)

    request = CurateMentionRequest(
        favorite=args.favorite,
        read=args.read,
        trashed=args.trashed,
        tone=args.tone,
    )

    with get_client() as client:
        mention = client.curate_mention(account_id, args.alert_id, args.mention_id, request)
        output_json(mention)
        print(f"\n✓ Mention {args.mention_id} updated", file=sys.stderr)


def cmd_mentions_mark_read(args: argparse.Namespace) -> None:
    """Mark all mentions as read."""
    account_id = get_account_id(args)
    with get_client() as client:
        client.mark_all_mentions_read(account_id, args.alert_id)
        print(f"✓ All mentions for alert {args.alert_id} marked as read", file=sys.stderr)


def cmd_mentions_stream(args: argparse.Namespace) -> None:
    """Stream all mentions with pagination."""
    account_id = get_account_id(args)

    kwargs = {}
    if args.source:
        kwargs["source"] = args.source
    if args.limit:
        kwargs["limit"] = args.limit

    count = 0
    with get_client() as client:
        for mention in client.iter_mentions(account_id, args.alert_id, **kwargs):
            output_json(mention)
            count += 1
            if args.max and count >= args.max:
                break

    print(f"\n{count} mentions streamed", file=sys.stderr)


# --- Argument parser ---


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="mention",
        description="Mention API command-line client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  MENTION_ACCESS_TOKEN  OAuth2 access token (required)
  MENTION_ACCOUNT_ID    Default account ID
  MENTION_BASE_URL      API base URL

Examples:
  mention app-data
  mention alerts list --account-id=abc123
  mention alerts create --account-id=abc123 --name="My Alert" --keywords="python,api"
  mention mentions list --account-id=abc123 --alert-id=xyz789 --limit=50
  mention mentions stream --account-id=abc123 --alert-id=xyz789 --max=1000
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    parser.add_argument(
        "--account-id",
        "-a",
        help="Account ID (or set MENTION_ACCOUNT_ID)",
    )

    parser.add_argument(
        "--output",
        "-o",
        choices=["json", "table"],
        default="json",
        help="Output format (default: json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- app-data command ---
    app_data_parser = subparsers.add_parser(
        "app-data",
        help="Get application data (sources, languages, etc.)",
    )
    app_data_parser.set_defaults(func=cmd_app_data)

    # --- alerts commands ---
    alerts_parser = subparsers.add_parser("alerts", help="Manage alerts")
    alerts_subparsers = alerts_parser.add_subparsers(dest="alerts_command", required=True)

    # alerts list
    alerts_list = alerts_subparsers.add_parser("list", help="List all alerts")
    alerts_list.set_defaults(func=cmd_alerts_list)

    # alerts get
    alerts_get = alerts_subparsers.add_parser("get", help="Get a single alert")
    alerts_get.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    alerts_get.set_defaults(func=cmd_alerts_get)

    # alerts create
    alerts_create = alerts_subparsers.add_parser("create", help="Create a new alert")
    alerts_create.add_argument("--name", "-n", required=True, help="Alert name")
    alerts_create.add_argument(
        "--keywords",
        "-k",
        required=True,
        help="Comma-separated keywords to monitor",
    )
    alerts_create.add_argument(
        "--excluded",
        "-e",
        help="Comma-separated keywords to exclude",
    )
    alerts_create.add_argument(
        "--languages",
        "-l",
        default="en",
        help="Comma-separated language codes (default: en)",
    )
    alerts_create.add_argument(
        "--sources",
        "-s",
        default="web",
        help="Comma-separated sources (default: web)",
    )
    alerts_create.set_defaults(func=cmd_alerts_create)

    # alerts delete
    alerts_delete = alerts_subparsers.add_parser("delete", help="Delete an alert")
    alerts_delete.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    alerts_delete.set_defaults(func=cmd_alerts_delete)

    # --- mentions commands ---
    mentions_parser = subparsers.add_parser("mentions", help="Manage mentions")
    mentions_subparsers = mentions_parser.add_subparsers(dest="mentions_command", required=True)

    # mentions list
    mentions_list = mentions_subparsers.add_parser("list", help="List mentions")
    mentions_list.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    mentions_list.add_argument(
        "--limit",
        "-l",
        type=int,
        default=100,
        help="Maximum mentions to return (default: 100, max: 1000)",
    )
    mentions_list.add_argument("--source", "-s", help="Filter by source")
    mentions_list.add_argument(
        "--tone",
        "-t",
        choices=["positive", "negative", "neutral"],
        help="Filter by tone",
    )
    mentions_list.add_argument(
        "--read",
        type=lambda x: x.lower() == "true",
        help="Filter by read status (true/false)",
    )
    mentions_list.add_argument(
        "--favorite",
        type=lambda x: x.lower() == "true",
        help="Filter by favorite status (true/false)",
    )
    mentions_list.set_defaults(func=cmd_mentions_list)

    # mentions get
    mentions_get = mentions_subparsers.add_parser("get", help="Get a single mention")
    mentions_get.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    mentions_get.add_argument("--mention-id", "-m", required=True, help="Mention ID")
    mentions_get.set_defaults(func=cmd_mentions_get)

    # mentions curate
    mentions_curate = mentions_subparsers.add_parser("curate", help="Update a mention")
    mentions_curate.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    mentions_curate.add_argument("--mention-id", "-m", required=True, help="Mention ID")
    mentions_curate.add_argument(
        "--favorite",
        type=lambda x: x.lower() == "true",
        help="Set favorite status",
    )
    mentions_curate.add_argument(
        "--read",
        type=lambda x: x.lower() == "true",
        help="Set read status",
    )
    mentions_curate.add_argument(
        "--trashed",
        type=lambda x: x.lower() == "true",
        help="Set trashed status",
    )
    mentions_curate.add_argument(
        "--tone",
        choices=["positive", "negative", "neutral"],
        help="Set tone",
    )
    mentions_curate.set_defaults(func=cmd_mentions_curate)

    # mentions mark-read
    mentions_mark_read = mentions_subparsers.add_parser(
        "mark-read",
        help="Mark all mentions as read",
    )
    mentions_mark_read.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    mentions_mark_read.set_defaults(func=cmd_mentions_mark_read)

    # mentions stream
    mentions_stream = mentions_subparsers.add_parser(
        "stream",
        help="Stream all mentions with pagination",
    )
    mentions_stream.add_argument("--alert-id", "-i", required=True, help="Alert ID")
    mentions_stream.add_argument("--source", "-s", help="Filter by source")
    mentions_stream.add_argument(
        "--limit",
        "-l",
        type=int,
        default=100,
        help="Mentions per page (default: 100)",
    )
    mentions_stream.add_argument(
        "--max",
        type=int,
        help="Maximum total mentions to stream",
    )
    mentions_stream.set_defaults(func=cmd_mentions_stream)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> NoReturn:
    """Main entry point for the CLI."""
    args = parse_args(argv)

    try:
        args.func(args)
        sys.exit(0)
    except MentionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
