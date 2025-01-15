# bilitool

[简体中文](./README.md) | English

> Welcome to use, provide feedback, and contribute to this project via PRs. Please do not use it for purposes that violate community guidelines.

`bilitool` is a Python toolkit that provides features such as persistent login, video download, and video upload to Bilibili. It can be used via command-line interface (CLI) or as a library in other projects.

## Major features

- `bilitool login` remembers and stores login status
  - Supports exporting `cookies.json` for use in other projects
- `bilitool logout` logs out
  - Logs out and clears cookies to protect privacy and prevent leaks
- `bilitool check` checks login status
- `bilitool upload` uploads videos
  - Supports various custom parameters for upload
  - Supports YAML configuration and parsing for video uploads
  - Displays logs and upload progress
- `bilitool download` downloads videos
  - Supports downloading by `bvid` and `avid`
  - Supports downloading comments
  - Supports downloading in various qualities
  - Supports downloading multi-part videos
  - Displays logs and download progress
- `bilitool list` queries the status of past uploaded videos on the account
  - Supports querying videos with various statuses
  - If a video fails review, the reason is displayed
- `bilitool convert` converts video IDs
  - Supports conversion between `bvid` and `avid`
- `bilitool show` displays detailed video information
  - Supports viewing basic video information and interaction status data
- `bilitool ip` displays the request IP address
  - Supports querying specified IP addresses
- Append videos to existing videos (planned support)

> Add `-h` or `--help` to the above commands to view command help information.
> 
> For more detailed commands, refer to [the documentation](https://bilitool.timerring.com).

## Installation

> Recommended Python version >= 3.10.

```bash
pip install bilitool
```

Alternatively, you can download the compiled CLI tool and run it directly [Download link](https://github.com/timerring/bilitool/releases).

## Usage

### CLI Method

> For more detailed commands, refer to [the documentation](https://bilitool.timerring.com), which is not elaborated here.

Help information:

```
usage: bilitool [-h] [-V] {login,logout,upload,check,download,list,ip} ...

The Python toolkit package and CLI designed for interaction with Bilibili

positional arguments:
  {login,logout,upload,check,download,list,show,convert,ip}
                        Subcommands
    login               Login and save the cookie
    logout              Logout the current account
    upload              Upload the video
    check               Check if the user is logged in
    download            Download the video
    list                Get the uploaded video list
    show                Show the video detailed info
    convert             Convert between avid and bvid
    ip                  Get the IP info

options:
  -h, --help            show this help message and exit
  -V, --version         Print version information
```

### API Method

Currently being updated and will be available soon.

## Acknowledgments

- Thanks to [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) for providing the API collection.