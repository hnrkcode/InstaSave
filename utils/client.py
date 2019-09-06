import random

from utils.settings import USER_AGENT_FILE


class HTTPHeaders:
    """Create HTTP headers with a random user agent string.

    Attributes:
        headers (dict): Common HTTP headers with a random user agent.

    """

    def __init__(self):
        """Initialise `headers` with a file of many different user agents.

        Args:
            headers (dict): HTTP headers.

        """
        self.headers = USER_AGENT_FILE

    @property
    def headers(self):
        """dict: Get HTTP headers.

        To generate new HTTP headers with a different user agent string
        reassign the file with the list of user agents.
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
        """Return random user agent listed inside a file.

        Args:
            filename (str): Path to a file with user agents.

        Returns:
            str: Random user agent.

        Raises:
            FileNotFoundError: No ``useragents.txt`` wasn't found in ``data``
            folder.
        """

        try:
            with open(filename, "r") as f:
                # Read the file and split it's lines into a list of user agents.
                lines = f.read().splitlines()
                # Randomly pick one user agent from the list.
                user_agent = random.choice(lines)
        except FileNotFoundError as e:
            raise SystemExit(f"{e.args[1]}: {filename}") from None

        return user_agent