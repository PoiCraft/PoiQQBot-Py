from nonebot import on_command, CommandSession, permission
from sqlalchemy.orm.exc import NoResultFound

import config

__plugin_name__ = '查询信息'
__plugin_usage__ = r"""查询信息
例：#查询
或者 #info"""

from database.Player import Player


@on_command('info', aliases='查询', only_to_me=False, permission=permission.GROUP)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    DbSession = config.SESSION()
    if str(SenderGroupNumber) in config.SendGroup:
        pass
    else:
        try:
            player = DbSession.query(Player).filter(Player.QQNumber == SenderQQNumber).one()
            await session.send(
                f'[CQ:at,qq={SenderQQNumber}] 您绑定了{player.GamerName}\n传送次数{player.TpNumber}/{config.RandomTp}!!!')
        except NoResultFound:
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 您没有绑定呢!!!')
