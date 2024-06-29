import unittest
from unittest.mock import Mock, patch
from exceptions import InvalidResponseException
import json
import mention

from unittest import TestCase
#TestCase.maxDiff = None


class TestMentionBase(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        
        self.client = mention.Mention(self.access_token)


    def test_params(self):
        result = self.client.params()
        expected = None

        self.assertEqual(result, expected)


    def test_url(self):
        result = self.client.url()
        expected = None

        self.assertEqual(result, expected)


    def test_query(self):
        result = self.client.url()
        expected = None

        self.assertEqual(result, expected)


class TestAppDataAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        
        self.client = mention.AppDataAPI(self.access_token)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/app/data"

        self.assertEqual(result, expected)


    @patch("mention.requests.get")
    def test_query_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())

    
    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testapidata.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.AppDataAPI(self.access_token)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response, self.client.query())


class TestCreateAnAlertAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.name = jsonfile["update_mention"]["name"]
            self.queryd = jsonfile["update_mention"]["query"]
            self.languages = jsonfile["update_mention"]["languages"]
        
        self.client = mention.CreateAnAlertAPI(self.access_token,
                                               self.account_id,
                                               self.name,
                                               self.queryd,
                                               self.languages)
        

    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/"

        self.assertEqual(result, expected)


    @patch("mention.requests.put")
    def test_query_404_response(self, mock_requests_put):
        # assert successful response
        with open("testcreateanalert.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["update_mention"]["alert_id"]
            self.client = mention.CreateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.queryd,
                                                   self.languages)


        mock_requests_put.return_value = Mock(ok=True)
        mock_requests_put.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response['text'], self.client.query())
        
"""
    @patch("mention.requests.put")
    def test_query_access_token_error(self, mock_requests_put):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_put.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.put")
    def test_query_account_id_error(self, mock_requests_put):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_put.return_value = response
        self.assertEqual(unsuccessful_response,
                         self.client.query())


    @patch("mention.requests.put")
    def test_query_alert_id_error(self, mock_requests_put):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_put.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.put")
    def test_query_success(self, mock_requests_put):
        # assert successful response
        with open("testupdateanalert.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["update_mention"]["alert_id"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)

        mock_requests_put.return_value = Mock(ok=True)
        mock_requests_put.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["alert"]["name"],
                         self.client.query()["alert"]["name"])
"""


class TestFetchAlertsAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        
        self.client = mention.FetchAlertsAPI(self.access_token,
                                             self.account_id)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.FetchAlertsAPI(self.access_token,
                                                 self.account_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testfetchalerts.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.client = mention.FetchAlertsAPI(self.access_token,
                                                 self.account_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

    
        self.assertEqual(successful_response, self.client.query())


class TestUpdateAnAlertAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.name = jsonfile["update_mention"]["name"]
            self.query = jsonfile["update_mention"]["query"]
            self.languages = jsonfile["update_mention"]["languages"]
        
        self.client = mention.UpdateAnAlertAPI(self.access_token,
                                               self.account_id,
                                               self.alert_id,
                                               self.name,
                                               self.query,
                                               self.languages)

    @patch("mention.requests.put")
    def test_query_success(self, mock_requests_put):
        # assert successful response
        with open("testupdateanalert.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["update_mention"]["alert_id"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)

        mock_requests_put.return_value = Mock(ok=True)
        mock_requests_put.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response, self.client.query())
        
"""
    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/c"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.put")
    def test_query_access_token_error(self, mock_requests_put):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_put.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.put")
    def test_query_account_id_error(self, mock_requests_put):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_put.return_value = response
        self.assertEqual(unsuccessful_response,
                         self.client.query())


    @patch("mention.requests.put")
    def test_query_alert_id_error(self, mock_requests_put):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_put.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.put")
    def test_query_success(self, mock_requests_put):
        # assert successful response
        with open("testupdateanalert.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["update_mention"]["alert_id"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages)

        mock_requests_put.return_value = Mock(ok=True)
        mock_requests_put.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["alert"]["name"],
                         self.client.query()["alert"]["name"])


    @patch("mention.requests.put")
    def test_query_success_with_noise_detetction(self, mock_requests_put):
        # assert successful response
        with open("testupdateanalert.json", "r") as read_file:
            successful_response = json.load(read_file)

        self.noise_detection = True

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["update_mention"]["alert_id"]
            self.client = mention.UpdateAnAlertAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.name,
                                                   self.query,
                                                   self.languages,
                                                   self.noise_detection)

        mock_requests_put.return_value = Mock(ok=True)
        mock_requests_put.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["alert"]["name"],
                         self.client.query()["alert"]["name"])
"""


class TestFetchAnAlertAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"
        
        self.client = mention.FetchAnAlertAPI(self.access_token,
                                              self.account_id,
                                              self.alert_id)



    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/c"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.FetchAnAlertAPI(self.access_token,
                                                  self.account_id,
                                                  self.alert_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_alert_id_error(self, mock_requests_get):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.FetchAnAlertAPI(self.access_token,
                                                  self.account_id,
                                                  self.alert_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testfetchanalert.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.client = mention.FetchAnAlertAPI(self.access_token,
                                                  self.account_id,
                                                  self.alert_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["alert"]["name"],
                         self.client.query()["alert"]["name"])


class TestFetchAMentionAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"
        self.mention_id = "d"
        
        self.client = mention.FetchAMentionAPI(self.access_token,
                                               self.account_id,
                                               self.alert_id,
                                               self.mention_id)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/c/mentions/d"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.FetchAMentionAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())

    """
    @patch("mention.requests.get")
    def test_query_alert_id_error(self, mock_requests_get):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.FetchAMentionAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
    """

    @patch("mention.requests.get")
    def test_query_mention_id_error(self, mock_requests_get):
        # assert mention ID error response
        unsuccessful_response = {
            'code': 404,
            'message': 'no such mention'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.client = mention.FetchAMentionAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testfetchamention.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.mention_id = jsonfile["mention_id"]
            self.client = mention.FetchAMentionAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id,
                                                   self.mention_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response, self.client.query())


class TestFetchAllMentionsAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"
        
        self.client = mention.FetchAllMentionsAPI(self.access_token,
                                                  self.account_id,
                                                  self.alert_id)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/c/mentions?&limit=20"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.FetchAllMentionsAPI(self.access_token,
                                                      self.account_id,
                                                      self.alert_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())

    """
    @patch("mention.requests.get")
    def test_query_alert_id_error(self, mock_requests_get):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.FetchAllMentionsAPI(self.access_token,
                                                      self.account_id,
                                                      self.alert_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
    """

    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testfetchmentions.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.client = mention.FetchAllMentionsAPI(self.access_token,
                                                   self.account_id,
                                                   self.alert_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["mentions"][0]["original_url"],
                         self.client.query()["mentions"][0]["original_url"])


class TestFetchMentionChildrenAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"
        self.mention_id = "d"
        
        self.client = mention.FetchMentionChildrenAPI(self.access_token,
                                                      self.account_id,
                                                      self.alert_id,
                                                      self.mention_id)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/"\
                   "c/mentions/d/children?&mention_id=d"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.FetchMentionChildrenAPI(self.access_token,
                                                          self.account_id,
                                                          self.alert_id,
                                                          self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())

    
    @patch("mention.requests.get")
    def test_query_alert_id_error(self, mock_requests_get):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.FetchMentionChildrenAPI(self.access_token,
                                                          self.account_id,
                                                          self.alert_id,
                                                          self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
    

    @patch("mention.requests.get")
    def test_query_mention_id_error(self, mock_requests_get):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message': 'no such mention'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.client = mention.FetchMentionChildrenAPI(self.access_token,
                                                          self.account_id,
                                                          self.alert_id,
                                                          self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testfetchmentionchildren.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.mention_id = jsonfile["mention_id"]
            self.client = mention.FetchMentionChildrenAPI(self.access_token,
                                                          self.account_id,
                                                          self.alert_id,
                                                          self.mention_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response, self.client.query())


class TestCurateAMentionAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"
        self.mention_id = "d"
        
        self.client = mention.CurateAMentionAPI(self.access_token,
                                                self.account_id,
                                                self.alert_id,
                                                self.mention_id)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/c/mentions/d"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.CurateAMentionAPI(self.access_token,
                                                    self.account_id,
                                                    self.alert_id,
                                                    self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())

    
    @patch("mention.requests.get")
    def test_query_alert_id_error(self, mock_requests_get):
        # assert alert ID error response
        unsuccessful_response = {
            'code': 404,
            'message':
                'This alert doesn’t exist or you are not allowed to access it'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.client = mention.CurateAMentionAPI(self.access_token,
                                                    self.account_id,
                                                    self.alert_id,
                                                    self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_mention_id_error(self, mock_requests_get):
        # assert mention ID error response
        unsuccessful_response = {
            'code': 404,
            'message': 'no such mention'
        }
        
        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.client = mention.CurateAMentionAPI(self.access_token,
                                                    self.account_id,
                                                    self.alert_id,
                                                    self.mention_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
    

    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testcuratemention.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id"]
            self.mention_id = jsonfile["mention_id"]
            self.client = mention.CurateAMentionAPI(self.access_token,
                                                    self.account_id,
                                                    self.alert_id,
                                                    self.mention_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["mention"]["description"],
                         self.client.query()["mention"]["description"])


class TestMarkAllMentionsAsReadAPI(unittest.TestCase):
    
    def setUp(self):
        self.access_token = "a"
        self.account_id = "b"
        self.alert_id = "c"
        
        self.client = mention.MarkAllMentionsAsReadAPI(self.access_token,
                                                       self.account_id,
                                                       self.alert_id)


    def test_url(self):
        result = self.client.url
        expected = "https://api.mention.net/api/accounts/b/alerts/c/mentions/"\
                   "markallread"

        self.assertEqual(result, expected)
        

    @patch("mention.requests.get")
    def test_query_access_token_error(self, mock_requests_get):
        # assert client error response
        unsuccessful_response = {
            'error': 'invalid_grant',
            'error_description': 'The access token provided is invalid.'
        }
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())
        

    @patch("mention.requests.get")
    def test_query_account_id_error(self, mock_requests_get):
        # assert account ID error response
        unsuccessful_response = {
            'code': 403,
            'message': 'You are not allowed to access this account'
        }
        
        with open("api_keys.json", "r") as read_file:
            self.access_token = json.load(read_file)["access_token"]
            self.client = mention.MarkAllMentionsAsReadAPI(self.access_token,
                                                           self.account_id,
                                                           self.alert_id)
        
        response = type('response', (object,),
                        {'text': json.dumps(unsuccessful_response)})
        
        mock_requests_get.return_value = response
        self.assertEqual(unsuccessful_response, self.client.query())


    @patch("mention.requests.get")
    def test_query_success(self, mock_requests_get):
        # assert successful response
        with open("testallmentionsasread.json", "r") as read_file:
            successful_response = json.load(read_file)

        with open("api_keys.json", "r") as read_file:
            jsonfile = json.load(read_file)
            self.access_token = jsonfile["access_token"]
            self.account_id = jsonfile["account_id"]
            self.alert_id = jsonfile["alert_id4"]
            self.client = mention.MarkAllMentionsAsReadAPI(self.access_token,
                                                           self.account_id,
                                                           self.alert_id)

        mock_requests_get.return_value = Mock(ok=True)
        mock_requests_get.return_value.json.return_value = successful_response

        response = type('response', (object,),
                        {'text': json.dumps(successful_response)})

        self.assertEqual(successful_response["alert"]["name"],
                         self.client.query()["alert"]["name"])


if __name__ == '__main__':
    unittest.main()
