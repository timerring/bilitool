# Copyright (c) 2025 bilitool

import json
import os


def add_headers_info(referer=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            headers = func(self, *args, **kwargs)
            config_info = self.get_config()
            cookies = config_info['cookies']
            cookie_string = "; ".join([f"{key}={value}" for key, value in cookies.items() if value])
            headers['Cookie'] = cookie_string
            if referer:
                headers['Referer'] = referer
            return headers
        return wrapper
    return decorator

class ioer:
    def __init__(self, path=None) -> None:
        if path is None:
            self.path = os.path.join(os.path.dirname(__file__), "config.json")
        else:
            self.path = path
        self.default_config = {
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            },
            "cookies": {
                "SESSDATA": "",
                "bili_jct": "",
                "DedeUserID": "",
                "DedeUserID__ckMd5": ""
            },
            "upload": {
                "copyright": 2,
                "title": "",
                "desc": "",
                "tid": 138,
                "tag": "bilitool",
                "line": "bda2",
                "source": "\u6765\u6e90\u4e8e\u4e92\u8054\u7f51",
                "cover": "",
                "dynamic": ""
            },
            "download": {
                "danmaku": 1,
                "quality": 64,
                "chunksize": 1024,
                "multiple": False
            }
        }

    def get_default_config(self):
        return self.default_config

    def reset_config(self):
        self.write(self.default_config)

    @add_headers_info()
    def get_headers_with_cookies(self):
        return self.get_config()['headers']

    @add_headers_info(referer='https://www.bilibili.com/')
    def get_headers_with_cookies_and_refer(self):
        return self.get_config()['headers']

    def save_cookies_info(self, sessdata, bili_jct, dede_user_id, dede_user_id_ckmd5):
        config_info = self.get_config()
        config_info['cookies']['SESSDATA'] = sessdata
        config_info['cookies']['bili_jct'] = bili_jct
        config_info['cookies']['DedeUserID'] = dede_user_id
        config_info['cookies']['DedeUserID__ckMd5'] = dede_user_id_ckmd5
        self.write(config_info)

    def update_specific_config(self, action, key, value):
        config_info = self.get_config()
        config_info[action][key] = value
        self.write(config_info)

    def update_multiple_config(self, action, updates: dict):
        config_info = self.get_config()
        for key, value in updates.items():
            config_info[action][key] = value
        self.write(config_info)

    def reset_cookies(self):
        config_info = self.get_config()
        config_info['cookies']['SESSDATA'] = ""
        config_info['cookies']['bili_jct'] = ""
        config_info['cookies']['DedeUserID'] = ""
        config_info['cookies']['DedeUserID__ckMd5'] = ""
        self.write(config_info)

    def get_config(self):
        if not os.path.exists(self.path):
            self.reset_config()
        return self.read()

    def read(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def write(self, config):
        with open(self.path, "w") as f:
            json.dump(config, f, indent=4)
