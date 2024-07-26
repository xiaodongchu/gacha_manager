from jsonschema import validate

from files.genshin_info import load_json, uigf_to_df_genshin, backup_and_merge_genshin, logger, genshin_schema_path


def import_genshin(ugif_path):
    schema = load_json(genshin_schema_path)
    new_ugif = load_json(ugif_path)
    validate(instance=new_ugif, schema=schema)
    uid = str(new_ugif["hk4e"][0]["uid"])
    new_df = uigf_to_df_genshin(new_ugif)
    backup_and_merge_genshin(uid, new_df)
    logger.info("原神抽卡数据导入完成:" + uid)


if __name__ == '__main__':
    path = r"D:\programming\yuanshen\gacha_manager\genshin\save\139163286.json"  # 导入uigf的绝对路径
    import_genshin(path)
