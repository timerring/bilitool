# Copyright (c) 2025 bilitool

from bilitool.authenticate.ioer import ioer
from bilitool.upload.bili_upload import BiliUploader
from pathlib import Path
import re
from math import ceil
import logging


class UploadController:
    def __init__(self):
        self.ioer = ioer()
        self.logger = logging.getLogger('bilitool')
        self.config = self.ioer.get_config()
        self.bili_uploader = BiliUploader(self.config, self.logger)

    @staticmethod
    def package_upload_metadata(line, copyright, tid, title, desc, tag, source, cover, dynamic):
            return {
                'line': line,
                'copyright': copyright,
                'tid': tid,
                'title': title,
                'desc': desc,
                'tag': tag,
                'source': source,
                'cover': cover,
                'dynamic': dynamic
            }

    def upload_and_publish_video(self, file):
        """upload and publish video on bilibili"""
        file = Path(file)
        assert file.exists(), f'The file {file} does not exist'
        filename = file.name
        title = self.config["upload"]["title"] or file.stem
        filesize = file.stat().st_size
        self.logger.info(f'The {title} to be uploaded')

        # upload video
        self.logger.info('Start preuploading the video')
        pre_upload_response = self.bili_uploader.preupload(filename=filename, filesize=filesize)
        upos_uri = pre_upload_response['upos_uri'].split('//')[-1]
        auth = pre_upload_response['auth']
        biz_id = pre_upload_response['biz_id']
        chunk_size = pre_upload_response['chunk_size']
        chunks = ceil(filesize/chunk_size)

        self.logger.info('Start uploading the video')
        upload_video_id_response = self.bili_uploader.get_upload_video_id(upos_uri=upos_uri, auth=auth)
        upload_id = upload_video_id_response['upload_id']
        key = upload_video_id_response['key']

        bilibili_filename = re.search(r'/(.*)\.', key).group(1)

        self.logger.info(f'Uploading the video in {chunks} batches')
        fileio = file.open(mode='rb')
        self.bili_uploader.upload_video_in_chunks(
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
        self.bili_uploader.finish_upload(upos_uri=upos_uri, auth=auth, filename=filename,
                           upload_id=upload_id, biz_id=biz_id, chunks=chunks)

        # publish video
        publish_video_response = self.bili_uploader.publish_video(bilibili_filename=bilibili_filename)
        bvid = publish_video_response['data']['bvid']
        # print(publish_video_response)
        self.logger.info(f'[{title}]upload success!\tbvid:{bvid}')
        # reset the video title
        self.ioer.update_specific_config("upload", "title", "")
