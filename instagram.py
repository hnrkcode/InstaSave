import os
import json
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from settings import USER_AGENT_FILE, POST_DATE_FORMAT


def random_user_agent():
    """Read in all possible user agents from a file and pick one."""

    filename = USER_AGENT_FILE

    with open(filename, 'r') as f:
        # Read the file and split it's lines into a list of user agents.
        lines = f.read().splitlines()
        # Randomly pick one user agent from the list.
        user_agent = random.choice(lines)

    f.close()

    return user_agent


class PostScraper:

    def __init__(self, output=None):
        self.headers = {"User-Agent": random_user_agent()}
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

        data = self._get_post_data(url)
        post_urls = data[0]
        post_type = data[1]

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
        html = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html, 'html.parser')
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
        f.close()

    def _write(self, buffer, file):
        """Write data to file."""
        # JPEG file signature.
        # The first two bytes are always FF D8.
        # The third and fourth bytes are FF Ex (where x = 0..F) which referres
        # to APP0 - APP15, and contain application-specific information.
        if buffer[0] == 0xff and buffer[1] == 0xd8 \
                and buffer[2] == 0xff and (buffer[3] & 0xe0) == 0xe0:
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
        elif buffer[4] == 0x66 and buffer[5] == 0x74 and \
                buffer[6] == 0x79 and buffer[7] == 0x70 \
                and \
                ((buffer[8] == 0x69 and buffer[9] == 0x73 and \
                buffer[10] == 0x6F and buffer[11] == 0x6D) \
                or \
                (buffer[8] == 0x4D and buffer[9] == 0x53 and \
                buffer[10] == 0x4E and buffer[11] == 0x56)):
            file.write(buffer)
