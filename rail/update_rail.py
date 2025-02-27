from files.rail_info import get_rail
from url_rail import get_rail_url

sleep_time = 1.2
url = get_rail_url()

if __name__ == '__main__':
    if url is None:
        raise Exception("未找到崩坏：星穹铁道链接")
    get_rail(url, sleep_time)
