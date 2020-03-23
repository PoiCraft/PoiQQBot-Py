import sys
import time

import config
from nonebot import on_command, CommandSession
from websocket import create_connection
from helper.SQLiteHelper import Player

__plugin_name__ = '绑定游戏数据库'
__plugin_usage__ = r"""添加白名单
例：#绑定 游戏ID
或者 #bind 游戏ID"""


@on_command('bind', aliases='绑定', only_to_me=False)
async def Bind(session: CommandSession):
    # 取一堆值
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    if not SenderGamerName:
        await session.send('#addw后面必须跟上你的用户名嗷，例：/addw HelloWorld')
    else:
        try:
            Player(QQNumber=SenderQQNumber).GamerName()
            # qq绑定过游戏id,用qq号查游戏id输出
            SqlGamerName = Player(QQNumber=SenderQQNumber).GamerName()
            await session.send('[CQ:at,qq=%s] 你已经绑定过%s了嗷' % (SenderQQNumber, SqlGamerName))
        except Player.PlayerNotFoundException:
            # 没有绑定过游戏id,判断游戏id是否被绑定
            try:
                # 查询游戏id是否被绑定过
                Player(GamerName=SenderGamerName).QQNumber()
                # 被绑定过了,用游戏名称查qq输出
                SqlQQNumber = Player(GamerName=SenderGamerName).QQNumber()
                await session.send('[CQ:at,qq=%s] %s已经被%s绑定了' % (SenderQQNumber, SenderGamerName, SqlQQNumber))
            except Player.PlayerNotFoundException:
                # 没有被绑定过,第一次绑定
                # 数据库插入数据
                Player(QQNumber=SenderQQNumber, GamerName=SenderGamerName)
                await session.send('[CQ:at,qq=%s] 成功绑定%s!' %(SenderQQNumber, SenderGamerName))