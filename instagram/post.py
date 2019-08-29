import json
import os
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from utils.decorators import start_at_shortcode_media, unique_filename


class PostScraper:

    def __init__(self, headers):
        self.headers = headers
        self.data = None

    def post_data(self, url):
        """Extract type and file URLs from dict and retrun it."""
        # Dict with data extracted from the HTML of the url parameter.
        self.data = self._json_data(url)

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
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Get all scripts in the HTML.
        script = soup.select("script[type='text/javascript']")
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

    def __init__(self, headers, output=None):
        self.headers = headers
        self.output = output
        self.scraper = PostScraper(headers)

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
        self._save(r.content, filename)

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

    def _save(self, content, filename):
        """Write content to file."""

        # Create folder for downloaded files if it not exist.
        if not os.path.isdir(self.output):
            os.mkdir(self.output)
        # Write content to file.
        with open(os.path.join(self.output, filename), 'wb') as f:
            self._write(content, f)

    def _write(self, buffer, file):
        """Write data to file."""
        # JPEG file signature.
        # The first two bytes are always FF D8.
        # The third and fourth bytes are FF Ex (where x = 0..F) which referres
        # to APP0 - APP15, and contain application-specific information.
        if buffer[:3] == b"\xff\xd8\xff" and (buffer[3] & 0xe0) == 0xe0:
            # Current position in the buffer.
            cur = 0
            for byte in buffer:
                # Remove IPTC special instructions from jpeg file, because it
                # could be used for tracking usage of downloaded images.
                if cur > 22 and cur < 146:
                    file.write(bytes(1))
                # Write unmodified data.
                else:
                    file.write(bytes([byte]))
                cur += 1
        # MP4 file signature, offset by 4 bytes.
        # The first four bytes are the same in both types.
        # 66 74 79 70 69 73 6F 6D - ISO Base Media file (MPEG-4) v1.
        # 66 74 79 70 4D 53 4E 56 - MPEG-4 video file.
        elif buffer[4:8] == b"\x66\x74\x79\x70" and \
                buffer[8:12] == b"\x69\x73\x6f\x6d" or \
                buffer[8:12] == b"\x4d\x53\x4e\x56":
            file.write(buffer)
