from nonebot.default_config import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

HOST = '127.0.0.1'
PORT = 12345
COMMAND_START = {'#'}
BEDROCKSERVEREXE = r'E:\\Python Projects\\BedrockServer\\bedrock_server.exe'
DATABASE = 'E:\\Python Projects\\BDS_Control\\database\\poicraft.db'

SendGroup = ['769885907']
DB_HOST = '1.1.1.1'
DB_USER = 'potbot'
DB_PASS = 'wdnmdcnmlgb'
DB_NAME = 'cao'

engine = create_engine(
        'mysql+pymysql://%s:%s@%s/%s' % (DB_USER, DB_PASS, DB_HOST, DB_NAME), echo=True)

SESSION = sessionmaker(bind=engine)