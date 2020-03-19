import nonebot

from aiocqhttp.message import unescape

from nonebot import on_command, CommandSession

__plugin_name__ = '帮助'
__plugin_usage__ = r"""帮助
例：#使用帮助
或者 #usage"""


@on_command('usage', aliases=['使用帮助', '帮助', '使用方法', 'help'], only_to_me=False)
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    user_id = session.ctx['user_id']
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(unescape('[CQ:at,qq=%s]我现在支持的功能有：\n-------\n' % user_id + '\n'.join(p.name for p in plugins)))
        await session.send('发送#help 功能 即可获取到详细用法')
        return

    # 如果发了参数则发送相应命令的使用帮助
    for p in plugins:
        if p.name.lower() == arg:
            await session.send(unescape('[CQ:at,qq=%s]' % user_id + p.usage))