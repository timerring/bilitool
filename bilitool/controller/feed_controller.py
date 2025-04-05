# Copyright (c) 2025 bilitool

from ..feed.bili_video_list import BiliVideoList
from ..utils.check_format import CheckFormat


class FeedController(object):
    def __init__(self):
        self.bili_video_list = BiliVideoList()

    def print_video_list_info(
        self, size: int = 20, status_type: str = "pubed,not_pubed,is_pubing"
    ):
        self.bili_video_list.print_video_list_info(size, status_type)

    def print_video_info(self, vid: str):
        bvid = CheckFormat().only_bvid(vid)
        video_info = self.bili_video_list.get_video_info(bvid)
        extracted_info = self.bili_video_list.extract_video_info(video_info)
        self.bili_video_list.print_video_info(extracted_info)

    def get_video_dict_info(
        self, size: int = 20, status_type: str = "pubed,not_pubed,is_pubing"
    ):
        return self.bili_video_list.get_video_dict_info(size, status_type)
