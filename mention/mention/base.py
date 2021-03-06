import requests
from requests_oauth2 import OAuth2BearerToken
import json
from abc import ABCMeta, abstractmethod
from requests.exceptions import HTTPError
from mention import utils


class Mention(object):
    """The base class for all of the Mention API calls.


    :param access_token: Mention API `access_token`
    :type access_token: str

    """
    __metaclass__ = ABCMeta

    def __init__(self, access_token):
        self.access_token = access_token

    @property
    def _base_url(self):
        """Base url.

        :return: the base url
        :rtype: str
        """
        return "https://api.mention.net/api"

    @abstractmethod
    def params(self):
        """Parameters used in the url of the API call.
        """
        return

    @abstractmethod
    def url(self):
        """The concatenation of the `base_url` and parameters that make up the
        resultant url.
        """
        return

    @abstractmethod
    def query(self):
        """The request that returns a JSON file of the API call given a url.
        """
        return


class AppDataAPI(Mention):
    """Retrieves useful details about the application.

    :param access_token: Mention API `access_token`
    :type access_token: str

    """

    def __init__(self, access_token):
        self.access_token = access_token
        super(AppDataAPI, self).__init__(access_token)

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = "/app/data"

        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.get(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass

        data = response.json()

        return data


class FetchAnAlertAPI(Mention):
    """Retrieve details about a single alert.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param alert_id: ID of the alert.
    :type access_token: str
    :type account_id: str
    :type alert_id: str
    """

    def __init__(self, access_token, account_id, alert_id):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id
        super(FetchAnAlertAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id
        return params

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts/"
            "{alert_id}".format(**self.params))

        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.get(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()

        return data


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


    :type access_token: str
    :type account_id: str
    :type queryd: dict
    :type languages: list
    :type countries: list
    :type sources: list
    :type blocked_sites: list
    :type noise_detection: boolean
    :type reviews_pages: list
    """

    def __init__(self,
                 access_token,
                 account_id,
                 name,
                 queryd,
                 languages,
                 countries=None,
                 sources=None,
                 blocked_sites=None,
                 noise_detection=None,
                 reviews_pages=None):
        self.access_token = access_token
        self.account_id = account_id
        self.name = name
        self.queryd = queryd
        self.languages = languages
        self.countries = countries
        self.sources = sources
        self.blocked_sites = blocked_sites

        if noise_detection is not None:
            self.noise_detection = utils.transform_boolean(noise_detection)
        else:
            self.noise_detection = noise_detection

        self.reviews_pages = reviews_pages
        super(CreateAnAlertAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        return params

    @property
    def data(self):
        """Parameters passed to the API containing the details to create a new
         alert.

        :return: parameters to create new alert.
        :rtype: dict
        """
        data = {}
        data["name"] = self.name
        data["query"] = self.queryd
        data["languages"] = self.languages
        data["countries"] = self.countries if self.countries else ""
        data["sources"] = self.sources if self.sources else ""
        data["blocked_sites"] = self.blocked_sites if self.blocked_sites else ""
        data["noise_detection"] = self.noise_detection if self.noise_detection else ""
        data["reviews_pages"] = self.reviews_pages if self.reviews_pages else ""

        # Deletes parameter if it does not have a value
        for key, value in list(data.items()):
            if value == '':
                del data[key]

        data = json.dumps(data)
        return data

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = "/accounts/{account_id}/alerts/".format(**self.params)
        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.post(self.url, data=self.data)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.text
        return data


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


    :type access_token: str
    :type account_id: str
    :type queryd: dict
    :type languages: list
    :type countries: list
    :type sources: list
    :type blocked_sites: list
    :type noise_detection: boolean
    :type reviews_pages: list
    """

    def __init__(self,
                 access_token,
                 account_id,
                 alert_id,
                 name,
                 queryd,
                 languages,
                 countries=None,
                 sources=None,
                 blocked_sites=None,
                 noise_detection=None,
                 reviews_pages=None):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id
        self.name = name
        self.queryd = queryd
        self.languages = languages
        self.countries = countries
        self.sources = sources
        self.blocked_sites = blocked_sites

        if noise_detection is not None:
            self.noise_detection = utils.transform_boolean(noise_detection)
        else:
            self.noise_detection = noise_detection

        self.reviews_pages = reviews_pages
        super(UpdateAnAlertAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id
        return params

    @property
    def data(self):
        """Parameters passed to the API containing the details to update a
         alert.

        :return: parameters to create new alert.
        :rtype: dict
        """
        data = {}
        data["name"] = self.name
        data["query"] = self.queryd
        data["languages"] = self.languages
        data["countries"] = self.countries if self.countries else ""
        data["sources"] = self.sources if self.sources else ""
        data["blocked_sites"] = self.blocked_sites if self.blocked_sites else ""
        data["noise_detection"] = self.noise_detection if self.noise_detection else ""
        data["reviews_pages"] = self.reviews_pages if self.reviews_pages else ""

        # Deletes parameter if it does not have a value
        for key, value in list(data.items()):
            if value == '':
                del data[key]

        data = json.dumps(data)
        return data

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts/{alert_id}"
                    .format(**self.params))
        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.put(self.url, data=self.data)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()
        return data


class FetchAlertsAPI(Mention):
    """This method will allow you to fetch a list of all alerts for a given account.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :type access_token: str
    :type account_id: str
    """

    def __init__(self, access_token, account_id):
        self.access_token = access_token
        self.account_id = account_id
        super(FetchAlertsAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        return params

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts".format(**self.params))
        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.get(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()

        return data


class FetchAMentionAPI(Mention):
    """Get a single mention by its mention ID.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param alert_id: ID of the alert.
    :param mention_id: ID of the mention.

    :type access_token: str
    :type account_id: str
    :type alert_id: str
    :type mention_id: str

    """

    def __init__(self, access_token, account_id, alert_id, mention_id):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id
        self.mention_id = mention_id
        super(FetchAMentionAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id
        params["mention_id"] = self.mention_id
        return params

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts/{alert_id}/mentions/"
                   "{mention_id}".format(**self.params))

        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.get(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()
        return data


class FetchAllMentionsAPI(Mention):
    """Get all or a filtered amount of mentions from an account.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param alert_id: ID of the alert.
    :param since_id: Returns mentions ordered by id.
     Can not be combined with before_date, not_before_date, cursor.

    :param limit: Number of mentions to return. max 1000.
    :param before_date: Mentions Before date in 'yyyy-MM-dd HH:mm' format

    :Example:

    >>> before_date = '2018-11-25 12:00'

    :param not_before_date: Mentions Not before date in
     'yyyy-MM-dd HH:mm' format

    :param source: Must be either web, twitter, blogs, forums, news,
     facebook, images or videos

    :param unread: return only unread mentions. Must not be combined
     with favorite, q, and tone.

    :param favorite: Whether to return only favorite mentions.
     Can not be combined with folder, when folder is not inbox or archive

    :param folder: Filter by folder. Can be: inbox, archive, spam, trash.
     With spam and trash, include_children is enabled by default.

    :param tone: Filter by tone. Must be one of 'negative', 'neutral',
     'positive'.

    :param countries: Filter by country.
    :param include_children: include children mentions.
    :param sort: Sort results. Must be one of published_at,
     author_influence.score, direct_reach, cumulative_reach, domain_reach.

    :param languages: Filter by language.
    :param timezone: Filter by timezone.
    :param q: Filter by q.
    :param cursor: Filter by cursor


    :type access_token: str
    :type account_id: str
    :type alert_id: str
    :type since_id: str
    :type limit: str
    :type before_date: str
    :type not_before_date: str
    :type source: str
    :type unread: boolean
    :type favorite: boolean
    :type folder: str
    :type tone: str
    :type countries: str
    :type include_children: boolean
    :type sort: str
    :type languages: str
    :type timezone: str
    :type q: str
    :type cursor: str
    """

    def __init__(self,
                 access_token,
                 account_id,
                 alert_id,
                 since_id=None,
                 limit='20',
                 before_date=None,  # 2018-07-07T00:00:00.12345+02:00
                 not_before_date=None,  # #2018-07-01T00:00:00.12345+02:00
                 source=None,
                 unread=None,
                 favorite=None,
                 folder=None,
                 tone=None,
                 countries=None,
                 include_children=None,
                 sort=None,
                 languages=None,
                 timezone=None,
                 q=None,
                 cursor=None):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id

        self.limit = limit

        self.since_id = since_id

        if before_date is not None:
            self.before_date = utils.transform_date(before_date)
        else:
            self.before_date = before_date

        if not_before_date is not None:
            self.not_before_date = utils.transform_date(not_before_date)
        else:
            self.not_before_date = not_before_date

        self.source = source

        if unread is not None:
            self.unread = utils.transform_boolean(unread)
        else:
            self.unread = unread

        if favorite is not None:
            self.favorite = utils.transform_boolean(favorite)
        else:
            self.favorite = favorite

        self.folder = folder

        if tone is not None:
            self.tone = tone = utils.transform_tone(tone)
        else:
            self.tone = tone

        self.countries = countries

        if include_children is not None:
            self.include_children = utils.transform_boolean(include_children)
        else:
            self.include_children = include_children

        self.sort = sort
        self.languages = languages
        self.timezone = timezone
        self.q = q
        self.cursor = cursor
        super(FetchAllMentionsAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id

        if self.since_id:
            params["since_id"] = self.since_id
        else:
            params["before_date"] = self.before_date if self.before_date else ""
            params["not_before_date"] = self.not_before_date if self.before_date else ""
            params["cursor"] = self.cursor if self.cursor else ""

        if self.unread:
            params["unread"] = self.unread
        else:
            if (self.favorite) and (
                (self.folder == "inbox") or (self.folder == "archive")):
                params["favorite"] = self.favorite
                params["folder"] = self.folder
            else:
                 params["folder"] = self.folder if self.folder else ""   
            params["q"] = self.q if self.q else ""
            params["tone"] = self.tone if self.tone else ""

        if int(self.limit) > 1000:
            params["limit"] = "1000"
        elif int(self.limit) < 1:
            params["limit"] = ""
        else:
            params["limit"] = self.limit

        params["source"] = self.source if self.source else ""

        params["countries"] = self.countries if self.countries else ""
        params["include_children"] = self.include_children if self.include_children else ""
        params["sort"] = self.sort if self.sort else ""
        params["languages"] = self.languages if self.languages else ""
        params["timezone"] = self.timezone if self.timezone else ""

        # Deletes parameter if it does not have a value
        for key, value in list(params.items()):
            if value == '':
                del params[key]

        return params

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = "/accounts/{account_id}/alerts/{alert_id}/mentions?"

        # Returns copy of dictionary excluding certain keys
        def without_keys(d, keys):
            return {x: d[x] for x in d if x not in keys}

        keys = {"access_token", "account_id", "alert_id"}
        parameters = without_keys(self.params, keys)

        for key, value in list(parameters.items()):
            if value != '':
                end_url += '&' + key + '={' + key + '}'

        end_url = end_url.format(**self.params)
        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.get(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()

        return data


class FetchMentionChildrenAPI(Mention):
    """""This class will allow you to fetch a list of all children mentions for a given mention.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param alert_id: ID of the alert.
    :param limit: Number of mentions to return. max 1000.
    :param before_date: Mentions Before date in 'yyyy-MM-dd HH:mm' format

    :Example:

    >>> before_date = '2018-11-25 12:00'

    :type access_token: str
    :type account_id: str
    :type alert_id: str
    :type limit: str
    :type before_date: str
    """

    def __init__(self, access_token, account_id, alert_id, mention_id,
                 limit=None, before_date=None):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id
        self.mention_id = mention_id
        self.limit = limit

        if before_date is not None:
            self.before_date = utils.transform_date(before_date)
        else:
            self.before_date = before_date
        super(FetchMentionChildrenAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id
        params["mention_id"] = self.mention_id
        params["before_date"] = self.before_date if self.before_date else ""

        if self.limit:
            if int(self.limit) > 1000:
                params["limit"] = "1000"
            elif int(self.limit) < 1:
                params["limit"] = ""
            else:
                params["limit"] = self.limit

        return params

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts/{alert_id}/mentions/"
                  "{mention_id}/children?")

        def without_keys(d, keys):
            return {x: d[x] for x in d if x not in keys}

        keys = {"access_token", "account_id", "alert_id"}
        parameters = without_keys(self.params, keys)

        for key, value in list(parameters.items()):
            if value != '':
                end_url += '&' + key + '={' + key + '}'

        end_url = end_url.format(**self.params)
        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.get(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()

        return data


# class StreamMentionsAPI(Mention):
#     """
#     :param access_token: Mention API `access_token`
#     :param account_id: ID of the account.
#     :param alerts: list of alerts to stream.
#     :param since_id: Returns mentions ordered by id.
#     Can not be combined with before_date, not_before_date, cursor.

#     :param time_open:
#     Sets the amount of time the connection should stay open for.

#     :type access_token: str
#     :type account_id: str
#     :type alerts: list
#     :type since_id: list
#     :type time_open: str
#     """

#     def __init__(self,
#                  access_token,
#                  account_id,
#                  alerts,
#                  since_ids=None,
#                  time_open=20):
#         self.access_token = access_token
#         self.account_id = account_id
#         self.alerts = alerts
#         self.since_ids = since_ids
#         self.time_open = time_open
#         super(StreamMentionsAPI, self).__init__(access_token)
       

#    @property
#    def params(self):
#        params = {}
#        params["access_token"] = self.access_token
#        params["account_id"] = self.account_id

#        querystring = ""

#        for alert in self.alerts:
#            querystring += "alerts[]=" + alert + "&"
           
#        if self.since_ids:
#            for i in range(self.since_ids):
#                querystring += ("since_id[{alert_id}]="
#                                "{since_id}&").format(self.since_ids[i],
#                                                      self.alerts[i])

#        params["querystring"] = querystring
               
#        return params

#    @property
#    def url(self):
#        base_url = "https://stream.mention.net/api"
#        end_url = ("/accounts/{account_id}/mentions?"
#                  "{querystring}").format(**self.params)

#        return base_url + end_url


#    def query(self):
#        with requests.Session() as session:
#            session.auth = OAuth2BearerToken(self.access_token)
           
#            response = session.get(self.url,
#                                   stream=True,
#                                   timeout=self.time_open)


#            for line in response.iter_lines():
#                if line:
#                    print(json.loads(line))
                           
#            try:
#                response.raise_for_status()
#            except HTTPError:
#                pass
#            data = response.json()

#        return data


class CurateAMentionAPI(Mention):
    """Updates an existing mention.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param alert_id: ID of the alert.
    :param mention_id: ID of the mention.

    :param favorite: Boolean value indicating if the mention was
     set as favorite.

    :param trashed: Boolean value indicating if the mention has
     been put in trash.

    :param read: Boolean value indicating that a mention was read.

    :param tags: add list of tags attributed to the mention.

    :param folder: Indicates the folder where the mention has been put.

    :param tone: Tone value given to the mention. Must be one of 'negative',
     'neutral', 'positive'.


    :type access_token: str
    :type account_id: str
    :type alert_id: str
    :type mention_id: str
    :type favorite: boolean
    :type trashed: boolean
    :type read: str
    :type tags: dict
    :type folder: str
    :type tone: str
    """

    def __init__(self,
                 access_token,
                 account_id,
                 alert_id,
                 mention_id,
                 favorite=None,
                 trashed=None,
                 read=None,
                 tags=None,
                 folder=None,
                 tone=None):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id
        self.mention_id = mention_id

        if favorite is not None:
            self.favorite = utils.transform_boolean(favorite)
        else:
            self.favorite = favorite

        if trashed is not None:
            self.trashed = utils.transform_boolean(trashed)
        else:
            self.trashed = trashed

        if read is not None:
            self.read = tone = utils.transform_tone(read)
        else:
            self.read = read

        self.tags = tags
        self.folder = folder
        self.tone = tone
        super(CurateAMentionAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id
        params["mention_id"] = self.mention_id
        return params

    @property
    def data(self):
        """Parameters passed to the API containing the details to update a
         alert.

        :return: parameters to create new alert.
        :rtype: dict
        """
        data = {}
        data["favorite"] = self.favorite if self.favorite else ""
        data["trashed"] = self.trashed if self.trashed else ""
        data["read"] = self.read if self.read else ""
        data["tags"] = self.tags if self.tags else ""
        data["folder"] = self.folder if self.folder else ""
        data["tone"] = self.tone if self.tone else ""

        # Deletes parameter if it does not have a value
        for key, value in list(data.items()):
            if value == '':
                del data[key]

        data = json.dumps(data)
        return data

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts/{alert_id}/mentions/"
                   "{mention_id}".format(**self.params))

        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.put(self.url, data=self.data)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()

        return data


class MarkAllMentionsAsReadAPI(Mention):
    """Marks all mentions as read.

    :param access_token: Mention API `access_token`
    :param account_id: ID of the account.
    :param alert_id: ID of the alert.

    :type access_token: str
    :type account_id: str
    :type alert_id: str
    """

    def __init__(self, access_token, account_id, alert_id):
        self.access_token = access_token
        self.account_id = account_id
        self.alert_id = alert_id
        super(MarkAllMentionsAsReadAPI, self).__init__(access_token)

    @property
    def params(self):
        """Parameters used in the url of the API call and for authentication.

        :return: parameters used in the url.
        :rtype: dict
        """
        params = {}
        params["access_token"] = self.access_token
        params["account_id"] = self.account_id
        params["alert_id"] = self.alert_id
        return params

    @property
    def url(self):
        """The concatenation of the `base_url` and `end_url` that make up the
        resultant url.

        :return: the `base_url` and the `end_url`.
        :rtype: str
        """
        end_url = ("/accounts/{account_id}/alerts/{alert_id}/mentions/"
                   "markallread".format(**self.params))

        return self._base_url + end_url

    def query(self):
        """The request that returns a JSON file of the API call given a url.

        :return: the `base_url` and the `end_url`.
        :rtype: :class: `json`
        """
        with requests.Session() as session:
            session.auth = OAuth2BearerToken(self.access_token)
            response = session.post(self.url)
            try:
                response.raise_for_status()
            except HTTPError:
                pass
            data = response.json()
        return data
