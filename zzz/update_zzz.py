from files.zzz_info import get_zzz
from url_zzz import get_zzz_url

sleep_time = 0.6
url = get_zzz_url()

if __name__ == '__main__':
    if url is None:
        raise Exception("未找到绝区零链接")
    get_zzz(url, sleep_time)
