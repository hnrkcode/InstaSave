# InstaSave

Download images and videos from Instagram.

## Usage

Download image/video files from a public instagram posts url. The output is in the current directory.

```sh
python instasave.py [url]
```

Use the `-o` or `--output` flags and path to where to save the output.

```sh
python instasave.py [url] -o ~/Desktop
```

To show information about what the program is doing, use the `-v` or `--verbose` flags.

```sh
python instasave.py [url] -v
```

## Run tests

```sh
python -m unittest -v
```
