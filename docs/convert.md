
## 查询转换视频编号

`bilitool convert -h ` 打印帮助信息：

```bash
usage: bilitool convert [-h] vid

positional arguments:
  vid         The avid or bvid of the video

options:
  -h, --help  show this help message and exit
```

示例：

```bash
# 转换视频编号
# 输入 bvid 输出 avid
bilitool convert BV1BpcPeqE2p
# 输出格式
# The avid of the video is:  113811163974247

# 输入 avid 输出 bvid
bilitool convert 113811163974247
# 输出格式
# The bvid of the video is:  BV1BpcPeqE2p
```