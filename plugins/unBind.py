import re
from helper.SQLiteHelper import Player
from nonebot import on_command, CommandSession,permission

__plugin_name__ = '解除绑定'
__plugin_usage__ = r"""解除绑定(仅管理及群主可用)
例：#解绑 @一个人
或者 #unbind 艾特一个人"""


@on_command('unbind', aliases='解绑', only_to_me=False, permission=permission.GROUP_OWNER | permission.GROUP_ADMIN)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderMessage = session.current_arg_text.strip()
    if not SenderMessage:
        await session.send('[CQ:at,qq={0}]#unbind后面必须跟上@的用户嗷，例：/unbind @helloworld'.format(SenderQQNumber))
    else:
        AtQQNumber = re.findall(r"(?<=\[CQ:at,qq=).*?(?=\])", SenderMessage)[0]
        ATGamerNumber = Player(QQNumber=AtQQNumber).GamerName()
        await session.send(f'[CQ:at,qq={SenderQQNumber}] 已解除{AtQQNumber}与{ATGamerNumber}的绑定!')
        try:
            Player(QQNumber=AtQQNumber).remove()
        except Player.PlayerNotFoundException:
            await session.send(f'[CQ:at,qq={SenderQQNumber}] 解绑失败，你都没有绑定呢!')
