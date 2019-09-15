import unittest
from unittest.mock import patch

import requests
from requests import exceptions

from instasave.utils import webaddr


class TestWebaddr(unittest.TestCase):
    def setUp(self):
        self.post_url = "https://www.instagram.com/p/abc_XYZ_0-9?asdf=1234"
        self.no_match = "https://www.instagram.com/"
        self.hashtag_url = "https://www.instagram.com/explore/tags/somename/"
        self.username_url = "https://www.instagram.com/somename/"
        self.name = "somename"

    @patch("requests.get")
    def test_validate_url_success(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.ok
        want = self.post_url[:39]
        got = webaddr.validate_url(self.post_url)
        self.assertEqual(got, want)

    @patch("requests.get")
    def test_validate_url_failure(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.not_found
        with self.assertRaisesRegex(
            SystemExit, "^Sorry, this page isn't available.$"
        ):
            webaddr.validate_url(self.post_url)

    def test_clean_url_return_clean_url(self):
        want = self.post_url[:39]
        got = webaddr.clean_url(self.post_url)
        self.assertEqual(got, want)

    def test_clean_url_not_a_post_url(self):
        with self.assertRaisesRegex(SystemExit, "^Didn't match a post url.$"):
            webaddr.clean_url(self.no_match)

    def test_get_url_input_url_to_hashtag(self):
        want = self.hashtag_url[:-1]
        got = webaddr.get_url(self.hashtag_url, True)
        self.assertEqual(got, want)

    def test_get_url_input_hashtag(self):
        want = self.hashtag_url[:-1]
        got = webaddr.get_url(self.name, True)
        self.assertEqual(got, want)

    def test_get_url_input_url_to_user(self):
        want = self.username_url[:-1]
        got = webaddr.get_url(self.name, False)
        self.assertEqual(got, want)

    def test_get_url_input_username(self):
        want = self.username_url[:-1]
        got = webaddr.get_url(self.name, False)
        self.assertEqual(got, want)

    def test_get_url_did_not_match_hashtag(self):
        with self.assertRaisesRegex(
            SystemExit,
            "^Some error occurred, couldn't match username or hashtag.$",
        ):
            webaddr.get_url(self.no_match, True)

    def test_get_url_did_not_match_username(self):
        with self.assertRaisesRegex(
            SystemExit,
            "^Some error occurred, couldn't match username or hashtag.$",
        ):
            webaddr.get_url(self.no_match, False)

    @patch("requests.get")
    def test_is_working_url_returns_ok(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.ok
        self.assertTrue(webaddr.is_working(self.post_url))

    @patch("requests.get")
    def test_is_working_url_returns_not_found(self, mock_requests):
        mock_requests.return_value.status_code = requests.codes.not_found
        self.assertFalse(webaddr.is_working(self.post_url))

    @patch.object(requests, "get", side_effect=exceptions.Timeout)
    def test_is_working_raises_timeout(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Timeout$"):
            webaddr.is_working(self.post_url)

    @patch.object(requests, "get", side_effect=exceptions.ConnectionError)
    def test_is_working_raises_connection_error(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Connection error$"):
            webaddr.is_working(self.post_url)

    @patch.object(requests, "get", side_effect=exceptions.MissingSchema)
    def test_is_working_raises_missing_schema(self, mock_requests):
        with self.assertRaisesRegex(SystemExit, "^Invalid URL$"):
            webaddr.is_working(self.post_url)
