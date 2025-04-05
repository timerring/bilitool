# Copyright (c) 2025 bilitool

from ..model.model import Model
from ..upload.bili_upload import BiliUploader
from pathlib import Path
import re
from math import ceil
import logging
from ..utils.parse_yaml import parse_yaml


class UploadController:
    def __init__(self):
        self.logger = logging.getLogger("bilitool")
        self.bili_uploader = BiliUploader(self.logger)

    @staticmethod
    def package_upload_metadata(
        copyright, tid, title, desc, tag, source, cover, dynamic
    ):
        return {
            "copyright": copyright,
            "tid": tid,
            "title": title,
            "desc": desc,
            "tag": tag,
            "source": source,
            "cover": cover,
            "dynamic": dynamic,
        }

    def upload_video(self, file, cdn=None):
        """upload and publish video on bilibili"""
        if cdn == "qn":
            upos_url = "//upos-cs-upcdnqn.bilivideo.com/"
            probe_version = "20221109"
        elif cdn == "bldsa":
            upos_url = "//upos-cs-upcdnbldsa.bilivideo.com/"
            probe_version = "20221109"
        elif cdn == "ws":
            upos_url = "//upos-sz-upcdnws.bilivideo.com/"
            probe_version = "20221109"
        elif cdn == "bda2":
            upos_url = "//upos-cs-upcdnbda2.bilivideo.com/"
            probe_version = "20221109"
        elif cdn == "tx":
            upos_url = "//upos-cs-upcdntx.bilivideo.com/"
            probe_version = "20221109"
        else:
            upos_url, cdn, probe_version = self.bili_uploader.probe()
        file = Path(file)
        assert file.exists(), f"The file {file} does not exist"
        filename = file.name
        title = Model().get_config()["upload"]["title"] or file.stem
        Model().update_specific_config("upload", "title", title)
        filesize = file.stat().st_size
        self.logger.info(f"The {title} to be uploaded")

        # upload video
        self.logger.info("Start preuploading the video")
        pre_upload_response = self.bili_uploader.preupload(
            filename=filename, filesize=filesize, cdn=cdn, probe_version=probe_version
        )
        upos_uri = pre_upload_response["upos_uri"].split("//")[-1]
        auth = pre_upload_response["auth"]
        biz_id = pre_upload_response["biz_id"]
        chunk_size = pre_upload_response["chunk_size"]
        chunks = ceil(filesize / chunk_size)

        self.logger.info("Start uploading the video")
        upload_video_id_response = self.bili_uploader.get_upload_video_id(
            upos_uri=upos_uri, auth=auth, upos_url=upos_url
        )
        upload_id = upload_video_id_response["upload_id"]
        key = upload_video_id_response["key"]

        bilibili_filename = re.search(r"/(.*)\.", key).group(1)

        self.logger.info(f"Uploading the video in {chunks} batches")
        fileio = file.open(mode="rb")
        self.bili_uploader.upload_video_in_chunks(
            upos_uri=upos_uri,
            auth=auth,
            upload_id=upload_id,
            fileio=fileio,
            filesize=filesize,
            chunk_size=chunk_size,
            chunks=chunks,
            upos_url=upos_url,
        )
        fileio.close()

        # notify the all chunks have been uploaded
        self.bili_uploader.finish_upload(
            upos_uri=upos_uri,
            auth=auth,
            filename=filename,
            upload_id=upload_id,
            biz_id=biz_id,
            chunks=chunks,
            upos_url=upos_url,
        )
        return bilibili_filename

    def publish_video(self, file, cdn=None):
        bilibili_filename = self.upload_video(file, cdn)
        # publish video
        publish_video_response = self.bili_uploader.publish_video(
            bilibili_filename=bilibili_filename
        )
        if publish_video_response["code"] == 0:
            bvid = publish_video_response["data"]["bvid"]
            self.logger.info(f"upload success!\tbvid:{bvid}")
            return True
        else:
            self.logger.error(publish_video_response["message"])
            return False
        # reset the video title
        Model().reset_upload_config()

    def append_video_entry(self, video_path, bvid, cdn=None, video_name=None):
        bilibili_filename = self.upload_video(video_path, cdn)
        video_name = video_name if video_name else Path(video_path).name.strip(".mp4")
        video_data = self.bili_uploader.get_video_list_info(bvid)
        response = self.bili_uploader.append_video(
            bilibili_filename, video_name, video_data
        ).json()
        if response["code"] == 0:
            self.logger.info(f"append {video_name} to {bvid} success!")
            return True
        else:
            self.logger.error(response["message"])
            return False
        # reset the video title
        Model().reset_upload_config()

    def upload_video_entry(
        self,
        video_path,
        yaml,
        copyright,
        tid,
        title,
        desc,
        tag,
        source,
        cover,
        dynamic,
        cdn=None,
    ):
        if yaml:
            # * is used to unpack the tuple
            upload_metadata = self.package_upload_metadata(*parse_yaml(yaml))
        else:
            upload_metadata = self.package_upload_metadata(
                copyright, tid, title, desc, tag, source, cover, dynamic
            )
        if upload_metadata["cover"]:
            upload_metadata["cover"] = self.bili_uploader.cover_up(
                upload_metadata["cover"]
            )
        Model().update_multiple_config("upload", upload_metadata)
        return self.publish_video(video_path, cdn)
