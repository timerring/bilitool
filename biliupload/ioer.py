# Copyright (c) 2025 biliupload

import json
import os


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
                "bili_jct": ""
            },
            "upload": {
                "copyright": 2,
                "title": "",
                "desc": "",
                "tid": 138,
                "tags": "biliupload",
                "line": "bda2",
                "source": "\u6765\u6e90\u4e8e\u4e92\u8054\u7f51",
                "cover": "",
                "dynamic": ""
            },
            "download": {
                "dm": 1,
                "qn": 999,
                "chunk_size": 1024
            }
        }

    def get_default_config(self):
        return self.default_config

    def reset_config(self):
        self.write(self.default_config)

    def save_cookies_info(self, sessdata, bili_jct):
        config_info = self.get_config()
        config_info['cookies']['SESSDATA'] = sessdata
        config_info['cookies']['bili_jct'] = bili_jct
        self.write(config_info)

    def update_specific_config(self, action, key, value):
        curr_config = self.get_config()
        curr_config[action][key] = value
        self.write(curr_config)

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
