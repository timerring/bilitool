# Copyright (c) 2025 bilitool

from ..model.model import Model
from ..download.bili_download import BiliDownloader
from ..utils.check_format import CheckFormat
import re
import logging


class DownloadController:
    def __init__(self):
        self.logger = logging.getLogger("bilitool")
        self.model = Model()
        self.bili_downloader = BiliDownloader(self.logger)
        self.config = self.model.get_config()

    def extract_filename(self, filename):
        illegal_chars = r'[\\/:"*?<>|]'
        filename = re.sub(illegal_chars, "", filename)
        return filename

    @staticmethod
    def package_download_metadata(danmaku, quality, chunksize, multiple):
        return {
            "danmaku": danmaku,
            "quality": quality,
            "chunksize": chunksize,
            "multiple": multiple,
        }

    def get_cid(self, bvid):
        return self.bili_downloader.get_cid(bvid)

    def download_video(self, bvid):
        cid_group = self.get_cid(bvid)
        if self.config["download"]["multiple"]:
            for i in range(0, len(cid_group)):
                cid = str(cid_group[i]["cid"])
                name = cid_group[i]["part"]
                self.logger.info(f"Begin download {name}")
                self.download_biv_and_danmaku(bvid, cid, name)
        else:
            cid = str(cid_group[0]["cid"])
            name = cid_group[0]["part"]
            self.logger.info(f"Begin download {name}")
            self.download_biv_and_danmaku(bvid, cid, name)

    def download_biv_and_danmaku(self, bvid, cid, name_raw="video"):
        name = self.extract_filename(name_raw)
        self.bili_downloader.get_bvid_video(bvid, cid, name)
        self.download_danmaku(cid, name)

    def download_danmaku(self, cid, name="video"):
        self.bili_downloader.download_danmaku(cid, name)

    def download_video_entry(self, vid, danmaku, quality, chunksize, multiple):
        download_metadata = self.package_download_metadata(
            danmaku, quality, chunksize, multiple
        )
        Model().update_multiple_config("download", download_metadata)
        bvid = CheckFormat().only_bvid(vid)
        self.download_video(bvid)
