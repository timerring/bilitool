---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "bilitool"
  text: "Official documentation"
  tagline: The Python toolkit package and cli designed for interaction with Bilibili.
  actions:
    - theme: brand
      text: 现在开始
      link: /getting-start
    - theme: alt
      text: 在 GitHub 上查看
      link: https://github.com/timerring/bilitool

features:
  - title: 持久化登录
    details: 记忆存储登录状态，支持导出 `cookies.json` 用于其他项目
  - title: 保护隐私
    details: 退出登录同时注销 cookies，保护隐私信息防止泄露
  - title: 检查登录状态
    details: 检查当前登录的账号名称
  - title: 上传视频
    details: 支持多种自定义参数上传
  - title: 下载视频
    details: 支持多编号，多画质，弹幕，多 p 视频下载
  - title: 查询视频详细信息
    details: 支持查询视频详细信息以及互动状态数据
  - title: 查询转换视频编号
    details: 支持 `bvid` 和 `avid` 两种编号互转
  - title: 查询 IP 地址
    details: 支持查询请求 IP 地址以及指定 IP 地址
---

