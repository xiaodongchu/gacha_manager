from utils import load_json, write_json, logger, uigf_to_df_genshin, backup_and_merge_genshin


def import_genshin(ugif_path):
    new_ugif = load_json(ugif_path)
    uid = str(new_ugif["info"]["uid"])
    new_df = uigf_to_df_genshin(new_ugif)
    backup_and_merge_genshin(uid, new_df)
    logger.info("原神抽卡数据导入完成:" + uid)


if __name__ == '__main__':
    path = ""  # 导入uigf的绝对路径
    # write_json(path, load_json(path))
    import_genshin(path)
