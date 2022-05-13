import pymysql as msql
import sqlite3

def db_login():
    "Connect to the database."
    host = "127.0.0.1"
    port = 3306
    user = "root"
    pwd = "123"
    dbname = "exam"

    #建立连接
    con = msql.connect(
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


conn = sqlite3.connect('C:/Users/Pacemark/Documents/Tencent Files/1712087754/FileRecv/first.db')
cur = conn.cursor()
sql = "select * from student"
try:
    cur.execute(sql)  # 执行sql语句
    results = cur.fetchall()  # 获取查询的所有记录
    print("id", "name", "password")
    # 遍历结果
    for row in results:
        id = row[0]
        name = row[1]
        password = row[2]
        print(id, name, password)
except Exception as e:
    raise e
#db_login()