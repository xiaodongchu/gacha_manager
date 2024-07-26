from files.rail_info import get_rail_url, get_rail


sleep_time = 0.6
url = get_rail_url()


if __name__ == '__main__':
    if url is None:
        raise Exception("未找到崩坏：星穹铁道链接")
    get_rail(url, sleep_time)
