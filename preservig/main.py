import os.path
import argparse
from instagram.post import Downloader
from helpers import clean, url_exists


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    parser.add_argument("-o", "--output", help="Custom output path.")
    args = parser.parse_args()

    # Custom download directory.
    if args.output:
        # Check if the output path exists.
        if not os.path.exists(args.output):
            sys.exit("Path doesn't exist.")
        file = Downloader(args.output)
    else:
        file = Downloader()

    # Clean and check that the url i working before downloading.
    post_url = clean(args.url)
    if not url_exists(post_url):
        raise SystemExit("Sorry, this page isn't available.")
    file.download(post_url)


if __name__ == '__main__':
    main()
