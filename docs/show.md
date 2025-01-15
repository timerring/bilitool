
## 查询视频详细信息

`bilitool show -h ` 打印帮助信息：

```bash
usage: bilitool show [-h] bvid

positional arguments:
  vid         The avid or bvid of the video

options:
  -h, --help  show this help message and exit
```

示例：

```bash
# 查询视频详细信息
# bvid 查询
bilitool show BV1BpcPeqE2p

# avid 查询
bilitool show 113811163974247
```

查询结果格式：

```
标题: 【MrBeast公益】我帮助2000人重新行走！
描述: 全球首发视频都在这里 记得关注哦
时长: 30:36
发布日期: 2025-01-12 04:05:00
作者名称: MrBeast官方账号
分区: 日常
版权: 原创
宽: 1920
高: 1080
观看数: 986457
弹幕数: 26129
评论数: 2612
硬币数: 90428
分享数: 1529
点赞数: 213320
```