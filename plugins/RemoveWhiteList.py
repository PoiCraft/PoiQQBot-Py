import time
import config
from websocket import create_connection
from nonebot import on_command, CommandSession, permission

__plugin_name__ = '删除白名单'
__plugin_usage__ = r"""删白名单(仅管理及群主可用)
例：#删白名单 游戏ID
或者#rmw 游戏ID"""


@on_command('rmw', aliases='删白名单', only_to_me=False, permission=permission.GROUP_OWNER | permission.GROUP_ADMIN)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    SenderGroupNumber = session.ctx['group_id']
    if SenderGroupNumber in config.SendGroup:
        pass
    else:
        if not SenderGamerName:
            await session.send('[CQ:at,qq={0}]#rmw后面必须跟上游戏ID嗷，例：#rmw HelloWorld'.format(SenderQQNumber))
        else:
            try:
                ws = create_connection("ws://127.0.0.1:30000")
            except:
                await session.send('[CQ:at,qq={0}] 服务器去火星了,等会儿再试试吧'.format(SenderQQNumber))
            ws.send(('whitelist remove %s' % SenderGamerName))
            time.sleep(0.1)
            result = ws.recv()
            if result == "Player removed from whitelist":
                await session.send('[CQ:at,qq=%s] %s已经从Poicraft的白名单中消失了呢!' % (SenderQQNumber, SenderGamerName))
            else:
                await session.send('[CQ:at,qq=%s] Poicraft的白名单并找不到%s呢!' % (SenderQQNumber, SenderGamerName))