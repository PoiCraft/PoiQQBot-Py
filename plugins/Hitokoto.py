import config
import requests
import json
from nonebot import on_command, CommandSession,permission

__plugin_name__ = '一言'
__plugin_usage__ = r"""一言
例：#一言
或者 #yy"""


@on_command('learn', aliases='学习', only_to_me=False, permission=permission.GROUP)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']
    SenderGroupNumber = session.ctx['group_id']
    if SenderGroupNumber in config.SendGroup:
        pass
    else:
        Return = requests.get('https://v1.hitokoto.cn/?c=a')
        JsonStr = json.loads(Return.text)
        await session.send('[CQ:at,qq=%s]%s\nFrom:%s' % (SenderQQNumber, JsonStr['hitokoto'], JsonStr['from']))

