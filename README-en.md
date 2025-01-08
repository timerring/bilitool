# biliupload

English | [简体中文](./README.md)

> This is a Python implementation of [biliup-rs](https://github.com/biliup/biliup-rs).

`biliupload` is a command line tool for logining and uploading videos to bilibili, which can also be used as a library for other projects.

## Features

- Save `cookies.json` for bilibili by scanning QR code or web login
- `Upload` videos
- Support uploading videos with yaml config
- `Append` videos to a existing video (WIP)
- `Show` the published videos infomation (planned feature)
- `Download` videos (planned feature)
- `Renew` the cookies (planned feature)
- Show the upload progress (planned feature)

> Over the passed few days, I have implemented the `login` and `upload` functions, and will continue to implement the other functions. Welcome to use and give me more feedback. And welcome to contribute to this project.

## Usage

### Installation

> Recommend Python version >= 3.10.

```bash
pip install biliupload
```

Help information:

```
usage: biliupload [-h] [-V] {login,upload} ...

Python implementation of biliup

positional arguments:
  {login,upload}  Subcommands
    login         login and save the cookies
    upload        upload the video

options:
  -h, --help      show this help message and exit
  -V, --version   Print version information
```

### Login

```bash
biliupload login
```
Then you can scan the QR code or click the link to login. The `cookie.json` will be saved in the current directory.

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-01-08-11-54-34.png)

### Upload

Help information:

```bash
$ biliupload upload -h
usage: biliupload upload [-h] -c COOKIES [-y YAML] [--copyright COPYRIGHT] [--title TITLE] [--desc DESC] [--tid TID] [--tags TAGS] [--line LINE] video_path

positional arguments:
  video_path            (required) the path to video file

options:
  -h, --help            show this help message and exit
  -c COOKIES, --cookies COOKIES
                        The path to cookies
  -y YAML, --yaml YAML  The path to yaml file(if yaml file is provided, the arguments below will be ignored)
  --copyright COPYRIGHT
                        (default is 2) 1 for original, 2 for reprint
  --title TITLE         (default is video name) The title of video
  --desc DESC           (default is empty) The description of video
  --tid TID             (default is 138) For more info to the type id, refer to https://biliup.github.io/tid-ref.html
  --tags TAGS           (default is biliupload) video tags, separated by comma
  --line LINE           (default is bda2) line refer to https://biliup.github.io/upload-systems-analysis.html
```

Example:

your can refer the [`template/example-config.yaml`](https://github.com/timerring/biliupload/tree/main/template/example-config.yaml) to know more about the yaml template.

```bash
# the video path and cookie path are required
biliupload upload /path/to/your/video.mp4 -c /path/to/your/cookie.json

# upload the video with command line parameters
biliupload upload /path/to/your/video.mp4 -c /path/to/your/cookie.json --title "test" --desc "test" --tid 138 --tags "test" --line bda2

# upload the video with yaml config
biliupload upload /path/to/your/video.mp4 -c /path/to/your/cookie.json -y /path/to/your/upload/template.yaml
```

## Acknowledgments

- Thanks to [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) for the API collection.
- Thanks to [biliup-rs](https://github.com/biliup/biliup-rs) for the inspiration.
