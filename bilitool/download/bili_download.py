# Copyright (c) 2025 bilitool

import requests
import time
import sys
from tqdm import tqdm
from bilitool.authenticate.ioer import ioer


class BiliDownloader:
    def __init__(self) -> None:
        self.config = ioer().get_config()
        self.headers = ioer().get_headers_with_cookies_and_refer()

    def get_cid(self,bvid):
        url="https://api.bilibili.com/x/player/pagelist?bvid="+bvid
        response = requests.get(url, headers=self.headers)
        return response.json()['data']

    def get_bvid_video(self, bvid, cid, name_raw="video"):
        url = "https://api.bilibili.com/x/player/playurl?cid="+str(cid)+"&bvid="+bvid+"&qn="+str(self.config["download"]["quality"])
        name = name_raw+'.mp4'
        response = None
        response = requests.get(url, headers=self.headers)
        video_url = response.json()["data"]["durl"][0]["url"]
        self.download_video(video_url, name)

    def download_video(self, url, name):
        print("Begin download MP4")
        response = requests.get(
            url, headers=self.headers, stream=True)
        if response.status_code == 200:
            with open(name, 'wb') as file:
                content_length = int(response.headers['Content-Length'])
                progress_bar = tqdm(total=content_length, unit='B', unit_scale=True, desc=name)
                for chunk in response.iter_content(chunk_size=self.config["download"]["chunksize"]):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                progress_bar.close()
                print("\nDownload completed")
        else:
            print(name, "Download failed")

    def download_danmaku(self, cid, name_raw="video"):
        if self.config["download"]["danmaku"]:
            print("Begin download danmaku")
            dm_url = "https://comment.bilibili.com/"+cid+".xml"
            response = requests.get(dm_url, headers=self.headers)
            with open(name_raw+'.xml', 'wb') as file:
                file.write(response.content)
            print("Successfully downloaded danmaku")
    