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

You can also download the compiled cli tool directly to run. [download address](https://github.com/timerring/biliupload/releases)

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

Then you can scan the QR code or click the link to login. If you add the `--export` parameter when inputting the command, the `cookie.json` file will be exported to the current directory (the `cookie.json` file can be used for other projects).

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-01-08-11-54-34.png)

`biliupload login -h ` print help information:

```
usage: biliupload login [-h] [--export]

options:
  -h, --help  show this help message and exit
  --export    (default is false) export the login cookie file
```

### Upload

`biliupload upload -h ` print help information:

```bash
$ biliupload upload -h
usage: biliupload upload [-h] [-y YAML] [--copyright COPYRIGHT] [--title TITLE] [--desc DESC] [--tid TID] [--tag TAG] [--line LINE] [--source SOURCE] [--cover COVER]
                         [--dynamic DYNAMIC]
                         video_path

positional arguments:
  video_path            (required) the path to video file

options:
  -h, --help            show this help message and exit
  -y YAML, --yaml YAML  The path to yaml file(if yaml file is provided, the arguments below will be ignored)
  --copyright COPYRIGHT
                        (default is 2) 1 for original, 2 for reprint
  --title TITLE         (default is video name) The title of video
  --desc DESC           (default is empty) The description of video
  --tid TID             (default is 138) For more info to the type id, refer to https://biliup.github.io/tid-ref.html
  --tag TAG             (default is biliupload) video tags, separated by comma
  --line LINE           (default is bda2) line refer to https://biliup.github.io/upload-systems-analysis.html
  --source SOURCE       (default is 来源于网络) The source of video (if your video is re-print)
  --cover COVER         (default is empty) The cover of video (if you want to customize, set it as the path to your cover image)
  --dynamic DYNAMIC     (default is empty) The dynamic information
```

Example:

your can refer the [`template/example-config.yaml`](https://github.com/timerring/biliupload/tree/main/template/example-config.yaml) to know more about the yaml template.

```bash
# the video path is required
biliupload upload /path/to/your/video.mp4

# upload the video with command line parameters
biliupload upload /path/to/your/video.mp4 --title "test" --desc "test" --tid 138 --tag "test" --line bda2

# upload the video with yaml config
biliupload upload /path/to/your/video.mp4 -y /path/to/your/upload/template.yaml
```

## Acknowledgments

- Thanks to [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) for the API collection.
- Thanks to [biliup-rs](https://github.com/biliup/biliup-rs) for the inspiration.
