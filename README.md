# biliupload

简体中文 | [English](./README-en.md)

> 这是一个 python 版本实现的 [biliup-rs](https://github.com/biliup/biliup-rs)。

`biliupload` 是一个 python 的命令行工具，用于登录和上传视频到 bilibili，也可以作为其他项目的库使用。

## 功能

- 保存 `cookies.json` 用于 bilibili 登录
- 上传视频
- 支持上传视频的 yaml 配置
- 追加视频到已有的视频（正在开发）
- 显示已发布的视频信息（预计支持）
- 下载视频（预计支持）
- 更新 cookies（预计支持）
- 显示上传进度（预计支持）

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

### 登录

```bash
biliupload login
```
然后你可以扫描二维码或点击链接登录，`cookie.json` 将保存在当前目录。

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-01-08-11-54-34.png)

### 上传

`biliupload upload -h ` 打印帮助信息：

```bash
$ biliupload upload -h
usage: biliupload upload [-h] -c COOKIES [-y YAML] [--copyright COPYRIGHT] [--title TITLE] [--desc DESC] [--tid TID] [--tag TAG] [--line LINE] video_path

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
  --tag TAG             (default is biliupload) video tags, separated by comma
  --line LINE           (default is bda2) line refer to https://biliup.github.io/upload-systems-analysis.html
```

示例：

你可以参考 [`template/example-config.yaml`](https://github.com/timerring/biliupload/tree/main/template/example-config.yaml) 了解更多的 yaml 模板。

```bash
# 视频路径和 cookie 路径是必需的
biliupload upload /path/to/your/video.mp4 -c /path/to/your/cookie.json

# 使用命令行参数上传视频
biliupload upload /path/to/your/video.mp4 -c /path/to/your/cookie.json --title "test" --desc "test" --tid 138 --tag "test" --line bda2

# 使用 yaml 配置上传视频
biliupload upload /path/to/your/video.mp4 -c /path/to/your/cookie.json -y /path/to/your/upload/template.yaml
```

## Acknowledgments

- 感谢 [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 提供的 API 集合。
- 感谢 [biliup-rs](https://github.com/biliup/biliup-rs) 提供的灵感。
