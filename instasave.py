#!/usr/bin/env python

import argparse
import os.path

from instagram.post import Downloader
from instagram.url import URLScraper
from utils.client import HTTPHeaders
from utils.geckoloader import GeckoLoader
from utils.webaddr import get_url, validate_url


def get_arguments():
    """Get arguments passed to the program by the user."""

    name = "./instasave.py"
    usage = "%(prog)s [options] input"
    descr = (
        "Download images, videos and metadata from public Instagram posts."
        "Can scrape data from individual post's URL or multiple posts from a"
        "user or a hashtag page."
    )

    parser = argparse.ArgumentParser(prog=name, usage=usage, description=descr)
    parser.add_argument(
        "input",
        help=(
            "URL to post, users or hashtags."
            "A name is enough for users and hashtags."
        ),
    )
    parser.add_argument(
        "-o", "--output", metavar="PATH", help="Set custom download location."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show information about the posts that are being downloaded.",
    )
    parser.add_argument(
        "-p",
        "--post",
        type=int,
        default=0,
        metavar="LIMIT",
        help="Limit number of posts to download from a user or a hashtag.",
    )
    parser.add_argument(
        "-H",
        "--hashtag",
        action="store_true",
        help="Download posts from a hashtag page.",
    )

    return parser.parse_args()


def set_downloader(headers, output, verbose):
    """Prepare to download files."""

    # Set custom download location.
    if output:
        if not os.path.exists(output):
            raise SystemExit("Path doesn't exist.")
        return Downloader(headers, output, verbose=verbose)

    return Downloader(headers, verbose=verbose)


def main():
    """The programs main function."""

    # Command line arguments from user.
    args = get_arguments()

    # HTTP headers with random user agent for requests.
    http_req = HTTPHeaders()

    urls = [args.input]
    post_limit = args.post
    is_hashtag = args.hashtag
    is_verbose = args.verbose
    output_path = args.output
    headers = http_req.headers
    useragent = http_req.headers["User-Agent"]

    # Get latest geckdriver for the system if isn't already in path.
    GeckoLoader(headers, is_verbose)

    # Set custom download directory otherwise use current working directory.
    file = set_downloader(headers, output_path, is_verbose)
    output_path = file.output

    # Scrape post data from user or hashtag feed.
    if post_limit > 0:
        # Get full url to the username or hashtag.
        page_url = get_url(urls[0], is_hashtag)
        if page_url:
            webdriver = URLScraper(useragent, output_path)
            webdriver.open(page_url)
            urls = webdriver.scrape(post_limit, is_hashtag)
            webdriver.close()

    # Download files and save them to the output directory.
    for url in urls:
        post = validate_url(url)
        file.download(post)


if __name__ == "__main__":
    main()
