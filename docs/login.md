## 登录

```bash
bilitool login
```

然后你可以扫描二维码或点击链接登录，如果输入命令时加上 `--export` 参数，则会导出 `cookie.json` 文件到当前目录，该 `cookie.json` 文件可以用于其他项目。

> 注意，请勿将 `cookie.json` 文件泄露给他人，否则很可能会导致账号被盗。

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-01-08-11-54-34.png)

`bilitool login -h ` 打印帮助信息：

```
usage: bilitool login [-h] [--export]

options:
  -h, --help  show this help message and exit
  --export    (default is false) export the login cookie file
```

登录示例：

```bash
# 扫码登录
bilitool login

# 登录成功后同时导出一份 cookie.json 文件
bilitool login --export

# 登录成功后会出现
# Login success!
```
