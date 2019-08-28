import os.path
import argparse
from instagram.post import Downloader
from helpers import clean, url_exists, HTTPHeaders
from settings import USER_AGENT_FILE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    parser.add_argument("-o", "--output", help="Custom output path.")
    args = parser.parse_args()

    # Current HTTP headers with random user agent.
    current = HTTPHeaders(USER_AGENT_FILE)

    # Custom download directory.
    if args.output:
        # Check if the output path exists.
        if not os.path.exists(args.output):
            sys.exit("Path doesn't exist.")
        file = Downloader(current.headers, args.output)
    else:
        file = Downloader(current.headers)

    # Clean and check that the url i working before downloading.
    post_url = clean(args.url)
    if not url_exists(post_url):
        raise SystemExit("Sorry, this page isn't available.")
    file.download(post_url)


if __name__ == '__main__':
    main()

    #from instagram.post import PostScraper
    #current = HTTPHeaders(USER_AGENT_FILE)
    #p = PostScraper(current.headers)
    #print(p.post_data("https://www.instagram.com/p/B0LqiitHLSC/"))
