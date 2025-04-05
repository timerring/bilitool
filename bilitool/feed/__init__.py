# Copyright (c) 2025 bilitool


def VideoListInfo():
    return {
        "bvid": str(),
        "title": "video title",
        "state_desc": "",
        # the status detail
        "state": 0,
        "reject_reason": "",
        # the overview of status 0: pass review 1: reviewing 2: rejected 3: clash 4: the codec issue
        "state_panel": 0,
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
    -100: "用户删除",
}

video_info_dict = {
    "title": "标题",
    "desc": "描述",
    "duration": "时长",
    "pubdate": "发布日期",
    "owner_name": "作者名称",
    "tname": "分区",
    "copyright": "版权",
    "width": "宽",
    "height": "高",
    "stat_view": "观看数",
    "stat_danmaku": "弹幕数",
    "stat_reply": "评论数",
    "stat_coin": "硬币数",
    "stat_share": "分享数",
    "stat_like": "点赞数",
}
