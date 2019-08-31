import json
import os
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from utils.decorators import start_at_shortcode_media, unique_filename
from utils.helpers import save_file


class PostScraper:

    def __init__(self, headers, verbose=False):
        self.headers = headers
        self.data = None
        self.verbose = verbose

    def post_data(self, url):
        """Extract type and file URLs from dict and retrun it."""
        # Dict with data extracted from the HTML of the url parameter.
        self.data = self._json_data(url)
        # Print information to terminal.
        if self.verbose:
            print(f"Scrape data from one of { self.get_username() }'s posts...")

        type = self._get_type(self.data)
        url = self._get_url(self.data, type)

        return (url, type)

    def get_username(self):
        """Return post creators username."""
        try:
            username = self.data["owner"]["username"]
        except KeyError as e:
            raise SystemExit(f"KeyError: {e}")

        return username

    def get_created_at(self):
        """Return post creation date and time."""
        try:
            t = self.data["taken_at_timestamp"]
            # Convert unix timestamp to custom date format.
            date = datetime.utcfromtimestamp(t).strftime("_%Y%m%d%H%M%S")
        except KeyError as e:
            raise SystemExit(f"KeyError: {e}")

        return date


    @start_at_shortcode_media
    def _json_data(self, url):
        """Get JSON from javascript and deserialize it into a Python dict."""

        # Get the page's HTML code and parse it with BeautifulSoup
        # to find the type of the post.
        r = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(r, 'html.parser')
        # Get all scripts in the HTML.
        script = soup.select("script[type=\"text/javascript\"]")
        # Pick the fourth script and remove variable name and semicolon.
        json_data = script[3].text[21:-1]
        # Deserialize the data to a python dict.
        data = json.loads(json_data)

        return data

    def _get_type(self, data):
        """Get the type of Instagram post."""
        # Return the type of the post.
        return data["__typename"]

    def _get_url(self, data, type):
        """Get the urls to the files in a Instagram post."""
        # Post with a video file.
        if type == "GraphVideo":
            url = data["video_url"]
        # Post with a image file.
        elif type == "GraphImage":
            url = data["display_url"]
        # Post with multiple files, either images and/or videos.
        elif type == "GraphSidecar":
            edges = data["edge_sidecar_to_children"]["edges"]
            # Differentiate between images and videos in multi-content posts.
            # Get urls with .jpg for images and .mp4 for videos.
            url = [edge["node"]["video_url"] if edge["node"]["__typename"] == "GraphVideo" else edge["node"]["display_url"] for edge in edges]

        return url


class Downloader:

    def __init__(self, headers, output=None, verbose=False):
        self.headers = headers
        self.output = output
        self.scraper = PostScraper(headers, verbose=verbose)
        self.verbose = verbose

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, output):
        # Custom output location.
        if output:
            self.__output = os.path.join(output, "downloads")
        # Default output location.
        else:
            self.__output = os.path.join(os.getcwd(), "downloads")

    def download(self, url):
        """Download files to disk."""

        post_url, post_type = self.scraper.post_data(url)

        if post_type == "GraphSidecar":
            for url in post_url:
                self._download_file(url)
        elif post_type in ["GraphVideo", "GraphImage"]:
            self._download_file(post_url)

    def _download_file(self, url):
        """Get content from the url, pick a name for the file and save it."""

        r = requests.get(url, headers=self.headers)
        filename = self._pick_filename(r.headers)
        save_file(r.content, self.output, filename)
        # Print information to terminal.
        if self.verbose:
            file = r.headers['Content-Type']
            user = self.scraper.get_username()
            print(f"Download {file} from {user}...")

    @unique_filename
    def _pick_filename(self, headers):
        """Create a filename based username, date and file type.

            Example: [username]_[post date].[file extension]"""

        filename = self.scraper.get_username()
        filename += self.scraper.get_created_at()
        # Add file extension based on the contents type.
        if headers.get('content-type') == "video/mp4":
            filename += ".mp4"
        else:
            filename += ".jpg"

        return filename
