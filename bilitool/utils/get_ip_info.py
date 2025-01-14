# Copyright (c) 2025 bilitool

import http.client
import urllib.parse
import json

class IPInfo:
    @staticmethod
    def get_ip_address(ip=None):
        url = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
        if ip:
            params = urllib.parse.urlencode({'ip': ip})
            full_url = f"{url}?{params}"
        else:
            full_url = url

        parsed_url = urllib.parse.urlparse(full_url)
        host = parsed_url.netloc
        path = parsed_url.path + ('?' + parsed_url.query if parsed_url.query else '')

        connection = http.client.HTTPSConnection(host)
        connection.request("GET", path)

        response = connection.getresponse()
        data = json.loads(response.read().decode('utf-8'))
        connection.close()

        return IPInfo.print_ip_info(data)

    @staticmethod
    def print_ip_info(ip_info):
        if ip_info['code'] != 0:
            return None
        else:
            addr = ip_info['data']['addr']
            isp = ip_info['data']['isp']
            location = ip_info['data']['country'] + ip_info['data']['province'] + ip_info['data']['city']
            position = ip_info['data']['latitude'] + ',' + ip_info['data']['longitude']
            print(f"IP: {addr}, ISP: {isp}, Location: {location}, Position: {position}")
            return addr, isp, location, position