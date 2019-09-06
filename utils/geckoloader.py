import os
import platform
import re
import tarfile

import requests
from bs4 import BeautifulSoup


class GeckoLoader:
    """Download latest geckodriver from github."""

    def __init__(self, headers):
        """Takes HTTP headers as argument and downloads the geckodriver."""
        self._url = "https://github.com/mozilla/geckodriver/releases/latest"
        self._get_geckodriver(self._url, headers)

    def _get_geckodriver(self, url, headers):
        """Download and extract the latest gecodriver if not already exists.

        Args:
            url (str): URL to latest geckodriver release.
            headers (dict): HTTP headers.
        """
        # Download geckodriver it doesn't already exists in path.
        if not os.path.isfile("geckodriver"):
            # Get list of download links for geckodrivers of different system.
            drivers = self._get_driver_paths(url, headers)
            # Get system information.
            info = self._get_system_info()
            # Name for the downloaded archive file with the driver inside.
            filename = self._download(drivers, info, headers)
            # Extract the geckodriver.
            self._extract(filename)
            print(
                f"Downloaded latest gecodriver version for { info['name'] } { info['bits'] }."
            )
        else:
            print("Geckodriver exists in path.")

    def _download(self, drivers, system, headers):
        """Download archive file with the geckodriver and return it's name.

        Args:
            drivers (bs4.element.ResultSet): List of available geckodrivers for
                different systems.
            system (dict): Contains the systems name (e.g linux) and the
                processors architecture (e.g 32-bit or 64-bit).
            headers (dict): HTTP headers.

        Returns:
            str: Archives filename.

        Raises:
            SystemExit: If it couldn't find any driver for the system.

        """
        filename = None
        # Check if any of the available drivers ar compatible with the system.
        for driver in drivers:
            path = driver.get("href")
            # Compatible driver found.
            if system["name"] in path and system["bits"] in path:
                url = self._url[:19] + path
                r = requests.get(url, headers)
                filename = re.search(
                    r"geckodriver-v[0-9\.-]+[a-z0-9]+\.[a-z\.]+$", path
                ).group()

        # Save the file if a driver for the current system was found.
        if filename:
            with open(filename, "wb") as f:
                f.write(r.content)
        else:
            raise SystemExit("Can't find any driver to download for your system.")

        return filename

    def _get_driver_paths(self, url, headers):
        """Return list of available geckodrivers.

        Args:
            url (str): URL to latest release.
            headers (dict): HTTP headers.

        Returns:
            bs4.element.ResultSet: List of available drivers.

        """
        r = requests.get(url, headers)
        soup = BeautifulSoup(r.text, "html.parser")
        paths = soup.find_all(
            "a", href=re.compile(r"([/][a-z]+)+[0-9\./]+geckodriver-v[a-z0-9\.\-]+")
        )

        return paths

    def _get_system_info(self):
        """Return dict with system name and processor architecture."""

        info = {"name": platform.system().lower(), "bits": platform.machine()[-2:]}

        return info

    def _extract(self, file):
        """Extract driver and delete it's archive file afterwards."""

        try:
            # Extract the geckodriver.
            tar = tarfile.open(file)
            tar.extractall()
            tar.close()
        except ValueError as e:
            raise SystemExit(e)

        try:
            # Delete the archive file that the geckodriver was extracted from.
            os.remove(file)
        except FileNotFoundError as e:
            print(e)
