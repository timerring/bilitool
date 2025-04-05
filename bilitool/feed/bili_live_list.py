# Copyright (c) 2025 bilitool

import requests


class BiliLiveList:
    def __init__(self, headers):
        self.headers = headers

    def get_live_info(self, room) -> dict:
        """Get the live info of the room"""

        url = (
            "https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room}".format(
                room=room
            )
        )
        response = requests.get(url=url, headers=self.headers)
        if response.status_code != 200:
            raise Exception("HTTP ERROR")
        response_json = response.json().get("data")
        if response.json().get("code") != 0:
            raise Exception(response.json().get("message"))
        return response_json
