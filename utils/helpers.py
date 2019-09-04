import io
import os
import random
import re

import requests
from PIL import Image


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
            with open(filename, "r") as f:
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
    match = re.match("^http[s]?://www.instagram.com/p/[a-zA-Z0-9_-]{11}", url)
    # Shut down the program if the URL didn't match the pattern.
    if not match:
        if is_user(url):
            raise SystemExit("Need to use the -p or --posts flag.")
        else:
            raise SystemExit("Not a link to an Instagram post or user")
    # If the link had any UTM code, it's now removed.
    clean_url = match.group()

    return clean_url


def is_user(text):
    # Pattern that match a link to an Instagram user profile.
    url = re.match("^http[s]?://www.instagram.com/[a-zA-Z0-9_]{2,30}", text)
    # Pattern that match a valid Instagram username.
    name = re.match("^[a-zA-Z0-9_]{2,30}$", text)
    if url:
        return url.group()
    elif name:
        return "https://www.instagram.com/" + name.group()
    return ""


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


def save_file(buffer, output, filename):
    """Write content to file."""

    # Create folder for downloaded files if it not exist.
    if not os.path.isdir(output):
        os.mkdir(output)
    # JPEG file signature always start with FF D8.
    # The other two bytes are FF Ex (x = 0-F).
    if buffer[:3] == b"\xff\xd8\xff" and (buffer[3] & 0xE0) == 0xE0:
        bytes = io.BytesIO(buffer)
        op = os.path.join(output, filename)
        # Save the image with Pillow to remove any unwanted meta data.
        # Also try to keep the same quality when saved.
        Image.open(bytes).save(op, quality="keep")
    # MP4 file signatures are 8 bytes long and are offset by 4 bytes.
    # The first four bytes are the same in both types of MP4 file formats.
    elif (
        buffer[4:8] == b"\x66\x74\x79\x70"
        and buffer[8:12] == b"\x69\x73\x6f\x6d"
        or buffer[8:12] == b"\x4d\x53\x4e\x56"
    ):
        with open(os.path.join(output, filename), "wb") as f:
            f.write(buffer)
