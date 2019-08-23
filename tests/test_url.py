import unittest
import requests
from unittest.mock import patch
from url import clean, is_working
from requests.exceptions import ConnectionError, MissingSchema, Timeout


class TestCleanURL(unittest.TestCase):

    def setUp(self):
        # Strings that should match the regular expression of a IG post url,
        # but a match doesn't mean it's an existing and working url
        # the is_working() function is checking that.
        self.match = [
            "https://www.instagram.com/p/B1ZFAoEgtoQ/?utm_source=web",
            "https://www.instagram.com/p/aaaaaaaaaaa/",
            "https://www.instagram.com/p/12345678901/",
            "https://www.instagram.com/p/AAAAAAAAAAA/",
            "https://www.instagram.com/p/------------/",
            "https://www.instagram.com/p/____________/",
            "https://www.instagram.com/p/AZaz023789-_/",
        ]

        # Strings that shouldn't match the regular expression of a IG post url.
        self.no_match = [
            "https://www.instagram.com/p/B1ZFAo/?utm_source=web",
            "https://www.instagram.com/",
            "https://instagram.com/",
            "asdf",
            "1234",
        ]

    def test_clean_match(self):
        for url in self.match:
            # A clean url to an instagram post is 39 character long.
            got, want = clean(url), url[:39]
            self.assertEqual(got, want)

    def test_clean_no_match(self):
        for url in self.no_match:
            with self.assertRaisesRegex(
                    SystemExit, "^Not a link to an Instagram post$"):
                clean(url)

    @patch.object(requests, 'get', side_effect=MissingSchema)
    def test_is_working_raises_missing_schema_message(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Invalid URL$"):
            is_working("URL")

    @patch.object(requests, 'get', side_effect=ConnectionError)
    def test_is_working_raises_connection_error_message(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Connection error$"):
            is_working("URL")

    @patch.object(requests, 'get', side_effect=Timeout)
    def test_is_working_raises_timeout_message(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Timeout$"):
            is_working("URL")

    @patch('requests.get')
    def test_is_working_response_ok(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.ok
        self.assertTrue(is_working("URL"))

    @patch('requests.get')
    def test_is_working_response_not_found(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.not_found
        self.assertFalse(is_working("URL"))
