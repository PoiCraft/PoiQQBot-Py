from os import path

import nonebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()
