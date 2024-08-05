from files.waves_info import get_waves
from url_waves import get_waves_url


if __name__ == '__main__':
    waves_api_body = get_waves_url()
    get_waves(waves_api_body)
