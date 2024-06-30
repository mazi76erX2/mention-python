"""API calls related to alerts."""
from requests_oauthlib import OAuth2Session

from .base import Mention


class FetchAnAlertAPI(Mention):
    """Retrieve details about a single alert."""

    def __init__(self, oauth: OAuth2Session, account_id: str, alert_id: str):
        super().__init__(oauth)
        self.account_id = account_id
        self.alert_id = alert_id

    def params(self) -> dict[str, str]:
        """Parameters used in the url of the API call and for authentication."""
        return {
            "account_id": self.account_id,
            "alert_id": self.alert_id,
        }

    def url(self) -> str:
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.
        """
        end_url = f"/accounts/{self.account_id}/alerts/{self.alert_id}"
        return f"{self._base_url}{end_url}"
