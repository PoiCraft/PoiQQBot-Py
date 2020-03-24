import re
import time

from helper.DatabaseHelper import Player
from nonebot import on_command, CommandSession,permission

__plugin_name__ = '解除绑定'
__plugin_usage__ = r"""解除绑定(仅管理及群主可用)
例：#解绑 @一个人
或者 #unbind 艾特一个人"""


@on_command('unbind', aliases='解绑', only_to_me=False, permission=permission.GROUP_OWNER | permission.GROUP_ADMIN)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    SenderAtQQNumber = session.ctx['message']
    try:
        AtQQNumber = re.findall(r"(?<=\[CQ:at,qq=).*?(?=\])", str(SenderAtQQNumber))[0]
        try:
            SqlGamerName = Player(QQNumber=AtQQNumber).GamerName()
            Player(AtQQNumber).remove()
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 解除{AtQQNumber}与{SqlGamerName}的绑定!!!')
        except Player.PlayerNotFoundException:
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 该用户没有绑定呢!!!')
    except:
        await session.send(f'[CQ:at,qq={SenderQQNumber}] #unbind后面艾特一个用户... 例如 #bind @user')
