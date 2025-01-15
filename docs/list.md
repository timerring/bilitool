## 查询近期投稿视频状态

`bilitool list -h ` 打印帮助信息：

```bash
usage: bilitool list [-h] [--size SIZE] [--status STATUS]

options:
  -h, --help       show this help message and exit
  --size SIZE      (default is 20) the size of video list
  --status STATUS  (default is all) the status of video list: pubed, not_pubed, is_pubing
```

示例：

```bash
# 默认显示近期所有投稿的 20 条视频信息
bilitool list

# 查询近期投稿审核未通过的 10 条视频
bilitool list --size 10 --status not_pubed
```

打印返回格式

```
开放浏览 | BV1xxxxxxxxx | the video title
开放浏览 | BV1xxxxxxxxx | the video title
已退回 | BV1xxxxxxxxx | the video title | 拒绝原因: 根据相关法律法规和政策，该视频【P1(00:20:40-00:21:59)】不予审核通过
```