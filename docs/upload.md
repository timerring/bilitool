## 上传

> 注意：上传功能需要先登录，登录后会记忆登录状态，下次上传时不需要再次登录。

`bilitool upload -h ` 打印帮助信息：

```bash
usage: bilitool upload [-h] [-y YAML] [--copyright COPYRIGHT] [--title TITLE] [--desc DESC] [--tid TID] [--tag TAG] [--source SOURCE] [--cover COVER]
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
  --source SOURCE       (default is 来源于网络) The source of video (if your video is re-print)
  --cover COVER         (default is empty) The cover of video (if you want to customize, set it as the path to your cover image)
  --dynamic DYNAMIC     (default is empty) The dynamic information
```

示例：

你可以参考 [`template/example-config.yaml`](https://github.com/timerring/bilitool/tree/main/template/example-config.yaml) 了解更多的 yaml 模板。

```bash
# 视频路径是必需的
bilitool upload /path/to/your/video.mp4

# 使用命令行参数上传视频
bilitool upload /path/to/your/video.mp4 --title "test" --desc "test" --tid 138 --tag "test"

# 使用 yaml 配置上传视频
bilitool upload /path/to/your/video.mp4 -y /path/to/your/upload/template.yaml
```

上传日志过程日志格式：

```
[INFO] - [2025-01-15 20:43:40,489 bilitool] - The video name to be uploaded
[INFO] - [2025-01-15 20:43:40,489 bilitool] - Start preuploading the video
[INFO] - [2025-01-15 20:43:41,860 bilitool] - Completed preupload phase
[INFO] - [2025-01-15 20:43:41,860 bilitool] - Start uploading the video
[INFO] - [2025-01-15 20:43:42,007 bilitool] - Completed upload_id obtaining phase
[INFO] - [2025-01-15 20:43:42,007 bilitool] - Uploading the video in 4 batches
Uploading video: 100%|████████████████████████████████████████████████| 7.43M/7.43M [00:01<00:00, 4.80MB/s]
[INFO] - [2025-01-15 20:43:44,305 bilitool] - [video name]upload success!     bvid:BV1XXXXXXXX

# 如果错误，则最后一条INFO会改为错误信息等
[ERROR] - [2025-01-15 20:56:56,646 bilitool] - 标题只能包含中文、英文、数字，日文等可见符号
```