from urllib.parse import urlparse, parse_qsl, urlencode

import requests
from pyperclip import copy

from config import genshin_game_path, star_rail_game_path
from utils import logger


def get_star_rail_url():
    logger.info("正在获取星穹铁道链接")
    logger.debug("路径:"+star_rail_game_path)
    f = open(star_rail_game_path, 'r', encoding='utf-8', errors='replace')
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
                retain = ["authkey", "authkey_ver", "sign_type", "game_biz", "auth_appid", "size",
                          "region", "win_mode", "plat_type"]
                parse = {key: parse[key] for key in parse if key in retain}
                parse["lang"] = "zh-cn"
                parse["page"] = "1"
                parse["end_id"] = "0"
                latest_url = url.split("?")[0] + "?" + urlencode(parse)
                copy(latest_url)
                logger.info(latest_url)
                return latest_url
    logger.error("未找到星穹铁道链接")
    return None


def get_genshin_url():
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
                retain = ["authkey", "authkey_ver", "sign_type", "game_biz", "auth_appid", "size",
                          "region", "win_mode", "device_type"]
                parse = {key: parse[key] for key in parse if key in retain}
                parse["lang"] = "zh-cn"
                parse["page"] = "1"
                parse["end_id"] = "0"
                latest_url = url.split("?")[0] + "?" + urlencode(parse)
                copy(latest_url)
                logger.info(latest_url)
                return latest_url
    logger.error("未找到原神链接")
    return None


if __name__ == '__main__':
    get_genshin_url()
    get_star_rail_url()
