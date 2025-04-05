# Copyright (c) 2025 bilitool

import unittest
from bilitool.utils.get_ip_info import IPInfo
from bilitool.utils.check_format import CheckFormat


class TestIPInfo(unittest.TestCase):
    def test_get_ip_address(self):
        self.assertEqual(
            IPInfo.get_ip_address("12.12.12.12"),
            (
                "12.12.12.12",
                "att.com",
                "美国阿拉斯加州安克雷奇",
                "61.108841,-149.373145",
            ),
        )


class TestCheckFormat(unittest.TestCase):
    def test_av2bv(self):
        check_format = CheckFormat()
        self.assertEqual(check_format.av2bv(2), "BV1xx411c7mD")

    def test_bv2av(self):
        check_format = CheckFormat()
        self.assertEqual(check_format.bv2av("BV1y7411Q7Eq"), 99999999)
