# genshin_star_rail_gacha
管理原神、星铁抽卡数据

### 安装需求

```bash
# 推荐python版本3.11+
# 推荐在conda或venv等虚拟环境中运行
pip install -r requirements.txt
```

### 导入数据

#### 原神

- 支持符合[统一可交换抽卡记录标准 | UIGF-org](https://uigf.org/zh/standards/UIGF.html)的JSON文件导入
- 在`update_genshin.py`的`main`函数中配置要导入的文件路径，运行即可
- ToDo：暂未实现json格式核对，请自行确保导入`json["list"]`中各项符合以下标准：[ Json Schema](https://uigf.org/zh/standards/UIGF.html#json-schema)

#### 崩坏：星穹铁道

- 支持符合[星穹铁道抽卡记录标准](https://uigf.org/zh/standards/SRGF.html)的JSON文件导入
- 在`update_star_rail.py`的`main`函数中配置要导入的文件路径，运行即可
- ToDo：暂未实现json格式核对，请自行确保导入`json["list"]`中各项符合以下标准:[ Json Schema](https://uigf.org/zh/standards/SRGF.html#json-schema)

### 数据储存

- 原神数据默认按`uid`储存于`/save/genshin/`下
- 星穹铁道数据默认按`uid`储存于`/save/star_rail/`下
- 在通常情况下，程序会自动导出符合上述标准的`json`文件、`excel`文件、`csv`文件
- 在通常情况下，**不建议对`csv`文件进行任何操作**，您可使用`json`文件向其他平台交换数据，使用`excel`文件查看数据。

### 更新数据

#### 原神

- 原神：启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`import_genshin.py`
- 查看`/save/genshin/uid.xlsx`

#### 崩坏：星穹铁道

- 在游戏中抽卡历史记录界面翻几页
- 运行`import_star_rail.py`
- 查看`/save/star_rail/uid.xlsx`

### 获取抽卡记录连接

#### 原神

- 原神：启动
- 在游戏中抽卡历史记录界面翻几页
- 运行`load_log.py`中的`get_genshin_url()`函数
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/log/log.txt`中复制

#### 崩坏：星穹铁道

- 在游戏中抽卡历史记录界面翻几页
- 运行`load_log.py`中的`get_star_rail_url()`函数
- 链接会自动复制入剪切板，您也可查看控制台输出，或从`/log/log.txt`中复制
