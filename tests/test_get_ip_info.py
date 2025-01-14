# Copyright (c) 2025 bilitool

import unittest
from bilitool.utils.get_ip_info import IPInfo

class TestIPInfo(unittest.TestCase):
    def test_get_ip_address(self):
        self.assertEqual(IPInfo.get_ip_address('12.12.12.12'), 
        ('12.12.12.12', 'att.com', '美国阿拉斯加州安克雷奇', '61.108841,-149.373145'))
 