import json

import mysql.connector

import config

db = mysql.connector.connect(
    host=config.DB_HOST,
    user=config.DB_USER,
    passwd=config.DB_PASS,
    database=config.DB_NAME
)
cursor = db.cursor()


class Player:
    "A helper to manager the players in database."

    class Error(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return self.msg

    class ParameterException(Error):
        "参数异常"
        pass

    class UsedQQException(Error):
        "出现相同QQ"
        pass

    class UsedIDException(Error):
        "出现相同ID"
        pass

    class PlayerNotFoundException(Error):
        "玩家不存在"
        pass

    class TooMuchTpException(Error):
        "TP 次数过多"
        pass

    __c = 0

    def __add(self):
        cursor.execute('INSERT INTO GameToQQData (QQNumber, GamerName ,TpNumber) VALUES (\'%s\', \'%s\',0)' % (
            self.__qq, self.__id))
        db.commit()

    @staticmethod
    def __get(key, value):
        cursor.execute('select * from GameToQQData where %s=\'%s\'' % (key, value))
        return cursor.fetchall()

    @staticmethod
    def __del(key, value):
        cursor.execute('delete from GameToQQData where %s=\'%s\'' % (key, value))
        db.commit()

    def __limit_tp(self, i):
        cursor.execute(f'update GameToQQData set TpNumber = {i} where QQNumber = \'{self.__qq}\'')
        db.commit()
        self.__init__(self.__qq)

    def __init__(self, QQNumber: str = None, GamerName: str = None):
        if QQNumber is None and GamerName is None:
            raise self.ParameterException("请提供 QQ 号或 Xbox ID 中的至少一个参数")
        self.__qq = QQNumber
        self.__id = GamerName
        if None not in (self.__qq, self.__id):
            r_qq = self.__get('QQNumber', self.__qq)
            r_id = self.__get('GamerName', self.__id)
            if not len(r_qq) == 0:
                raise self.UsedQQException('此QQ已被绑定')
            if not len(r_id) == 0:
                raise self.UsedIDException('此ID已被绑定')
            self.__add()
        else:
            if not self.__qq is None:
                r = self.__get('QQNumber', self.__qq)
            else:
                r = self.__get('GamerName', self.__id)
            if len(r) == 0:
                raise self.PlayerNotFoundException('找不到此玩家')
            self.__qq = r[0][0]
            self.__id = r[0][1]
            self.__c = int(r[0][2])

    def remove(self):
        if self.__qq is not None:
            self.__del("QQNumber", self.__qq)
        else:
            self.__del("GamerName", self.__id)

    @staticmethod
    def list():
        cursor.execute('select * from GameToQQData')
        players = cursor.fetchall()
        return [Player(v[0]) for v in players]

    def QQNumber(self):
        return self.__qq

    def GamerName(self):
        return self.__id

    def cleanTpCount(self):
        self.__limit_tp(0)

    @staticmethod
    def cleanAllTpCount():
        cursor.execute('update GameToQQData set TpNumber = 0')
        db.commit()

    def addTpCount(self, t_max=3):
        if self.__c < t_max:
            self.__limit_tp(self.__c + 1)
            return self.__c
        else:
            raise self.TooMuchTpException("过多的TP")

    def TpCount(self):
        self.__init__(self.__qq)
        return self.__c

    def __str__(self):
        return self.__id

    def __int__(self):
        return int(self.__qq)

    def __repr__(self):
        self.__init__(self.__qq)
        return 'Player<qq=%s,id=%s,tp=%s>' % (self.__qq, self.__id, self.__c)


class Team:
    class Error(Exception):
        def __init__(self, msg):
            self.msg = msg

        def __str__(self):
            return self.msg

    class UsedTeamNameException(Error):
        "队伍名称已被占用"
        pass

    class TeamNotFoundException(Error):
        "找不到此队伍"
        pass

    class AddedMemberException(Error):
        "已加入的玩家"
        pass

    class MemberNotFoundException(Error):
        "队伍中找不到玩家"
        pass

    def __add(self):
        cursor.execute('INSERT INTO TpTeam (TeamName,TeamOwner,TeamMember) VALUES (\'%s\', \'%s\',\'[]\')' % (
            self.__name, self.__owner))
        db.commit()

    def __get(self):
        cursor.execute('select * from TpTeam where TeamName = \'%s\'' % self.__name)
        return cursor.fetchall()

    def __setMember(self, member):
        cursor.execute(f'update TpTeam set TeamMember =\'{json.dumps(member)}\' where TeamName = \'{self.__name}\'')
        db.commit()

    def __init__(self, TeamName: str, Owner: Player = None):
        self.__name = TeamName
        team = self.__get()
        if Owner:
            if len(team) > 0:
                raise self.UsedTeamNameException()
            self.__owner = Owner.QQNumber()
            self.__add()
        elif len(team) == 0:
            raise self.TeamNotFoundException()
        else:
            self.__owner = team[0][1]

    def getMember(self):
        team = self.__get()[0]
        member = [Player(v) for v in json.loads(team[2])]
        return member

    def getOwner(self):
        owner = Player(self.__owner)
        return owner

    def getOwnerAndMember(self):
        team = self.__get()[0]
        member = [Player(v) for v in json.loads(team[2])] + [Player(team[1])]
        return member

    def addMember(self, player: Player):
        team = self.__get()[0]
        if (not player.QQNumber() in json.loads(team[2])) or player.QQNumber() == self.__owner:
            member = json.loads(team[2])
            member.append(player.QQNumber())
            print(member)
            self.__setMember(member)
        else:
            raise self.AddedMemberException()

    def removeMember(self, player: Player):
        team = self.__get()[0]
        m = json.loads(team[2])
        try:
            m.remove(player.QQNumber())
        except:
            raise self.MemberNotFoundException()
        self.__setMember(m)

    def ifIn(self, player: Player):
        m = self.getOwnerAndMember()
        return player.QQNumber() in [i.QQNumber() for i in m]

    def remove(self):
        cursor.execute('delete from TpTeam where TeamName = \'%s\'' % self.__name)
        db.commit()

    @staticmethod
    def list():
        cursor.execute('select * from TpTeam')
        m = cursor.fetchall()
        return [Team(v[0]) for v in m]

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f'Team<name={self.__name},owner={self.__owner}>'
