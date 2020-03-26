import nonebot
import config
from nonebot import on_command, CommandSession,permission

__plugin_name__ = '晚安套餐'
__plugin_usage__ = r"""晚安套餐
例：#晚安
或者 #sleep"""

bot = nonebot.get_bot()


@on_command('sleep', aliases='晚安', only_to_me=False)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    if str(SenderGroupNumber) in config.SendGroup:
        pass
    else:
        await bot.set_group_ban(group_id='769885907', user_id=f'{SenderQQNumber}', duration=6 * 60 * 60)
        await session.send(f'[CQ:at,qq={SenderQQNumber}] 晚安，做个好梦，明天也要元气满满嗷!')