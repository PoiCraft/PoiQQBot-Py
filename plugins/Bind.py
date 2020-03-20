import sqlite3
import config
from nonebot import on_command, CommandSession

__plugin_name__ = '绑定游戏数据库'
__plugin_usage__ = r"""添加白名单
例：#绑定 游戏ID
或者 #bind 游戏ID"""


@on_command('bind', aliases='绑定', only_to_me=False)
async def Bind(session: CommandSession):
    def FindSql(Field, Content):  # 数据库命令
        print('select * from GameToQQData where %s=\'%s\'' % (Field, Content))
        Cursor.execute('select * from GameToQQData where %s=\'%s\'' % (Field, Content))  # 执行数据库命令
        try:
            return Cursor.fetchall()  # 取查询结果
        except:
            return 'error'

    def InsertSql(QQNumber, GamerName):
        Cursor.execute('INSERT INTO GameToQQData (QQNumber, GamerName) VALUES (\'%s\', \'%s\')' %(QQNumber, GamerName))
        ConnectSql.commit()

    # 取一堆值
    SenderQQNumber = session.ctx['user_id']  # 取发送者的qq号
    SenderGamerName = session.current_arg_text.strip()  # 去空格取命令参数
    if not SenderGamerName:
        await session.send('#addw后面必须跟上你的用户名嗷，例：/addw HelloWorld')
    else:
        ConnectSql = sqlite3.Connection(config.DATABASE)  # 连接数据库
        Cursor = ConnectSql.cursor()  # 创建游标
        GamerName = FindSql('QQNumber',SenderQQNumber)  # 通过发送者的QQ号来查询是否有绑定游戏ID
        if len(GamerName) == 0:  # QQ没有绑定过
            #数据库命令--通过发送者带的游戏ID来查询是否有绑定QQ
            SqlGamerName = FindSql('GamerName', SenderGamerName)
            print('--->{0}'.format(SqlGamerName))
            print(len(SqlGamerName))
            if len(SqlGamerName) == 0:
                await session.send('[CQ:at,qq={0}]第一次绑定，正在努力为您添加呢，请稍后...'.format(SenderQQNumber))  # 艾特并发送消息
                InsertSql(SenderQQNumber, SenderGamerName)  # 插入数据库
                AddReturn = FindSql('QQNumber', SenderQQNumber)  # 查询qq是否存在，存在即为导入成功
                WhiteListFile = open(config.WHITELIST, 'r', encoding='utf-8')
                if len(AddReturn) == 0:
                    await session.send('[CQ:at,qq={0}]哦豁，添加失败了呢!再试一次吧'.format(SenderQQNumber))
                else:
                    await session.send('[CQ:at,qq={0}]wow，添加成功了呢！'.format(SenderQQNumber))
            else:  # 数据库中已经有了该用户名
                FindSqlGamerName = FindSql('GamerName', SqlGamerName[0][1])  # 查询数据库是否有这个ID，有就代表这个ID已经被绑定过了
                await session.send('[CQ:at,qq=%s]%s已经绑定了-->%s' % (SenderQQNumber, FindSqlGamerName[0][1], FindSqlGamerName[0][0]))
        else:
            await session.send('[CQ:at,qq=%s]您的QQ号已经绑定了--> %s' % (SenderQQNumber, GamerName[0][1]))