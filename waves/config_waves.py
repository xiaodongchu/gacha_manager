import os


# 鸣潮游戏日志文件夹绝对路径
waves_game_path = "D:/software/games/Wuthering Waves/Wuthering Waves Game/Client/Saved/Logs/"
# 当前路径，无需修改
base_dir = os.path.dirname(__file__)
# 用户uid，若不配置，会从日志中自动获取
waves_uid = ""
# api信息
waves_api_info = {
    "1": "角色活动唤取",
    "2": "武器活动唤取",
    "3": "角色常驻唤取",
    "4": "武器常驻唤取",
    "5": "新手唤取",
    "6": "新手自选唤取",
    "7": "新手自选唤取（感恩定向唤取）"
}
waves_base_url = "https://gmserver-api.aki-game2.com/gacha/record/query"
# 每次请求间隔时间
sleep_time = 2
# 请求头
headers = {
    "Content-Type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
    "accept": "application/json",
    "origin": "https://aki-gm-resources.aki-game.com",
    "referer": "https://aki-gm-resources.aki-game.com/",
}
