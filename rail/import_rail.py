from jsonschema import validate

from files.rail_info import load_json, uigf_to_df_rail, backup_and_merge_rail, logger, rail_schema_path


def import_rail(ugif_path):
    schema = load_json(rail_schema_path)
    new_ugif = load_json(ugif_path)
    validate(instance=new_ugif, schema=schema)
    uid = str(int(new_ugif["hkrpg"][0]["uid"]))
    new_df = uigf_to_df_rail(new_ugif)
    backup_and_merge_rail(uid, new_df)
    logger.info("崩坏：星穹铁道抽卡数据导入完成:" + uid)


if __name__ == '__main__':
    path = r"D:\programming\yuanshen\gacha_manager\rail\save\104876574.json"  # 导入uigf的绝对路径
    import_rail(path)
