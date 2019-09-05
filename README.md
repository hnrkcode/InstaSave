# InstaSave

> Download images and videos from Instagram.

This Instagram scraper can download any public post on Instagram. If you want to download an individual post just enter it's url.

You can also scrape a public users feed or public posts with a certain hashtag. The scraper ignores posts it has already saved. So if you want to download a users whole feed, you can download the latest 15 posts at one time and continue at the 16th the next time.

All downloaded files are saved in folders named after the uploaders.

## Usage

**Download posts**

Download image/video files from a public instagram posts url. The output is in the current directory.

```sh
python instasave.py [url]
```

**Custom download location**

Use the `-o` or `--output` flags and path to where to save the output.

```sh
python instasave.py [url] -o ~/Desktop
```

**Display more information**

To show information about what the program is doing, use the `-v` or `--verbose` flags.

```sh
python instasave.py [url] -v
```

**Scrape a users feed**

To download a certain number of posts from a users feed, starting from the most recent, use the `-p` or `--posts` flags. `[username]` can be either just the username or the url to the users Instagram profile.

The `-p` flag only works if used along with a username or user profile url.

```sh
python instasave.py [username] -p [number]
```

**Scrape posts tagged with a certain #hashtag**

Works almost exactly the same as if you would scrape a users feed, except that you also need to use the `-t` ir `--hashtag` flags.

```sh
python instasave.py [hashtag] -p [number] --hashtag
```

## Run tests

```sh
python -m unittest -v
```
