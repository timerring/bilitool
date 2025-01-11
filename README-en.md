# biliupload

English | [简体中文](./README.md)

> If you find this project useful, feel free to use it and :star: it, and provide more feedback and requests. Contributions via PR are welcome.

`biliupload` is a Python library for logging in, uploading, and downloading videos to Bilibili. It can be used via command line operations or as a library in other projects.

## Features

- Persistent memory storage of login status
  - Support exporting `cookies.json` for other projects
- `Logout` the current account
- `Check` the login status
- `Upload` videos
  - Support uploading videos with custom parameters
  - Support uploading videos with yaml config
- `Download` videos
  - Support downloading danmaku
  - Support downloading various qualities
  - Support downloading multi-part videos
- Show the upload progress (in development)
- Append videos to an existing video (in development)
- Show the published videos information (planned feature)

> Currently, I have implemented the `login` and `upload` functions and will continue to implement other features. Welcome to use and give me more feedback. And welcome to contribute to this project.

## Usage

### Installation

> Recommend Python version >= 3.10.

```bash
pip install biliupload
```

You can also download the compiled CLI tool directly to run. [Download address](https://github.com/timerring/biliupload/releases)

Help information:

```
usage: biliupload [-h] [-V] {login,logout,upload,check,download} ...

Python implementation of biliup

positional arguments:
  {login,logout,upload,check,download}
                        Subcommands
    login               Login and save the cookies
    logout              Logout the current account
    upload              Upload the video
    check               Check if the user is logged in
    download            Download the video

options:
  -h, --help            show this help message and exit
  -V, --version         Print version information
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

### Check Login Status

> Check the name of the currently logged-in account

```bash
biliupload check
```

### Logout

> After logging out, the `cookies.json` file will also become invalid (if the `--export` parameter was used to export cookies during login).

```bash
biliupload logout
```

### Upload

> Note: The upload function requires login first. After logging in, the login status will be remembered, and you do not need to log in again for the next upload.

`biliupload upload -h ` print help information:

```bash
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

You can refer to the [`template/example-config.yaml`](https://github.com/timerring/biliupload/tree/main/template/example-config.yaml) to know more about the yaml template.

```bash
# the video path is required
biliupload upload /path/to/your/video.mp4

# upload the video with command line parameters
biliupload upload /path/to/your/video.mp4 --title "test" --desc "test" --tid 138 --tag "test" --line bda2

# upload the video with yaml config
biliupload upload /path/to/your/video.mp4 -y /path/to/your/upload/template.yaml
```

### Download

> Note: To download videos in high quality or above, you need to log in first to obtain the download.

`biliupload download -h ` print help information:

```bash
usage: biliupload download [-h] [--danmaku] [--quality QUALITY] [--chunksize CHUNKSIZE] [--multiple] bvid

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
biliupload download bvid --danmaku --quality 80 --chunksize 1024 --multiple
```

## Acknowledgments

- Thanks to [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) for the API collection.
- Thanks to [biliup-rs](https://github.com/biliup/biliup-rs) for the inspiration.