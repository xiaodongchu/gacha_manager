from urllib.parse import urlparse, parse_qsl, urlencode

import requests
from pyperclip import copy

from config_zzz import zzz_game_path
from files.zzz_info import logger


def get_zzz_url():
    zzz_link_retain = ["authkey", "authkey_ver", "sign_type", "game_biz", "auth_appid",
                       "size", "region", "win_mode", "device_type"]
    logger.info("正在获取绝区零链接")
    logger.debug("路径:" + zzz_game_path)
    f = open(zzz_game_path, 'r', encoding='utf-8', errors='replace')
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
                parse = {key: parse[key] for key in parse if key in zzz_link_retain}
                parse["lang"] = "zh-cn"
                parse["game_biz"] = "nap_cn"
                parse["region"] = "prod_gf_cn"
                parse["page"] = "1"
                parse["end_id"] = "0"
                latest_url = url.split("?")[0] + "?" + urlencode(parse)
                copy(latest_url)
                logger.info(latest_url)
                return latest_url
    logger.error("未找到绝区零链接")


if __name__ == "__main__":
    get_zzz_url()
