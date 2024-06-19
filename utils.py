import os
import json
from loguru import logger
import pandas
import requests
from time import time, localtime, strftime

now_dir = os.path.dirname(__file__) + "/"
genshin_save_path = now_dir + "save/genshin/"
star_rail_save_path = now_dir + "save/star_rail/"
log_file = now_dir + "log/log.txt"
logger.add(log_file, level="DEBUG", encoding="utf-8", enqueue=True)
genshin_id_path = now_dir + "config_jsons/genshin_id.json"
star_rail_id_path = now_dir + "config_jsons/star_rail_id.json"
genshin_idx = ["uigf_gacha_type", "gacha_type", "item_id", "count", "time", "name", "item_type", "rank_type", "api_id"]
star_rail_idx = ["gacha_id", "gacha_type", "item_id", "count", "time", "name", "item_type", "rank_type", "api_id"]


def get_genshin_ids():
    genshin_url = "https://api.uigf.org/dict/genshin/chs.json"
    genshin_ids = requests.get(genshin_url).json()
    write_json(genshin_id_path, genshin_ids)
    return genshin_ids


def get_star_rail_ids():
    star_rail_url = "https://api.uigf.org/dict/starrail/chs.json"
    star_rail_ids = requests.get(star_rail_url).json()
    write_json(star_rail_id_path, star_rail_ids)
    return star_rail_ids


def get_genshin_uigf_info(uid):
    time_now = time()
    info = {
        "info": {
            "uid": str(uid),
            "lang": "zh-Hans",
            "export_timestamp": int(time_now),
            "export_time": strftime("%Y-%m-%d %H:%M:%S", localtime(time_now)),
            "export_app": "原神·启动",
            "export_app_version": "0.1",
            "uigf_version": "v2.4",
            "region_time_zone": 8
        },
        "list": []
    }
    return info


def df_to_uigf_genshin(df: pandas.DataFrame, uid):
    info = get_genshin_uigf_info(uid)
    df = df.to_dict(orient="records")
    for i in df:
        i["id"] = i["api_id"]
        del i["api_id"]
    info["list"] = df
    return info


def uigf_to_df_genshin(uigf_json: dict):
    genshin_ids = get_genshin_ids()
    data = uigf_json['list']
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
    old_path = genshin_save_path + uid + ".csv"
    if os.path.exists(old_path):
        old_df = load_csv(old_path)
        if set(new_df.columns) != set(old_df.columns):
            raise Exception("列名不同" + str(set(new_df.columns)) + str(set(old_df.columns)))
        old_backup_path = genshin_save_path + uid + "_backup" + ".csv"
        try_remove(old_backup_path)
        logger.info("备份数据:" + uid + " -> " + old_backup_path)
        os.rename(old_path, old_backup_path)
        logger.info("合并数据")
        new_df = pandas.concat([new_df, old_df], ignore_index=True)
        new_df = new_df.drop_duplicates(subset=["api_id"], keep="first", ignore_index=True)
    logger.info(uid+"共计"+str(len(new_df))+"条数据,排序中...")
    new_df = new_df.sort_values(by=["time", "api_id"], ascending=False, ignore_index=True)
    logger.info("写入csv:" + uid)
    write_csv(genshin_save_path + uid + ".csv", new_df)
    new_json = df_to_uigf_genshin(new_df, uid)
    logger.info("写入json:" + uid)
    write_json(genshin_save_path + uid + ".json", new_json)
    logger.info("写入excel:" + uid)
    write_excel(genshin_save_path + uid + ".xlsx", new_df)
    return new_df


def get_star_rail_uigf_info(uid):
    time_now = time()
    info = {
        "info": {
            "uid": str(uid),
            "lang": "zh-Hans",
            "region_time_zone": 8,
            "export_timestamp": int(time_now),
            "export_app": "原神·启动",
            "export_app_version": "0.1",
            "srgf_version": "v1.0"
        },
        "list": []
    }
    return info


def df_to_uigf_star_rail(df: pandas.DataFrame, uid):
    info = get_star_rail_uigf_info(uid)
    df = df.to_dict(orient="records")
    for i in df:
        i["id"] = i["api_id"]
        del i["api_id"]
    info["list"] = df
    return info


def uigf_to_df_star_rail(uigf_json: dict):
    star_rail_ids = get_star_rail_ids()
    data = uigf_json['list']
    for i in data:
        i['item_id'] = star_rail_ids[i['name']]
        i['api_id'] = i['id']
        del i['id']
    df = get_new_df(columns=star_rail_idx, dtype=str, data=data)
    return df


def backup_and_merge_star_rail(uid, new_df: pandas.DataFrame):
    if new_df["api_id"].duplicated().any():
        raise Exception("api_id重复")
    uid = str(uid)
    new_df = new_df.astype(str)
    old_path = star_rail_save_path + uid + ".csv"
    if os.path.exists(old_path):
        old_df = load_csv(old_path)
        if set(new_df.columns) != set(old_df.columns):
            raise Exception("列名不同" + str(set(new_df.columns)) + str(set(old_df.columns)))
        old_backup_path = star_rail_save_path + uid + "_backup" + ".csv"
        try_remove(old_backup_path)
        logger.info("备份数据:" + uid + " -> " + old_backup_path)
        os.rename(old_path, old_backup_path)
        logger.info("合并数据")
        new_df = pandas.concat([new_df, old_df], ignore_index=True)
        new_df = new_df.drop_duplicates(subset=["api_id"], keep="first", ignore_index=True)
    logger.info(uid+"共计"+str(len(new_df))+"条数据,排序中...")
    new_df = new_df.sort_values(by=["time", "api_id"], ascending=False, ignore_index=True)
    logger.info("写入csv:" + uid)
    write_csv(star_rail_save_path + uid + ".csv", new_df)
    new_json = df_to_uigf_star_rail(new_df, uid)
    logger.info("写入json:" + uid)
    write_json(star_rail_save_path + uid + ".json", new_json)
    logger.info("写入excel:" + uid)
    write_excel(star_rail_save_path + uid + ".xlsx", new_df)
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

