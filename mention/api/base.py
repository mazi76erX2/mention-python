"""The base class for all of the Mention API calls."""
from abc import ABC, abstractmethod
from typing import Any

from oauthlib.oauth2 import BackendApplicationClient
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session


class Mention(ABC):
    """The base class for all of the Mention API calls."""

    def __init__(self, oauth: OAuth2Session):
        self.oauth = oauth

    @property
    def _base_url(self) -> str:
        """Base url."""
        return "https://api.mention.net/api"

    @abstractmethod
    def params(self) -> dict[str, str]:
        """Parameters used in the url of the API call."""
        return {}

    @abstractmethod
    def url(self) -> str:
        """The concatenation of the `base_url` and parameters that make up the
        resultant url.
        """
        return ""

    def query(self) -> dict[str, Any]:
        """The request that returns a JSON file of the API call given a url."""
        try:
            response = self.oauth.get(self.url())
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return {}


def create_oauth_session(access_token: str) -> OAuth2Session:
    """Create an OAuth2Session with the given access token."""
    client = BackendApplicationClient(client_id=access_token)
    return OAuth2Session(client=client)
