# Copyright (c) 2025 bilitool

import unittest
import logging
from bilitool.upload.bili_upload import BiliUploader


class TestBiliUploader(unittest.TestCase):
    def test_get_updated_video_info(self):
        logger = logging.getLogger("bilitool")
        bili = BiliUploader(logger)
        print(bili.get_updated_video_info("BVXXXXXXXXX"))
