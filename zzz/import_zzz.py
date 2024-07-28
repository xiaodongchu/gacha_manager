from jsonschema import validate

from files.zzz_info import load_json, uigf_to_df_zzz, backup_and_merge_zzz, logger, zzz_schema_path


def import_zzz(ugif_path):
    schema = load_json(zzz_schema_path)
    new_ugif = load_json(ugif_path)
    validate(instance=new_ugif, schema=schema)
    uid = str(int(new_ugif["nap"][0]["uid"]))
    new_df = uigf_to_df_zzz(new_ugif)
    backup_and_merge_zzz(uid, new_df)
    logger.info("绝区零抽卡数据导入完成:" + uid)


if __name__ == '__main__':
    path = r"D:\programming\yuanshen\gacha_manager\zzz\save\17338321.json"  # 导入uigf的绝对路径
    import_zzz(path)
