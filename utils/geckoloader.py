import os
import platform
import re
import tarfile

import requests
from bs4 import BeautifulSoup

from utils.color import TextColors
from utils.settings import DATA_DIR, GECKODRIVER


class GeckoLoader:
    """Download latest geckodriver from github."""

    def __init__(self, headers, verbose=False):
        """Takes HTTP headers as argument and downloads the geckodriver."""

        self._text = TextColors()
        self._url = "https://github.com/mozilla/geckodriver/releases/latest"

        downloaded_driver = self._get_geckodriver(self._url, headers)

        if verbose:
            if downloaded_driver:
                print(
                    self._text.bold(
                        "Downloaded latest version of geckodriver for "
                        + f"{self.sysinfo['bits']}-bit "
                        + f"{self.sysinfo['name']} system."
                    )
                )
            else:
                print(self._text.bold("Geckodriver exists in path."))

    @property
    def sysinfo(self):
        """Return dict with system name and processor architecture."""

        system = platform.system().lower()
        architecture = platform.machine()[-2:]

        return {"name": system, "bits": architecture}

    def _get_geckodriver(self, url, headers):
        """Download and extract the geckodriver if not already exists."""

        # Geckodriver already exists in path.
        if os.path.isfile(GECKODRIVER):
            return False

        # Get list of download links for geckodrivers of different system.
        drivers = self._get_driver_paths(url, headers)
        filename = self._download_driver(drivers, self.sysinfo, headers)
        self._extract_driver(filename)

        return True

    def _download_driver(self, drivers, system_info, headers):
        """Return name of archive file after downloading it.

        Check if there is any geckodriver for the users system. If there is
        download it and return the name of the archive file.
        """

        filename = None

        # Check if any of the available drivers ar compatible with the system.
        for driver in drivers:

            system_name = system_info["name"] in driver
            architecture_bits = system_info["bits"] in driver

            # Compatible driver found.
            if system_name and architecture_bits:

                url = self._url[:19] + driver
                file_content = requests.get(url, headers).content
                pattern = r"geckodriver-v[0-9\.-]+[a-z0-9]+\.[a-z\.]+$"
                filename = re.search(pattern, driver).group()

                break

        if not filename:
            raise SystemExit("Couldn't download driver for your system.")

        # Save the archive with the geckodriver.
        with open(os.path.join(DATA_DIR, filename), "wb") as f:
            f.write(file_content)

        return filename

    def _get_driver_paths(self, url, headers):
        """Return list of available geckodrivers."""

        r = requests.get(url, headers)
        soup = BeautifulSoup(r.text, "html.parser")
        pattern = r"([/][a-z]+)+[0-9\./]+geckodriver-v[a-z0-9\.\-]+"
        paths = [
            path.get("href")
            for path in soup.find_all("a", href=re.compile(pattern))
        ]

        return paths

    def _extract_driver(self, file):
        """Extract driver and delete it's archive file afterwards."""

        file = os.path.join(DATA_DIR, file)

        # Extract the geckodriver.
        with tarfile.open(file) as tar:
            tar.extractall(DATA_DIR)

        # Delete the archive file.
        os.remove(file)
