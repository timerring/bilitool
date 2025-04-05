# Copyright (c) 2025 bilitool

import unittest
from bilitool.feed.bili_video_list import BiliVideoList
from bilitool.feed.bili_live_list import BiliLiveList


class TestBiliList(unittest.TestCase):
    def setUp(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108"
        }

    def test_get_bili_video_list(self):
        bili = BiliVideoList()
        bili.print_video_list_info(bili.get_bili_video_list(50, "not_pubed"))

    def test_print_video_info_via_bvid(self):
        bili = BiliVideoList()
        bili.print_video_info_via_bvid("BV1pCr6YcEgD")

    def test_get_live_info(self):
        bili = BiliLiveList(self.headers)
        print(bili.get_live_info(25538755))
