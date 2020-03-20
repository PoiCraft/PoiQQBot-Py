import socket

from nonebot import on_command, CommandSession, permission

__plugin_name__ = '删除白名单'
__plugin_usage__ = r"""删白名单(仅管理及群主可用)
例：#删白名单 游戏ID
或者 #rmw 游戏ID"""


@on_command('rmw', aliases='删白名单', only_to_me=False, permission=permission.GROUP_ADMIN | permission.GROUP_OWNER)
async def Bind(session: CommandSession):
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    if not SenderGamerName:
        await session.send('[CQ:at,qq={0}]#rmw后面必须跟上游戏ID嗷，例：/addw HelloWorld'.format(SenderQQNumber))
    else:
        sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket连接
        host = '127.0.0.1'  # socket地址
        port = 30000  # socket端口
        try:
            sc.connect((host, port))
        except:  # 连接不成功
            await session.send('[CQ:at,qq={0}]服务端可能没有开启嗷，稍后再试试吧'.format(SenderQQNumber))
        try:
            sc.send(bytes('whitelist remove %s' % SenderGamerName, encoding='utf-8'))
            await session.send('Success')
        except:
            await session.send('Failed')