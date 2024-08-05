# gacha_manager
管理原神、崩坏：星穹铁道、绝区零、鸣潮抽卡数据

### 支持游戏列表
- **原神**
- **崩坏：星穹铁道**
- 绝区零
- 鸣潮

`绝区零与鸣潮暂停维护，若遇api更新，请自行完善代码`

### 安装需求*

```bash
# 推荐python版本3.11+
# 推荐在conda或venv等虚拟环境中运行
pip install -r requirements.txt
```

### 路径配置*

- 在`config_genshin.py`中配置原神`data_2`日志路径
- 在`config_rail.py`中配置崩坏：星穹铁道`data_2`日志路径
- 在`config_zzz.py`中配置绝区零`data_2`日志路径
- 在`config_waves.py`中配置鸣潮`Client.log`日志路径

### 数据储存

- 原神数据默认按`uid`储存于`/genshin/save/`下
- 崩坏：星穹铁道数据默认按`uid`储存于`/rail/save/`下
- 绝区零数据默认按`uid`储存于`/zzz/save/`下
- 鸣潮数据默认按`uid`储存于`/waves/save/`下
- 您可使用`json`文件与其他支持UIGF-4.0的平台交换数据
- 在通常情况下，**不建议对`csv`文件进行任何操作**，请通过`excel`文件查看数据。

### 获取抽卡记录连接

- 需先完成路径配置

#### 原神

- 原神:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`url_genshin.py`
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/backup/log_genshin.txt`中复制

#### 崩坏：星穹铁道

- 崩坏：星穹铁道:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`url_rail.py`
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/backup/log_rail.txt`中复制

#### 绝区零

- 绝区零:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`url_zzz.py`
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/backup/log_zzz.txt`中复制

### 更新数据

- 需先完成路径配置

#### 原神

- 原神:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`update_genshin.py`
- 查看`/genshin/save/{uid}.xlsx`

#### 崩坏：星穹铁道

- 崩坏：星穹铁道:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`update_rail.py`
- 查看`/rail/save/{uid}.xlsx`

#### 绝区零

- 绝区零:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`update_zzz.py`
- 查看`/zzz/save/{uid}.xlsx`

#### 鸣潮

- 鸣潮:启动
- 在游戏中查看抽卡历史记录界面
- 运行`update_waves.py`
- 查看`/waves/save/{uid}.xlsx`

```json
{
    "list": [{
        "uid": "(uid)",
        "gacha_type": "4",
        "cardPoolType": "武器调谐（常驻池）",
        "count": "1",
        "name": "源能长刃·测壹",
        "qualityLevel": "3",
        "resourceId": "21010023",
        "resourceType": "武器",
        "time": "2024-08-05 10:43:50"
    }]
}
```

### 导入数据

- 支持符合[UIGF-4.0](https://uigf.org/zh/standards/uigf.html)的JSON文件导入
- 请自行确保导入各项符合以下标准：[Json Schema](https://uigf.org/zh/standards/uigf.html#json-schema)

#### 原神

- 在`import_genshin.py`中配置要导入的`json`文件绝对路径
- 运行`import_genshin.py`
- 查看`/genshin/save/{uid}.xlsx`
- 若出现问题，请使用`/backup/{uid}_backup_{时间戳}.csv`恢复（重命名为`{uid}.csv`，并覆盖`/genshin/save/{uid}.csv`文件）

#### 崩坏：星穹铁道

- 在`import_rail.py`中配置要导入的`json`文件绝对路径
- 运行`import_rail.py`
- 查看`/rail/save/{uid}.xlsx`
- 若出现问题，请使用`/backup/{uid}_backup_{时间戳}.csv`恢复（重命名为`{uid}.csv`，并覆盖`/rail/save/{uid}.csv`文件）

#### 绝区零

- 在`import_zzz.py`中配置要导入的`json`文件绝对路径
- 运行`import_zzz.py`
- 查看`/zzz/save/{uid}.xlsx`
- 若出现问题，请使用`/backup/{uid}_backup_{时间戳}.csv`恢复（重命名为`{uid}.csv`，并覆盖`/zzz/save/{uid}.csv`文件）
