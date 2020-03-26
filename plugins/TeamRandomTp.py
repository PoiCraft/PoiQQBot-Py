import random
import config
from nonebot import on_command, CommandSession,permission

__plugin_name__ = '随机传送'
__plugin_usage__ = r"""随机传送
例：#随机传送
或者 #rtp"""

import config


@on_command('rtp', aliases='随机传送', only_to_me=False, permission=permission.GROUP)
async def RandomTp(session: CommandSession):
    # 查数据库
    # 定义一些东西...
    x = random.randint(30000, 70000) * -1  # 随机X轴
    z = random.randint(30000, 70000) * -1  # 随机Z轴
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    if SenderGroupNumber in config.SendGroup:
        pass
    else:
    # 联系数据库获取到玩家名称
        await session.send('组队传送正在筹备中...')