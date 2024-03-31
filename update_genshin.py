from time import sleep
from urllib.parse import parse_qsl, urlparse

import requests

from load_log import get_genshin_url
from utils import logger, get_new_df, get_genshin_ids, genshin_idx, backup_and_merge_genshin
from config_jsons.api_info import genshin_api_info


sleep_time = 0.6


def get_genshin():
    url = get_genshin_url()
    if url is None:
        raise Exception("未找到原神链接")
    urp = urlparse(url)
    parse = dict(parse_qsl(urp.query))
    new_df = get_new_df(columns=genshin_idx)
    genshin_ids = get_genshin_ids()
    uid = ""
    for gtype, gname in genshin_api_info.items():
        page = 1
        parse["end_id"] = "0"
        parse["gacha_type"] = gtype
        while True:
            parse["page"] = str(page)
            response = requests.get(url.split("?")[0], params=parse, headers={"Content-Type": "application/json"})
            sleep(sleep_time)
            res = response.json()
            if res["retcode"] != 0:
                raise Exception("获取失败" + res["message"])
            res = res["data"]["list"]
            if len(res) < 1:
                logger.info("获取 "+" ["+gtype+"]:"+gname+" 结束")
                break
            if not uid:
                uid = str(res[0]["uid"])
                logger.info("uid: "+uid)
            for i in res:
                # ["uigf_gacha_type", "gacha_type", "item_id", "count", "time",
                # "name", "item_type", "rank_type", "api_id"]
                j = {
                    "uigf_gacha_type": i["gacha_type"],
                    "gacha_type": gtype,
                    "item_id": genshin_ids[i['name']],
                    "count": i["count"],
                    "time": i["time"],
                    "name": i["name"],
                    "item_type": i["item_type"],
                    "rank_type": i["rank_type"],
                    "api_id": i["id"]
                }
                # 如果api_id已经存在,报错
                if j["api_id"] in new_df["api_id"].values:
                    raise Exception("api_id已经存在"+str(j)+str(parse))
                new_df.loc[len(new_df)] = j
            parse["end_id"] = res[-1]["id"]
            items = [i["name"] for i in res]
            logger.info(gname+" "+str(page)+" 页,"+str(items)+",end_id: "+parse["end_id"])
            page += 1
    backup_and_merge_genshin(uid, new_df)
    logger.info("原神抽卡数据更新完成:"+uid)


if __name__ == '__main__':
    get_genshin()
