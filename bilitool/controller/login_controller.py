# Copyright (c) 2025 bilitool

from bilitool.model.model import Model
import qrcode
from bilitool.login.login_bili import LoginBili
from bilitool.login.logout_bili import LogoutBili
from bilitool.login.check_bili_login import CheckBiliLogin


class LoginController(object):
    def __init__(self):
        self.model = Model()
        self.login_bili = LoginBili()
        self.logout_bili = LogoutBili()
        self.check_bili_login = CheckBiliLogin()
    
    def login_bilibili(self, export):
        input("Please maximize the window to ensure the QR code is fully displayed, press Enter to continue: ")
        login_url, auth_code = self.login_bili.get_tv_qrcode_url_and_auth_code()
        qr = qrcode.QRCode()
        qr.add_data(login_url)
        qr.print_ascii()
        print("Or copy this link to your phone Bilibili:", login_url)
        self.login_bili.verify_login(auth_code, export)

    def logout_bilibili(self):
        self.logout_bili.logout_bili()

    def check_bilibili_login(self):
        return self.check_bili_login.check_bili_login()
