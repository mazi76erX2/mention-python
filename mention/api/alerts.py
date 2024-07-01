"""API calls related to alerts."""
import json
from typing import Any, Dict, List, Optional

from requests.exceptions import HTTPError
from requests_oauthlib import OAuth2Session

from .base import Mention


class CreateAnAlertAPI(Mention):
    """Retrieve details about a single alert.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param name: Alert name.
    :param queryd: `queryd` is a dictionary that can be of two different
        types: basic or advanced.


    :Example:

    >>> queryd = {
            'type'='basic',
            'included_keywords' : ["NASA", "Arianespace", "SpaceX",
            "Pockocmoc"],
            'required_keywords' : ["mars"],
            'excluded_keywords' : ["nose", "fil d'ariane"],
            'monitored_website' : ["domain":"www.nasa.gov",
             "block_self":true]
        }

    OR

    >>> queryd = {
            'type' : 'advanced',
            'query_string' : '(NASA AND Discovery) OR
            (Arianespace AND Ariane)'
        }

    :param languages: A list of language codes. eg: ['en'].
    :param countries: A list of country codes. eg: ['US', 'RU', 'XX'].
    :param sources: A list of sources from which mentions should be
        tracked. Must be either web, twitter, blogs, forums, news,
         facebook, images or videos
    :param blocked_sites: A list of blocked sites from which you
     don't want mentions to be tracked.
    :param noise_detection: Enables noise detection.
    :param reviews_pages: List of reviews pages.
    """

    def __init__(
        self,
        oauth: OAuth2Session,
        account_id: str,
        name: str,
        query: Dict[str, Any],
        languages: List[str],
        countries: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        blocked_sites: Optional[List[str]] = None,
        noise_detection: Optional[bool] = None,
        reviews_pages: Optional[List[str]] = None,
    ):
        super().__init__(oauth)
        self.account_id = account_id
        self.name = name
        self.query_data = query
        self.languages = languages
        self.countries = countries
        self.sources = sources
        self.blocked_sites = blocked_sites
        self.noise_detection = noise_detection
        self.reviews_pages = reviews_pages

    def params(self) -> Dict[str, str]:
        """Parameters used in the url of the API call."""
        return {"account_id": self.account_id}

    def url(self) -> str:
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.
        """
        return f"{self._base_url}/accounts/{self.account_id}/alerts"

    def data(self) -> Dict[str, Any]:
        """Parameters passed to the API containing the details to create a new alert."""
        data = {
            "name": self.name,
            "query": self.query_data,
            "languages": self.languages,
        }
        if self.countries:
            data["countries"] = self.countries
        if self.sources:
            data["sources"] = self.sources
        if self.blocked_sites:
            data["blocked_sites"] = self.blocked_sites
        if self.noise_detection is not None:
            data["noise_detection"] = str(self.noise_detection).lower()
        if self.reviews_pages:
            data["reviews_pages"] = self.reviews_pages
        return data

    def query(self) -> Dict[str, Any]:
        """The request that creates a new alert and returns the response as JSON."""
        try:
            response = self.oauth.post(self.url(), json=self.data())
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return {}


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


class FetchAlertsAPI(Mention):
    """Fetch a list of all alerts for a given account."""

    def __init__(self, oauth: OAuth2Session, account_id: str):
        super().__init__(oauth)
        self.account_id = account_id

    def params(self) -> Dict[str, str]:
        """Parameters used in the url of the API call."""
        return {"account_id": self.account_id}

    def url(self) -> str:
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.
        """
        return f"{self._base_url}/accounts/{self.account_id}/alerts"

    def query(self) -> Dict[str, Any]:
        """Fetch and return the list of alerts as JSON."""
        try:
            response = self.oauth.get(self.url())
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return {}


class UpdateAnAlertAPI(Mention):
    """Modifies an existing alert, usually to update the criteria and to improve the search's efficiency.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param name: Alert name.
    :param `queryd`: Queryd is a dictionary that can be of two different
        types: basic or advanced.


    :Example:

    >>> queryd = {
            'type'='basic',
            'included_keywords' : ["NASA", "Arianespace", "SpaceX",
            "Pockocmoc"],
            'required_keywords' : ["mars"],
            'excluded_keywords' : ["nose", "fil d'ariane"],
            'monitored_website' : ["domain":"www.nasa.gov",
             "block_self":true]
        }

    OR

    >>> queryd = {
            'type' : 'advanced',
            'query_string' : '(NASA AND Discovery) OR
            (Arianespace AND Ariane)'
        }

    :param languages: A list of language codes. eg: ['en'].
    :param countries: A list of country codes. eg: ['US', 'RU', 'XX'].
    :param sources: A list of sources from which mentions should be
        tracked. Must be either web, twitter, blogs, forums, news,
         facebook, images or videos
    :param blocked_sites: A list of blocked sites from which you
     don't want mentions to be tracked.
    :param noise_detection: Enables noise detection.
    :param reviews_pages: List of reviews pages.
    """

    def __init__(
        self,
        oauth: OAuth2Session,
        account_id: str,
        alert_id: str,
        name: str,
        query: Dict[str, Any],
        languages: List[str],
        countries: Optional[List[str]] = None,
        sources: Optional[List[str]] = None,
        blocked_sites: Optional[List[str]] = None,
        noise_detection: Optional[bool] = None,
        reviews_pages: Optional[List[str]] = None
    ):
        super().__init__(oauth)
        self.account_id = account_id
        self.alert_id = alert_id
        self.name = name
        self.query_data = query
        self.languages = languages
        self.countries = countries
        self.sources = sources
        self.blocked_sites = blocked_sites
        self.noise_detection = noise_detection
        self.reviews_pages = reviews_pages

    def params(self) -> Dict[str, str]:
        """Parameters used in the url of the API call."""
        return {
            "account_id": self.account_id,
            "alert_id": self.alert_id
        }

    def data(self) -> Dict[str, Any]:
        """Parameters passed to the API containing the details to update an alert."""
        data = {
            "name": self.name,
            "query": self.query_data,
            "languages": self.languages
        }
        if self.countries:
            data["countries"] = self.countries
        if self.sources:
            data["sources"] = self.sources
        if self.blocked_sites:
            data["blocked_sites"] = self.blocked_sites
        if self.noise_detection is not None:
            data["noise_detection"] = self.noise_detection
        if self.reviews_pages:
            data["reviews_pages"] = self.reviews_pages
        return data

    def url(self) -> str:
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.
        """
        return f"{self._base_url}/accounts/{self.account_id}/alerts/{self.alert_id}"

    def query(self) -> Dict[str, Any]:
        """Update the alert and return the response as JSON."""
        try:
            response = self.oauth.put(self.url(), json=self.data())
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return {}
