genshin_api_info = {
    "100": "新手祈愿",
    "200": "常驻祈愿",
    "301": "角色活动祈愿",
    "302": "武器活动祈愿"
}
star_rail_api_info = {
    '1': "常驻",
    '2': "新手",
    '11': "角色",
    '12': "光锥",
}
genshin_gacha_type = {
    "100": "新手祈愿",
    "200": "常驻祈愿",
    "301": "角色活动祈愿",
    "302": "武器活动祈愿",
    "400": "角色活动祈愿-2"
}

a = {
    "list": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "uigf_gacha_type": {
                    "type": "string",
                    "title": "UIGF 卡池类型",
                    "description": "用于区分卡池类型不同，但卡池保底计算相同的物品"
                },
                "gacha_type": {
                    "type": "string",
                    "title": "卡池类型"
                },
                "item_id": {
                    "type": "string",
                    "title": "物品的内部 ID"
                },
                "count": {
                    "type": "string",
                    "title": "个数，一般为1"
                },
                "time": {
                    "type": "string",
                    "title": "获取物品的时间"
                },
                "name": {
                    "type": "string",
                    "title": "物品名称"
                },
                "item_type": {
                    "type": "string",
                    "title": "物品类型"
                },
                "rank_type": {
                    "type": "string",
                    "title": "物品等级"
                },
                "id": {
                    "type": "string",
                    "title": "记录内部 ID"
                }
            },
            "required": ["uigf_gacha_type", "gacha_type", "id", "item_id", "time"],
            "title": "UIGF 物品"
        },
        "title": "物品列表"
    }
}
