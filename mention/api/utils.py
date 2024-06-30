from datetime import datetime
from typing import Literal


def transform_date(date: str) -> str:
    """Encodes date and time into URL format.

    :param date: Date and time string in the format 'YYYY-MM-DD HH:MM'.
    :return: Encoded date in the format 'YYYY-MM-DDTHH%3AMM%3A00.000%2B00%3A00'.
    """
    # Parse the input date string
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M")

    # Format the datetime object into the desired string format
    formatted_date = dt.strftime("%Y-%m-%dT%H%%3A%M%%3A00.000%%2B00%%3A00")

    return formatted_date


def transform_boolean(value: bool) -> str:
    """Transforms boolean to `1` or `0`.

    :param value: Boolean value.
    :return: Number representation of boolean `1` or `0`.
    """
    return "1" if value else "0"


def transform_tone(tone: Literal["negative", "neutral", "positive"]) -> str:
    """Transforms keyword `negative`, `neutral` or `positive` into `-1`, `0` or `1`.

    :param tone: String representation of tone.
    :return: Number representation of tone.
    """
    if tone == "negative":
        return "-1"
    elif tone == "neutral":
        return "0"
    else:
        return "1"
