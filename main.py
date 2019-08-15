import argparse
import instagram
from url import CleanURL


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    args = parser.parse_args()
    clean = CleanURL(args.url)
    post = instagram.PostScraper()
    post.download(clean.url)


if __name__ == '__main__':
    main()
