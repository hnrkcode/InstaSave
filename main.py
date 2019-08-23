import sys
import os.path
import argparse
import instagram
from url import clean, is_working


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
        post = instagram.PostScraper(args.output)
    else:
        post = instagram.PostScraper()

    # Clean and check that the url i working before downloading.
    post_url = clean(args.url)
    if not is_working(post_url):
        sys.exit("Sorry, this page isn't available.")
    post.download(post_url)


if __name__ == '__main__':
    main()
