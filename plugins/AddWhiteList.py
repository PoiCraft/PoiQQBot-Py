import time
from websocket import create_connection
from nonebot import on_command, CommandSession

__plugin_name__ = '添加白名单'
__plugin_usage__ = r"""添加白名单(仅管理及群主可用)
例：#加白名单 游戏ID
或者 #addw 游戏ID"""


@on_command('addw', aliases='加白名单', only_to_me=False)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    if not SenderGamerName:
        await session.send('[CQ:at,qq={0}]#rmw后面必须跟上游戏ID嗷，例：/addw HelloWorld'.format(SenderQQNumber))
    else:
        try:
            ws = create_connection("ws://127.0.0.1:30000")
        except:
            await session.send('[CQ:at,qq={0}] 服务器去火星了,等会儿再试试吧'.format(SenderQQNumber))
        ws.send(('whitelist add %s' % SenderGamerName))
        time.sleep(0.1)
        result = ws.recv()
        if result == "Player added to whitelist":
            await session.send('[CQ:at,qq=%s] 已经把%s添加到Poicraft的白名单中了呢!' % (SenderQQNumber, SenderGamerName))
        elif result == 'Player already in whitelist':
            await session.send('[CQ:at,qq=%s] %s已经在Poicraft的白名单中了呢!' % (SenderQQNumber, SenderGamerName))
        else:
            await session.send('[CQ:at,qq=%s] 出了点问题?试试提个issues???' % SenderQQNumber)