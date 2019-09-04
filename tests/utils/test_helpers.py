import unittest
from unittest.mock import mock_open, patch

import requests
from requests.exceptions import ConnectionError, MissingSchema, Timeout

from utils.helpers import HTTPHeaders, clean, url_exists


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.useragents = (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36\n"
            + "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36\n"
            + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36\n"
            + "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0\n"
            + "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0\n"
        )

        # Strings that should match the regular expression of a IG post url,
        # but a match doesn't mean it's an existing and working url
        # the url_exists() function is checking that.
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
        ]

    def test_random_useragent_file_not_found(self):
        file = "file.txt"
        msg = f"^No such file or directory: {file}$"
        with self.assertRaisesRegex(SystemExit, msg):
            HTTPHeaders(file)

    def test_random_useragent_return_value(self):
        with patch(
            "builtins.open", new_callable=mock_open, read_data=self.useragents
        ) as mock_file:
            # Mock a file to open and return one random line from read_data.
            ua = HTTPHeaders("some/path/some_file.txt")
            # Create a list of user agents in the string passed to read_data.
            ua_list = self.useragents.splitlines()
            # Make sure that the returned user agent also appears in the list.
            self.assertIn(ua.headers["User-Agent"], ua_list)

    def test_clean_match(self):
        for url in self.match:
            # A clean url to an instagram post is 39 character long.
            got, want = clean(url), url[:39]
            self.assertEqual(got, want)

    def test_clean_no_match(self):
        for url in self.no_match:
            with self.assertRaisesRegex(
                SystemExit, "^Not a link to an Instagram post or user$"
            ):
                clean(url)

    def test_clean_match_username_without_flag(self):
        for url in ["asdf", "asdfgd", "aaaaa"]:
            with self.assertRaisesRegex(
                SystemExit, "^Need to use the -p or --posts flag.$"
            ):
                clean(url)

    @patch.object(requests, "get", side_effect=MissingSchema)
    def test_url_exists_raises_missing_schema_message(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Invalid URL$"):
            url_exists("URL")

    @patch.object(requests, "get", side_effect=ConnectionError)
    def test_url_exists_raises_connection_error_message(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Connection error$"):
            url_exists("URL")

    @patch.object(requests, "get", side_effect=Timeout)
    def test_url_exists_raises_timeout_message(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Timeout$"):
            url_exists("URL")

    @patch("requests.get")
    def test_url_exists_response_ok(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.ok
        self.assertTrue(url_exists("URL"))

    @patch("requests.get")
    def test_url_exists_response_not_found(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.not_found
        self.assertFalse(url_exists("URL"))

    # TODO: write test for save_file().
    # def test_save_file(self):
    #    pass
