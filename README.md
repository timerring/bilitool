# bilitool

简体中文 | [English](./README-en.md)

> 欢迎使用，欢迎提供更多反馈，欢迎 PR 贡献此项目，请勿用于违反社区规定的用途。

`bilitool` 是一个 python 的工具库，实现持久化登录，下载视频，上传视频到 bilibili 等功能，可以使用命令行 cli 操作，也可以作为其他项目的库使用。

## Major features

- `bilitool login` 记忆存储登录状态
  - 支持导出 `cookies.json` 用于其他项目
- `bilitool logout` 退出登录
  - 退出登录同时注销 cookies，保护隐私防止泄露
- `bilitool check` 检查登录状态
- `bilitool upload` 上传视频
  - 支持多种自定义参数上传
  - 支持上传视频的 yaml 配置与解析
  - 显示日志与上传进度
- `bilitool download` 下载视频
  - 支持 `bvid` 和 `avid` 两种编号下载
  - 支持下载弹幕
  - 支持下载多种画质
  - 支持下载多 p 视频
  - 显示日志与下载进度
- `bilitool list` 查询本账号过往投稿视频状态
  - 支持查询多种状态的视频
  - 若视频审核未通过，同时会显示原因
- `bilitool convert` 查询转换视频编号
  - 支持 `bvid` 和 `avid` 两种编号互转
- `bilitool show` 显示视频详细信息
  - 支持查看视频基本信息以及互动状态数据
- `bilitool ip` 显示请求 IP 地址
  - 支持查询指定 IP 地址
- 追加视频到已有的视频（预计支持）

> 以上命令添加 `-h` 或 `--help` 参数可以查看命令帮助信息。
> 
> 更详细的命令可以参考[项目文档](https://bilitool.timerring.com)。

## Installation

> 推荐 Python 版本 >= 3.10.

```bash
pip install bilitool
```

或者你也可以下载编译好的 cli 工具直接运行 [下载地址](https://github.com/timerring/bilitool/releases)。

## Usage

### cli 方式

> 更详细的命令可以参考[项目文档](https://bilitool.timerring.com)，这里不赘述。

帮助信息：

```
usage: bilitool [-h] [-V] {login,logout,upload,check,download,list,ip} ...

The Python toolkit package and cli designed for interaction with Bilibili

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
    ip                  Get the ip info

options:
  -h, --help            show this help message and exit
  -V, --version         Print version information
```

### 接口调用方式

正在更新，即将开放。

## Acknowledgments

- 感谢 [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) 提供的 API 集合。
