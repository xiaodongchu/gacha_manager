from collections import Counter
from time import time, sleep

import requests
from loguru import logger

from waves.config_waves import *
from waves.files.base_func import *

waves_save_dir = os.path.join(base_dir, "save")
backup_dir = os.path.join(os.path.dirname(base_dir), "backup")

now_dir = os.path.dirname(__file__)
log_file = os.path.join(backup_dir, "log_waves.txt")
logger.add(log_file, level="DEBUG", encoding="utf-8", enqueue=True)

waves_idx = ["uid", "gacha_type", "cardPoolType", "count", "name", "qualityLevel", "resourceId", "resourceType", "time"]


def get_waves(waves_api_body: dict):
    new_df = get_new_df(columns=waves_idx)
    for gtype, gname in waves_api_info.items():
        waves_api_body["cardPoolType"] = int(gtype)
        response = requests.post(waves_base_url, json=waves_api_body, headers={"Content-Type": "application/json"})
        res = response.json()
        sleep(sleep_time)
        if res["code"] != 0:
            raise Exception("获取失败" + res["message"])
        res = res["data"]
        logger.info(gname + " 共" + str(len(res)) + "条数据 ")
        if len(res) < 1:
            continue
        for i in res:
            i["uid"] = waves_api_body["playerId"]
            i["gacha_type"] = gtype
            new_df.loc[len(new_df)] = i
    backup_and_merge_waves(new_df, waves_api_body["playerId"])
    logger.info("鸣潮抽卡数据更新完成:" + waves_api_body["playerId"])


def merge_waves(old_df: pandas.DataFrame, new_df: pandas.DataFrame):
    """
    由于鸣潮api不对每条数据标注id
    :param old_df:
    :param new_df:
    :return:
    """
    if set(new_df.columns) != set(old_df.columns):
        raise Exception("列名不同" + str(set(new_df.columns)) + str(set(old_df.columns)))
    for gtype, gname in waves_api_info.items():
        old_df_i = old_df[old_df["gacha_type"] == gtype]
        new_df_i = new_df[new_df["gacha_type"] == gtype]
        if len(new_df_i) < 1:
            continue
        old_df_i = old_df_i.groupby("time")["name"].apply(list).reset_index()
        new_df_i_name = new_df_i.groupby("time")["name"].apply(list).reset_index()
        new_df_i_name.sort_values(by="time", ascending=False, ignore_index=True, inplace=True)
        keep_time = []
        old_time_list = old_df_i["time"].to_list()
        for index, row in new_df_i_name.iterrows():
            if row["time"] not in old_time_list:
                keep_time.append(row["time"])
                continue
            old_name_list = old_df_i[old_df_i["time"] == row["time"]]
            old_name_list = old_name_list["name"].to_list()[0]
            if Counter(row["name"]) != Counter(old_name_list):
                # 保留新数据
                for j in old_name_list:
                    j_index = new_df_i[(new_df_i["time"] == row["time"]) & (new_df_i["name"] == j)].index[0]
                    new_df_i.drop(index=j_index, inplace=True)
                keep_time.append(row["time"])
                logger.error("卡池名称：" + gname + " 时间：" + row["time"] + " 数据合并可能有误")
            break
        new_df_i = new_df_i[new_df_i["time"].isin(keep_time)]
        old_df = pandas.concat([old_df, new_df_i], ignore_index=True)
    return old_df


def backup_and_merge_waves(new_df: pandas.DataFrame, uid: str):
    new_df = new_df.astype(str)
    old_path = os.path.join(waves_save_dir, uid + ".csv")
    if os.path.exists(old_path):
        old_df = load_csv(old_path)
        old_backup_path = os.path.join(backup_dir, str(uid + "_backup_" + str(int(time())) + ".csv"))
        logger.info("备份数据:" + uid + " -> " + old_backup_path)
        try_rename(old_path, old_backup_path)
        logger.info("合并数据")
        new_df = merge_waves(old_df, new_df)
    logger.info(uid + "共计" + str(len(new_df)) + "条数据,排序中...")
    new_df.sort_values(by=["time", "cardPoolType"], ascending=False, ignore_index=True, inplace=True)
    update_df(new_df)
    logger.info("写入csv:" + uid)
    csv_path = os.path.join(waves_save_dir, uid + ".csv")
    write_csv(csv_path, new_df)
    new_json = df_to_dict_waves(new_df, uid)
    logger.info("写入json:" + uid)
    json_path = os.path.join(waves_save_dir, uid + ".json")
    write_json(json_path, new_json)
    logger.info("写入excel:" + uid)
    excel_path = os.path.join(waves_save_dir, uid + ".xlsx")
    write_excel(excel_path, new_df)
    return new_df


def get_waves_dict(uid: str):
    time_now = time()
    info = {
        "info": {
            "uid": str(uid),
            "export_timestamp": int(time_now),
            "export_app": "原神·启动",
            "export_app_version": "0.1",
            "version": "v0.1",
            "timezone": 8,
            "lang": "zh-cn",
        },
        "list": [],
    }
    return info


def df_to_dict_waves(df: pandas.DataFrame, uid: str):
    info = get_waves_dict(uid)
    df = df.to_dict(orient="records")
    info["list"] = df
    return info


def dict_to_df_waves(d: dict):
    data = d["list"]
    return pandas.DataFrame(columns=waves_idx, dtype=str, data=data)


def update_df(df: pandas.DataFrame):
    return
