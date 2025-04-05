# Copyright (c) 2025 bilitool

import re
import sys
import logging
import argparse
from math import ceil
import json
from pathlib import Path
import requests
from tqdm import tqdm
from ..utils.parse_cookies import parse_cookies
from ..model.model import Model
import hashlib
import time
import base64


class BiliUploader(object):
    def __init__(self, logger):
        self.logger = logger
        self.config = Model().get_config()
        self.session = requests.Session()
        self.session.headers = self.config["headers"]
        self.session.cookies = requests.utils.cookiejar_from_dict(
            self.config["cookies"]
        )
        self.headers = Model().get_headers_with_cookies_and_refer()

    def cover_up(self, img: str):
        """Upload the cover image
        Parameters
        ----------
        - img: img path or stream
        Returns
        -------
        - url: str
            the url of the cover image in bili server
        """
        from PIL import Image
        from io import BytesIO

        with Image.open(img) as im:
            # you should keep the image ratio 16:10
            xsize, ysize = im.size
            if xsize / ysize > 1.6:
                delta = xsize - ysize * 1.6
                region = im.crop((delta / 2, 0, xsize - delta / 2, ysize))
            else:
                delta = ysize - xsize * 10 / 16
                region = im.crop((0, delta / 2, xsize, ysize - delta / 2))
            buffered = BytesIO()
            region.save(buffered, format=im.format)
        r = self.session.post(
            url="https://member.bilibili.com/x/vu/web/cover/up",
            data={
                "cover": b"data:image/jpeg;base64,"
                + (base64.b64encode(buffered.getvalue())),
                "csrf": self.config["cookies"]["bili_jct"],
            },
            timeout=30,
        )
        buffered.close()
        res = r.json()
        if res.get("data") is None:
            raise Exception(res)
        self.logger.info(f"the cover image has been uploaded as {res['data']['url']}")
        return res["data"]["url"]

    def probe(self):
        self.logger.info("begin to probe the best cdn line")
        ret = requests.get(
            "https://member.bilibili.com/preupload?r=probe",
            headers=self.headers,
            timeout=5,
        ).json()
        data, auto_os = None, None
        min_cost = 0
        if ret["probe"].get("get"):
            method = "get"
        else:
            method = "post"
            data = bytes(int(1024 * 0.1 * 1024))
        for line in ret["lines"]:
            start = time.perf_counter()
            test = requests.request(
                method, f"https:{line['probe_url']}", data=data, timeout=30
            )
            cost = time.perf_counter() - start
            print(line["query"], cost)
            if test.status_code != 200:
                return
            if not min_cost or min_cost > cost:
                auto_os = line
                min_cost = cost
        auto_os["cost"] = min_cost
        self.logger.info(f"the best cdn line is:{auto_os}")
        upos_url = auto_os["probe_url"].rstrip("OK")
        self.logger.info(f"the upos_url is:{upos_url}")
        query_params = dict(param.split("=") for param in auto_os["query"].split("&"))
        cdn = query_params.get("upcdn")
        self.logger.info(f"the cdn is:{cdn}")
        probe_version = query_params.get("probe_version")
        self.logger.info(f"the probe_version is:{probe_version}")
        return upos_url, cdn, probe_version

    def preupload(self, *, filename, filesize, cdn, probe_version):
        """The preupload process to get `upos_uri` and `auth` information.
        Parameters
        ----------
        filename : str
            the name of the video to be uploaded
        filesize : int
            the size of the video to be uploaded
        biz_id : num
            the business id

        Returns
        -------
        - upos_uri: str
            the uri of the video will be stored in server
        - auth: str
            the auth information

        [Easter egg] Sometimes I'm also confused why it is called `upos`
        So I ask a question on the V2EX: https://v2ex.com/t/1103152
        Finally, the netizens reckon that may be the translation style of bilibili.
        """
        url = "https://member.bilibili.com/preupload"
        params = {
            "name": filename,
            "size": filesize,
            # The parameters below are fixed
            "r": "upos",
            "profile": "ugcupos/bup",
            "ssl": 0,
            "version": "2.8.9",
            "build": "2080900",
            "upcdn": cdn,
            "probe_version": probe_version,
        }
        res_json = self.session.get(
            url, params=params, headers={"TE": "Trailers"}
        ).json()
        assert res_json["OK"] == 1
        self.logger.info("Completed preupload phase")
        # print(res_json)
        return res_json

    def get_upload_video_id(self, *, upos_uri, auth, upos_url):
        """Get the `upload_id` of video.

        Parameters
        ----------
        - upos_uri: str
            get from `preupload`
        - auth: str
            get from `preupload`
        Returns
        -------
        - upload_id: str
            the id of the video to be uploaded
        """
        url = f"https:{upos_url}{upos_uri}?uploads&output=json"
        res_json = self.session.post(url, headers={"X-Upos-Auth": auth}).json()
        assert res_json["OK"] == 1
        self.logger.info("Completed upload_id obtaining phase")
        # print(res_json)
        return res_json

    def upload_video_in_chunks(
        self,
        *,
        upos_uri,
        auth,
        upload_id,
        fileio,
        filesize,
        chunk_size,
        chunks,
        upos_url,
    ):
        """Upload the video in chunks.

        Parameters
        ----------
        - upos_uri: str
            get from `preupload`
        - auth: str
            get from `preupload`
        - upload_id: str
            get from `get_upload_video_id`
        - fileio: io.BufferedReader
            the io stream of the video to be uploaded
        - filesize: int
            the size of the video to be uploaded
        - chunk_size: int
            the size of each chunk to be uploaded
        - chunks: int
            the number of chunks to be uploaded
        """
        url = f"https:{upos_url}{upos_uri}"
        params = {
            "partNumber": None,  # start from 1
            "uploadId": upload_id,
            "chunk": None,  # start from 0
            "chunks": chunks,
            "size": None,  # current batch size
            "start": None,
            "end": None,
            "total": filesize,
        }
        # Single thread upload
        with tqdm(
            total=filesize, desc="Uploading video", unit="B", unit_scale=True
        ) as pbar:
            for chunknum in range(chunks):
                start = fileio.tell()
                batchbytes = fileio.read(chunk_size)
                params["partNumber"] = chunknum + 1
                params["chunk"] = chunknum
                params["size"] = len(batchbytes)
                params["start"] = start
                params["end"] = fileio.tell()
                res = self.session.put(
                    url, params=params, data=batchbytes, headers={"X-Upos-Auth": auth}
                )
                assert res.status_code == 200
                self.logger.debug(f"Completed chunk{chunknum+1} uploading")
                pbar.update(len(batchbytes))
                # print(res)

    def finish_upload(
        self, *, upos_uri, auth, filename, upload_id, biz_id, chunks, upos_url
    ):
        """Notify the all chunks have been uploaded.

        Parameters
        ----------
        - upos_uri: str
            get from `preupload`
        - auth: str
            get from `preupload`
        - filename: str
            the name of the video to be uploaded
        - upload_id: str
            get from `get_upload_video_id`
        - biz_id: num
            get from `preupload`
        - chunks: int
            the number of chunks to be uploaded
        """
        url = f"https:{upos_url}{upos_uri}"
        params = {
            "output": "json",
            "name": filename,
            "profile": "ugcupos/bup",
            "uploadId": upload_id,
            "biz_id": biz_id,
        }
        data = {"parts": [{"partNumber": i, "eTag": "etag"} for i in range(chunks, 1)]}
        res_json = self.session.post(
            url, params=params, json=data, headers={"X-Upos-Auth": auth}
        ).json()
        assert res_json["OK"] == 1
        # print(res_json)

    # API docs: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/creativecenter/upload.md
    def publish_video(self, bilibili_filename):
        """publish the uploaded video"""
        config = Model().get_config()
        url = f'https://member.bilibili.com/x/vu/client/add?access_key={config["cookies"]["access_key"]}'
        data = {
            "copyright": config["upload"]["copyright"],
            "videos": [
                {
                    "filename": bilibili_filename,
                    "title": config["upload"]["title"],
                    "desc": config["upload"]["desc"],
                }
            ],
            "source": config["upload"]["source"],
            "tid": config["upload"]["tid"],
            "title": config["upload"]["title"],
            "cover": config["upload"]["cover"],
            "tag": config["upload"]["tag"],
            "desc_format_id": 0,
            "desc": config["upload"]["desc"],
            "dynamic": config["upload"]["dynamic"],
            "subtitle": {"open": 0, "lan": ""},
        }
        if config["upload"]["copyright"] != 2:
            del data["source"]
        res_json = self.session.post(url, json=data, headers={"TE": "Trailers"}).json()
        # print(res_json)
        return res_json

    def get_updated_video_info(self, bvid: str):
        url = f"http://member.bilibili.com/x/client/archive/view"
        params = {
            "access_key": Model().get_config()["cookies"]["access_key"],
            "bvid": bvid,
        }
        resp = requests.get(url=url, headers=self.headers, params=params)
        return resp.json()["data"]

    def get_video_list_info(self, bvid: str):
        raw_data = self.get_updated_video_info(bvid)
        # print(raw_data)
        videos = []
        for video in raw_data["videos"]:
            videos.append(
                {
                    "filename": video["filename"],
                    "title": video["title"],
                    "desc": video["desc"],
                }
            )

        data = {
            "bvid": bvid,
            "build": 1054,
            "copyright": raw_data["archive"]["copyright"],
            "videos": videos,
            "source": raw_data["archive"]["source"],
            "tid": raw_data["archive"]["tid"],
            "title": raw_data["archive"]["title"],
            "cover": raw_data["archive"]["cover"],
            "tag": raw_data["archive"]["tag"],
            "no_reprint": raw_data["archive"]["no_reprint"],
            "open_elec": raw_data["archive_elec"]["state"],
            "desc": raw_data["archive"]["desc"],
        }
        return data

    @staticmethod
    def sign_dict(data: dict, app_secret: str):
        """sign a dictionary of request parameters
        Parameters
        ----------
        - data: dictionary of request parameters.
        - app_secret: a secret string coupled with app_key.

        Returns
        -------
        - A hash string. len=32
        """
        data_str = []
        keys = list(data.keys())
        keys.sort()
        for key in keys:
            data_str.append("{}={}".format(key, data[key]))
        data_str = "&".join(data_str)
        data_str = data_str + app_secret
        return hashlib.md5(data_str.encode("utf-8")).hexdigest()

    def append_video(self, bilibili_filename, video_name, data):
        """append the uploaded video"""
        # Parse JSON string to dict if data is a string
        video_to_be_appended = {
            "filename": bilibili_filename,
            "title": video_name,
            "desc": "",
        }
        data["videos"].append(video_to_be_appended)
        headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "User-Agent": "",
        }
        params = {
            "access_key": Model().get_config()["cookies"]["access_key"],
        }
        APPSECRET = "af125a0d5279fd576c1b4418a3e8276d"
        params["sign"] = BiliUploader.sign_dict(params, APPSECRET)

        res_json = requests.post(
            url="http://member.bilibili.com/x/vu/client/edit",
            params=params,
            headers=headers,
            verify=False,
            cookies={"sid": Model().get_config()["cookies"]["sid"]},
            json=data,
        )
        print(res_json.json())
        return res_json
