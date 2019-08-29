import random
import re

import requests


class HTTPHeaders:

    def __init__(self, user_agent_file):
        self.headers = user_agent_file

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, user_agent_file):
        self.__headers = {
            "User-Agent": self.random_useragent(user_agent_file),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def random_useragent(self, filename):
        """Read in all possible user agents from a file and pick one."""

        try:
            with open(filename, 'r') as f:
                # Read the file and split it's lines into a list of user agents.
                lines = f.read().splitlines()
                # Randomly pick one user agent from the list.
                user_agent = random.choice(lines)
        except FileNotFoundError as e:
            raise SystemExit(f"{e.args[1]}: {filename}") from None

        return user_agent


def clean(url):
    """Check if it's a link to a post and remove UTM code."""

    # Pattern that match a link to an Instagram post.
    pattern = "^http[s]?://www.instagram.com/p/[a-zA-Z0-9_-]{11}"
    match = re.match(pattern, url)
    # Shut down the program if the URL didn't match the pattern.
    if not match:
        raise SystemExit("Not a link to an Instagram post")
    # If the link had any UTM code, it's now removed.
    clean_url = match.group()

    return clean_url


def url_exists(url):
    """Check if the URL is working."""

    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        raise SystemExit("Invalid URL")
    except requests.exceptions.ConnectionError:
        raise SystemExit("Connection error")
    except requests.exceptions.Timeout:
        raise SystemExit("Timeout")

    # If the request didn't return 200, it probably returned 404.
    # That could indicate that the link has been removed,
    # belongs to a private account or never existed.
    if r.status_code != 200:
        return False

    return True
