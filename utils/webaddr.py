import re

import requests


def clean_url(url):
    """Return clean post URL.

    Removes UTM code after a URL that belongs to an Instagram post. Otherwise,
    an error will be raised.

    Args:
        url (str): URL string, should lead to a public instagram post.

    Returns:
        str: Post url without tracking code at the end.

    Raises:
        SystemExit: If URL didn't match the pattern of a post URL.

    """
    # Pattern that match a link to an Instagram post.
    match = re.match("^http[s]?://www.instagram.com/p/[a-zA-Z0-9_-]{11}", url)
    # Shut down the program if the URL didn't match the pattern.
    if not match:
        raise SystemExit("Didn't match a post url.")
    # If the link had any UTM code, it's now removed.
    clean_url = match.group()

    return clean_url


def get_url(id, hashtag):
    """Return URL to a hashtag or a user.

    Args:
        id (str): Username or hashtag name.
        hashtag (bool): Is hashtag if True, otherwise it's a username.

    Returns:
        str: URL if it's a hashtag or a username.

    Raises:
        SystemExit: If the result wasn't a username or a hashtag.

    """
    if hashtag:
        # Pattern for hashtags.
        url = re.match("^http[s]?://www.instagram.com/explore/tags/[a-zA-Z0-9_]+", id)
        name = re.match("^[a-zA-Z0-9_]+", id)
    else:
        # Patterns for usernames.
        url = re.match(r"^http[s]?://www.instagram.com/[a-zA-Z0-9_\.]{2,30}[/]?$", id)
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
        raise SystemExit("Some error occurred, couldn't match username or hashtag.")


def is_working(url):
    """Check if URL is working.

    If the request didn't return OK, it probably returned NOT FOUND. That could
    indicate that the link has been removed, belongs to a private account or
    never existed.

    Args:
        url (str): URL to test.

    Returns:
        bool: True if response is OK (200), False in all other cases.

    Raises:
        requests.exceptions.MissingSchema: Not a URL.
        requests.exceptions.ConnectionError: Connection problem.
        requests.exceptions.Timeout: Took too long to get a response.

    """
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
