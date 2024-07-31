import json
import os
import shutil
from time import time, sleep
from urllib.parse import urlparse, parse_qsl, urlencode

import pandas
import requests
from loguru import logger

from rail.config_rail import base_dir

rail_save_dir = os.path.join(base_dir, "save")
backup_dir = os.path.join(os.path.dirname(base_dir), "backup")

now_dir = os.path.dirname(__file__)
rail_id_path = os.path.join(now_dir, "rail_id.json")
rail_schema_path = os.path.join(now_dir, "json_schema.json")
log_file = os.path.join(backup_dir, "log_rail.txt")
logger.add(log_file, level="DEBUG", encoding="utf-8", enqueue=True)

rail_idx = ["gacha_id", "gacha_type", "item_id", "count", "time", "name", "item_type", "rank_type", "api_id"]

rail_api_info = {
    '1': "常驻",
    '2': "新手",
    '11': "角色",
    '12': "光锥",
}


def get_rail(url: str, sleep_time=0.6):
    urp = urlparse(url)
    url = url.split("?")[0]
    parse = dict(parse_qsl(urp.query))
    new_df = get_new_df(columns=rail_idx)
    rail_ids = get_rail_ids()
    uid = ""
    for gtype, gname in rail_api_info.items():
        page = 1
        parse["end_id"] = "0"
        parse["gacha_type"] = gtype
        while True:
            parse["page"] = str(page)
            new_url = url + "?" + urlencode(parse)
            logger.debug(new_url)
            response = requests.get(new_url, headers={"Content-Type": "application/json"})
            res = response.json()
            sleep(sleep_time)
            if res["retcode"] != 0:
                raise Exception("获取失败" + res["message"])
            res = res["data"]["list"]
            if len(res) < 1:
                logger.info("获取 " + " [" + gtype + "]:" + gname + " 结束")
                break
            if not uid:
                uid = str(res[0]["uid"])
                logger.info("uid: " + uid)
            for i in res:
                # ["gacha_id", "gacha_type", "item_id", "count", "time",
                # "name", "item_type", "rank_type", "api_id"]
                j = {
                    "gacha_id": i["gacha_id"],
                    "gacha_type": gtype,  # ugif
                    "item_id": rail_ids[i['name']],
                    "count": i["count"],
                    "time": i["time"],
                    "name": i["name"],
                    "item_type": i["item_type"],
                    "rank_type": i["rank_type"],
                    "api_id": i["id"]
                }
                # 如果api_id已经存在,报错
                if j["api_id"] in new_df["api_id"].values:
                    raise Exception("api_id已经存在" + str(j) + str(parse))
                new_df.loc[len(new_df)] = j
            parse["end_id"] = res[-1]["id"]
            items = [i["name"] for i in res]
            logger.info(gname + " " + str(page) + " 页," + str(items) + ",end_id:" + parse["end_id"])
            page += 1
    backup_and_merge_rail(uid, new_df)
    logger.info("崩坏：星穹铁道抽卡数据更新完成:" + uid)


def backup_and_merge_rail(uid, new_df: pandas.DataFrame):
    if new_df["api_id"].duplicated().any():
        raise Exception("api_id重复")
    uid = str(uid)
    new_df = new_df.astype(str)
    old_path = os.path.join(rail_save_dir, uid + ".csv")
    if os.path.exists(old_path):
        old_df = load_csv(old_path)
        if set(new_df.columns) != set(old_df.columns):
            raise Exception("列名不同" + str(set(new_df.columns)) + str(set(old_df.columns)))
        old_backup_path = os.path.join(backup_dir, str(uid + "_backup_" + str(int(time())) + ".csv"))
        logger.info("备份数据:" + uid + " -> " + old_backup_path)
        try_rename(old_path, old_backup_path)
        logger.info("合并数据")
        new_df = pandas.concat([new_df, old_df], ignore_index=True)
        new_df = new_df.drop_duplicates(subset=["api_id"], keep="first", ignore_index=True)
    logger.info(uid + "共计" + str(len(new_df)) + "条数据,排序中...")
    new_df = new_df.sort_values(by=["time", "api_id"], ascending=False, ignore_index=True)
    update_df(new_df)
    logger.info("写入csv:" + uid)
    csv_path = os.path.join(rail_save_dir, uid + ".csv")
    write_csv(csv_path, new_df)
    new_json = df_to_uigf_rail(new_df, uid)
    logger.info("写入json:" + uid)
    json_path = os.path.join(rail_save_dir, uid + ".json")
    write_json(json_path, new_json)
    logger.info("写入excel:" + uid)
    excel_path = os.path.join(rail_save_dir, uid + ".xlsx")
    write_excel(excel_path, new_df)
    return new_df


def get_rail_uigf_info(uid):
    time_now = time()
    info = {
        "info": {
            "export_timestamp": int(time_now),
            "export_app": "原神·启动",
            "export_app_version": "0.1",
            "version": "v4.0",
        },
        "hkrpg": [
            {
                "uid": str(uid),
                "timezone": 8,
                "lang": "zh-cn",
                "list": [],
            }
        ],
    }
    return info


def df_to_uigf_rail(df: pandas.DataFrame, uid):
    info = get_rail_uigf_info(uid)
    df = df.to_dict(orient="records")
    for i in df:
        i["id"] = i["api_id"]
        del i["api_id"]
    info["hkrpg"][0]["list"] = df
    return info


def uigf_to_df_rail(uigf_json: dict):
    """

    :param uigf_json: 须确保仅包含1个uid，且为中文
    :return:
    """
    rail_ids = get_rail_ids()
    data = uigf_json['hkrpg'][0]["list"]
    for i in data:
        i['item_id'] = rail_ids[i['name']]
        i['api_id'] = i['id']
        del i['id']
    df = get_new_df(columns=rail_idx, dtype=str, data=data)
    return df


def get_rail_ids():
    rail_url = "https://api.uigf.org/dict/starrail/chs.json"
    try:
        rail_ids = requests.get(rail_url).json()
        if len(rail_ids) > 10:
            write_json(rail_id_path, rail_ids)
            return rail_ids
    except:
        pass
    return load_json(rail_id_path)


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


def try_rename(old_file, new_path):
    if os.path.exists(old_file) and not os.path.exists(new_path) and os.path.isfile(old_file):
        os.chmod(old_file, 0o777)
        shutil.move(old_file, new_path)
    else:
        raise Exception("文件备份错误")


def update_df(df: pandas.DataFrame):
    return
