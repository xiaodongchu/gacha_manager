import json
import os
import shutil
import pandas


def load_json(path):
    f = open(path, "r", encoding="utf-8")
    j = json.load(f)
    f.close()
    return j


def write_json(path, j):
    f = open(path, "w", encoding="utf-8")
    json.dump(j, f, ensure_ascii=False, indent=4)
    f.close()


def load_csv(path):
    return pandas.read_csv(path, index_col=0, encoding="utf-8", dtype=str)


def write_csv(path, df):
    df.to_csv(path, encoding="utf-8")
    os.chmod(path, 0o444)


def write_excel(path, df):
    df.to_excel(path)


def get_new_df(columns, dtype=str, data=None):
    return pandas.DataFrame(columns=columns, data=data, dtype=dtype)


def try_rename(old_file, new_path):
    if os.path.exists(old_file) and not os.path.exists(new_path) and os.path.isfile(old_file):
        os.chmod(old_file, 0o777)
        shutil.copy(old_file, new_path)
    else:
        raise Exception("文件备份错误")
