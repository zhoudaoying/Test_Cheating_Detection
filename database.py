
import pymysql  as sql
import numpy as np

def db_login():
    "Connect to the database."
    host = "127.0.0.1"
    port = 3306
    user = "root"
    pwd = "123"
    dbname = "exam"

    #建立连接
    con = sql.connect(
     host=host,
     port=port,
     user=user,
     password=pwd,
     db = dbname,
     charset='utf8',
     autocommit = True
     )

    #拿到游标
    cursor = con.cursor()
    return con




