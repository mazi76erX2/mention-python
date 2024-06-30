"""This module contains the `AppDataAPI` class that retrieves useful details"""

from .base import Mention


class AppDataAPI(Mention):
    """Retrieves useful details about the application."""

    def url(self) -> str:
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.
        """
        end_url = "/app/data"
        return f"{self._base_url}{end_url}"
