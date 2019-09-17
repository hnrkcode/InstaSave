# InstaSave

> Download images and videos from Instagram in a structured way.

This Instagram scraper can download public posts from Instagram, which means images and videos from posts, users, or hashtag pages.

The scraper remembers which posts that has been scraped and ignores them if encountered again.

The downloaded files are by default organized in a directory named `downloads` in the projects root directory, but the output directory's name and path can be changed, if desired.

To easier get an overview of downloaded posts, metadata about them are saved in `data.csv` which is located in the output folders root directory.

## Setup

#### Install & uninstall package

```sh
pip install .
```
```sh
pip uninstall instasave
```

#### Editable mode install

Install package in editable mode to be able to develop and test the code without uninstall and reinstall over and over again.

```sh
pip install -e .
```


## Usage

`instasave [options] input`

Use any combination of the options in the table below together with the input value. A name is sufficient for users and hashtags, but posts needs a full url.

| short opt |  long opt  |       args       |         descr           |
|:---------:|------------|------------------|-------------------------|
| `-h`      | `--help`   | None             | Show usage information  |
| `-o`      | `--output` | [path] [dirname] | custom output location  |
| `-v`      | `--verbose`| None             | show more information   |
| `-p`      | `--posts`  | [limit]          | download this many posts|
| `-H`      | `--hashtag`| None             | download posts from hashtag page, used together with `-p`, `--post`|


## Examples

#### Download specific posts

Download image/video files from a public instagram posts url. The output is in the current directory.

```sh
instasave [url]
```

#### Set a custom download location

To set a custom download location, use the `-o` or `--output` flags, which requires two arguments:

1. Path to an existing directory in the file system (e.g. ~/Desktop).

2. Name of output directory (e.g. output), will be created if not already exists.

```sh
instasave [url] -o [path] [dirname]
```

#### Display more information

To show information about what the program is doing, use the `-v` or `--verbose` flags.

```sh
instasave [url] -v
```

#### Scrape a users feed

To download a certain number of posts from a users feed, starting from the most recent, use the `-p` or `--post` flags. `[username]` can be either just the username or the url to the users Instagram profile.

The `-p` flag only works if used along with a username or user profile url.

```sh
instasave [username] -p [number]
```

#### Scrape posts tagged with a certain hashtag

Works almost exactly the same as if you would scrape a users feed, except that you also need to use the `-H` ir `--hashtag` flags.

```sh
instasave [hashtag] -p [number] --hashtag
```

## Run tests

```sh
python -m unittest -v
```
