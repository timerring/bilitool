# Copyright (c) 2025 bilitool

from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests
from ..model.model import Model

# https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md


class WbiSign(object):
    def __init__(self):
        self.config = Model().get_config()

    mixinKeyEncTab = [
        46,
        47,
        18,
        2,
        53,
        8,
        23,
        32,
        15,
        50,
        10,
        31,
        58,
        3,
        45,
        35,
        27,
        43,
        5,
        49,
        33,
        9,
        42,
        19,
        29,
        28,
        14,
        39,
        12,
        38,
        41,
        13,
        37,
        48,
        7,
        16,
        24,
        55,
        40,
        61,
        26,
        17,
        0,
        1,
        60,
        51,
        30,
        4,
        22,
        25,
        54,
        21,
        56,
        59,
        6,
        63,
        57,
        62,
        11,
        36,
        20,
        34,
        44,
        52,
    ]

    def get_wbi_keys(self) -> tuple[str, str]:
        """Get the refresh token"""
        headers = Model().get_headers_with_cookies_and_refer()
        resp = requests.get(
            "https://api.bilibili.com/x/web-interface/nav", headers=headers
        )
        resp.raise_for_status()
        json_content = resp.json()
        img_url: str = json_content["data"]["wbi_img"]["img_url"]
        sub_url: str = json_content["data"]["wbi_img"]["sub_url"]
        img_key = img_url.rsplit("/", 1)[1].split(".")[0]
        sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
        return img_key, sub_key

    def get_mixin_key(self, orig: str):
        """shuffle the string"""
        return reduce(lambda s, i: s + orig[i], self.mixinKeyEncTab, "")[:32]

    def enc_wbi(self, params: dict, img_key: str, sub_key: str):
        """wbi sign"""
        mixin_key = self.get_mixin_key(img_key + sub_key)
        curr_time = round(time.time())
        params["wts"] = curr_time
        params = dict(sorted(params.items()))
        # filter the value of "!'()*"
        params = {
            k: "".join(filter(lambda char: char not in "!'()*", str(v)))
            for k, v in params.items()
        }
        query = urllib.parse.urlencode(params)
        wbi_sign = md5((query + mixin_key).encode()).hexdigest()
        # add `w_rid` parameter in the url
        params["w_rid"] = wbi_sign
        return params

    def get_wbi_signed_params(self, params):
        img_key, sub_key = self.get_wbi_keys()

        signed_params = self.enc_wbi(params=params, img_key=img_key, sub_key=sub_key)
        return signed_params
