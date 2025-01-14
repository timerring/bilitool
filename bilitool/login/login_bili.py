# Copyright (c) 2025 bilitool

import hashlib
import subprocess
import time
import json
import qrcode
from urllib.parse import urlencode
from bilitool.authenticate.ioer import ioer

APP_KEY = "4409e2ce8ffd12b8"
APP_SEC = "59b43e04ad6965f34319062b478f83dd"

def signature(params):
    params['appkey'] = APP_KEY
    keys = sorted(params.keys())
    query = '&'.join(f"{k}={params[k]}" for k in keys)
    query += APP_SEC
    md5_hash = hashlib.md5(query.encode('utf-8')).hexdigest()
    params['sign'] = md5_hash

def map_to_string(params):
    return urlencode(params)

def execute_curl_command(api, data):
    data_string = map_to_string(data)
    headers = "Content-Type: application/x-www-form-urlencoded"
    curl_command = f"curl -X POST -H \"{headers}\" -d \"{data_string}\" {api}"
    result = subprocess.run(
        curl_command, shell=True, capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        raise Exception(f"curl command failed: {result.stderr}")
    return json.loads(result.stdout)

def get_tv_qrcode_url_and_auth_code():
    api = "https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code"
    data = {
        "local_id": "0",
        "ts": str(int(time.time()))
    }
    signature(data)
    body = execute_curl_command(api, data)
    if body['code'] == 0:
        qrcode_url = body['data']['url']
        auth_code = body['data']['auth_code']
        return qrcode_url, auth_code
    else:
        raise Exception("get_tv_qrcode_url_and_auth_code error")

def verify_login(auth_code, export):
    api = "https://passport.bilibili.com/x/passport-tv-login/qrcode/poll"
    data = {
        "auth_code": auth_code,
        "local_id": "0",
        "ts": str(int(time.time()))
    }
    signature(data)
    while True:
        body = execute_curl_command(api, data)
        if body['code'] == 0:
            filename = "cookie.json"
            if export:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(body, f, ensure_ascii=False, indent=4)
                print(f"cookie has been saved to {filename}")

            sessdata_value = body['data']['cookie_info']['cookies'][0]['value']
            bili_jct_value = body['data']['cookie_info']['cookies'][1]['value']
            dede_user_id_value = body['data']['cookie_info']['cookies'][2]['value']
            dede_user_id_ckmd5_value = body['data']['cookie_info']['cookies'][3]['value']
            ioer().save_cookies_info(sessdata_value, bili_jct_value, dede_user_id_value, dede_user_id_ckmd5_value)
            print("Login success!")
            break
        else:
            time.sleep(3)

def login_bili(export):
    input("Please maximize the window to ensure the QR code is fully displayed, press Enter to continue: ")
    login_url, auth_code = get_tv_qrcode_url_and_auth_code()
    qr = qrcode.QRCode()
    qr.add_data(login_url)
    qr.print_ascii()
    print("Or copy this link to your phone Bilibili:", login_url)
    verify_login(auth_code, export)

if __name__ == "__main__":
    login_bili()