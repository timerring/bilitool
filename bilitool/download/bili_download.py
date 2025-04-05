# Copyright (c) 2025 bilitool

import requests
import time
import sys
from tqdm import tqdm
from ..model.model import Model


class BiliDownloader:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.config = Model().get_config()
        self.headers = Model().get_headers_with_cookies_and_refer()

    def get_cid(self, bvid):
        url = "https://api.bilibili.com/x/player/pagelist?bvid=" + bvid
        response = requests.get(url, headers=self.headers)
        return response.json()["data"]

    def get_bvid_video(self, bvid, cid, name_raw="video"):
        url = (
            "https://api.bilibili.com/x/player/playurl?cid="
            + str(cid)
            + "&bvid="
            + bvid
            + "&qn="
            + str(self.config["download"]["quality"])
        )
        name = name_raw + ".mp4"
        response = None
        response = requests.get(url, headers=self.headers)
        video_url = response.json()["data"]["durl"][0]["url"]
        self.download_video(video_url, name)

    def download_video(self, url, name):
        response = requests.get(url, headers=self.headers, stream=True)
        if response.status_code == 200:
            with open(name, "wb") as file:
                content_length = int(response.headers["Content-Length"])
                progress_bar = tqdm(
                    total=content_length, unit="B", unit_scale=True, desc=name
                )
                for chunk in response.iter_content(
                    chunk_size=self.config["download"]["chunksize"]
                ):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                progress_bar.close()
                self.logger.info(f"Download completed")
        else:
            self.logger.info(f"{name} Download failed")

    def download_danmaku(self, cid, name_raw="video"):
        if self.config["download"]["danmaku"]:
            self.logger.info(f"Begin download danmaku")
            dm_url = "https://comment.bilibili.com/" + cid + ".xml"
            response = requests.get(dm_url, headers=self.headers)
            with open(name_raw + ".xml", "wb") as file:
                file.write(response.content)
            self.logger.info(f"Successfully downloaded danmaku")
