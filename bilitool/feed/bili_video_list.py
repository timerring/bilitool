# Copyright (c) 2025 bilitool

import time
import requests
from ..model.model import Model
from ..authenticate.wbi_sign import WbiSign
from . import VideoListInfo, state_dict, video_info_dict


class BiliVideoList(object):
    def __init__(self):
        self.headers = Model().get_headers_with_cookies_and_refer()

    @staticmethod
    def save_video_list_info(archive: dict):
        """
        Save the video info
        """
        info = VideoListInfo()
        info["bvid"] = archive.get("bvid")
        info["title"] = archive.get("title")
        info["state"] = archive.get("state")
        info["state_desc"] = archive.get("state_desc")
        info["reject_reason"] = archive.get("reject_reason")
        info["state_panel"] = archive.get("state_panel")
        return info

    def get_bili_video_list(
        self, size: int = 20, status_type: str = "pubed,not_pubed,is_pubing"
    ):
        """Query the video list

        :param size: page size
        :param status_type: pubed,not_pubed,is_pubing
        """
        url = f"https://member.bilibili.com/x/web/archives?status={status_type}&pn=1&ps={size}"
        resp = requests.get(url=url, headers=self.headers)
        if resp.status_code != 200:
            raise Exception(f"HTTP ERROR code {resp.status_code}")
        response_data = resp.json().get("data")
        if resp.json().get("code") != 0:
            raise Exception(resp.json().get("message"))
        arc_items = list()
        page_info = response_data.get("1")
        if response_data.get("arc_audits") is not None:
            for item in response_data.get("arc_audits"):
                archive = item["Archive"]
                for i, v in enumerate(item["Videos"]):
                    if v["reject_reason"] != "":
                        archive["reject_reason"] += "\nP{p_num}-{r}".format(
                            p_num=i + 1, r=v["reject_reason"]
                        )
                arc_items.append(self.save_video_list_info(archive))
        data: dict = {
            "page": page_info,
            "status": response_data.get("class"),
            "items": arc_items,
        }
        return data

    def print_video_list_info(
        self, size: int = 20, status_type: str = "pubed,not_pubed,is_pubing"
    ):
        video_data = self.get_bili_video_list(size, status_type)
        for item in video_data["items"]:
            info = f"{item['state_desc']} | {item['bvid']} | {item['title']}"
            extra_info = []
            if item["reject_reason"]:
                extra_info.append(f"拒绝原因: {item['reject_reason']}")
            if extra_info:
                info += f" | {' | '.join(extra_info)}"
            print(info)

    def get_video_dict_info(
        self, size: int = 20, status_type: str = "pubed,not_pubed,is_pubing"
    ):
        video_data = self.get_bili_video_list(size, status_type)
        data = dict()
        for item in video_data["items"]:
            data[item["title"]] = item["bvid"]
        return data

    def get_video_info(self, bvid: str) -> dict:
        """Get the video info of the bvid"""
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        resp = requests.get(url=url, headers=self.headers)
        if resp.status_code != 200:
            raise Exception("HTTP ERROR")
        return resp.json()

    @staticmethod
    def extract_video_info(response_data):
        data = response_data.get("data", {})

        video_info = {
            # video info
            "title": data.get("title"),
            "desc": data.get("desc"),
            "duration": data.get("duration"),
            "pubdate": data.get("pubdate"),
            "owner_name": data.get("owner", {}).get("name"),
            "tname": data.get("tname"),
            "copyright": data.get("copyright"),
            "width": data.get("dimension", {}).get("width"),
            "height": data.get("dimension", {}).get("height"),
            # video status
            "stat_view": data.get("stat", {}).get("view"),
            "stat_danmaku": data.get("stat", {}).get("danmaku"),
            "stat_reply": data.get("stat", {}).get("reply"),
            "stat_coin": data.get("stat", {}).get("coin"),
            "stat_share": data.get("stat", {}).get("share"),
            "stat_like": data.get("stat", {}).get("like"),
        }

        return video_info

    @staticmethod
    def print_video_info(video_info):
        for key, value in video_info.items():
            if key == "duration":
                value = f"{value // 60}:{value % 60}"
            elif key == "pubdate":
                value = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(value))
            elif key == "copyright":
                value = "原创" if value == 1 else "转载"
            label = video_info_dict.get(key, key)
            print(f"{label}: {value}")
