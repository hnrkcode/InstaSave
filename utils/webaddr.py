import re

import requests


def validate_url(url):
    """Validate that the url is working and belongs to a post."""

    url = clean_url(url)

    if not is_working(url):
        raise SystemExit("Sorry, this page isn't available.")

    return url


def clean_url(url):
    """Return clean post URL without UTM code at the end."""

    # Pattern that match a link to an Instagram post.
    match = re.match("^http[s]?://www.instagram.com/p/[a-zA-Z0-9_-]{11}", url)
    # Shut down the program if the URL didn't match the pattern.
    if not match:
        raise SystemExit("Didn't match a post url.")
    # If the link had any UTM code, it's now removed.
    clean_url = match.group()

    return clean_url


def get_url(id, hashtag):
    """Return URL to a hashtag or a user."""

    if hashtag:
        # Pattern for hashtags.
        url = re.match(
            "^http[s]?://www.instagram.com/explore/tags/[a-zA-Z0-9_]+", id
        )
        name = re.match("^[a-zA-Z0-9_]+", id)
    else:
        # Patterns for usernames.
        url = re.match(
            r"^http[s]?://www.instagram.com/[a-zA-Z0-9_\.]{2,30}[/]?$", id
        )
        name = re.match(r"^[a-zA-Z0-9_\.]{2,30}$", id)

    # Return full username or hashtag url.
    if url:
        return url.group()
    elif name and hashtag:
        return "https://www.instagram.com/explore/tags/" + name.group()
    elif name and not hashtag:
        return "https://www.instagram.com/" + name.group()
    # Shut down program if some unexpected error occurres.
    else:
        raise SystemExit(
            "Some error occurred, couldn't match username or hashtag."
        )


def is_working(url):
    """Check if URL is working."""

    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        raise SystemExit("Invalid URL")
    except requests.exceptions.ConnectionError:
        raise SystemExit("Connection error")
    except requests.exceptions.Timeout:
        raise SystemExit("Timeout")

    if r.status_code != 200:
        return False

    return True
