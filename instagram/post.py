import os
from datetime import datetime

import requests

from utils import decorator, hook
from utils.color import TextColors
from utils.jsonparser import parse_json
from utils.path import save_file, save_meta

JSON_CSS_SELECTOR = "body > script:nth-child(6)"


class PostScraper:
    """Scrape data from posts including image and video files urls.

    Attributes:
        headers (dict): HTTP headers.
        data (dict): JSON data from Instagram's HTML code.
        verbose (bool): Display more information if set to true.

    """

    def __init__(self, headers):
        """Prepare scraping post data by initializing attributes."""
        self.headers = headers
        self.data = None

    @property
    def username(self):
        return self.data["owner"]["username"]

    @property
    def shortcode(self):
        return self.data["shortcode"]

    @property
    def created_at(self):
        t = self.data["taken_at_timestamp"]
        # Convert unix timestamp to custom date format.
        date = datetime.utcfromtimestamp(t).strftime("%Y%m%d%H%M%S")
        return date

    def post_data(self, url):
        source = requests.get(url, headers=self.headers).text
        self.data = parse_json(source, JSON_CSS_SELECTOR, hook.shortcode_media)
        type = self._get_type(self.data)
        url = self._get_url(self.data, type)

        return (url, type)

    def _get_type(self, data):
        """Return post type."""
        # Return the type of the post.
        return data["__typename"]

    def _get_url(self, data, type):
        """Return file urls from post."""
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
            url = [
                edge["node"]["video_url"]
                if edge["node"]["__typename"] == "GraphVideo"
                else edge["node"]["display_url"]
                for edge in edges
            ]

        return url


class Downloader:
    """Download files from Instagram posts.

    Attributes:
        scraper (obj): PostScraper object.
        headers (dict): HTTP headers.
        output (str): Download location.
        verbose (bool): Display more information if set to true.

    """

    def __init__(self, headers, output=None, verbose=False):
        """Initialize Downloader."""
        self.scraper = PostScraper(headers)
        self.headers = headers
        self.output = output
        self.verbose = verbose
        self.text = TextColors()

    @property
    def output(self):
        """Return default or custom download location."""
        return self.__output

    @output.setter
    def output(self, output):
        # Custom output location.
        if output:
            self.__output = os.path.join(output, "downloads")
        # Default output location.
        else:
            self.__output = os.path.join(os.getcwd(), "downloads")

    @decorator.count_calls
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
        # Change date format from 'yyyymmddhhmmss' to 'yyyy-mm-dd' for folders.
        d = self.scraper.created_at[:8]
        date = "-".join([d[:4], d[4:6], d[6:8]])
        output = os.path.join(
            self.output, self.scraper.username, date, self.scraper.shortcode
        )
        save_file(r.content, output, filename)
        save_meta(self.scraper.data, output)

        if self.verbose:
            file = self.text.blue(r.headers["Content-Type"])
            user = self.text.green(self.scraper.username)
            print(f"Download { file } from { user }...")

    @decorator.unique_filename
    def _pick_filename(self, headers):
        """Create a filename based username, date, url and file type.

            Example: [username]_[post date]_[shortcode].[file extension]"""

        filename = self.scraper.username
        filename += "_" + self.scraper.created_at
        filename += "_" + self.scraper.shortcode
        # Add file extension based on the contents type.
        if headers.get("content-type") == "video/mp4":
            filename += ".mp4"
        else:
            filename += ".jpg"

        return filename
