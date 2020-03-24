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
    class ParameterException(Error):
        "参数异常"
        pass
    class TheSameQQException(Error):
        "出现相同QQ"
        pass
    class TheSameIDException(Error):
        "出现相同ID"
        pass
    class PlayerNotFoundException(Error):
        "玩家不存在"
        pass
    class ToMuchTpException(Error):
        "TP 次数过多"
    pass

    __c = 0

    def __add(self):
        cursor.execute('INSERT INTO GameToQQData (QQNumber, GamerName ,UseNumber) VALUES (\'%s\', \'%s\',0)' %(self.__qq, self.__id))
        db.commit()

    def __get(self,key,value):
        cursor.execute('select * from GameToQQData where %s=\'%s\''%(key,value))
        return cursor.fetchall()

    def __del(self,key,value):
        cursor.execute('delete from GameToQQData where %s=\'%s\''%(key,value))
        db.commit()

    def __limit_tp(self,i):
        cursor.execute(f'update GameToQQData set UseNumber = {i} where QQNumber = \'{self.__qq}\'')
        db.commit()
        self.__init__(self.__qq)

    def __init__(self,QQNumber:str=None,GamerName:str=None):
        if (QQNumber == None and GamerName == None):
            raise self.ParameterException("请提供 QQ 号或 Xbox ID 中的至少一个参数")
        self.__qq = QQNumber
        self.__id = GamerName
        if None not in (self.__qq,self.__id):
            r_qq = self.__get('QQNumber',self.__qq)
            r_id = self.__get('GamerName',self.__id)
            if not len(r_qq) == 0:
                raise self.TheSameQQException('此QQ已被绑定')
            if not len(r_id) == 0:
                raise self.TheSameIDException('此ID已被绑定')
            self.__add()
        else:
            if not self.__qq == None:
                r = self.__get('QQNumber',self.__qq)
            else:
                r = self.__get('GamerName',self.__id)
            if len(r)==0:
                raise self.PlayerNotFoundException('找不到此玩家')
            self.__qq = r[0][0]
            self.__id = r[0][1]
            self.__c  = int(r[0][2])
    def remove(self):
        if (self.__qq is not None):
            self.__del("QQNumber",self.__qq)
        else:
            self.__del("GamerName",self.__id)

    def list():
        cursor.execute('select * from GameToQQData')
        palyers = cursor.fetchall()
        return [{'qq':v[0],'id':v[1],'tp':v[2]} for v in palyers]

    def QQNumber(self):
        return self.__qq

    def GamerName(self):
        return self.__id

    def cleanTpCount(self):
        self.__limit_tp(0)

    def cleanAllTpCount():
        cursor.execute('update GameToQQData set UseNumber = 0')
        db.commit()

    def addTpCount(self,t_max=3):
        if self.__c < t_max:
            self.__limit_tp(self.__c + 1)
            return self.__c
        else:
            raise self.ToMuchTpException("过多的TP")


    def TpCount(self):
        self.__init__(self.__qq)
        return self.__c

    def __str__(self):
        return self.__id

    def __int__(self):
        return int(self.__qq)

    def __repr__(self):
        self.__init__(self.__qq)
        return 'Player<qq=%s,id=%s,tp=%s>'%(self.__qq,self.__id,self.__c)



