# Copyright (c) 2025 bilitool

import re
import sys
import logging
import argparse
from math import ceil
from json import dumps
from pathlib import Path
from time import sleep
import requests
from bilitool.utils.parse_cookies import parse_cookies

# you can test your best cdn line https://member.bilibili.com/preupload?r=ping
# cdn_lines = {
#     'qn': 'upos-sz-upcdnqn.bilivideo.com',
#     'bda2': 'upos-sz-upcdnbda2.bilivideo.com',
# }

class BiliUploader(object):
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self.session = requests.Session()
        self.session.headers = self.config["headers"]
        self.session.cookies = requests.utils.cookiejar_from_dict(self.config["cookies"])

    def preupload(self, *, filename, filesize):
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
        url = 'https://member.bilibili.com/preupload'
        params = {
            'name':	filename,
            'size':	filesize,
            # The parameters below are fixed
            'r': 'upos',
            'profile': 'ugcupos/bup',
            'ssl':	0,
            'version':	'2.8.9',
            'build': '2080900',
            'upcdn': 'bda2',
            'probe_version': '20200810'
        }
        res_json = self.session.get(
            url,
            params=params,
            headers={'TE': 'Trailers'}
        ).json()
        assert res_json['OK'] == 1
        self.logger.info('Completed preupload phase')
        # print(res_json)
        return res_json

    def get_upload_video_id(self, *, upos_uri, auth):
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
        url = f'https://upos-sz-upcdnbda2.bilivideo.com/{upos_uri}?uploads&output=json'
        res_json = self.session.post(url, headers={'X-Upos-Auth': auth}).json()
        assert res_json['OK'] == 1
        self.logger.info('Completed upload_id obtaining phase')
        # print(res_json)
        return res_json

    def upload_video_in_chunks(self, *, upos_uri, auth, upload_id, fileio, filesize, chunk_size, chunks):
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
        url = f'https://upos-sz-upcdnbda2.bilivideo.com/{upos_uri}'
        params = {
            'partNumber': None,  # start from 1
            'uploadId':	upload_id,
            'chunk': None,  # start from 0
            'chunks': chunks,
            'size':	None,  # current batch size
            'start': None,
            'end':	None,
            'total': filesize,
        }
        # Single thread upload
        for chunknum in range(chunks):
            start = fileio.tell()
            batchbytes = fileio.read(chunk_size)
            params['partNumber'] = chunknum + 1
            params['chunk'] = chunknum
            params['size'] = len(batchbytes)
            params['start'] = start
            params['end'] = fileio.tell()
            res = self.session.put(url, params=params, data=batchbytes, headers={
                                   'X-Upos-Auth': auth})
            assert res.status_code == 200
            self.logger.debug(f'Completed chunk{chunknum+1} uploading')
            # print(res)

    def finish_upload(self, *, upos_uri, auth, filename, upload_id, biz_id, chunks):
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
        url = f'https://upos-sz-upcdnbda2.bilivideo.com/{upos_uri}'
        params = {
            'output':	'json',
            'name':	filename,
            'profile'	: 'ugcupos/bup',
            'uploadId':	upload_id,
            'biz_id':	biz_id
        }
        data = {"parts": [{"partNumber": i, "eTag": "etag"}
                          for i in range(chunks, 1)]}
        res_json = self.session.post(url, params=params, json=data,
                                     headers={'X-Upos-Auth': auth}).json()
        assert res_json['OK'] == 1
        # print(res_json)

    # API docs: https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/creativecenter/upload.md
    def publish_video(self, bilibili_filename):
        """publish the uploaded video"""
        url = f'https://member.bilibili.com/x/vu/web/add?csrf={self.config["cookies"]["bili_jct"]}'
        data = {'copyright': self.config["upload"]["copyright"],
                'videos': [{'filename': bilibili_filename,
                            'title': self.config["upload"]["title"],
                            'desc': self.config["upload"]["desc"]}],
                'source': self.config["upload"]["source"],
                'tid': self.config["upload"]["tid"],
                'title': self.config["upload"]["title"],
                'cover': self.config["upload"]["cover"],
                'tag': self.config["upload"]["tag"],
                'desc_format_id': 0,
                'desc': self.config["upload"]["desc"],
                'dynamic': self.config["upload"]["dynamic"],
                'subtitle': {'open': 0, 'lan': ''}}
        if self.config["upload"]["copyright"] != 2:
            del data['source']
            # copyright: 1 original 2 reprint
            data['copyright'] = 1
        res_json = self.session.post(url, json=data, headers={'TE': 'Trailers'}).json()
        # print(res_json)
        return res_json