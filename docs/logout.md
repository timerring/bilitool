## 退出登录

> 退出登录后，同时会使 `cookies.json` 文件失效（如果登录时使用了 `--export` 参数导出了 cookies）。

```bash
bilitool logout

# 成功退出后会显示
# Logout successfully, the cookie has expired

# 退出失败则会显示
# Logout failed, check the info: XXX
```