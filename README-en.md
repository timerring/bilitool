# bilitool

[简体中文](./README.md) | English

> Welcome to use, feel free to provide feedback, and contribute to this project via PR.

`bilitool` is a Python toolkit for logging in, downloading videos, uploading videos to Bilibili, and more. It can be operated via command-line CLI or used as a library in other projects.

## Features

- `login` Remember and store login status
  - Supports exporting `cookies.json` for use in other projects
- `logout` Log out
- `check` Check login status
- `upload` Upload videos
  - Supports various custom parameters for uploading
  - Supports YAML configuration and parsing for video uploads
- `download` Download videos
  - Supports downloading danmaku (comments)
  - Supports downloading in various qualities
  - Supports downloading multi-part videos
- `ip` Display request IP address
  - Supports querying specified IP addresses
- `list` Query the status of past video submissions
  - If a video fails review, the reason will be displayed
- Display published video information (planned support)
- Display upload progress (in development)
- Append videos to existing videos (in development)

## Usage

### Installation

> Recommended Python version >= 3.10.

```bash
pip install bilitool
```

Alternatively, you can download the compiled CLI tool and run it directly [Download link](https://github.com/timerring/bilitool/releases).

Help information:

```
usage: bilitool [-h] [-V] {login,logout,upload,check,download,list,ip} ...

The Python toolkit package and cli designed for interaction with Bilibili

positional arguments:
  {login,logout,upload,check,download,list,ip}
                        Subcommands
    login               Login and save the cookie
    logout              Logout the current account
    upload              Upload the video
    check               Check if the user is logged in
    download            Download the video
    list                Get the uploaded video list
    ip                  Get the ip info

options:
  -h, --help            show this help message and exit
  -V, --version         Print version information
```

### Login

```bash
bilitool login
```

Then you can scan the QR code or click the link to log in. If you add the `--export` parameter when entering the command, a `cookie.json` file will be exported to the current directory (the `cookie.json` file can be used in other projects).

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-01-08-11-54-34.png)

`bilitool login -h` prints help information:

```
usage: bilitool login [-h] [--export]

options:
  -h, --help  show this help message and exit
  --export    (default is false) export the login cookie file
```

### Check Login Status

> Check the name of the currently logged-in account

```bash
bilitool check
```

### Logout

> Logging out will also invalidate the `cookies.json` file (if the `--export` parameter was used to export cookies during login).

```bash
bilitool logout
```

### Upload

> Note: The upload function requires login first. After logging in, the login status will be remembered, so you don't need to log in again for the next upload.

`bilitool upload -h` prints help information:

```
usage: bilitool upload [-h] [-y YAML] [--copyright COPYRIGHT] [--title TITLE] [--desc DESC] [--tid TID] [--tag TAG] [--line LINE] [--source SOURCE] [--cover COVER]
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
  --tag TAG             (default is bilitool) video tags, separated by comma
  --line LINE           (default is bda2) line refer to https://biliup.github.io/upload-systems-analysis.html
  --source SOURCE       (default is 来源于网络) The source of video (if your video is re-print)
  --cover COVER         (default is empty) The cover of video (if you want to customize, set it as the path to your cover image)
  --dynamic DYNAMIC     (default is empty) The dynamic information
```

Example:

You can refer to [`template/example-config.yaml`](https://github.com/timerring/bilitool/tree/main/template/example-config.yaml) for more YAML templates.

```bash
# The video path is required
bilitool upload /path/to/your/video.mp4

# Upload video using command-line parameters
bilitool upload /path/to/your/video.mp4 --title "test" --desc "test" --tid 138 --tag "test" --line bda2

# Upload video using YAML configuration
bilitool upload /path/to/your/video.mp4 -y /path/to/your/upload/template.yaml
```

### Download

> Note: To download videos in high quality or above, you need to log in first to obtain the download.

`bilitool download -h` prints help information:

```
usage: bilitool download [-h] [--danmaku] [--quality QUALITY] [--chunksize CHUNKSIZE] [--multiple] bvid

positional arguments:
  bvid                  (required) the bvid of video

options:
  -h, --help            show this help message and exit
  --danmaku             (default is false) download the danmaku of video
  --quality QUALITY     (default is 64) the resolution of video
  --chunksize CHUNKSIZE
                        (default is 1024) the chunk size of video
  --multiple            (default is false) download the multiple videos if have set
```

Example:

```bash
# Download the video with bvid, download danmaku, set quality to 1080p HD, chunk size to 1024, and download all videos if there are multiple parts
bilitool download bvid --danmaku --quality 80 --chunksize 1024 --multiple
```

### Query Recent Video Submission Status

`bilitool list -h` prints help information:

```
usage: bilitool list [-h] [--size SIZE] [--status STATUS]

options:
  -h, --help       show this help message and exit
  --size SIZE      (default is 20) the size of video list
  --status STATUS  (default is all) the status of video list: pubed, not_pubed, is_pubing
```

Example:

```bash
# By default, display the recent 20 video submissions
bilitool list
# Query the recent 10 video submissions that failed review
bilitool list --size 10 --status not_pubed
```

### Query IP Address

`bilitool ip -h` prints help information:

```
usage: bilitool ip [-h] [--ip IP]

options:
  -h, --help  show this help message and exit
  --ip IP     the ip address you want to query
```

Example:

```bash
bilitool ip
bilitool ip --ip 8.8.8.8
# IP: 8.8.8.8, ISP: level3.com, Location: GOOGLE.COMGOOGLE.COM, Position: ,
```

## Acknowledgments

- Thanks to [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) for providing the API collection.
- Thanks to [biliup-rs](https://github.com/biliup/biliup-rs) for providing direction.