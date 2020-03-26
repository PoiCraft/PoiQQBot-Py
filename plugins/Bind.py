import config
from nonebot import on_command, CommandSession, permission
from helper.DatabaseHelper import Player

__plugin_name__ = '绑定游戏数据库'
__plugin_usage__ = r"""添加白名单
例：#绑定 游戏ID
或者 #bind 游戏ID"""


@on_command('bind', aliases='绑定', only_to_me=False, permission=permission.GROUP)
async def Bind(session: CommandSession):
    # 取一堆值
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    SenderGroupNumber = session.ctx['group_id']
    if str(SenderGroupNumber) in config.SendGroup:
        pass
    else:
        if not SenderGamerName:
            await session.send('#bind后面必须跟上你的用户名嗷，例：#bind HelloWorld')
        else:
            try:
                Player(SenderQQNumber, SenderGamerName)
            except Player.TheSameQQException:
                # 存在相同QQ号
                SqlGamerName = Player(QQNumber=SenderQQNumber).GamerName()
                await session.send('[CQ:at,qq=%s] 你已经绑定过%s了嗷' % (SenderQQNumber, SqlGamerName))
            except Player.TheSameIDException:
                # 当已存在相同的游戏ID
                SqlQQNumber = Player(GamerName=SenderGamerName).QQNumber()
                await session.send('[CQ:at,qq=%s] %s已经被%s绑定了' % (SenderQQNumber, SenderGamerName, SqlQQNumber))
            else:
                await session.send('[CQ:at,qq=%s] 成功绑定%s!' % (SenderQQNumber, SenderGamerName))
