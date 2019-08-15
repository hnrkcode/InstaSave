import re
import sys
import requests

class CleanURL:

    def __init__(self, url):
        self.url = url

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = self._valid_url(self._remove_utm_code(url))

    def _valid_url(self, url):
        """Make sure it is a working instagram url."""

        if url is None:
            sys.exit("That's not an instagram post.")
        if not self._url_exists(url.group()):
            sys.exit("The page does not exist.")

        return url.group()

    def _url_exists(self, url):
        """Return true if the HTTP request is sucessful."""

        r = requests.get(url)

        if r.status_code == 200:
            return True

        return False

    def _remove_utm_code(self, url):
        """Remove tracking code from url."""

        pattern = "^http[s]*\:\/+www.instagram.com\/[a-z]\/[A-Za-z0-9_-]+"
        match = re.match(pattern, url)

        return match
