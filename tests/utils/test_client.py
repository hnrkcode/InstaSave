import os.path
import unittest
from unittest.mock import mock_open, patch

from instasave.utils.client import HTTPHeaders

path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "test_data", "text"
)
with open(os.path.join(path, "useragents.txt")) as f:
    USERAGENTS = f.read()


class TestClient(unittest.TestCase):
    def test_random_useragent_file_not_found(self):
        ua = HTTPHeaders()
        with self.assertRaisesRegex(
            SystemExit, "^No such file or directory: test.txt$"
        ):
            ua.headers = "test.txt"

    @patch("builtins.open", new_callable=mock_open, read_data=USERAGENTS)
    def test_random_useragent_return_useragent_from_file(self, mock_file):
        ua = HTTPHeaders()
        ua_list = USERAGENTS.splitlines()
        self.assertIn(ua.headers["User-Agent"], ua_list)

    @patch("builtins.open", new_callable=mock_open, read_data=USERAGENTS)
    def test_random_useragent_request_headers(self, mock_file):
        ua = HTTPHeaders()
        ua_list = USERAGENTS.splitlines()
        self.assertEqual(
            ua.headers["Accept"],
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        )
        self.assertEqual(ua.headers["Accept-Language"], "en-US,en;q=0.5")
        self.assertEqual(ua.headers["Accept-Encoding"], "gzip, deflate, br")
        self.assertEqual(ua.headers["Connection"], "keep-alive")
