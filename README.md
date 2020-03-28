# PoiQQBot

一个允许玩家和管理员通过 QQ 对 Bedrock 服务器进行操作的简易机器人.  
此机器人为20人及以下，玩家之间和睦友好，启用白名单制的小型服务器设计。不适用于人数较多，人员较杂的大型服务器.  


## 如何使用

* 使用了酷Q的 webapi 插件，安装方法参阅 <https://cqhttp.cc/>
* 使用了 nonebot ,请先运行 `pip install -r requirements.txt` 安装依赖. 更多api参阅 <https://nonebot.cqp.moe/api.html>

### 修改配置文件
1. 酷Q安装目录/data/app/io.github.richardchien.coolqhttpapi\config\xxxxxx.json\  
    * `"ws_reverse_api_url": ""` -> `"ws_reverse_api_url": "ws://127.0.0.1:12345/ws/api/"`
    * `"ws_reverse_event_url": ""` -> `"ws_reverse_event_url": "ws://127.0.0.1:12345/ws/event/"`
    * `"use_ws_reverse": false` -> `"use_ws_reverse": true`

2. config.py  
    将`config.example.py` 复制为 `config.py`  
    根据以下格式修改:  

    ```Python
    from nonebot.default_config import *
    HOST = '127.0.0.1' #无需修改
    PORT = 12345 #无需修改
    COMMAND_START = {'#'} #命令前缀，无需修改
    BEDROCKSERVEREXE = r'E:\\Python Projects\\BedrockServer\\bedrock_server.exe' #Bedrock Server 的绝对地址.
    DATABASE = 'E:\\Python Projects\\BDS_Control\\database\\poicraft.db' # 用于绑定 QQ 和 Xbox ID 的数据库的绝对地址.
    ``` 


## 注意事项

**确保TCP12345、30000端口不被占用**
