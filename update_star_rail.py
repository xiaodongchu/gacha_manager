from time import sleep
from urllib.parse import parse_qsl, urlparse

import requests

from load_log import get_star_rail_url
from utils import logger, get_new_df, get_star_rail_ids, star_rail_idx, backup_and_merge_star_rail
from config_jsons.api_info import star_rail_api_info


sleep_time = 0.6


def get_star_rail():
    url = get_star_rail_url()
    if url is None:
        raise Exception("未找到崩坏：星穹铁道链接")
    urp = urlparse(url)
    parse = dict(parse_qsl(urp.query))
    new_df = get_new_df(columns=star_rail_idx)
    star_rail_ids = get_star_rail_ids()
    uid = ""
    for gtype, gname in star_rail_api_info.items():
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
                logger.info("获取 "+gname+" ["+gtype+"]:"+gname+" 结束")
                break
            if not uid:
                uid = str(res[0]["uid"])
                logger.info("uid: "+uid)
            for i in res:
                # ["gacha_id", "gacha_type", "item_id", "count", "time",
                # "name", "item_type", "rank_type", "api_id"]
                j = {
                    "gacha_id": i["gacha_id"],
                    "gacha_type": gtype,
                    "item_id": star_rail_ids[i['name']],
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
            logger.info(gname+" "+str(page)+" 页,"+str(items)+",end_id:"+parse["end_id"])
            page += 1
    backup_and_merge_star_rail(uid, new_df)
    logger.info("崩坏：星穹铁道抽卡数据更新完成:"+uid)


if __name__ == '__main__':
    get_star_rail()
