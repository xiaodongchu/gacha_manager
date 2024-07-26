import json
import os
from time import time, sleep
from urllib.parse import urlparse, parse_qsl, urlencode

import pandas
import requests
from loguru import logger
from pyperclip import copy

from genshin.config_genshin import genshin_game_path, base_dir


genshin_save_dir = os.path.join(base_dir, "save")

now_dir = os.path.dirname(__file__)
genshin_id_path = os.path.join(now_dir, "genshin_id.json")
genshin_schema_path = os.path.join(now_dir, "json_schema.json")
log_file = os.path.join(genshin_save_dir, "log.txt")
logger.add(log_file, level="DEBUG", encoding="utf-8", enqueue=True)

genshin_idx = ["uigf_gacha_type", "gacha_type", "item_id", "count", "time", "name", "item_type", "rank_type", "api_id"]

genshin_api_info = {
    "100": "新手祈愿",
    "200": "常驻祈愿",
    "301": "角色活动祈愿",
    "302": "武器活动祈愿",
    "500": "集录祈愿"
}


def get_genshin_url():
    genshin_link_retain = ["authkey", "authkey_ver", "sign_type", "game_biz", "auth_appid", "size", "region", "win_mode", "device_type"]
    logger.info("正在获取原神链接")
    logger.debug("路径:"+genshin_game_path)
    f = open(genshin_game_path, 'r', encoding='utf-8', errors='replace')
    words = f.read()
    f.close()
    words = words.split('1/0/')
    for i in range(len(words) - 1, -1, -1):
        line = words[i]
        if line.startswith('http') and "getGachaLog" in line:
            url = line.split("\0")[0]
            response = requests.get(url, headers={"Content-Type": "application/json"})
            res = response.json()
            if res["retcode"] == 0:
                urp = urlparse(url)
                parse = dict(parse_qsl(urp.query))
                parse = {key: parse[key] for key in parse if key in genshin_link_retain}
                parse["lang"] = "zh-cn"
                parse["page"] = "1"
                parse["end_id"] = "0"
                latest_url = url.split("?")[0] + "?" + urlencode(parse)
                copy(latest_url)
                logger.info(latest_url)
                return latest_url
    logger.error("未找到原神链接")
    return None


def get_genshin(url: str, sleep_time=0.6):
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
                    "uigf_gacha_type": gtype,
                    "gacha_type": i["gacha_type"],
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


def get_genshin_ids():
    genshin_url = "https://api.uigf.org/dict/genshin/chs.json"
    genshin_ids = requests.get(genshin_url).json()
    write_json(genshin_id_path, genshin_ids)
    return genshin_ids


def get_genshin_uigf_info(uid):
    time_now = time()
    info = {
        "info": {
            "export_timestamp": int(time_now),
            "export_app": "原神·启动",
            "export_app_version": "0.1",
            "version": "v4.0",
        },
        "hk4e": [
            {
                "uid": str(uid),
                "timezone": 8,
                "lang": "zh-cn",
                "list": [],
            }
        ],
    }
    return info


def df_to_uigf_genshin(df: pandas.DataFrame, uid):
    info = get_genshin_uigf_info(uid)
    df = df.to_dict(orient="records")
    for i in df:
        i["id"] = i["api_id"]
        del i["api_id"]
    info["hk4e"][0]["list"] = df
    return info


def uigf_to_df_genshin(uigf_json: dict):
    """

    :param uigf_json: 须确保仅包含1个uid，且为中文
    :return:
    """
    genshin_ids = get_genshin_ids()
    data = uigf_json['hk4e'][0]['list']
    for i in data:
        i['item_id'] = genshin_ids[i['name']]
        i['api_id'] = i['id']
        del i['id']
    df = get_new_df(columns=genshin_idx, dtype=str, data=data)
    return df


def backup_and_merge_genshin(uid, new_df: pandas.DataFrame):
    if new_df["api_id"].duplicated().any():
        raise Exception("api_id重复")
    uid = str(uid)
    new_df = new_df.astype(str)
    old_path = os.path.join(genshin_save_dir, uid + ".csv")
    if os.path.exists(old_path):
        old_df = load_csv(old_path)
        if set(new_df.columns) != set(old_df.columns):
            raise Exception("列名不同" + str(set(new_df.columns)) + str(set(old_df.columns)))
        old_backup_path = os.path.join(genshin_save_dir, uid + "_backup" + ".csv")
        try_remove(old_backup_path)
        logger.info("备份数据:" + uid + " -> " + old_backup_path)
        os.rename(old_path, old_backup_path)
        logger.info("合并数据")
        new_df = pandas.concat([new_df, old_df], ignore_index=True)
        new_df = new_df.drop_duplicates(subset=["api_id"], keep="first", ignore_index=True)
    logger.info(uid+"共计"+str(len(new_df))+"条数据,排序中...")
    new_df = new_df.sort_values(by=["time", "api_id"], ascending=False, ignore_index=True)
    update_df(new_df)
    logger.info("写入csv:" + uid)
    csv_path = os.path.join(genshin_save_dir, uid + ".csv")
    write_csv(csv_path, new_df)
    new_json = df_to_uigf_genshin(new_df, uid)
    logger.info("写入json:" + uid)
    json_path = os.path.join(genshin_save_dir, uid + ".json")
    write_json(json_path, new_json)
    logger.info("写入excel:" + uid)
    excel_path = os.path.join(genshin_save_dir, uid + ".xlsx")
    write_excel(excel_path, new_df)
    return new_df


def load_json(path):
    f = open(path, "r", encoding="utf-8")
    j = json.load(f)
    f.close()
    return j


def write_json(path, j):
    f = open(path, "w", encoding="utf-8")
    json.dump(j, f, ensure_ascii=False, indent=4)
    f.close()


def load_csv(path):
    return pandas.read_csv(path, index_col=0, encoding="utf-8", dtype=str)


def write_csv(path, df):
    df.to_csv(path, encoding="utf-8")
    os.chmod(path, 0o444)


def write_excel(path, df):
    df.to_excel(path)


def get_new_df(columns, dtype=str, data=None):
    return pandas.DataFrame(columns=columns, data=data, dtype=dtype)


def try_remove(path):
    if os.path.exists(path):
        os.chmod(path, 0o777)
        os.remove(path)


def update_df(df):
    # uigf_gacha_type列中的400改为301
    df.replace({"uigf_gacha_type": {"400": "301"}}, inplace=True)
