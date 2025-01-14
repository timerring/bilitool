# Copyright (c) 2025 biliupload

import unittest
from biliupload.feed.bili_video_list import BiliVideoList

class TestBiliList(unittest.TestCase):
    def test_get_bili_video_list(self):
        bili = BiliVideoList()
        bili.print_video_list_info(bili.get_bili_video_list(50, 'not_pubed'))