## 下载

> 注意：如果要下载高清以上画质的视频，需要先登录才能获取下载。

`bilitool download -h ` 打印帮助信息：

```bash
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

示例：

```bash
# 默认下载视频
bilitool download bvid

# 下载序号为 bvid 的视频，并下载弹幕，设置画质为 1080p 高清，分段大小为 1024，如果有多 p，则一次性下载所有视频
bilitool download bvid --danmaku --quality 80 --chunksize 1024 --multiple
```

下载过程日志格式：

```
[INFO] - [2025-01-15 21:54:13,026 bilitool] - Begin download the video name
the video name.mp4: 100%|███████████████████████████████████████████████████████████████████████| 6.54M/6.54M [00:00<00:00, 9.74MB/s]
[INFO] - [2025-01-15 21:54:14,109 bilitool] - Download completed
[INFO] - [2025-01-15 21:54:14,112 bilitool] - Begin download danmaku
[INFO] - [2025-01-15 21:54:14,225 bilitool] - Successfully downloaded danmaku
```