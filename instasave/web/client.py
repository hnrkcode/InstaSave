import random

from instasave.utils.color import TextColors
from instasave.utils.settings import USER_AGENT_FILE

DEFAULT_UA_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 Edg/44.18362.267.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 OPR/63.0.3368.88",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 OPR/63.0.3368.88",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 OPR/63.0.3368.88",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 Vivaldi/2.7.1628.33",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 Vivaldi/2.7.1628.33",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36 Vivaldi/2.7.1628.33",
    "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 YaBrowser/19.7.3.172 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 YaBrowser/19.6.0.1583 Yowser/2.5 Safari/537.36",
]


class HTTPHeaders:
    """Create HTTP headers with a random user agent string."""

    def __init__(self, verbose=False):
        """Initialise `headers` with a file of many different user agents."""

        self.verbose = verbose
        self.headers = USER_AGENT_FILE

    @property
    def headers(self):
        """Return dict with HTTP headers.

        To generate new HTTP headers with a different user agent string
        reassign the useragent file list.
        """

        return self.__headers

    @headers.setter
    def headers(self, file):
        self.__headers = {
            "User-Agent": self.random_useragent(file),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def random_useragent(self, filename):
        """Return random user agent listed inside a file."""

        try:
            with open(filename, "r") as f:
                # Read the file and split it's lines into a list of user agents.
                lines = f.read().splitlines()
                # Randomly pick one user agent from the list.
                ua = random.choice(lines)

        except FileNotFoundError as e:
            ua = random.choice(DEFAULT_UA_LIST)

            if self.verbose:
                print(TextColors().warning(f"{e.args[1]}: {filename}"))
                print(TextColors().warning(f"Using default user agent."))

        return ua
