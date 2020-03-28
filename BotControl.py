from os import path

import nonebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

if __name__ == '__main__':
    engine = create_engine(
        'mysql+pymysql://%s:%s@$%s/%s' % (config.DB_USER, config.DB_PASS, config.DB_HOST, config.DB_NAME), echo=True)
    session = sessionmaker(bind=engine)()
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()
