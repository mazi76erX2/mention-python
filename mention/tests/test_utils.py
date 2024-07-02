"""Tests for the utils module."""

from typing import Literal

import pytest

from ..api import utils


def test_transform_date():
    """Test the transform_date function."""
    result = utils.transform_date("2018-11-25 12:00")
    assert result == "2018-11-25T12%3A00%3A00.12345%2B00%3A00"


@pytest.mark.parametrize("input_value, expected", [(True, "1"), (False, "0")])
def test_transform_boolean(input_value: bool, expected: str):
    """Test the transform_boolean function."""
    result = utils.transform_boolean(input_value)
    assert result == expected


@pytest.mark.parametrize(
    "input_tone, expected", [("negative", "-1"), ("neutral", "0"), ("positive", "1")]
)
def test_transform_tone(
    input_tone: Literal["negative", "neutral", "positive"], expected: str
):
    """Test the transform_tone function."""
    result = utils.transform_tone(input_tone)
    assert result == expected
