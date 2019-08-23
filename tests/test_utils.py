import utils
import unittest
from unittest.mock import patch, mock_open


class TestUtilsModule(unittest.TestCase):

    def setUp(self):
        self.useragents = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36\n" + \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36\n" + \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36\n" + \
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0\n" + \
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0\n"

    def test_random_useragent_file_not_found(self):
        file = "file.txt"
        msg = f"^No such file or directory: {file}$"
        with self.assertRaisesRegex(SystemExit, msg):
            utils.random_useragent(file)

    def test_random_useragent_return_value(self):
        with patch(
                "builtins.open",
                new_callable=mock_open,
                read_data=self.useragents) as mock_file:
            # Mock a file to open and return one random line from read_data.
            ua = utils.random_useragent("some/path/some_file.txt")
            # Create a list of user agents in the string passed to read_data.
            ua_list = self.useragents.splitlines()
            # Make sure that the returned user agent also appears in the list.
            self.assertIn(ua, ua_list)
