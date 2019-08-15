import sys
import os.path
import argparse
import instagram
from url import CleanURL


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    parser.add_argument("-o", "--output", help="Custom output path.")
    args = parser.parse_args()

    clean = CleanURL(args.url)

    if args.output:
        # Check if the output path exists.
        if not os.path.exists(args.output):
            sys.exit("Path doesn't exist.")
        post = instagram.PostScraper(args.output)
    else:
        post = instagram.PostScraper()

    post.download(clean.url)


if __name__ == '__main__':
    main()
