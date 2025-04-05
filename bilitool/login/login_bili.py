# Copyright (c) 2025 bilitool

import hashlib
import subprocess
import time
import json
from urllib.parse import urlencode
from ..model.model import Model
from .check_bili_login import CheckBiliLogin


class LoginBili(object):
    def __init__(self):
        self.APP_KEY = "4409e2ce8ffd12b8"
        self.APP_SEC = "59b43e04ad6965f34319062b478f83dd"

    def signature(self, params):
        params["appkey"] = self.APP_KEY
        keys = sorted(params.keys())
        query = "&".join(f"{k}={params[k]}" for k in keys)
        query += self.APP_SEC
        md5_hash = hashlib.md5(query.encode("utf-8")).hexdigest()
        params["sign"] = md5_hash

    @staticmethod
    def map_to_string(params):
        return urlencode(params)

    def execute_curl_command(self, api, data):
        data_string = LoginBili.map_to_string(data)
        headers = "Content-Type: application/x-www-form-urlencoded"
        curl_command = f'curl -X POST -H "{headers}" -d "{data_string}" {api}'
        result = subprocess.run(
            curl_command, shell=True, capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode != 0:
            raise Exception(f"curl command failed: {result.stderr}")
        return json.loads(result.stdout)

    def get_tv_qrcode_url_and_auth_code(self):
        api = "https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code"
        data = {"local_id": "0", "ts": str(int(time.time()))}
        self.signature(data)
        body = self.execute_curl_command(api, data)
        if body["code"] == 0:
            qrcode_url = body["data"]["url"]
            auth_code = body["data"]["auth_code"]
            return qrcode_url, auth_code
        else:
            raise Exception("get_tv_qrcode_url_and_auth_code error")

    def verify_login(self, auth_code, export):
        api = "https://passport.bilibili.com/x/passport-tv-login/qrcode/poll"
        data = {"auth_code": auth_code, "local_id": "0", "ts": str(int(time.time()))}
        self.signature(data)
        while True:
            body = self.execute_curl_command(api, data)
            if body["code"] == 0:
                filename = "cookie.json"
                if export:
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(body, f, ensure_ascii=False, indent=4)
                    print(f"cookie has been saved to {filename}")

                access_key_value = body["data"]["access_token"]
                sessdata_value = body["data"]["cookie_info"]["cookies"][0]["value"]
                bili_jct_value = body["data"]["cookie_info"]["cookies"][1]["value"]
                dede_user_id_value = body["data"]["cookie_info"]["cookies"][2]["value"]
                dede_user_id_ckmd5_value = body["data"]["cookie_info"]["cookies"][3][
                    "value"
                ]
                sid_value = body["data"]["cookie_info"]["cookies"][4]["value"]
                Model().save_cookies_info(
                    access_key_value,
                    sessdata_value,
                    bili_jct_value,
                    dede_user_id_value,
                    dede_user_id_ckmd5_value,
                    sid_value,
                )
                print("Login success!")
                break
            else:
                time.sleep(3)

    def get_cookie_file_login(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            body = json.load(f)
            access_key_value = body["data"]["access_token"]
            sessdata_value = body["data"]["cookie_info"]["cookies"][0]["value"]
            bili_jct_value = body["data"]["cookie_info"]["cookies"][1]["value"]
            dede_user_id_value = body["data"]["cookie_info"]["cookies"][2]["value"]
            dede_user_id_ckmd5_value = body["data"]["cookie_info"]["cookies"][3][
                "value"
            ]
            sid_value = body["data"]["cookie_info"]["cookies"][4]["value"]
            Model().save_cookies_info(
                access_key_value,
                sessdata_value,
                bili_jct_value,
                dede_user_id_value,
                dede_user_id_ckmd5_value,
                sid_value,
            )
            if CheckBiliLogin().check_bili_login():
                print("Login success!", flush=True)
            else:
                print("Login failed, please check the cookie file again", flush=True)
