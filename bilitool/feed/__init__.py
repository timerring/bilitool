# Copyright (c) 2025 bilitool

def VideoListInfo():
    return {
        "bvid": str(),
        "title": 'video title',
        "state_desc": '',
        # the status detail
        "state": 0,
        "reject_reason": '',
        # the overview of status 0: pass review 1: reviewing 2: rejected 3: clash 4: the codec issue
        "state_panel": 0
    }

# https://github.com/SocialSisterYi/bilibili-API-collect/blob/e5fbfed42807605115c6a9b96447f6328ca263c5/docs/video/attribute_data.md?plain=1#L44
state_dict = {
    1: "橙色通过",
    0: "开放浏览",
    -1: "待审",
    -2: "被打回",
    -3: "网警锁定",
    -4: "被锁定",
    -5: "管理员锁定",
    -6: "修复待审",
    -7: "暂缓审核",
    -8: "补档待审",
    -9: "等待转码",
    -10: "延迟审核",
    -11: "视频源待修",
    -12: "转储失败",
    -13: "允许评论待审",
    -14: "临时回收站",
    -15: "分发中",
    -16: "转码失败",
    -20: "创建未提交",
    -30: "创建已提交",
    -40: "定时发布",
    -50: "仅UP主可见",
    -100: "用户删除"
}