import argparse
import os.path

from instagram.post import Downloader
from instagram.url import URLScraper
from utils.client import HTTPHeaders
from utils.geckoloader import GeckoLoader
from utils.webaddr import clean_url, get_url, url_exists


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    parser.add_argument("-o", "--output", help="Custom output path.")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print download information."
    )
    parser.add_argument("-p", "--posts", type=int)
    parser.add_argument(
        "-t", "--hashtag", action="store_true", help="Scrape posts under a hashtag."
    )

    return parser.parse_args()


def set_downloader(headers, output, verbose):
    if output:
        if not os.path.exists(output):
            raise SystemExit("Path doesn't exist.")
        return Downloader(headers, output, verbose=verbose)

    return Downloader(headers, verbose=verbose)


def main():
    # Get command line arguments.
    args = get_arguments()
    # Current HTTP headers with random user agent.
    current = HTTPHeaders()
    # Get latest geckdriver for the system if isn't already in path.
    GeckoLoader(current.headers)
    # List of urls to posts that will be downloaded.
    url_list = [args.url]
    # Set custom download directory otherwise use current working directory.
    file = set_downloader(current.headers, args.output, args.verbose)

    # Scrape user's or hashtag's feed.
    if args.posts:
        url = get_url(args.url, args.hashtag)
        if url:
            webdriver = URLScraper(current.headers["User-Agent"], file.output)
            webdriver.open(url)
            url_list = webdriver.scrape(args.posts, args.hashtag)
            webdriver.close()

    # Download files and save them to the output directory.
    for url in url_list:
        # Clean and check that the url i working before downloading.
        post_url = clean_url(url)
        if not url_exists(post_url):
            raise SystemExit("Sorry, this page isn't available.")
        file.download(post_url)


if __name__ == "__main__":
    main()
