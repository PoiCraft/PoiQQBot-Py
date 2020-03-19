import random
import socket
import time
import sqlite3
from nonebot import on_command, CommandSession

__plugin_name__ = '随机传送'
__plugin_usage__ = r"""随机传送
例：#随机传送
或者 #rtp"""

import config


@on_command('RandomTp', aliases=('rtp', '随机传送'), only_to_me=False)
async def RandomTp(session: CommandSession):
    # 查数据库
    def FindSql(SqlCommand):
        SqlFindGamerName = SqlCommand  # 数据库命令
        Cursor.execute(SqlFindGamerName)  # 执行数据库命令
        try:
            return Cursor.fetchall()[0][1]  # 取查询结果
        except:
            return 'error'

    # 定义一些东西...
    x = random.randint(30000, 70000) * -1  # 随机X轴
    z = random.randint(30000, 70000) * -1  # 随机Z轴
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket连接
    host = '127.0.0.1'  # socket地址
    port = 30000  # socket端口
    SenderQQNumber = session.ctx['user_id']
    # 联系数据库获取到玩家名称
    ConnectSql = sqlite3.Connection(config.DATABASE)  # 连接数据库
    Cursor = ConnectSql.cursor()  # 创建游标
    SqlFindGamerName = 'select * from GameToQQData where QQNumber={0}'.format(SenderQQNumber)  # 数据库命令--查询qq号获取玩家ID
    GamerName = FindSql(SqlFindGamerName)  ##QQ取玩家ID
    if GamerName == 'error':
        await session.send('[CQ:at,qq={0}]你没有绑定，请输入/addw 你的游戏ID，例：/addw blueworldsmile进行绑定'.format(SenderQQNumber))
        exit()
    else:
        # 联系BedrockServer处理
        try:
            sc.connect((host, port))
            print("连接到服务器")
        except:  # 连接不成功
            await session.send('[CQ:at,qq={0}]服务端可能没有开启嗷，稍后再试试吧'.format(SenderQQNumber))
            exit()

        sc.send(bytes('effect %s resistance 15 5 true' % GamerName, encoding='utf-8'))
        print("给予玩家防摔死buff*15s")
        time.sleep(0.1)
        sc.send(bytes('tp %s %s 100 %s' % (GamerName, x, z), encoding='utf-8'))
        await session.send('%s-->%s,100,%s' % (GamerName, x, z))
        print('%s-->%s,100,%s' % (GamerName, x, z))
