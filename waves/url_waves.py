from re import compile
from time import sleep
from urllib.parse import parse_qsl

from requests import post

from config_waves import *
from files.waves_info import logger

waves_api_body = {
    "playerId": waves_uid,
    "cardPoolId": "",
    "cardPoolType": 1,
    "serverId": "",
    "recordId": "",
    "languageCode": "zh-Hans",
}


def update_waves_body(playerId: str, cardPoolId: str, serverId: str, recordId: str):
    """
    更新请求体
    :param playerId: uid
    :param cardPoolId: resources_id
    :param serverId: svr_id
    :param recordId: record_id
    """
    waves_api_body["playerId"] = playerId
    waves_api_body["cardPoolId"] = cardPoolId
    waves_api_body["serverId"] = serverId
    waves_api_body["recordId"] = recordId


def get_waves_url():
    url_re = compile(r"https?.*/aki/gacha/index\.html#/record[\?=&\w\-]+")
    waves_game_path_list = [os.path.join(waves_game_path, i) for i in os.listdir(waves_game_path)]
    waves_game_path_list = sorted([i for i in waves_game_path_list
                                   if ".log" in i and os.path.isfile(i)],
                                  key=lambda x: os.path.getmtime(x),
                                  reverse=True)
    for p in waves_game_path_list:
        logger.debug("路径:" + p)
        f = open(p, 'r', encoding='utf-8', errors='replace')
        words = f.read()
        f.close()
        words = url_re.findall(words)
        for i in words:
            if waves_uid and waves_uid not in i:
                continue
            parse = dict(parse_qsl(i.split("?")[1]))
            update_waves_body(parse["player_id"], parse["resources_id"], parse["svr_id"], parse["record_id"])
            response = post(waves_base_url, json=waves_api_body, headers=headers)
            res = response.json()
            sleep(sleep_time)
            if res["code"] == 0:
                logger.info(i)
                logger.info("uid:" + waves_api_body["playerId"])
                logger.info("body:" + str(waves_api_body))
                return waves_api_body
    logger.error("未找到鸣潮链接")


if __name__ == '__main__':
    get_waves_url()
