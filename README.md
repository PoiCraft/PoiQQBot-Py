# BDS_QQControl
## 如何使用
* 使用了酷Q的webapi插件，安装方法参阅https://cqhttp.cc/
* 使用了nonebot，请先`pip install -r requirements.txt`，更多api参阅https://nonebot.cqp.moe/api.html

## 需要修改的地方
* 酷Q安装目录/data/app/io.github.richardchien.coolqhttpapi\config\xxxxxx.json\  
    * 修改前
        * `"ws_reverse_api_url": ""`
        * `"ws_reverse_event_url": ""`
        * ` "use_ws_reverse": false`
    * 修改后
        * `"ws_reverse_api_url": "ws://127.0.0.1:12345/ws/api/"`
        * `"ws_reverse_event_url": "ws://127.0.0.1:12345/ws/event/"`
        * `"use_ws_reverse": true`

* 将`config.example.py` 复制为 `config.py`
* config.py 第六行
    * 修改前
        * `BEDROCKSERVEREXE = r'E:\\Python Projects\\BedrockServer\\bedrock_server.exe'`
    * 修改后
        * `BEDROCKSERVEREXE = r'所在的目录\\bedrock_server.exe'`  
* config.py 第七行
    * 修改前
        * `DATABASE = 'E:\\Python Projects\\BDS_Control\\database\\poicraft.db'`
    * 修改后
        * `DATABASE = 'DB所在的目录\\poicraft.db'`  
## 注意事项
* **确保TCP12345、30000端口不被占用**
