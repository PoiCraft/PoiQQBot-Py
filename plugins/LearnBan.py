import nonebot
import config
from nonebot import on_command, CommandSession, permission

__plugin_name__ = '学习套餐'
__plugin_usage__ = r"""学习套餐
例：#学习
或者 #learn"""

bot = nonebot.get_bot()


@on_command('learn', aliases='学习', only_to_me=False, permission=permission.GROUP)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    if str(SenderGroupNumber) in config.SendGroup:
        pass
    else:
        await bot.set_group_ban(group_id='769885907', user_id=f'{SenderQQNumber}', duration=1 * 60 * 60)
        await session.send(f'[CQ:at,qq={SenderQQNumber}] 加油，奥里给!完事了记得来Poicraft放松一下嗷')
