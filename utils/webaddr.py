import re

import requests


def clean_url(url):
    """Check if it's a link to a post and remove UTM code."""

    # Pattern that match a link to an Instagram post.
    match = re.match("^http[s]?://www.instagram.com/p/[a-zA-Z0-9_-]{11}", url)
    # Shut down the program if the URL didn't match the pattern.
    if not match:
        raise SystemExit("Didn't match a post url.")
    # If the link had any UTM code, it's now removed.
    clean_url = match.group()

    return clean_url


def get_url(text, hashtag):

    name, url = None, None

    if hashtag:
        url = re.match("^http[s]?://www.instagram.com/explore/tags/[a-zA-Z0-9_]+", text)
        name = re.match("^[a-zA-Z0-9_]+", text)
    else:
        url = re.match(r"^http[s]?://www.instagram.com/[a-zA-Z0-9_\.]{2,30}[/]?$", text)
        name = re.match(r"^[a-zA-Z0-9_\.]{2,30}$", text)

    if url:
        return url.group()
    elif name and hashtag:
        return "https://www.instagram.com/explore/tags/" + name.group()
    elif name and not hashtag:
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
