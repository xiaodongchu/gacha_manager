from files.genshin_info import get_genshin
from url_genshin import get_genshin_url

sleep_time = 0.6
url = get_genshin_url()

if __name__ == '__main__':
    if url is None:
        raise Exception("未找到原神链接")
    get_genshin(url, sleep_time)
