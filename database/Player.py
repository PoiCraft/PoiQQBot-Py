from sqlalchemy import Column, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    __tablename__ = 'GameToQQData'
    QQNumber = Column(Integer,primary_key=True)
    GamerName = Column(Text)
    TpNumber = Column(Integer)
