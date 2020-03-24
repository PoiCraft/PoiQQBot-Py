import random
import time
from nonebot import on_command, CommandSession
from websocket import create_connection
from helper.DatabaseHelper import Player

__plugin_name__ = '随机传送'
__plugin_usage__ = r"""随机传送
例：#随机传送
或者 #rtp"""

import config


@on_command('rtp', aliases='随机传送', only_to_me=False)
async def RandomTp(session: CommandSession):
    # 查数据库
    # 定义一些东西...
    x = random.randint(30000, 70000) * -1  # 随机X轴
    z = random.randint(30000, 70000) * -1  # 随机Z轴
    SenderQQNumber = session.ctx['user_id']

    # 联系数据库获取到玩家名称
    try:
        GamerName = Player('%s' % SenderQQNumber)  ##QQ取玩家ID
    except Player.PlayerNotFoundException:
        await session.send('[CQ:at,qq={0}]你没有绑定，请输入#bind 你的游戏ID，例：#addw username进行绑定'.format(SenderQQNumber))
        exit()
    # 联系BedrockServer处理
    try:
        ws = create_connection("ws://127.0.0.1:30000")
    except:
        await session.send('[CQ:at,qq={0}] 服务器去火星了,等会儿再试试吧'.format(SenderQQNumber))
    ws.send('testfor %s' % GamerName)
    result = ws.recv()
    if result != 'No targets matched selector':
        player = Player(SenderQQNumber)
        try:
            player.addTpCount()
        except Player.TooMuchTpException:
            await session.send('[CQ:at,qq={0}] 今日随机传送次数已用完,且行且珍惜'.format(SenderQQNumber))
        else:
            ws.send('effect %s resistance 15 5 true' % GamerName)
            print("给予玩家%s防摔死buff*15s" % GamerName)
            time.sleep(0.3)
            ws.send('tp %s %s 120 %s' % (GamerName, x, z))
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 您已被传送至{x},100,{z}\n使用次数:{player.TpCount()}/{config.RandomTp}\n传送本不易，且行且珍惜')
    else:
        await session.send('[CQ:at,qq={0}] 当前您不在线嗷,上线后再试试吧'.format(SenderQQNumber))
