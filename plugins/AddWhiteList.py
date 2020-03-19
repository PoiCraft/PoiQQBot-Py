import sqlite3
from nonebot import on_command, CommandSession

__plugin_name__ = '添加白名单'
__plugin_usage__ = r"""添加白名单
例：#加白 游戏ID
或者 #addw 游戏ID"""


# Poicraft第一次绑定数据库
import config


@on_command('White', aliases=['加白', 'addw'], only_to_me=False)
async def AddWhiteList(session: CommandSession):
    # 取一堆值
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    if not SenderGamerName:
        await session.send('#addw后面必须跟上你的用户名嗷，例：/addw HelloWorld')
        exit()
    else:
        # 操作数据库&返回消息
        ConnectSql = sqlite3.Connection(config.DATABASE)  # 连接数据库
        Cursor = ConnectSql.cursor()  # 创建游标
        SqlFindGamerName = 'select * from GameToQQData where QQNumber={0}'.format(SenderQQNumber)  # 数据库命令--查询qq号
        Cursor.execute(SqlFindGamerName)  # 执行数据库命令
        GamerName = Cursor.fetchall()  # 取查询结果

        if len(GamerName) == 0:  # QQ没有绑定过
            SqlFindQQNumber = 'select * from GameToQQData where GamerName={0}'.format(SenderQQNumber)  # 数据库命令--查询qq号
            Cursor.execute(SqlFindQQNumber)  # 执行数据库命令--查有没有用户名
            SqlGamerName = Cursor.fetchall()  # 取查询结果
            if SqlGamerName == 0:
                await session.send('[CQ:at,qq={0}]第一次绑定，正在努力为您添加呢，请稍后...'.format(SenderQQNumber))  # 艾特并发送消息
                SqlAddData = 'INSERT INTO GameToQQData (QQNumber, GamerName) VALUES (\'%s\', \'%s\');' % (SenderQQNumber, SenderGamerName)
                Cursor.execute(SqlAddData)
                ConnectSql.commit()
                SqlFindAddGamerName = 'select * from GameToQQData where QQNumber={0}'.format(SenderQQNumber)  # 数据库命令--查询是否添加成功
                Cursor.execute(SqlFindAddGamerName)
                AddReturn = Cursor.fetchall()
                if len(AddReturn) == 0:
                    await session.send('[CQ:at,qq={0}]哦豁，添加失败了呢!再试一次吧'.format(SenderQQNumber))
                else:
                    await session.send('[CQ:at,qq={0}]wow，添加成功了呢！'.format(SenderQQNumber))
            else:  # 数据库中已经有了该用户名
                FindSqlQQNumber = 'select * from GameToQQData where GamerName={0}'.format(SqlGamerName)  # 数据库命令--查询是否添加成功
                Cursor.execute(FindSqlQQNumber)
                FindSqlGamerName = Cursor.fetchall()[0][0] #取出qq
                await session.send('查询到了您的游戏账号已经绑定了-->{0}'.format(FindSqlQQNumber))
        else:
            await session.send('[CQ:at,qq=%s]您的QQ号已经绑定了--> %s' % (SenderQQNumber, GamerName[0][1]))

    def FindSql(SqlCommand):
        SqlFindGamerName = SqlCommand  # 数据库命令
        Cursor.execute(SqlFindGamerName)  # 执行数据库命令
        return  Cursor.fetchall()  # 取查询结果