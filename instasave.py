import argparse
import os.path

from instagram.post import Downloader
from utils.helpers import HTTPHeaders, clean, url_exists
from utils.settings import USER_AGENT_FILE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    parser.add_argument("-o", "--output", help="Custom output path.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print download information.")
    args = parser.parse_args()

    # Current HTTP headers with random user agent.
    current = HTTPHeaders(USER_AGENT_FILE)

    # Custom download directory.
    if args.output:
        # Check if the output path exists.
        if not os.path.exists(args.output):
            sys.exit("Path doesn't exist.")
        file = Downloader(current.headers, args.output, verbose=args.verbose)
    else:
        file = Downloader(current.headers, verbose=args.verbose)

    # Clean and check that the url i working before downloading.
    post_url = clean(args.url)
    if not url_exists(post_url):
        raise SystemExit("Sorry, this page isn't available.")
    file.download(post_url)


if __name__ == '__main__':
    main()
