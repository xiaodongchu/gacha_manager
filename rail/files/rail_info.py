from time import time, sleep
from copy import deepcopy
from urllib.parse import urlparse, parse_qsl, urlencode

import requests
from loguru import logger

from rail.config_rail import base_dir
from rail.files.base_func import *

rail_save_dir = os.path.join(base_dir, "save")
backup_dir = os.path.join(os.path.dirname(base_dir), "backup")

now_dir = os.path.dirname(__file__)
rail_id_path = os.path.join(now_dir, "rail_id.json")
rail_schema_path = os.path.join(now_dir, "json_schema.json")
log_file = os.path.join(backup_dir, "log_rail.txt")
logger.add(log_file, level="DEBUG", encoding="utf-8", enqueue=True)

rail_ids = load_json(rail_id_path)

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
                    "item_id": get_id_by_name(i['name']),
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
        new_df.drop_duplicates(subset=["api_id"], keep="first", ignore_index=True, inplace=True)
    logger.info(uid + "共计" + str(len(new_df)) + "条数据,排序中...")
    new_df.sort_values(by=["time", "api_id"], ascending=False, ignore_index=True, inplace=True)
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
    data = uigf_json['hkrpg'][0]["list"]
    for i in data:
        i['item_id'] = get_id_by_name(i['name'])
        i['api_id'] = i['id']
        del i['id']
    df = get_new_df(columns=rail_idx, dtype=str, data=data)
    return df


def update_df(df: pandas.DataFrame):
    return


def get_id_by_name(name: str):
    global rail_ids
    if name in rail_ids:
        return rail_ids[name]
    rail_ids = get_rail_ids()
    return rail_ids[name]


def get_rail_ids():
    global rail_ids
    rail_ids_new = deepcopy(rail_ids)
    target_host = "https://raw.githubusercontent.com/Dimbreath/StarRailData/master/"
    avatar_config_file = "ExcelOutput/AvatarConfig.json"
    weapon_config_file = "ExcelOutput/EquipmentConfig.json"
    avatar_excel_config_data = json.loads(requests.get(target_host + avatar_config_file).text)
    weapon_excel_config_data = json.loads(requests.get(target_host + weapon_config_file).text)
    chs_dict = json.loads(requests.get(target_host + "TextMap/TextMapCHS.json").text)
    try:
        for item in avatar_excel_config_data:
            try:
                item_id = str(item['AvatarID'])
                hash_id = item['AvatarName']['Hash']
                if hash_id not in chs_dict:
                    hash_id = str(hash_id)
                if hash_id in chs_dict and item_id:
                    name = str(chs_dict[hash_id])
                    if len(name) > 0:
                        rail_ids_new[name] = item_id
            except Exception as e:
                logger.error(e)
        for item in weapon_excel_config_data:
            try:
                item_id = str(item['EquipmentID'])
                hash_id = item['EquipmentName']['Hash']
                if hash_id not in chs_dict:
                    hash_id = str(hash_id)
                if hash_id in chs_dict and item_id:
                    name = str(chs_dict[hash_id])
                    if len(name) > 0:
                        rail_ids_new[name] = item_id
            except Exception as e:
                logger.error(e)
        rail_ids = rail_ids_new
        write_json(rail_id_path, rail_ids)
    except:
        pass
    return rail_ids
