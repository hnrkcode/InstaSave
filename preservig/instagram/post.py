import os
import json
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from settings import POST_DATE_FORMAT


class Downloader:

    def __init__(self, headers, output=None):
        self.headers = headers
        self.output = output

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

        post_urls, post_type = self._get_post_data(url)

        # Post with a video file.
        if post_type == "GraphVideo":
            self._download_file(post_urls)
        # Post with a image file.
        elif post_type == "GraphImage":
            self._download_file(post_urls)
        # Post with multiple files, either images and/or videos.
        elif post_type == "GraphSidecar":
            for url in post_urls:
                self._download_file(url)

    def _get_post_data(self, url):
        """Returns the file URLs and the post type."""

        # Get the page's HTML code and parse it with BeautifulSoup
        # to find the type of the post.
        html = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        # Get all scripts in the HTML.
        js = soup.select("script[type='text/javascript']")
        # Pick the fourth script and remove variable name and semicolon.
        json_data = js[3].text[21:-1]
        # Deserialize the data to a python object and access the information
        # at the 'shortcode_media' key.
        data = json.loads(json_data)
        data = data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
        # Get the type of the post.
        post_type = data["__typename"]

        # Post with a video file.
        if post_type == "GraphVideo":
            image_url = data["video_url"]
        # Post with a image file.
        elif post_type == "GraphImage":
            image_url = data["display_url"]
        # Post with multiple files, either images and/or videos.
        elif post_type == "GraphSidecar":
            edges = data["edge_sidecar_to_children"]["edges"]
            # Differentiate between images and videos in multi-content posts.
            # Get urls with .jpg for images and .mp4 for videos.
            image_url = [edge["node"]["video_url"] if edge["node"]["__typename"] == "GraphVideo" else edge["node"]["display_url"] for edge in edges]

        return image_url, post_type

    def _download_file(self, url):
        """Get content from the url, pick a name for the file and save it."""

        r = requests.get(url, headers=self.headers)
        filename = self._pick_filename(r.headers)
        self._save(r.content, filename)

    def _pick_filename(self, headers):
        """Give the file a unique name."""

        # Get the date the post was uploaded.
        d = datetime.strptime(headers.get('last-modified'), POST_DATE_FORMAT)
        # Format the date and time and use it in the filename.
        filename = d.strftime("%Y%m%d_%H%M%S_")
        # Add a unique string to the filename to prevent conflicting names.
        filename += headers.get('x-enc-origin-req-handler')
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
