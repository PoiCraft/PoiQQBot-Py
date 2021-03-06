import random
import time

from nonebot import on_command, CommandSession, permission
from sqlalchemy.orm.exc import NoResultFound
from websocket import create_connection

import config
from database.Player import Player

__plugin_name__ = '单人随机传送'
__plugin_usage__ = r"""单人随机传送
例：#传送
或者 #rtp"""


@on_command('rtp', aliases='传送', only_to_me=False, permission=permission.GROUP)
async def RandomTp(session: CommandSession):
    # 查数据库
    # 定义一些东西...
    global ws, GamerName
    x = random.randint(30000, 70000) * -1  # 随机X轴
    z = random.randint(30000, 70000) * -1  # 随机Z轴
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    DbSession = config.SESSION()
    if str(SenderGroupNumber) in config.SendGroup:
        pass
    else:
        # 联系数据库获取到玩家名称
        try:
            player = DbSession.query(Player).filter(Player.QQNumber == SenderQQNumber).one()
            GamerName = player.GamerName
        except NoResultFound:
            await session.send('[CQ:at,qq={0}]你没有绑定，请输入#bind 你的游戏ID，例：#addw username进行绑定'.format(SenderQQNumber))
            session.finish()

        # 联系BedrockServer处理
        try:
            ws = create_connection("ws://127.0.0.1:30000")
        except:
            await session.send('[CQ:at,qq={0}] 服务器去火星了,等会儿再试试吧'.format(SenderQQNumber))
            session.finish()

        ws.send('testfor \"%s\"' % GamerName)
        result = ws.recv()
        if result != 'No targets matched selector':
            player.TpNumber = player.TpNumber+1
            if player.TpNumber > config.RandomTp:
                await session.send('[CQ:at,qq={0}] 今日随机传送次数已用完,且行且珍惜'.format(SenderQQNumber))
                session.finish()
            DbSession.commit()
            ws.send('effect \"%s\" resistance 15 5 true' % GamerName)
            print("给予玩家%s防摔死buff*15s" % GamerName)
            time.sleep(0.3)
            ws.send('tp \"%s\" %s 120 %s' % (GamerName, x, z))
            await session.send(
                f'[CQ:at,qq={SenderQQNumber}] 您已被传送至{x},100,{z}\n使用次数:{player.TpNumber}/{config.RandomTp}\n传送本不易，且行且珍惜')
        else:
            await session.send('[CQ:at,qq={0}] 当前您不在线嗷,上线后再试试吧'.format(SenderQQNumber))
