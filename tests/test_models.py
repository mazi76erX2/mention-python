"""Tests for Pydantic models."""

from __future__ import annotations

import pytest

from mention.models import (
    Alert,
    AlertQuery,
    Author,
    CreateAlertRequest,
    CurateMentionRequest,
    Mention,
    MentionsResponse,
    QueryType,
    Tag,
    Tone,
)


class TestAlertModels:
    """Tests for alert-related models."""

    def test_alert_query_defaults(self) -> None:
        """Test AlertQuery with defaults."""
        query = AlertQuery(included_keywords=["python"])

        assert query.type == QueryType.BASIC
        assert query.included_keywords == ["python"]
        assert query.excluded_keywords == []

    def test_alert_from_dict(self) -> None:
        """Test Alert parsing from dict."""
        data = {
            "id": "alert-123",
            "name": "Test Alert",
            "query": {
                "type": "basic",
                "included_keywords": ["python", "api"],
            },
            "languages": ["en"],
            "sources": ["web", "twitter"],
        }

        alert = Alert.model_validate(data)

        assert alert.id == "alert-123"
        assert alert.name == "Test Alert"
        assert alert.query.included_keywords == ["python", "api"]

    def test_create_alert_request_validation(self) -> None:
        """Test CreateAlertRequest validation."""
        request = CreateAlertRequest(
            name="My Alert",
            query=AlertQuery(included_keywords=["test"]),
        )

        assert request.name == "My Alert"
        assert request.languages == ["en"]  # Default

    def test_create_alert_empty_name_raises(self) -> None:
        """Test that empty name raises validation error."""
        with pytest.raises(ValueError):
            CreateAlertRequest(
                name="",
                query=AlertQuery(included_keywords=["test"]),
            )


class TestMentionModels:
    """Tests for mention-related models."""

    def test_mention_from_dict(self) -> None:
        """Test Mention parsing from dict."""
        data = {
            "id": "mention-123",
            "title": "Test Mention",
            "description": "This is a test mention",
            "original_url": "https://example.com/post",
            "source_name": "twitter",
            "tone": "positive",
            "favorite": False,
            "read": True,
        }

        mention = Mention.model_validate(data)

        assert mention.id == "mention-123"
        assert mention.title == "Test Mention"
        assert mention.tone == Tone.POSITIVE
        assert mention.read is True

    def test_mention_tone_from_int(self) -> None:
        """Test tone parsing from integer."""
        data = {"id": "m1", "tone": 1}
        mention = Mention.model_validate(data)
        assert mention.tone == Tone.POSITIVE

        data = {"id": "m2", "tone": -1}
        mention = Mention.model_validate(data)
        assert mention.tone == Tone.NEGATIVE

        data = {"id": "m3", "tone": 0}
        mention = Mention.model_validate(data)
        assert mention.tone == Tone.NEUTRAL

    def test_mention_with_author(self) -> None:
        """Test Mention with Author."""
        data = {
            "id": "mention-123",
            "author": {
                "id": "author-1",
                "name": "John Doe",
                "username": "johndoe",
                "followers_count": 1000,
            },
        }

        mention = Mention.model_validate(data)

        assert mention.author is not None
        assert mention.author.name == "John Doe"
        assert mention.author.followers_count == 1000

    def test_mention_with_tags(self) -> None:
        """Test Mention with Tags."""
        data = {
            "id": "mention-123",
            "tags": [
                {"id": "tag-1", "name": "Important", "color": "#ff0000"},
                {"id": "tag-2", "name": "Review"},
            ],
        }

        mention = Mention.model_validate(data)

        assert len(mention.tags) == 2
        assert mention.tags[0].name == "Important"
        assert mention.tags[0].color == "#ff0000"

    def test_curate_mention_request(self) -> None:
        """Test CurateMentionRequest."""
        request = CurateMentionRequest(
            favorite=True,
            tone=Tone.POSITIVE,
        )

        data = request.model_dump(exclude_none=True)

        assert data == {"favorite": True, "tone": "positive"}

    def test_mentions_response_has_more(self) -> None:
        """Test MentionsResponse pagination."""
        response = MentionsResponse(
            mentions=[],
            links={"more": "https://api.mention.net/next"},
        )

        assert response.has_more is True

        response_no_more = MentionsResponse(mentions=[])
        assert response_no_more.has_more is False


class TestTagModel:
    """Tests for Tag model."""

    def test_tag_from_dict(self) -> None:
        """Test Tag parsing."""
        data = {
            "id": "tag-123",
            "name": "Important",
            "color": "#ff5500",
        }

        tag = Tag.model_validate(data)

        assert tag.id == "tag-123"
        assert tag.name == "Important"
        assert tag.color == "#ff5500"


class TestAuthorModel:
    """Tests for Author model."""

    def test_author_from_dict(self) -> None:
        """Test Author parsing."""
        data = {
            "id": "author-123",
            "name": "Jane Doe",
            "username": "janedoe",
            "profile_url": "https://twitter.com/janedoe",
            "followers_count": 5000,
            "influence_score": 75.5,
        }

        author = Author.model_validate(data)

        assert author.id == "author-123"
        assert author.name == "Jane Doe"
        assert author.followers_count == 5000
        assert author.influence_score == 75.5
