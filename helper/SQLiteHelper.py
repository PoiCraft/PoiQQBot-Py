import sqlite3

import config

db = sqlite3.Connection(config.DATABASE)
cursor = db.cursor()

class Player:
    "A helper to mamager the palyers in database"
    
    class Error(Exception):
        def __init__(self,msg):
            self.msg = msg
        def __str__(self):
            return self.msg
    class MissingParameterException(Error):
        "参数缺失"
        pass
    class TooManyPlayersException(Error):
        "出现相同账号"
        pass
    class PlayerNotFoundException(Error):
        "玩家不存在"
        pass

    def __add(self):
        cursor.execute('INSERT INTO GameToQQData (QQNumber, GamerName) VALUES (\'%s\', \'%s\')' %(self.__qq, self.__id))
        db.commit()

    def __get(self,key,value):
        cursor.execute('select * from GameToQQData where %s=\'%s\''%(key,value))
        self.__result = cursor.fetchall()

    def __del(self,key,value):
        cursor.execute('delete from GameToQQData where %s=\'%s\''%(key,value))
        db.commit()

    def __list():
        cursor.execute('select * from GameToQQData')
        return cursor.fetchall()

    def __init__(self,QQNumber:str=None,GamerName:str=None):
        if (QQNumber == None and GamerName == None):
            raise self.MissingParameterException("请提供 QQ 号或 Xbox ID 中的至少一个参数")
        self.__qq = QQNumber
        self.__id = GamerName
        if (self.__qq is not None):
            self.__get("QQNumber",self.__qq)
        else:
            self.__get("GamerName",self.__id)
        if (self.__qq and self.__id):
            if len(self.__result) == 0:
                self.__add()
            else:
                raise self.TooManyPlayersException('此QQ已被绑定过了')
        elif len(self.__result) == 1:
            self.__qq = self.__result[0][0]
            self.__id = self.__result[0][1]
        else:
            raise self.PlayerNotFoundException('无法找到此玩家')

    def remove(self):
        if (self.__qq is not None):
            self.__del("QQNumber",self.__qq)
        else:
            self.__del("GamerName",self.__id)

    def list():
        cursor.execute('select * from GameToQQData')
        palyers = cursor.fetchall()
        return [{'qq':v[0],'id':v[1]} for v in palyers]

    def QQNumber(self):
        return self.__qq

    def GamerName(self):
        return self.__id

    def __str__(self):
        return self.__id

    def __int__(self):
        return int(self.__qq)



