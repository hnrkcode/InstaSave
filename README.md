# InstaSave

> Download images and videos from Instagram.

This Instagram scraper can download any public post on Instagram. If you want to download a specific post just enter it's url.

If you on the other hand want to scrape a public users feed or public posts with a certain hashtag, enter a username/hashtag or the the full url to the profile/hashtag and specify how many posts to download. The scraper then starts from the most recent post and ignores anything it has already saved.

So if you want to download posts from a users feed, you can for instance download the latest 15 posts and then stop. If you continue to scrape posts from the same users feed in the future, it will start by saving everything that has been uploaded since the last time and then save any posts after the originally 15 posts.

Downloaded files are organized in folders named `/downloads/username/upload_date/shortcode/`, which contains images, videos and metadata from the individual post. By default they are stored in the current working directory, but can be changed.

## Usage

Use any combination of the flags to get the desired output.

### Download specific posts:

Download image/video files from a public instagram posts url. The output is in the current directory.

```sh
./instasave.py [url]
```

### Set a custom download location:

To set a custom download location, use the `-o` or `--output` flags, which requires two arguments:

1. Path to an existing directory.

2. Directory name, which will be created if not already exists.

```sh
./instasave.py [url] -o ~/Desktop output_files
```

### Display more information:

To show information about what the program is doing, use the `-v` or `--verbose` flags.

```sh
./instasave.py [url] -v
```

### Scrape a users feed:

To download a certain number of posts from a users feed, starting from the most recent, use the `-p` or `--post` flags. `[username]` can be either just the username or the url to the users Instagram profile.

The `-p` flag only works if used along with a username or user profile url.

```sh
./instasave.py [username] -p [number]
```

### Scrape posts tagged with a certain hashtag:

Works almost exactly the same as if you would scrape a users feed, except that you also need to use the `-H` ir `--hashtag` flags.

```sh
./instasave.py [hashtag] -p [number] --hashtag
```

## Run tests

```sh
python -m unittest -v
```
