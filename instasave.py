import argparse
import os.path

from instagram.post import Downloader
from instagram.url import URLScraper
from utils.geckoloader import GeckoLoader
from utils.helpers import HTTPHeaders, clean, is_user, url_exists
from utils.settings import USER_AGENT_FILE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    parser.add_argument("-o", "--output", help="Custom output path.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print download information.")
    parser.add_argument("-p", "--posts", type=int)
    parser.add_argument("-t", "--hashtag", action="store_true", help="Scrape posts under a hashtag.")
    args = parser.parse_args()

    # Current HTTP headers with random user agent.
    current = HTTPHeaders(USER_AGENT_FILE)
    # Get latest geckdriver for the system if isn't already in path.
    GeckoLoader(current.headers)
    # List of urls to posts that will be downloaded.
    url_list = [args.url]

    # Set custom download directory otherwise use current working directory.
    if args.output:
        # Check if the output path exists.
        if not os.path.exists(args.output):
            sys.exit("Path doesn't exist.")
        file = Downloader(current.headers, args.output, verbose=args.verbose)
    else:
        file = Downloader(current.headers, verbose=args.verbose)

    # Scrape a given number of post urls from a users feed.
    if args.posts:
        input = None
        if args.hashtag:
            input = "https://www.instagram.com/explore/tags/" + args.url
        else:
            input = is_user(args.url)

        if input:
            webdriver = URLScraper(current.headers["User-Agent"])
            webdriver.open(input)
            url_list = webdriver.scrape(args.posts, args.hashtag)
            webdriver.close()

    # Download files and save them to the output directory.
    for url in url_list:
        # Clean and check that the url i working before downloading.
        post_url = clean(url)
        if not url_exists(post_url):
            raise SystemExit("Sorry, this page isn't available.")
        file.download(post_url)


if __name__ == '__main__':
    main()
