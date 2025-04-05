# Copyright (c) 2025 bilitool

import json
import os
import sys


def parse_cookies(cookies_path):
    try:
        with open(cookies_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return "Error: Cookies file not found."
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON from cookies file."

    cookies = data.get("data", {}).get("cookie_info", {}).get("cookies", [])

    sessdata_value = None
    bili_jct_value = None

    for cookie in cookies:
        if cookie["name"] == "SESSDATA":
            sessdata_value = cookie["value"]
        elif cookie["name"] == "bili_jct":
            bili_jct_value = cookie["value"]

    if not sessdata_value or not bili_jct_value:
        return "Error: Required cookies not found."

    return sessdata_value, bili_jct_value


if __name__ == "__main__":
    sessdata, bili_jct = parse_cookies("")
