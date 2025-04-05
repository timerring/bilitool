# Copyright (c) 2025 bilitool

from ..model.model import Model
import requests
import json


class CheckBiliLogin(object):
    def __init__(self):
        self.config = Model().get_config()

    def check_bili_login(self):
        url = "https://api.bilibili.com/x/web-interface/nav"
        with requests.Session() as session:
            session.headers = self.config["headers"]
            session.cookies = requests.utils.cookiejar_from_dict(self.config["cookies"])
            response = session.get(url)
            if response.status_code == 200:
                response_data = json.loads(response.text)
                if response_data["data"]["isLogin"] == True:
                    self.obtain_bili_login_info(response_data)
                    return True
                else:
                    print(
                        "There is currently no login account, some functions may not work"
                    )
                    # print(response.text)
                    return False
            else:
                print("Check failed, please check the info")
                print(response.text)
                return False

    def obtain_bili_login_info(self, response_data):
        current_level = response_data["data"]["level_info"]["current_level"]
        uname = response_data["data"]["uname"]
        vip_status = response_data["data"]["vipStatus"]

        print(f"Current account: {uname}")
        print(f"Current level: {current_level}")
        if vip_status == 1:
            print(f"Status: 大会员")
        else:
            print(f"Status: 非大会员")
