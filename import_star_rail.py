from utils import load_json, logger, uigf_to_df_star_rail, backup_and_merge_star_rail


def import_star_rail(ugif_path):
    new_ugif = load_json(ugif_path)
    uid = new_ugif["info"]["uid"]
    new_df = uigf_to_df_star_rail(new_ugif)
    backup_and_merge_star_rail(uid, new_df)
    logger.info("崩坏：星穹铁道抽卡数据导入完成:" + uid)


if __name__ == '__main__':
    path = ""  # 导入uigf的绝对路径
    # write_json(path, load_json(path))
    import_star_rail(path)

