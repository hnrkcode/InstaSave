import random

from utils.settings import USER_AGENT_FILE


class HTTPHeaders:
    def __init__(self):
        self.headers = USER_AGENT_FILE

    @property
    def headers(self):
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
        """Read in all possible user agents from a file and pick one."""

        try:
            with open(filename, "r") as f:
                # Read the file and split it's lines into a list of user agents.
                lines = f.read().splitlines()
                # Randomly pick one user agent from the list.
                user_agent = random.choice(lines)
        except FileNotFoundError as e:
            raise SystemExit(f"{e.args[1]}: {filename}") from None

        return user_agent
