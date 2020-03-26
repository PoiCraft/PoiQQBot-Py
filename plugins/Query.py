import config
from helper.DatabaseHelper import Player
from nonebot import on_command, CommandSession,permission

__plugin_name__ = '查询信息'
__plugin_usage__ = r"""查询信息
例：#查询
或者 #info"""


@on_command('info', aliases='查询', only_to_me=False, permission=permission.GROUP)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    if SenderGroupNumber in config.SendGroup:
        pass
    else:
        try:
            SqlGamerName = Player(QQNumber=SenderQQNumber).GamerName()
            player = Player(SenderQQNumber)
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 您绑定了{SqlGamerName}\n传送次数{player.TpCount()}/{config.RandomTp}!!!')
            player.TpCount()
        except:
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 您没有绑定呢!!!')