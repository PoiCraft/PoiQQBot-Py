import sqlite3
import config

sql = 'update GameToQQData set UseNumber = 0'
conn=sqlite3.connect(config.DATABASE)
conn.execute(sql)
conn.commit()