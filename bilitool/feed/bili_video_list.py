# Copyright (c) 2025 bilitool

import time
import requests
from bilitool.authenticate.ioer import ioer
from bilitool.authenticate.wbi_sign import WbiSign
from bilitool.feed import VideoListInfo, state_dict


class BiliVideoList(object):
    def __init__(self):
        self.cookies = ioer().get_config()['cookies']
        self.headers = ioer().get_headers_with_cookies_and_refer()

    @staticmethod
    def save_video_list_info(archive: dict):
        """
        Save the video info
        """
        info = VideoListInfo()
        info['bvid'] = archive.get("bvid")
        info['title'] = archive.get("title")
        info['state'] = archive.get("state")
        info['state_desc'] = archive.get("state_desc")
        info['reject_reason'] = archive.get('reject_reason')
        info['state_panel'] = archive.get('state_panel')
        return info

    def get_bili_video_list(self, size: int = 20, target_type: str = 'pubed,not_pubed,is_pubing'):
        """Query the video list
        
        :param size: page size
        :param target_type: pubed,not_pubed,is_pubing
        """
        url = f"https://member.bilibili.com/x/web/archives?status={target_type}&pn=1&ps={size}"
        resp = requests.get(url=url, headers=self.headers)
        if resp.status_code != 200:
            raise Exception(f"HTTP ERROR code {resp.status_code}")
        response_data = resp.json().get("data")
        if resp.json().get("code") != 0:
            raise Exception(resp.json().get("message"))
        arc_items = list()
        page_info = response_data.get('1')
        if response_data.get("arc_audits") is not None:
            for item in response_data.get("arc_audits"):
                archive = item['Archive']
                for i, v in enumerate(item['Videos']):
                    if v['reject_reason'] != '':
                        archive['reject_reason'] += "\nP{p_num}-{r}".format(p_num=i + 1, r=v['reject_reason'])
                arc_items.append(self.save_video_list_info(archive))
        data: dict = {
            "page": page_info,
            "status": response_data.get('class'),
            "items": arc_items
        }
        return data

    @staticmethod
    def print_video_list_info(video_data):
        for item in video_data['items']:
            info = f"{item['state_desc']} | {item['bvid']} | {item['title']}"
            extra_info = []
            if item['reject_reason']:
                extra_info.append(f"拒绝原因: {item['reject_reason']}")
            if extra_info:
                info += f" | {' | '.join(extra_info)}"
            print(info)

    def get_video_info(self, bvid: str) -> dict:
        """Get the video info of the bvid"""
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        resp = requests.get(url=url, headers=self.headers)
        if resp.status_code != 200:
            raise Exception('HTTP ERROR')
        return resp.json()
