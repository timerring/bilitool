
## 查询 IP 地址

`bilitool ip -h ` 打印帮助信息：

```bash
usage: bilitool ip [-h] [--ip IP]

options:
  -h, --help  show this help message and exit
  --ip IP     the ip address you want to query
```

示例：

> 由于国内网络搭建的历史原因以及复杂性，查询 IP 普遍有误差，这也是为什么 IP 结果只能精确到省的原因。详细内容可以参考 IPIP 创始人高春辉的微信公众号。

```bash
# 默认查询本机 IP
bilitool ip
# 输出格式
# IP: 183.xxx.xxx.xxx, ISP: 移动, Location: 中国广东广州, Position: xx.xxxx,xxx.xxxxxx

# 查询指定 IP
bilitool ip --ip 8.8.8.8
# 输出格式
# IP: 8.8.8.8, ISP: level3.com, Location: GOOGLE.COMGOOGLE.COM, Position: ,
```