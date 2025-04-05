# Copyright (c) 2025 bilitool

import http.client
import urllib.parse
from ..model.model import Model
import json


# The requests lib here was suspended by the official, so use http.client to make the request
class LogoutBili(object):
    def __init__(self):
        self.config = Model().get_config()

    def logout_bili(self):
        host = "passport.bilibili.com"
        path = "/login/exit/v2"

        headers = {
            "Cookie": f'DedeUserID={self.config["cookies"]["DedeUserID"]}; bili_jct={self.config["cookies"]["bili_jct"]}; SESSDATA={self.config["cookies"]["SESSDATA"]}',
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {"biliCSRF": self.config["cookies"]["bili_jct"]}
        encoded_data = urllib.parse.urlencode(data)
        connection = http.client.HTTPSConnection(host)

        connection.request("POST", path, body=encoded_data, headers=headers)

        response = connection.getresponse()
        response_json = json.loads(response.read().decode("utf-8"))
        if response_json["code"] == 0:
            print("Logout successfully, the cookie has expired")
            Model().reset_cookies()
        else:
            print("Logout failed, check the info:")
            print(response_json)
        connection.close()
