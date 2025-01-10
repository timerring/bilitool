# Copyright (c) 2025 biliupload

import re
import sys
import logging
import argparse
from math import ceil
from json import dumps
from pathlib import Path
from time import sleep
import requests
from biliupload.utils.parse_cookies import parse_cookies

# you can test your best cdn line https://member.bilibili.com/preupload?r=ping
cdn_lines = {
    'qn': 'upos-sz-upcdnqn.bilivideo.com',
    'bda2': 'upos-sz-upcdnbda2.bilivideo.com',
}

class BiliUploader(object):
    ua = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0',
    }

    def __init__(self, sessdata, bili_jct, line):
        self.logger = logging.getLogger('biliupload')
        self.SESSDATA = sessdata
        self.bili_jct = bili_jct
        self.auth_cookies = {
            'SESSDATA': sessdata,
            'bili_jct': bili_jct
        }
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(self.auth_cookies)
        self.session.headers = self.ua
        self.line = line

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
            'upcdn': self.line,
            'probe_version': '20200810'
        }
        res_json = self.session.get(
            url,
            params=params,
            headers={'TE': 'Trailers'}
        ).json()
        assert res_json['OK'] == 1
        self.logger.info('Completed preupload phase')
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
        url = f'https://{cdn_lines[self.line]}/{upos_uri}?uploads&output=json'
        res_json = self.session.post(url, headers={'X-Upos-Auth': auth}).json()
        assert res_json['OK'] == 1
        self.logger.info('Completed upload_id obtaining phase')
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
        url = f'https://{cdn_lines[self.line]}/{upos_uri}'
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
        url = f'https://{cdn_lines[self.line]}/{upos_uri}'
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

    def publish_video(self, bilibili_filename, title, tid, tags, source='来源于网络', copyright=2, desc='', cover_url=''):
        """publish the uploaded video"""
        url = f'https://member.bilibili.com/x/vu/web/add?csrf={self.bili_jct}'
        data = {'copyright': copyright,
                'videos': [{'filename': bilibili_filename,
                            'title': title,
                            'desc': desc}],
                'source': source,
                'tid': tid,
                'cover': cover_url,
                'title': title,
                'tag': tags,
                'desc_format_id': 0,
                'desc': desc,
                'dynamic': '',
                'subtitle': {'open': 0, 'lan': ''}}
        if copyright != 2:
            del data['source']
            # copyright: 1 original 2 reprint
            data['copyright'] = 1
            # interactive: 0 no 1 yes
            data['interactive'] = 0
            # no_reprint: 0 no 1 yes
            data['no_reprint'] = 1
        res_json = self.session.post(url, json=data, headers={'TE': 'Trailers'}).json()
        return res_json

    def upload_and_publish_video(self, file, *, title=None, desc='', copyright=2, tid=None, tags=None):
        """upload and publish video on bilibili"""
        file = Path(file)
        assert file.exists(), f'The file {file} does not exist'
        filename = file.name
        title = title or file.stem
        filesize = file.stat().st_size
        self.logger.info(f'The {title} to be uploaded')

        # upload video
        self.logger.info('Start preuploading the video')
        pre_upload_response = self.preupload(filename=filename, filesize=filesize)
        upos_uri = pre_upload_response['upos_uri'].split('//')[-1]
        auth = pre_upload_response['auth']
        biz_id = pre_upload_response['biz_id']
        chunk_size = pre_upload_response['chunk_size']
        chunks = ceil(filesize/chunk_size)

        self.logger.info('Start uploading the video')
        upload_video_id_response = self.get_upload_video_id(upos_uri=upos_uri, auth=auth)
        upload_id = upload_video_id_response['upload_id']
        key = upload_video_id_response['key']

        bilibili_filename = re.search(r'/(.*)\.', key).group(1)

        self.logger.info(f'Uploading the video in {chunks} batches')
        fileio = file.open(mode='rb')
        self.upload_video_in_chunks(
            upos_uri=upos_uri,
            auth=auth,
            upload_id=upload_id,
            fileio=fileio,
            filesize=filesize,
            chunk_size=chunk_size,
            chunks=chunks
        )
        fileio.close()

        # notify the all chunks have been uploaded
        self.finish_upload(upos_uri=upos_uri, auth=auth, filename=filename,
                           upload_id=upload_id, biz_id=biz_id, chunks=chunks)

        # select tid
        tid = 138

        # customize tags
        if not tags:
            tags_text = 'biliupload'
        else:
            tags_text = tags

        # customize video cover
        # cover_url = 

        # publish video
        publish_video_response = self.publish_video(bilibili_filename=bilibili_filename, title=title,
                       tid=tid, tags=tags_text, copyright=copyright, desc=desc)
        bvid = publish_video_response['data']['bvid']
        self.logger.info(f'[{title}]upload success!\tbvid:{bvid}')