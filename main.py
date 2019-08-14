import argparse
from url import CleanURL
from instascraper import get_post_data, download

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url to the Instagram post.")
    args = parser.parse_args()

    clean = CleanURL(args.url)
    data = get_post_data(clean.url)
    download(data)

if __name__ == '__main__':
    main()
