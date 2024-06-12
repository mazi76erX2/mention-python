from datetime import datetime

def transform_date(date_str: str) -> str:
    """Converts a datetime string into URL-encoded format.

    Args:
        date_str: The datetime string to be converted (e.g., "2024-06-12 15:30").

    Returns:
        The URL-encoded datetime string (e.g., "2024-06-12T15%3A30%3A00.000000%2B00%3A00").

    Raises:
        ValueError: If the input `date_str` is not in the expected format.
    """

    try:
        # Parse the date string (assuming default format is YYYY-MM-DD HH:MM)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Incorrect date string format. Should be YYYY-MM-DD HH:MM")

    # Convert to ISO 8601 format with microseconds and UTC offset
    formatted_date = date_obj.isoformat(timespec='microseconds')

    # Replace colons and plus signs with URL-encoded equivalents
    return formatted_date.replace(":", "%3A").replace("+", "%2B")



def transform_boolean(value: bool) -> str:
    """Converts a boolean value to its string representation ('1' or '0').

    Args:
        value: The boolean value to be converted.

    Returns:
        '1' if value is True, '0' if value is False.
    """
    return '1' if value else '0'


def transform_tone(tone: str) -> str:
    """Converts a tone keyword to its numerical representation.

    Args:
        tone: The tone keyword ("negative", "neutral", or "positive").

    Returns:
        '-1' for "negative", '0' for "neutral", '1' for "positive".
        Raises a ValueError for invalid tone values.
    """
    tone_map = {"negative": "-1", "neutral": "0", "positive": "1"}
    if tone in tone_map:
        return tone_map[tone]
    else:
        raise ValueError("Invalid tone value. Expected 'negative', 'neutral', or 'positive'.")
