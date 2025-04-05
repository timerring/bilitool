# Copyright (c) 2025 bilitool


class CheckFormat(object):
    def __init__(self):
        self.XOR_CODE = 23442827791579
        self.MASK_CODE = 2251799813685247
        self.MAX_AID = 1 << 51
        self.ALPHABET = "FcwAPNKTMug3GV5Lj7EJnHpWsx4tb8haYeviqBz6rkCy12mUSDQX9RdoZf"
        self.ENCODE_MAP = 8, 7, 0, 5, 1, 3, 2, 4, 6
        self.DECODE_MAP = tuple(reversed(self.ENCODE_MAP))

        self.BASE = len(self.ALPHABET)
        self.PREFIX = "BV1"
        self.PREFIX_LEN = len(self.PREFIX)
        self.CODE_LEN = len(self.ENCODE_MAP)

    @staticmethod
    def is_bvid(bvid: str) -> bool:
        if len(bvid) != 12:
            return False
        if bvid[0:2] != "BV":
            return False
        return True

    @staticmethod
    def is_chinese(word: str) -> bool:
        for ch in word:
            if "\u4e00" <= ch <= "\u9fff":
                return True
        return False

    # https://github.com/SocialSisterYi/bilibili-API-collect/blob/e5fbfed42807605115c6a9b96447f6328ca263c5/docs/misc/bvid_desc.md

    def av2bv(self, aid: int) -> str:
        bvid = [""] * 9
        tmp = (self.MAX_AID | aid) ^ self.XOR_CODE
        for i in range(self.CODE_LEN):
            bvid[self.ENCODE_MAP[i]] = self.ALPHABET[tmp % self.BASE]
            tmp //= self.BASE
        return self.PREFIX + "".join(bvid)

    def bv2av(self, bvid: str) -> int:
        assert bvid[:3] == self.PREFIX

        bvid = bvid[3:]
        tmp = 0
        for i in range(self.CODE_LEN):
            idx = self.ALPHABET.index(bvid[self.DECODE_MAP[i]])
            tmp = tmp * self.BASE + idx
        return (tmp & self.MASK_CODE) ^ self.XOR_CODE

    def convert_bv_and_av(self, vid: str):
        if self.is_bvid(str(vid)):
            print("The avid of the video is: ", self.bv2av(str(vid)))
        else:
            print("The bvid of the video is: ", self.av2bv(int(vid)))

    def only_bvid(self, vid: str):
        if self.is_bvid(str(vid)):
            return vid
        else:
            return self.av2bv(int(vid))
