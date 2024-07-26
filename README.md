# gacha_manager
管理原神、崩坏：星穹铁道抽卡数据

### 支持游戏列表
- 原神
- 崩坏：星穹铁道
- TODO:绝区零

### 安装需求

```bash
# 推荐python版本3.11+
# 推荐在conda或venv等虚拟环境中运行
pip install -r requirements.txt
```

### 数据储存

- 原神数据默认按`uid`储存于`/genshin/save/`下
- 崩坏：星穹铁道数据默认按`uid`储存于`/rail/save/`下
- 在通常情况下，程序会自动导出符合上述标准的`json`文件、`excel`文件、`csv`文件
- 在通常情况下，**不建议对`csv`文件进行任何操作**，您可使用`json`文件向其他平台交换数据，使用`excel`文件查看数据。

### 获取抽卡记录连接

#### 原神

- 在`config_genshin.py`中仿照示例，找到自己对应游戏的`data_2`日志路径:
- 原神:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`url_genshin.py`
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/genshin/save/log.txt`中复制

#### 崩坏：星穹铁道

- 在`config_rail.py`中仿照示例，找到自己对应游戏的`data_2`日志路径:
- 崩坏：星穹铁道:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`url_rail.py`
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/rail/save/log.txt`中复制

### 更新数据

#### 原神

- 在`config_genshin.py`中仿照示例，找到自己对应游戏的`data_2`日志路径:
- 原神:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`update_genshin.py`
- 查看`/genshin/save/uid.xlsx`

#### 崩坏：星穹铁道

- 在`config_rail.py`中仿照示例，找到自己对应游戏的`data_2`日志路径:
- 崩坏：星穹铁道:启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`update_rail.py`
- 查看`/rail/save/uid.xlsx`

### 导入数据

#### 原神

- 支持符合[统一可交换抽卡记录标准 | UIGF-org](https://uigf.org/zh/standards/UIGF.html)的JSON文件导入
- 在`import_genshin.py`的`main`函数中配置要导入的文件路径，运行即可
- TODO:暂未实现json格式核对，请自行确保导入`json["list"]`中各项符合以下标准:[Json Schema](https://uigf.org/zh/standards/UIGF.html#json-schema)

#### 崩坏：星穹铁道

- 支持符合[崩坏：星穹铁道抽卡记录标准](https://uigf.org/zh/standards/SRGF.html)的JSON文件导入
- 在`import_rail.py`的`main`函数中配置要导入的文件路径，运行即可
- TODO:暂未实现json格式核对，请自行确保导入`json["list"]`中各项符合以下标准:[Json Schema](https://uigf.org/zh/standards/SRGF.html#json-schema)
