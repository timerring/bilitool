# biliupload

简体中文 | [English](./README-en.md)

> 这是一个 python 版本实现的 [biliup-rs](https://github.com/biliup/biliup-rs)。

`biliupload` 是一个 python 的命令行工具，用于登录和上传视频到 bilibili，也可以作为其他项目的库使用。

## 功能

- 持久记忆存储登录状态
  - 支持导出 `cookies.json` 用于其他项目
- 退出登录 `logout`
- 检查登录状态 `check`
- 上传视频 `upload`
  - 支持多种自定义参数上传
  - 支持上传视频的 yaml 配置与解析
- 下载视频 `download`
  - 支持下载弹幕
  - 支持下载多种画质
  - 支持下载多 p 视频
- 显示上传进度（正在开发）
- 追加视频到已有的视频（正在开发）
- 显示已发布的视频信息（预计支持）

> 目前我实现了 `login` 和 `upload` 功能，并会继续实现其他功能。欢迎使用并给我更多反馈。欢迎贡献此项目。

## 使用方法

### 安装

> 推荐 Python 版本 >= 3.10.

```bash
pip install biliupload
```

或者你也可以下载编译好的 cli 工具直接运行 [下载地址](https://github.com/timerring/biliupload/releases)。

帮助信息：

```
usage: biliupload [-h] [-V] {login,logout,upload,check,download} ...

Python implementation of biliup

positional arguments:
  {login,logout,upload,check,download}
                        Subcommands
    login               Login and save the cookie
    logout              Logout the current account
    upload              Upload the video
    check               Check if the user is logged in
    download            Download the video

options:
  -h, --help            show this help message and exit
  -V, --version         Print version information
```

### 登录

```bash
biliupload login
```

然后你可以扫描二维码或点击链接登录，如果输入命令时加上 `--export` 参数，则会导出 `cookie.json` 文件到当前目录（cookie.json 文件可以用于其他项目）。

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-01-08-11-54-34.png)

`biliupload login -h ` 打印帮助信息：

```
usage: biliupload login [-h] [--export]

options:
  -h, --help  show this help message and exit
  --export    (default is false) export the login cookie file
```

### 检查登录状态

> 检查当前登录的账号名称

```bash
biliupload check
```

### 退出登录

> 退出登录后，同时会使 `cookies.json` 文件失效（如果登录时使用了 `--export` 参数导出了 cookies）。

```bash
biliupload logout
```

### 上传

> 注意：上传功能需要先登录，登录后会记忆登录状态，下次上传时不需要再次登录。

`biliupload upload -h ` 打印帮助信息：

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

示例：

你可以参考 [`template/example-config.yaml`](https://github.com/timerring/biliupload/tree/main/template/example-config.yaml) 了解更多的 yaml 模板。

```bash
# 视频路径是必需的
biliupload upload /path/to/your/video.mp4

# 使用命令行参数上传视频
biliupload upload /path/to/your/video.mp4 --title "test" --desc "test" --tid 138 --tag "test" --line bda2

# 使用 yaml 配置上传视频
biliupload upload /path/to/your/video.mp4 -y /path/to/your/upload/template.yaml
```

### 下载

> 注意：如果要下载高清以上画质的视频，需要先登录才能获取下载。

`biliupload download -h ` 打印帮助信息：

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

示例：

```bash
# 下载序号为 bvid 的视频，并下载弹幕，设置画质为 1080p 高清，分段大小为 1024，如果有多 p，则一次性下载所有视频
biliupload download bvid --danmaku --quality 80 --chunksize 1024 --multiple
```

## Acknowledgments

- 感谢 [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 提供的 API 集合。
- 感谢 [biliup-rs](https://github.com/biliup/biliup-rs) 提供的灵感。
